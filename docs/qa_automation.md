# QA Automation Plan

## 1. Automated Testing Strategy
Quality Assurance will be automated primarily at the API level using `pytest` and at the UI level using `Playwright` or `Selenium`. Integration with GitHub Actions ensures that tests run on every Pull Request and Push to main.

## 2. API Test Scenarios (Backend)
- **Positive Testing (/chat):** 
  - Send a valid POST request with an inquiry. Expect 200 OK and a non-empty `reply` string payload.
- **Negative Testing (/chat):**
  - **Empty Message:** Send a POST request with an empty string. Expect a 400 Bad Request response.
  - **Missing Field:** Send a POST request without the `message` field. Expect a 422 Unprocessable Entity response (Pydantic validation).
- **Health Check (/health):**
  - Send a GET request to `/health`. Expect 200 OK and `{"status": "healthy"}`.
- **Failure Simulations:**
  - **Bad API Key:** Inject a fake `OPENAI_API_KEY` via env overrides and verify the API returns a 500 status with an appropriate user-facing error message handled gracefully.
  - **Timeout:** Mock the OpenAI client to simulate a timeout, verifying the FastAPI app doesn't hang indefinitely but returns a 504 Gateway Timeout or 500 Server Error.

## 3. UI Test Scenarios (Frontend)
- **Rendering:** Verify key elements (`#chat-messages`, `#message-input`, `#send-button`) load and are visible correctly.
- **Input Behavior:** Verify the Send button remains disabled while the input field is empty, and enables when text is typed.
- **End-to-End Chat Flow:**
  - Type a message and click Submit.
  - Verify the typing indicator `.typing-indicator` appears.
  - Verify a `.bot-message` appears after a delay and the typing indicator is removed.
- **Error States:** Simulate a 500 response from the mock backend and verify the UI shows the ".error-message" visual styling to the user.
