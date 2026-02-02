from dataclasses import dataclass
from pathlib import Path

@dataclass
class Config:
    # Paths
    data_dir: Path = Path("data")
    db_path: Path = Path("data/database/ecommerce.db")
    
    # LLM
    ollama_url: str = "http://localhost:11434/api/generate"
    model: str = "mistral"
    temperature: float = 0.0
    max_tokens: int = 200
    
    # SQL Generation
    max_retries: int = 2

CONFIG = Config()
