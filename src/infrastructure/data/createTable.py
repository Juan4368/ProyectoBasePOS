from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

from sqlalchemy import create_engine

from src.infrastructure.models.models import Base


def _load_dotenv_if_available() -> None:
    """
    Carga variables de entorno desde `.env`.

    - Si `python-dotenv` está instalado, lo usa.
    - Si no, intenta un parseo simple de archivos `.env`.
    """
    try:
        from dotenv import load_dotenv  # type: ignore
    except Exception:
        project_root = Path(__file__).resolve().parents[3]
        candidates = [
            project_root / ".env",
            project_root / "src" / "app" / ".env",
            project_root / "app" / ".env",
        ]
        for env_path in candidates:
            if env_path.exists():
                _load_env_file_simple(env_path)
                break
        return

    load_dotenv()


def _load_env_file_simple(path: Path) -> None:
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip("\"'").strip()
        if key and key not in os.environ:
            os.environ[key] = value


def create_tables(database_url: Optional[str] = None) -> None:
    """
    Crea todas las tablas declaradas en `Base.metadata`.

    - Si `database_url` es None, intenta usar la variable de entorno `DATABASE_URL`.
    - Si existe `python-dotenv`, carga `.env` automáticamente.
    """
    _load_dotenv_if_available()

    db_url = (database_url or os.getenv("DATABASE_URL") or "").strip()
    if not db_url:
        raise ValueError(
            "DATABASE_URL no está configurada. Define la variable de entorno DATABASE_URL "
            "o pasa `database_url` a create_tables()."
        )

    engine = create_engine(db_url, future=True)
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    create_tables()
    print("Tablas creadas exitosamente.")
