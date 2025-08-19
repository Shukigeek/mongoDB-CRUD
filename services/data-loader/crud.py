import os
from mongo_dal import Connection
from soldier import Soldier
from pymongo import ReturnDocument

class CRUD:
    def __init__(self):
        self.conn = Connection()
        self.client = self.conn.connect()
        if self.client is None:
            raise Exception(
                "Cannot connect to MongoDB. Check MONGO_HOST, MONGO_PORT, MONGO_USER, MONGO_PASSWORD, MONGO_DB"
            )

        self.db = self.client[self.conn.db]
        self.collection = self.db[os.getenv("MONGO_COLLECTION", "soldier_details")]
        self.counter_collection = self.db.get_collection("counters")

    def _get_next_id(self):
        counter = self.counter_collection.find_one_and_update(
            {"_id": "soldier_id"},
            {"$inc": {"seq": 1}},
            upsert=True,
            return_document=ReturnDocument.AFTER
        )
        if counter is None or "seq" not in counter:
            self.counter_collection.insert_one({"_id": "soldier_id", "seq": 1})
            return 1
        return counter["seq"]

    def create(self, soldier):
        if isinstance(soldier, Soldier):
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

    def read(self, ID=None, first_name=None):
        filter_query = {}
        if ID is not None:
            filter_query["ID"] = ID
        elif first_name is not None:
            filter_query["first_name"] = first_name

        cursor = list(self.collection.find(filter_query, {"_id": 0}))
        if not cursor:
            return [{"error": "No matching record found"}]
        return cursor

    def update(self, ID, updates: dict):
        result = self.collection.update_one({"ID": ID}, {"$set": updates})
        if result.matched_count:
            return {"success": True, "modified_count": result.modified_count}
        else:
            return {"success": False, "error": f"ID {ID} not found"}

    def delete(self, ID):
        result = self.collection.delete_one({"ID": ID})
        if result.deleted_count:
            return {"success": True}
        else:
            return {"success": False, "error": f"ID {ID} not found"}
