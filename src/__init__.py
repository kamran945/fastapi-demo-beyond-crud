from fastapi import FastAPI
from contextlib import asynccontextmanager

from src.products.routes import product_router
from src.auth.routes import auth_router
from src.reviews.routes import review_router
from src.db.main import init_db
from .errors import register_all_errors
from .middleware import register_middleware


@asynccontextmanager
async def life_span(app: FastAPI):
    print("Server is starting...")
    try:
        await init_db()  # Initialize DB here
    except Exception as e:
        print(f"Error initializing DB: {e}")
    yield
    print("Server is stopping...")


version = "v1"

description = """
A REST API for a POS Software.
    """

version_prefix = f"/api/{version}"

app = FastAPI(
    title="pos-software",
    description=description,
    version=version,
    # lifespan=life_span,
)
register_all_errors(app)
register_middleware(app)

app.include_router(
    product_router, prefix=f"{version_prefix}/products", tags=["products"]
)
app.include_router(auth_router, prefix=f"{version_prefix}/auth", tags=["auth"])
app.include_router(review_router, prefix=f"{version_prefix}/reviews", tags=["reviews"])
