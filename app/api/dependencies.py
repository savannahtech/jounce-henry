from app.db.session import get_db
from sqlalchemy.orm import Session

def get_database_session() -> Session:
    db = get_db()
    try:
        yield db
    finally:
        db.close()
