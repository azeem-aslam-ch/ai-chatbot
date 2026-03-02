# Security Plan

This project implements the following measures to operate securely in a production environment.

## 1. Secrets Management
- **API Key Protection:** The `OPENAI_API_KEY` is completely isolated from the frontend. It is only accessible within the backend container via environment variables.
- **No Secrets in Source:** The `.env` file is excluded from version control via `.gitignore`. The repository only includes `.env.example`.
- **Cloud Secrets:** In production (AWS), secrets will be managed by AWS Secrets Manager or Systems Manager Parameter Store, rather than plaintext `.env` files.

## 2. Network Security
- **CORS Rules:** Cross-Origin Resource Sharing (CORS) is enabled in FastAPI (`main.py`). Currently set to `allow_origins=["*"]` for local development. **Must be restricted to the exact production domain (e.g., `["https://www.antigravityservices.com"]`) before deployment.**
- **Backend Isolation:** The backend API (port 8000) does not need to be exposed to the public internet. The frontend Nginx container (port 80) proxies traffic explicitly and only for the `/api/` matching routes.

## 3. Application Security & Input Sanitization
- **XSS Prevention:** The frontend `app.js` employs a custom `escapeHTML()` function on all user input and server output before rendering it into the DOM to prevent Cross-Site Scripting (XSS) attacks.
- **Payload Validation:** FastAPI leverages Pydantic models to strictly validate incoming JSON payloads, refusing arbitrary keys or overly large inputs depending on additional validations implemented.
- **Rate Limiting:** (To be implemented before production) Nginx `limit_req` or a FastAPI rate-limiting middleware should be added to prevent DDoS or excessive OpenAI API cost exploitation.
