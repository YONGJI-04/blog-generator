import os
import requests
import base64
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from dotenv import load_dotenv
import anthropic

load_dotenv()

app = FastAPI(title="AI Blog Generator API")
client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
HF_API_URL = "https://router.huggingface.co/hf-inference/models/black-forest-labs/FLUX.1-schnell"


class BlogRequest(BaseModel):
    topic: str
    tone: str = "informative"


@app.get("/")
def root():
    return {"status": "running", "message": "AI Blog Generator API"}


@app.post("/generate")
def generate_blog(req: BlogRequest):
    if not req.topic.strip():
        raise HTTPException(status_code=400, detail="주제를 입력해주세요")

    blog_msg = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2048,
        messages=[{
            "role": "user",
            "content": f"""다음 주제로 블로그 글을 작성해주세요.

주제: {req.topic}
톤: {req.tone}

형식:
# 제목
## 서론
## 본론 (2-3개 소제목)
## 결론

한국어로 작성하고, 마지막 줄에 커버 이미지용 영어 프롬프트를 작성해주세요.
형식: [IMAGE_PROMPT]: (영어 프롬프트)"""
        }]
    )

    content = blog_msg.content[0].text
    image_prompt = "professional blog cover image, high quality"

    if "[IMAGE_PROMPT]:" in content:
        parts = content.split("[IMAGE_PROMPT]:")
        blog_content = parts[0].strip()
        image_prompt = parts[1].strip()
    else:
        blog_content = content

    headers = {"Authorization": f"Bearer {os.environ['HF_TOKEN']}"}
    image_resp = requests.post(HF_API_URL, headers=headers, json={"inputs": image_prompt}, timeout=120)
    cover_image_b64 = base64.b64encode(image_resp.content).decode("utf-8") if image_resp.status_code == 200 else None

    return JSONResponse(content={
        "topic": req.topic,
        "blog_content": blog_content,
        "image_prompt": image_prompt,
        "cover_image_base64": cover_image_b64,
    })
