# System Architecture & Flow

## 1. High-Level Architecture
The AI Chatbot Platform follows a containerized, decoupled microservices architecture designed for local development and direct cloud deployment.

## 2. Components
### A. Frontend Container (Nginx)
- **Role:** Serves the static HTML, CSS, and JavaScript files to the client's browser. acts as a reverse proxy for the API.
- **Technology:** Nginx on Alpine Linux.
- **Networking:** Exposed on host port `3000`. Internally routes `/api/` traffic to the backend container.

### B. Backend Container (FastAPI)
- **Role:** The core application logic. It receives user messages, validates them, communicates with the OpenAI API, and returns the response.
- **Technology:** Python FastAPI, Uvicorn, OpenAI Python SDK.
- **Networking:** Exposed internally on port `8000`. It reaches out to the external internet to access the OpenAI API.

### C. External Services
- **OpenAI API:** Provides the generative AI capabilities (LLM) using `gpt-3.5-turbo` or `gpt-4`.

## 3. Service Communication Flow
1. **User Input:** The user types a message in the browser and clicks send.
2. **Frontend Request:** `app.js` makes a `POST /api/chat` request containing the message payload.
3. **Nginx Proxy:** The Nginx container intercepts the request on port 80 and reverse-proxies it to `http://backend:8000/api/chat`.
4. **Backend Processing:**
   - FastAPI receives the request and validates the body schema using Pydantic.
   - FastAPI forms a request to OpenAI using the configured API Key and System Prompt.
5. **OpenAI Generation:** OpenAI processes the request and returns the AI-generated reply.
6. **Response Routing:**
   - FastAPI receives the reply and formats it into a JSON response `{"reply": "..."}`.
   - Nginx forwards this JSON response back to the client.
7. **UI Update:** The client's JavaScript receives the JSON, removes the typing indicator, and appends the new message to the chat interface.

## 4. Container Interaction Model
The `docker-compose.yml` orchestrates the setup using a dedicated bridge network (`chatbot-network`). This ensures that:
- Containers can resolve each other by service name (e.g., `http://backend:8000`).
- The internal backend port does not need to be exposed directly to the outside world in production.
