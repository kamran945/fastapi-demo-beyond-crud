from datetime import datetime

from sqlmodel import desc, select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.db.models import Product

from .schemas import ProductCreateModel, ProductUpdateModel


class ProductService:
    async def get_all_products(self, session: AsyncSession):
        statement = select(Product).order_by(desc(Product.created_at))

        result = await session.exec(statement)

        return result.all()

    async def get_user_products(self, user_uid: str, session: AsyncSession):
        statement = (
            select(Product)
            .where(Product.user_uid == user_uid)
            .order_by(desc(Product.created_at))
        )

        result = await session.exec(statement)

        return result.all()

    async def get_product(self, product_uid: str, session: AsyncSession):
        statement = select(Product).where(Product.puid == product_uid)

        # from sqlalchemy.orm import selectinload

        # statement = (
        #     select(Product)
        #     .options(selectinload(Product.reviews))
        #     .where(Product.puid == product_uid)
        # )

        result = await session.exec(statement)

        product = result.first()

        return product if product is not None else None

    async def create_product(
        self, product_data: ProductCreateModel, user_uid: str, session: AsyncSession
    ):
        product_data_dict = product_data.model_dump()

        new_product = Product(**product_data_dict)
        new_product.user_uid = user_uid

        session.add(new_product)
        await session.commit()

        return new_product

    async def update_product(
        self, product_uid: str, update_data: ProductUpdateModel, session: AsyncSession
    ):
        product_to_update = await self.get_product(product_uid, session)

        if product_to_update is not None:
            update_data_dict = update_data.model_dump()

            for k, v in update_data_dict.items():
                setattr(product_to_update, k, v)

            await session.commit()

            return product_to_update
        else:
            return None

    async def delete_product(self, product_uid: str, session: AsyncSession):
        product_to_delete = await self.get_product(product_uid, session)

        if product_to_delete is not None:
            await session.delete(product_to_delete)

            await session.commit()

            return {}

        else:
            return None
