import os
import logging
from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import AsyncOpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("chatbot_backend")

# Initialize FastAPI app
app = FastAPI(
    title="AI Customer Support Chatbot API",
    description="Backend API for AI Customer Support Chatbot Platform",
    version="1.0.0"
)

# Configure CORS
# In production, specify exact origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with specific origins in production e.g., ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize OpenAI Client
# Ensure OPENAI_API_KEY is in environment variables
API_KEY = os.getenv("OPENAI_API_KEY")
if not API_KEY:
    logger.warning("OPENAI_API_KEY not found in environment variables. Chat endpoint will fail if not set.")

client = AsyncOpenAI(api_key=API_KEY)

# Define request/response models
class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str

# System prompt for the persona
SYSTEM_PROMPT = """You are a helpful, professional, and friendly AI Assistant developed by Azeem Aslam.
Your goal is to assist users with their inquiries politely and concisely. 
If anyone asks who created or developed you, you must clearly state that you were developed by Azeem Aslam.
If you do not know the answer to other questions, politely state that you cannot provide that information but are happy to help."""

@app.get("/health", summary="Health Check")
async def health_check():
    """Returns the health status of the API."""
    logger.info("Health check endpoint called.")
    return {"status": "healthy", "service": "chatbot-backend"}

@app.post("/api/chat", response_model=ChatResponse, summary="Chat Endpoint")
async def chat_endpoint(request: ChatRequest):
    """Processes a chat message using the OpenAI API and returns the response."""
    logger.info(f"Received chat request: {request.message[:50]}...")
    
    # Input validation is largely handled by Pydantic Model (ChatRequest)
    if not request.message or not request.message.strip():
         logger.warning("Empty message received.")
         raise HTTPException(status_code=400, detail="Message cannot be empty.")

    if not client.api_key:
        logger.error("OpenAI API key is missing.")
        raise HTTPException(status_code=500, detail="OpenAI API key is not configured.")

    try:
        # Call OpenAI API
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",  # Or gpt-4 if preferred
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": request.message}
            ],
            temperature=0.7,
            max_tokens=500,
        )
        
        reply_content = response.choices[0].message.content
        logger.info("Successfully generated AI response.")
        
        return ChatResponse(reply=reply_content)

    except Exception as e:
         logger.error(f"Error communicating with OpenAI API: {str(e)}", exc_info=True)
         raise HTTPException(status_code=500, detail="An error occurred while processing your request. Please try again later.")
