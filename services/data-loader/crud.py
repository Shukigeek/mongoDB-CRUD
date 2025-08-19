import os
from mongo_dal import Connection
from soldier import Soldier

class CRUD:
    def __init__(self):
        self.conn = Connection()
        self.client = self.conn.connect()
        if self.client is None:
            raise Exception(
                "Cannot connect to MongoDB. Check MONGO_HOST, MONGO_PORT, MONGO_USER, MONGO_PASSWORD, MONGO_DB"
            )

        self.db = self.client[self.conn.db]
        self.collection = self.db[os.getenv("MONGO_COLLECTION")]
        # special collection for the ID count (auto increment)
        self.counter_collection = self.db["counters"]

    def _get_next_id(self):
        # Finds the current value and increments it by 1,
        # if no current value found, new creator exists.
        counter = self.counter_collection.find_one_and_update(
            {"_id": "soldier_id"},
            {"$inc": {"seq": 1}},
            upsert=True,
            return_document=True
        )
        return counter["seq"]

    def create(self, soldier):
        if isinstance(soldier, Soldier):
            # adding ID automatically
            soldier.ID = self._get_next_id()
            result = self.collection.insert_one(soldier.dict())
            return {"record_inserted": str(result.inserted_id)}
        elif isinstance(soldier, list) and all(isinstance(s, Soldier) for s in soldier):
            for s in soldier:
                s.ID = self._get_next_id()
            result = self.collection.insert_many([s.dict() for s in soldier])
            return {"records_inserted": len(result.inserted_ids)}
        else:
            raise ValueError("Input must be a Soldier instance or a list of Soldier instances")

    def read(self, name=None):
        if name is None:
            cursor = self.collection.find({}, {"_id": 0})
            res = list(cursor)
            return res  # if collection is empty it will return -> []
        else:
            cursor = list(self.collection.find({"first_name": name}, {"_id": 0}))
            if cursor:
                return cursor
            else:
                return [{"error": f"{name} not exist in db"}]

    def update(self, ID, updates: dict):
        result = self.collection.update_one({"ID": ID}, {"$set": updates})
        if result.matched_count:
            return {"success": True, "modified_count": result.modified_count}
        else:
            return {"success": False, "error": f"ID {ID} not found"}

    def delete(self):
        pass