import uvicorn
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
import os

from database import engine, SessionLocal, Base, Offer

# Инициализация приложения FastAPI
app = FastAPI()

# Добавление CORS-middleware для разрешения запросов с вашего фронтенда
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic-модель для валидации данных о предложении
class OfferModel(BaseModel):
    title: str
    category: str
    city: str
    discount: int
    price: int
    popularity: int
    start_date: str
    end_date: str

class OfferResponse(BaseModel):
    id: int
    title: str
    category: str
    city: str
    discount: int
    price: int
    popularity: int
    start_date: str
    end_date: str

# Создание таблиц в базе данных
@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)

# Зависимость для сессии базы данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Путь для получения всех предложений
@app.get("/offers", response_model=List[OfferResponse])
def get_offers(category: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(Offer)
    if category:
        query = query.filter(Offer.category == category)
    offers = query.all()
    return offers

# Путь для добавления нового предложения
# Защищенный маршрут, который будет использоваться админом
@app.post("/offers", response_model=OfferResponse)
def create_offer(offer: OfferModel, db: Session = Depends(get_db)):
    new_offer = Offer(**offer.dict())
    db.add(new_offer)
    db.commit()
    db.refresh(new_offer)
    return new_offer

# Дополнительные маршруты для администратора
@app.delete("/offers/{offer_id}")
def delete_offer(offer_id: int, db: Session = Depends(get_db)):
    offer = db.query(Offer).filter(Offer.id == offer_id).first()
    if not offer:
        raise HTTPException(status_code=404, detail="Offer not found")
    db.delete(offer)
    db.commit()
    return {"message": "Offer deleted successfully"}

@app.put("/offers/{offer_id}", response_model=OfferResponse)
def update_offer(offer_id: int, offer: OfferModel, db: Session = Depends(get_db)):
    existing_offer = db.query(Offer).filter(Offer.id == offer_id).first()
    if not existing_offer:
        raise HTTPException(status_code=404, detail="Offer not found")
    
    for key, value in offer.dict().items():
        setattr(existing_offer, key, value)
    
    db.commit()
    db.refresh(existing_offer)
    return existing_offer

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)