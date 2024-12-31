from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession

from src.products.service import ProductService
from src.db.main import get_session
from src.auth.dependencies import AccessTokenBearer, RoleChecker

from .schemas import Product, ProductCreateModel, ProductUpdateModel, ProductDetailModel
from src.errors import ProductNotFound

product_router = APIRouter()
product_service = ProductService()
access_token_bearer = AccessTokenBearer()
role_checker = Depends(RoleChecker(allowed_roles=["admin", "user"]))


@product_router.get("/", response_model=List[Product], dependencies=[role_checker])
async def get_all_products(
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(access_token_bearer),
):
    products = await product_service.get_all_products(session)
    return products


@product_router.get(
    "/user/{user_uid}", response_model=List[Product], dependencies=[role_checker]
)
async def get_user_Product_submissions(
    user_uid: str,
    session: AsyncSession = Depends(get_session),
    _: dict = Depends(access_token_bearer),
):
    products = await product_service.get_user_products(user_uid, session)
    return products


@product_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=Product,
    dependencies=[role_checker],
)
async def create_a_product(
    product_data: ProductCreateModel,
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(access_token_bearer),
) -> dict:
    # print(f"user_uid: {token_details.get('user')['user_uid']}")
    user_uid = token_details.get("user")["user_uid"]
    new_product = await product_service.create_product(product_data, user_uid, session)

    return new_product


@product_router.get(
    "/{product_uid}", response_model=ProductDetailModel, dependencies=[role_checker]
)
async def get_product(
    product_uid: str,
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(access_token_bearer),
) -> dict:
    product = await product_service.get_product(product_uid, session)

    if product:
        return product
    else:
        raise ProductNotFound()


@product_router.patch(
    "/{product_uid}", response_model=Product, dependencies=[role_checker]
)
async def update_product(
    product_uid: str,
    product_update_data: ProductUpdateModel,
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(access_token_bearer),
) -> dict:
    updated_product = await product_service.update_product(
        product_uid, product_update_data, session
    )

    if updated_product is None:
        raise ProductNotFound()
    else:
        return updated_product


@product_router.delete(
    "/{product_uid}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[role_checker],
)
async def delete_product(
    product_uid: str,
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(access_token_bearer),
):
    product_to_delete = await product_service.delete_product(product_uid, session)

    if product_to_delete is None:
        raise ProductNotFound()
    else:
        return {}
