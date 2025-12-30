import os
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from models import Product 
from database import session
import database_models
from database import engine
from sqlalchemy.orm import Session


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins =["*"],
    allow_credentials=True,
    allow_methods = ["*"],
    allow_headers=["*"],
)

database_models.Base.metadata.create_all(bind=engine)

@app.get("/")
def greet():
    return "Welome to fastapi tutorial"

products = [
    Product(id=1, name="Phone", description="A smartphone", price=99, quantity=20),
    Product(id=2, name="Lapttop", description="A powerful laptop", price=999, quantity=10),
    Product(id=3, name="Pen", description="A blue ink pen", price=9, quantity=30),
    Product(id=4, name="Table", description="A wooden table", price=79, quantity=20),
]

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()

def init_db():
    db = session()

    count = db.query(database_models.Product).count()

    if count == 0:
        for product in products:
            db.add(database_models.Product(**product.model_dump()))

        db.commit() 
    db.close()   
init_db()


#Fetch all records at once
@app.get("/products")
def get_all_products(db:Session = Depends(get_db)):

    db_products = db.query(database_models.Product).all()
    return db_products

#fetch multiple records by id
@app.get("/products/{id}")
def get_product_by_id(id: int, db:Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_product:
        return db_product        
    return "Product not found"


#Add product
@app.post("/products")
def add_product(product: Product, db:Session = Depends(get_db)):
    db.add(database_models.Product(**product.model_dump()))
    db.commit()
    return product

#Update product list 
@app.put("/products/{id}")
def update_product(id: int, product: Product, db:Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_product:
        db_product.name = product.name
        db_product.description = product.description
        db_product.price = product.price
        db_product.quantity = product.quantity
        db.commit()
        return "product updated"
    else:
        return "Product not found"


#Delete product on the basis of id
@app.delete("/products/{id}")
def delete_product(id: int, db:Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
        return "Product deleted successfully"
    else:
        return "product not found"
    
# IMPORTANT: This allows Railway to run the app
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
