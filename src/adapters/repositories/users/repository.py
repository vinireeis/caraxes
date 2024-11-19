from loguru import logger
from sqlalchemy import select, func, insert, delete
from sqlalchemy.exc import NoResultFound, IntegrityError

from src import UserModel
from src.adapters.data_types.requests.users_request import (
    NewUserRequest,
    UpdateUserRequest,
)
from src.adapters.data_types.typed_dicts.users_typed_dict import PaginatedUsersTypedDict
from src.domain.exceptions.repository.exception import (
    UserNotFoundError,
    EmailAlreadyExists,
)
from src.externals.infrastructures.postgres.infrastructure import PostgresInfrastructure


class UserRepository:
    postgres_infrastructure = PostgresInfrastructure()

    @classmethod
    async def insert_one_user(cls, user_request: NewUserRequest) -> UserModel:
        try:
            async with cls.postgres_infrastructure.get_session() as session:
                user_dict = user_request.model_dump()
                statement = insert(UserModel).values(user_dict).returning(UserModel)
                db_result = await session.execute(statement)

                await session.commit()
                new_user_model = db_result.fetchone()

                return new_user_model

        except IntegrityError as ex:
            logger.info(ex.orig.__str__())
            raise EmailAlreadyExists()

    @classmethod
    async def get_users_paginated(cls, limit=10, offset=0) -> PaginatedUsersTypedDict:
        async with cls.postgres_infrastructure.get_session() as session:
            statement = select(UserModel).limit(limit).offset(offset)
            db_result = await session.execute(statement)
            users_model = db_result.scalars().all()

            total_users = await session.execute(select(func.count(UserModel.id)))
            total_count = total_users.scalar()

            return PaginatedUsersTypedDict(
                users=users_model, total=total_count, limit=limit, offset=offset
            )

    async def get_one_user_by_id(self, user_id: int) -> UserModel:
        async with self.postgres_infrastructure.get_session() as session:
            statement = select(UserModel).where(UserModel.id == user_id)
            try:
                db_result = await session.execute(statement)
                user = db_result.scalar_one()
                return user

            except NoResultFound as ex:
                logger.info(ex)
                raise UserNotFoundError(user_id)

    async def update_user(
        self, user_id: int, update_user_request: UpdateUserRequest
    ) -> UserModel:
        async with self.postgres_infrastructure.get_session() as session:
            statement = select(UserModel).where(UserModel.id == user_id)
            try:
                db_result = await session.execute(statement)
                user = db_result.scalar_one()

                user_data = update_user_request.model_dump(exclude_unset=True)
                for key, value in user_data.items():
                    setattr(user, key, value)

                await session.commit()
                return user

            except NoResultFound as ex:
                logger.info(ex)
                raise UserNotFoundError(user_id)

            except IntegrityError as ex:
                logger.info(ex)
                raise EmailAlreadyExists()

    async def delete_one_user_by_id(self, user_id: int) -> None:
        async with self.postgres_infrastructure.get_session() as session:
            statement = (
                delete(UserModel).where(UserModel.id == user_id).returning(UserModel.id)
            )

            db_result = await session.execute(statement)
            deleted_id = db_result.scalar()

            if not deleted_id:
                raise UserNotFoundError(user_id=user_id)

            await session.commit()
