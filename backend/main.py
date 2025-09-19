from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import SessionLocal, engine
from models import Product
import database_models
database_models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS for React dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# list of products with 4 products like phones, laptops, pens, tables
products = [
    Product(id=1, name="Siddharth", email="siddharth@example.com", phone_number=1234567890, current_status="Active", resume_link="https://drive.google.com/file/d/1PVIq4p1ua0G3zRRjQmERA4nSFwNWZzHY/view?usp=sharing"),
    Product(id=2, name="Yash", email="yash@example.com", phone_number=1234567891, current_status="Inactive", resume_link="https://drive.google.com/file/d/1PVIq4p1ua0G3zRRjQmERA4nSFwNWZzHY/view?usp=sharing"),
    Product(id=3, name="Priya", email="priya@example.com", phone_number=1234567892, current_status="Active", resume_link="https://drive.google.com/file/d/1PVIq4p1ua0G3zRRjQmERA4nSFwNWZzHY/view?usp=sharing"),
    Product(id=4, name="Abhi", email="abhi@example.com", phone_number=1234567893, current_status="Inactive", resume_link="https://drive.google.com/file/d/1PVIq4p1ua0G3zRRjQmERA4nSFwNWZzHY/view?usp=sharing"),
    Product(id=5, name="Anita", email="anita@example.com", phone_number=1234567894, current_status="Active", resume_link="https://drive.google.com/file/d/1PVIq4p1ua0G3zRRjQmERA4nSFwNWZzHY/view?usp=sharing"),
    Product(id=6, name="Rohit", email="rohit@example.com", phone_number=1234567895, current_status="Inactive", resume_link="https://drive.google.com/file/d/1PVIq4p1ua0G3zRRjQmERA4nSFwNWZzHY/view?usp=sharing"),
]





def init_db():
    db = SessionLocal()

    existing_count = db.query(database_models.Product).count()

    if existing_count == 0:
        for product in products:
            db.add(database_models.Product(**product.model_dump()))
        db.commit()
        print("Database initialized with sample products.")
        
    db.close()

init_db()    

@app.get('/')
def read_root():
    return {"message": "Welcome to the HR Database API"}

@app.get("/candidates/")
def get_all_products(db: Session = Depends(get_db)):
    products = db.query(database_models.Product).all()
    return products


@app.get("/candidates/{product_id}")
def get_product_by_id(product_id: int, db: Session = Depends(get_db)):
    product = db.query(database_models.Product).filter(database_models.Product.id == product_id).first()
    if product:
        return product
    return {"error": "Product not found"}

@app.post("/candidates/")
def create_product(product: Product, db: Session = Depends(get_db)):
    db.add(database_models.Product(**product.model_dump()))
    db.commit()
    return {"message": "Product created successfully", "product": product}

@app.put("/candidates/{product_id}")
def update_product(product_id: int, product: Product, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    db_product.name = product.name
    db_product.email = product.email
    db_product.phone_number = product.phone_number
    db_product.current_status = product.current_status
    db_product.resume_link = product.resume_link
    db.commit()
    db.refresh(db_product)
    return {"message": "Product updated successfully", "product": db_product}


@app.delete("/candidates/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(db_product)
    db.commit()
    return {"message": "Product deleted successfully"}
