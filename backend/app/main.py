import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("agentforge.backend")

app = FastAPI(
    title="AgentForge API",
    description="Backend services and orchestration API for AgentForge",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "name": "AgentForge API",
        "status": "healthy",
        "version": "1.0.0"
    }

@app.get("/api/v1/health")
async def health_check():
    return {"status": "healthy"}
