import os
from pymongo import MongoClient, errors

class Connection:
    def __init__(self):
        self.user = os.getenv("MONGO_USER")
        self.password = os.getenv("MONGO_PASSWORD")
        self.host = os.getenv("MONGO_HOST", "localhost")
        self.port = os.getenv("MONGO_PORT", "27017")
        self.db = os.getenv("MONGO_DB","enemy_soldiers")
        self.auth = os.getenv("MONGO_AUTH_DB","admin")

        self.client = None

    def connect(self):
        try:
            self.client = MongoClient(
                host=self.host,
                port=int(self.port),
                username=self.user,
                password=self.password,
                authSource=self.auth,
                serverSelectionTimeoutMS=5000
            )
            self.client.server_info()
            print("MongoDB connected successfully")
            return self.client
        except errors.ServerSelectionTimeoutError as e:
            print("Failed to connect to MongoDB:", e)
            return None
        except errors.OperationFailure as e:
            print("Authentication failed:", e)
            return None

    def close(self):
        if self.client:
            self.client.close()
            print("MongoDB connection closed")
