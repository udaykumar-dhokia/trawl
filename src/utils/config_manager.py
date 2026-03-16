import os
import json
from pathlib import Path
from typing import Optional, List, Dict, Any
import httpx

class ConfigManager:
    """Manages SearchX configuration in ~/.searchx/config.json"""
    
    CONFIG_DIR = Path.home() / ".searchx"
    CONFIG_FILE = CONFIG_DIR / "config.json"

    @classmethod
    def get_config(cls) -> Dict[str, Any]:
        """Read configuration from file."""
        if not cls.CONFIG_FILE.exists():
            return {}
        try:
            with open(cls.CONFIG_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return {}

    @classmethod
    def save_config(cls, config: Dict[str, Any]) -> None:
        """Save configuration to file."""
        cls.CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        with open(cls.CONFIG_FILE, "w") as f:
            json.dump(config, f, indent=4)

    @classmethod
    def is_configured(cls) -> bool:
        """Check if essential configuration exists."""
        config = cls.get_config()
        if not config:
            return False
            
        provider = config.get("provider")
        if provider == "google":
            return bool(config.get("google_api_key") and config.get("model"))
        elif provider == "ollama":
            return bool(config.get("ollama_base_url") and config.get("model"))
        return False

    @staticmethod
    async def fetch_ollama_models(base_url: str) -> List[str]:
        """Fetch available models from Ollama."""
        try:
            url = f"{base_url.rstrip('/')}/api/tags"
            async with httpx.AsyncClient(timeout=5) as client:
                resp = await client.get(url)
                if resp.status_code == 200:
                    data = resp.json()
                    return [m["name"] for m in data.get("models", [])]
        except Exception:
            pass
        return ["llama3", "mistral", "phi3"]

    @staticmethod
    async def fetch_google_models(api_key: str) -> List[str]:
        """Fetch available Gemini models."""
        try:
            import google.generativeai as genai
            genai.configure(api_key=api_key)
            models = []
            for m in genai.list_models():
                if "generateContent" in m.supported_generation_methods:
                    models.append(m.name.replace("models/", ""))
            return models if models else ["gemini-2.5-flash", "gemini-2.5-pro"]
        except Exception:
            pass
        return ["gemini-2.5-flash", "gemini-2.5-pro"]
