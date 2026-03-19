from fastapi import FastAPI, HTTPException, Query
from typing import Optional
from products import get_product_by_id, search_products
from models import Product

app = FastAPI(title="Product API")

@app.get("/product/{product_id}", response_model=Product)
async def get_product(product_id: int):
    product = get_product_by_id(product_id)
    
    if not product:
        raise HTTPException(status_code=404, detail=f"Товар с ID {product_id} не найден")
    return product

@app.get("/products/search", response_model=list[Product])
async def search_products_endpoint(
    keyword: str = Query(..., description="Ключевое слово для поиска"),
    category: Optional[str] = Query(None, description="Категория для фильтрации"),
    limit: int = Query(10, description="Максимальное количество результатов", ge=1, le=50)
):
    results = search_products(keyword, category, limit)
    return results