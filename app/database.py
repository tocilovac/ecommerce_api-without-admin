from sqlmodel import SQLModel, create_engine, Session

# You can switch to PostgreSQL later if needed
DATABASE_URL = "sqlite:///./ecommerce.db"

engine = create_engine(DATABASE_URL, echo=True)

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
