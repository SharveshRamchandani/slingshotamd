class BaseConnector:
    async def fetch_data(self, user_id: int):
        raise NotImplementedError("fetch_data must be implemented")

    async def save_raw_data(self, db, user_id: int, source: str, data: dict):
        document = {
            "user_id": user_id,
            "source": source,
            "data": data,
            "processed": False
        }
        await db["raw_messages"].insert_one(document)
        return document
