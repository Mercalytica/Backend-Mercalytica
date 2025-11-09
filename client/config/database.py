from pymongo import MongoClient
from config.env import EnvConfig


class DatabaseConfig:
     def __init__(self):
          env = EnvConfig()
          mongo_url = env.get("MONGO_URL")
          self.client = MongoClient(mongo_url)
          self.db = self.client.get_database()

     def get_collection(self, collection_name: str):
          return self.db[collection_name]