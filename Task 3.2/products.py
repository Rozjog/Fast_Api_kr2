from models import Product

sample_product_1 = Product(
    product_id=123,
    name="Smartphone",
    category="Electronics",
    price=599.99
)

sample_product_2 = Product(
    product_id=456,
    name="Phone Case",
    category="Accessories",
    price=19.99
)

sample_product_3 = Product(
    product_id=789,
    name="Iphone",
    category="Electronics",
    price=1299.99
)

sample_product_4 = Product(
    product_id=101,
    name="Headphones",
    category="Accessories",
    price=99.99
)

sample_product_5 = Product(
    product_id=202,
    name="Smartwatch",
    category="Electronics",
    price=299.99
)

sample_products = [sample_product_1, sample_product_2, sample_product_3, sample_product_4, sample_product_5]

def get_product_by_id(product_id: int):
    for product in sample_products:
        if product.product_id == product_id:
            return product
    return None

def search_products(keyword: str, category: str = None, limit: int = 10):
    results = []
    keyword_lower = keyword.lower()
    
    for product in sample_products:
        name_match = keyword_lower in product.name.lower()

        
        if name_match:
            if category and category.lower() != product.category.lower():
                continue
            results.append(product)
    
    return results[:limit]