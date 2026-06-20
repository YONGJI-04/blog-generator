import os
import base64
import anthropic
import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Literal
from dotenv import load_dotenv

load_dotenv()
claude = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
HF_API_URL = "https://router.huggingface.co/hf-inference/models/black-forest-labs/FLUX.1-schnell"

app = FastAPI(title="Blog Generator API", description="주제를 입력하면 AI가 블로그 글과 커버 이미지를 생성합니다", version="1.1.0")

WORD_COUNT_MAP = {"short": 300, "medium": 600, "long": 1200}

class BlogRequest(BaseModel):
    topic: str
    tone: Literal["formal", "casual", "technical", "creative"] = "casual"
    length: Literal["short", "medium", "long"] = "medium"
    language: Literal["ko", "en"] = "ko"

@app.get("/")
def root():
    return {"status": "running", "message": "Blog Generator API"}

@app.post("/generate")
def generate_blog(req: BlogRequest):
    word_count = WORD_COUNT_MAP[req.length]
    lang = "한국어" if req.language == "ko" else "English"
    tone_map = {"formal": "격식체", "casual": "친근한 구어체", "technical": "전문적", "creative": "창의적"}
    tone_kr = tone_map.get(req.tone, req.tone)

    blog_prompt = f"""다음 주제로 {lang} 블로그 글을 작성해주세요.
주제: {req.topic}
어조: {tone_kr}
목표 분량: 약 {word_count}자

다음 구조로 작성해주세요:
# [제목]

## 서론
(독자의 관심을 끄는 도입부)

## 본론
(핵심 내용을 소제목과 함께 구조적으로)

## 결론
(핵심 정리 및 마무리)

---
*태그: #관련태그1 #관련태그2 #관련태그3*"""

    blog_res = claude.messages.create(model="claude-sonnet-4-6", max_tokens=3000, messages=[{"role": "user", "content": blog_prompt}])
    blog_content = blog_res.content[0].text

    cover_prompt_res = claude.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=200,
        messages=[{"role": "user", "content": f"Create a short FLUX.1 image generation prompt for a blog cover image about: {req.topic}. Focus on visual elements only, 30 words max."}]
    )
    cover_prompt = cover_prompt_res.content[0].text.strip()

    hf_response = requests.post(HF_API_URL, headers={"Authorization": f"Bearer {os.environ['HF_TOKEN']}"}, json={"inputs": cover_prompt, "parameters": {"width": 1280, "height": 720}}, timeout=120)
    cover_b64 = base64.b64encode(hf_response.content).decode("utf-8") if hf_response.status_code == 200 else None

    return {"topic": req.topic, "tone": req.tone, "length": req.length, "word_count": word_count, "blog_content": blog_content, "cover_image_prompt": cover_prompt, "cover_image_base64": cover_b64}
