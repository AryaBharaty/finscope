from backend.app.models.transaction import Base
from backend.app.core.database import engine

Base.metadata.create_all(bind=engine)
