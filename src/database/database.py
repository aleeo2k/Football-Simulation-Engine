from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.database.models import Base


class Database:
    def __init__(self):
        db_dir = Path("data/database")
        db_dir.mkdir(parents=True, exist_ok=True)

        self.db_path = db_dir / "football.db"

        self.engine = create_engine(
            f"sqlite:///{self.db_path}",
            echo=False
        )

        self.Session = sessionmaker(bind=self.engine)

        # Создаем все таблицы
        Base.metadata.create_all(self.engine)

    def get_session(self):
        return self.Session()