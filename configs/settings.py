"""
configs/settings.py

Centralized, type-safe configuration for the entire JARVIS app.

Design rule (see docs/ARCHITECTURE.md, section 6):
    - This is the ONLY place that reads environment variables / .env.
    - Every other module receives config via the `settings` singleton below,
      never via `os.getenv()` directly. This keeps secrets and config
      auditable from one place and makes testing easy (just monkeypatch
      `settings`).

Usage:
    from configs.settings import settings
    print(settings.anthropic_api_key)
"""

from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

# Project root = two levels up from this file (configs/settings.py -> jarvis/)
PROJECT_ROOT = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    """
    All application configuration lives here. Values are loaded, in order
    of precedence, from: real environment variables > .env file > defaults
    below.
    """

    model_config = SettingsConfigDict(
        env_file=str(PROJECT_ROOT / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # --- App ---
    app_name: str = Field(default="JARVIS", alias="JARVIS_APP_NAME")
    env: str = Field(default="development", alias="JARVIS_ENV")
    log_level: str = Field(default="INFO", alias="JARVIS_LOG_LEVEL")

    # --- LLM ---
    anthropic_api_key: str = Field(default="", alias="ANTHROPIC_API_KEY")
    llm_model: str = Field(default="claude-sonnet-4-6", alias="JARVIS_LLM_MODEL")

    # --- Memory ---
    memory_backend: str = Field(default="json", alias="JARVIS_MEMORY_BACKEND")
    memory_path: str = Field(default="database/memory.json", alias="JARVIS_MEMORY_PATH")
    memory_max_turns: int = Field(default=20, alias="JARVIS_MEMORY_MAX_TURNS")

    # --- Voice (filled in Day 6-7) ---
    wake_word: str = Field(default="jarvis", alias="JARVIS_WAKE_WORD")
    stt_backend: str = Field(default="faster_whisper", alias="JARVIS_STT_BACKEND")
    tts_backend: str = Field(default="pyttsx3", alias="JARVIS_TTS_BACKEND")

    # --- Paths (derived, not env-driven) ---
    @property
    def project_root(self) -> Path:
        return PROJECT_ROOT

    @property
    def logs_dir(self) -> Path:
        path = PROJECT_ROOT / "logs"
        path.mkdir(parents=True, exist_ok=True)
        return path

    @property
    def memory_full_path(self) -> Path:
        path = PROJECT_ROOT / self.memory_path
        path.parent.mkdir(parents=True, exist_ok=True)
        return path

    def validate_required(self) -> list[str]:
        """
        Returns a list of human-readable problems with the current config.
        Called once at startup so we fail fast and loud instead of crashing
        deep inside a skill at demo time.
        """
        problems = []
        if not self.anthropic_api_key:
            problems.append(
                "ANTHROPIC_API_KEY is not set. Copy configs/.env.example to "
                ".env (project root) and fill in a real key."
            )
        return problems


@lru_cache
def get_settings() -> Settings:
    """Cached singleton so .env is only parsed once per process."""
    return Settings()


# Convenience import: `from configs.settings import settings`
settings = get_settings()
