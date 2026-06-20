# Blog Generator

주제를 입력하면 Claude가 블로그 글을 작성하고 FLUX.1이 커버 이미지를 생성하는 API

## 아키텍처

```
주제 + 톤 입력
        ↓
Claude API - 블로그 글 작성 + 이미지 프롬프트 생성
        ↓
HuggingFace FLUX.1-schnell - 커버 이미지 생성
        ↓
블로그 글 + 커버 이미지(base64) 반환
```

## 블로그 구성

- 제목
- 서론
- 본론 (2-3개 소제목)
- 결론
- 커버 이미지 (자동 생성)

## API 엔드포인트

| 메서드 | 경로 | 설명 |
|--------|------|------|
| GET | `/` | 서버 상태 확인 |
| POST | `/generate` | 블로그 글 + 이미지 생성 |
| GET | `/docs` | Swagger UI |

## 요청 예시

```bash
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"topic": "AI가 바꾸는 미래 직업", "tone": "informative"}'
```

## 응답 예시

```json
{
  "topic": "AI가 바꾸는 미래 직업",
  "blog_content": "# AI가 바꾸는 미래 직업\n\n...",
  "image_prompt": "futuristic workplace with AI robots...",
  "cover_image_base64": "iVBORw0KGgo..."
}
```

## 실행 방법

```bash
cp .env.example .env
pip install -r requirements.txt
cd app && uvicorn main:app --host 0.0.0.0 --port 8003
```

## 환경 변수

```
ANTHROPIC_API_KEY=   # Anthropic Claude API 키
HF_TOKEN=            # HuggingFace API 토큰
```
