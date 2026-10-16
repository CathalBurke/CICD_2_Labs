import os
import httpx2
PRODUCT_SERVICE_URL = os.getenv(
    "PRODUCT_SERVICE_URL", "http://127.0.0.1:8001"
)

def fetch_product(product_id: int) -> dict:
    response = httpx2.get(
        f"{PRODUCT_SERVICE_URL}/products/{product_id}",
        timeout=3.0,
    )
    response.raise_for_status()
    return response.json()

#dependancy injection for Product service client
def get_product_fetcher():
    return fetch_product