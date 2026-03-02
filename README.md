# Antigravity Subspace Chatbot Platform

A complete, production-grade AI Customer Support Chatbot Platform built for Antigravity Services. 

This repository contains a full-stack solution featuring a modern, responsive frontend and a highly performant Python FastAPI backend leveraging the OpenAI API. The entire system is fully containerized, CI/CD-ready, and architected for seamless cloud deployment.

![Chatbot Screenshot Placeholder](docs/screenshot.png) *(Note: Add a screenshot here before portfolio presentation)*

## Features
- **Frontend:** Responsive chat interface (HTML/CSS/JS) with premium modern aesthetics, typing indicators, and error resilience.
- **Backend:** Python FastAPI offering asynchronous endpoints (`/chat`, `/health`), strict payload validation via Pydantic, and structured logging.
- **AI Integration:** Direct integration with OpenAI's Chat Completions API with a customized support agent persona.
- **Containerization:** Multi-container Docker Compose architecture ensuring identical dev and production parity.
- **Proxy:** Nginx deployed as a reverse proxy for serving static files and securely routing API requests.

## Quick Start (Local Development)

### Prerequisites
- Docker and Docker Compose installed.
- An active OpenAI API Key.

### Setup Instructions
1. **Clone the repository:**
   ```bash
   git clone <repository_url>
   cd "Project 3 AI Chatbot Website Project"
   ```
2. **Configure Environment Variables:**
   ```bash
   cp .env.example .env
   ```
   Edit the `.env` file and insert your actual `OPENAI_API_KEY`.

3. **Run the System:**
   ```bash
   docker compose up --build
   ```
4. **Access the Chatbot:**
   Open your browser and navigate to: [http://localhost:3000](http://localhost:3000)

## System Architecture

The project consists of two main microservices managed via `docker-compose.yml`:
- **`frontend` (Nginx, Port 3000):** Serves the UI and proxies `/api/` calls to the backend service to bypass CORS complexities and establish a clean routing layer.
- **`backend` (FastAPI, Port 8000):** Validates input, constructs the Langchain/OpenAI prompt pipeline, performs the LLM call asynchronously, and handles error reporting securely.

Detailed documentation on the architecture and cloud deployment strategies can be found in the `docs/` folder:
- [Product Design](docs/product_design.md)
- [Architecture](docs/architecture.md)
- [AWS Deployment Plan](docs/aws_deployment.md)
- [QA Automation Plan](docs/qa_automation.md)
- [Security Plan](docs/security_plan.md)

## CI/CD Pipeline
A GitHub Actions workflow (`.github/workflows/ci.yml`) is included to automatically build the Docker containers and test the FastAPI `/health` endpoint on any `push` or `pull_request` to the `main` branch.

## Technologies Used
- **Backend:** Python 3.11, FastAPI, Uvicorn, Pydantic, OpenAI SDK.
- **Frontend:** Native HTML5, CSS3 Variables/Animations, Vanilla JavaScript (ES6+), Lucide Icons.
- **Infrastructure:** Docker, Docker Compose, Nginx, GitHub Actions.
