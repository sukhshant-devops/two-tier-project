from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
from bson.objectid import ObjectId
import os

app = Flask(__name__)

mongo_uri = os.getenv("MONGO_URI", "mongodb://mongo:27017/")
client = MongoClient(mongo_uri)
db = client["taskdb"]
collection = db["tasks"]

@app.route("/")
def index():
    tasks = list(collection.find())
    return render_template("index.html", tasks=tasks)

@app.route("/add", methods=["POST"])
def add_task():
    task = request.form.get("task")
    if task:
        collection.insert_one({"task": task})
    return redirect("/")

@app.route("/delete/<id>")
def delete_task(id):
    collection.delete_one({"_id": ObjectId(id)})
    return redirect("/")

@app.route("/health")
def health():
    return {"status": "OK"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
