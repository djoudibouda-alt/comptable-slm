import os
from dotenv import load_dotenv

load_dotenv()

NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY")
NVIDIA_BASE_URL = "https://integrate.api.nvidia.com/v1"

EMBEDDING_MODEL = "nvidia/nemotron-3-embed-1b"
EMBEDDING_DIMENSIONS = 2048

LLM_MODEL = "meta/llama-3.1-8b-instruct"

CHUNK_SIZE = 512
CHUNK_OVERLAP = 64
TOP_K = 4

USE_LOCAL_LLM = os.getenv("USE_LOCAL_LLM", "false").lower() == "true"
LOCAL_LLM_URL = os.getenv("LOCAL_LLM_URL", "http://localhost:11434/v1")
LOCAL_LLM_MODEL = os.getenv("LOCAL_LLM_MODEL", "comptable-slm")

if USE_LOCAL_LLM:
    LLM_MODEL = LOCAL_LLM_MODEL
elif not NVIDIA_API_KEY:
    raise ValueError(
        "NVIDIA_API_KEY non trouvée. "
        "Créez un fichier .env avec votre clé API NVIDIA (NGC), "
        "ou activez le LLM local avec USE_LOCAL_LLM=true."
    )
