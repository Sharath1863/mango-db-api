from fastapi import FastAPI
from pymongo import MongoClient
from configuration import Config

app = FastAPI()

# MongoDB connection
client = MongoClient(Config.MONGO_URI)
db = client[Config.DATABASE_NAME]
collection = db[Config.COLLECTION_NAME]

@app.get("/")
async def homepage():
    return {"message": "Hello, World!"}

@app.get("/users")
async def get_users():
    users = list(collection.find({}, {"_id": 0}))
    return {"users": users}
