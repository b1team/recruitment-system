from sqlalchemy import Table
from databases import Database
from pydantic import BaseModel


class BaseHandler:
    def __init__(self, database: Database, model: Table):
        self._model = model
        self.db = database

    async def create(self, obj: BaseModel):
        result = None
        await self.db.connect()
        query = self._model.insert().values(**obj.dict())
        transaction = await self.db.transaction()
        try:
            result = await self.db.execute(query)
        except Exception as e:
            await transaction.rollback()
        else:
            await transaction.commit()
        await self.db.disconnect()
        return result

    async def read(self, _id: int):
        ...

    async def update(self, _id: int, new_obj: BaseModel):
        result = None
        await self.db.connect()
        query = self._model.update().where(self._model.c.id == _id).values(**new_obj.dict())
        transaction = await self.db.transaction()
        try:
            result = await self.db.execute(query)
        except Exception as e:
            await transaction.rollback()
        else:
            await transaction.commit()
        await self.db.disconnect()
        return result

    async def delete(self, _id: int):
        result = None
        await self.db.connect()
        query = self._model.delete().where(self._model.c.id == _id)
        transaction = await self.db.transaction()
        try:
            result = await self.db.execute(query)
        except Exception as e:
            await transaction.rollback()
        else:
            await transaction.commit()
        await self.db.disconnect()
        return result
