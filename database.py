from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

# Имя файла базы данных SQLite
DATABASE_URL = "sqlite:///./offers.db"

# Создание движка SQLAlchemy
engine = create_engine(DATABASE_URL)

# Создание сессии для работы с базой данных
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовый класс для объявления таблиц
Base = declarative_base()

# Определение модели таблицы "offers"
class Offer(Base):
    __tablename__ = "offers"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    category = Column(String)
    city = Column(String)
    discount = Column(Integer)
    price = Column(Integer)
    popularity = Column(Integer)
    start_date = Column(String)
    end_date = Column(String)