import asyncio
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from database import SessionLocal, engine, Base
from models import Item
from schemas import ItemCreate, ItemUpdate

app = FastAPI()

# Функция для получения сессии
async def get_db():
    async with SessionLocal() as session:
        yield session

# Создание таблиц при старте приложения
@app.on_event("startup")
async def startup():
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        print("Connection to DB OK!")
    except Exception as e:
        print("Connection to DB FAIL!")
        raise e

# Создание элемента
@app.post("/items/")
async def create_item(item: ItemCreate, db: AsyncSession = Depends(get_db)):
    item_db = Item(name=item.name, last_name=item.last_name, tel=item.tel, email=item.email)
    db.add(item_db)
    await db.commit()
    await db.refresh(item_db)
    return {"id": item_db.id, "name": item_db.name, "last name": item_db.last_name, "tel": item_db.tel, "email": item_db.email}

# Чтение одного элемента
@app.get("/items/{item_id}")
async def read_item(item_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Item).filter(Item.id == item_id))
    item = result.scalar_one_or_none()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"id": item.id, "name": item.name, "last name": item.last_name, "tel": item.tel, "email": item.email}

# Чтение всех элементов
@app.get("/items/")
async def read_items(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Item))
    items = result.scalars().all()
    return [{"id": item.id, "name": item.name, "last name": item.last_name, "tel": item.tel, "email": item.email} for item in items]

# Обновление элемента
@app.put("/items/{item_id}")
async def update_item(item_id: int, item_update: ItemUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Item).filter(Item.id == item_id))
    item = result.scalar_one_or_none()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    item.name = item_update.name
    item.last_name = item_update.last_name
    item.tel = item_update.tel
    item.email = item_update.email
    await db.commit()
    await db.refresh(item)
    return {"id": item.id, "name": item.name, "last name": item.last_name, "tel": item.tel, "email": item.email}

# Удаление элемента
@app.delete("/items/{item_id}")
async def delete_item(item_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Item).filter(Item.id == item_id))
    item = result.scalar_one_or_none()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    await db.delete(item)
    await db.commit()
    return {"message": "Item deleted"}