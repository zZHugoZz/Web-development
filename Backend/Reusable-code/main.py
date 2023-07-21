from fastapi import FastAPI, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from . import models
from .database import engine, get_db
from .schemas import Product


models.Base.metadata.create_all(bind=engine)
app = FastAPI()


@app.get(
    "/products",
    status_code=status.HTTP_200_OK,
    response_model=list[Product]
)
def get_products(db: Session = Depends(get_db)):
    """queries all the products stored in the database"""
    products = db.query(models.Product).all()
    return products


@app.get(
    "/products/{product_id}",
    status_code=status.HTTP_200_OK,
    response_model=Product
)
def get_product(product_id: int, db: Session = Depends(get_db)):
    """gets only one product. We query it by filtering the products table
    to retrieve only the product that has the id that we passed"""
    product_query = db.query(models.Product).filter(
        models.Product.id == product_id
    )
    if product_query.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id: {product_id} doesn't exist"
        )
    return product_query.first()


@app.post(
    "/products",
    status_code=status.HTTP_201_CREATED,
    response_model=Product
)
def create_product(product: Product, db: Session = Depends(get_db)):
    """creates a new product. We pass the fields by converting the product pydantic model
    to a dictionay and unpacking it, then we add the new instance to the databsase,
    we commit the changes and refresh the database to get the newly created instance so that
    we can return it to the client"""
    created_product = models.Product(**product.model_dump())
    db.add(created_product)
    db.commit()
    db.refresh(created_product)
    return created_product


@app.put(
    "/products/{product_id}",
    status_code=status.HTTP_200_OK,
    response_model=Product
)
def update_product(
    product_id: int,
    product: Product,
    db: Session = Depends(get_db)
):
    """updates an existing product. We query the product by filtering the products
    table using the id, the we check if a product with the id that we passed exists
    if it doesn't we raise an exception. If it exists we update it and commit the
    changes. Then we simply return it to the client"""
    product_query = db.query(models.Product).filter(
        models.Product.id == product_id
    )
    if product_query.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id: {product_id} doesn't exist"
        )
    product_query.update(product.model_dump())
    db.commit()
    return product_query.first()


@app.delete(
    "/products/{product_id}",
    status_code=status.HTTP_200_OK,
)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    """deletes a product. We query the product that we want to delete just like before,
    we check if it exists then we delete it, commit the changes and return a response with
    a status code of 204 signaling that every went well"""
    product_query = db.query(models.Product).filter(
        models.Product.id == product_id
    )
    if product_query.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id: {product_id} doesn't exist"
        )
    product_query.delete()
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
