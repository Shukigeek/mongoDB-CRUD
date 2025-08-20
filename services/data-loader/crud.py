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
        self.collection = self.db[os.getenv("MONGO_COLLECTION", "soldier_details")]

    def create(self, soldier: Soldier):
        if isinstance(soldier, Soldier):
            # checking if there is a soldier with that ID in db
            existing = self.collection.find_one({"ID": soldier.ID})
            if existing:
                return {"error": f"Soldier with ID {soldier.ID} already exists. Try update instead."}

            # if not exist insert to db
            result = self.collection.insert_one(soldier.dict())
            return {"record_inserted": str(result.inserted_id)}

        elif isinstance(soldier, list) and all(isinstance(s, Soldier) for s in soldier):
            # list of all the soldiers
            inserted = []
            for s in soldier:
                if not self.collection.find_one({"ID": s.ID}):  # insert only if not already exist
                    result = self.collection.insert_one(s.dict())
                    inserted.append(result.inserted_id)
            return {"records_inserted": len(inserted)}

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
