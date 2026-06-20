# Blog Generator

주제를 입력하면 **Claude API**가 블로그 글을 자동 작성하고, **FLUX.1**이 어울리는 커버 이미지를 생성해주는 AI 콘텐츠 생성 API

---

## 프로젝트 개요

블로그 글 작성부터 커버 이미지 생성까지 한 번의 API 호출로 완성합니다. Claude가 글의 맥락을 파악하여 이미지 프롬프트를 직접 생성하기 때문에 글 내용과 이미지가 자연스럽게 어울립니다.

---

## 아키텍처

```
주제 텍스트 + 톤 설정 입력
            ↓
    [ Claude API ]
    claude-sonnet-4-6
    블로그 글 작성 (제목/서론/본론/결론)
    + 커버 이미지용 영어 프롬프트 자동 생성
            ↓
    [ HuggingFace FLUX.1-schnell ]
    커버 이미지 생성
            ↓
    블로그 글 + 커버 이미지(Base64) 동시 반환
```

---

## 사용 기술 스택

| 기술 | 역할 |
|------|------|
| **Claude API** (claude-sonnet-4-6) | 블로그 글 작성 + 이미지 프롬프트 생성 |
| **FLUX.1-schnell** | 커버 이미지 생성 |
| **FastAPI** | REST API 서버 |

---

## 블로그 구성 형식

```
# 제목
## 서론
## 본론 1
## 본론 2
## 본론 3 (선택)
## 결론
[커버 이미지 자동 생성]
```

---

## API 엔드포인트

| 메서드 | 경로 | 설명 |
|--------|------|------|
| `GET` | `/` | 서버 상태 확인 |
| `POST` | `/generate` | 블로그 글 + 커버 이미지 생성 |
| `GET` | `/docs` | Swagger UI |

---

## 요청 / 응답 예시

```bash
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "AI가 바꾸는 미래의 직업",
    "tone": "informative"
  }'
```

**톤 옵션**: `informative` (정보 전달) / `casual` (친근한) / `professional` (전문적)

**응답:**

```json
{
  "topic": "AI가 바꾸는 미래의 직업",
  "blog_content": "# AI가 바꾸는 미래의 직업\n\n## 서론\n인공지능은 빠른 속도로...",
  "image_prompt": "futuristic office with AI robots and humans working together...",
  "cover_image_base64": "iVBORw0KGgo..."
}
```

---

## 실행 방법

```bash
cp .env.example .env
pip install -r requirements.txt
cd app && uvicorn main:app --host 0.0.0.0 --port 8003
```

## 환경 변수

| 변수 | 설명 |
|------|------|
| `ANTHROPIC_API_KEY` | Anthropic Claude API 키 |
| `HF_TOKEN` | HuggingFace API 토큰 |
