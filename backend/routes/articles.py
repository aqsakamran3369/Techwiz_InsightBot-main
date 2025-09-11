from flask import Blueprint, request, jsonify
from pymongo import MongoClient

articles_bp = Blueprint("articles", __name__)

# MongoDB connection
client = MongoClient(
    "mongodb+srv://thewebwiz23:TheWebWiz2988@cluster0.8edmm.mongodb.net/insightbot_db?retryWrites=true&w=majority"
)
db = client.insightbot_db
collection = db.articles

@articles_bp.route("/", methods=["GET"])
def get_articles():
    """
    Fetch articles with optional filters:
    ?language=EN&dataset=training&page=1&limit=10
    """
    language = request.args.get("language")
    dataset = request.args.get("dataset")
    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 10))
    skip = (page - 1) * limit

    query = {}
    if language:
        query["language"] = {"$regex": language, "$options": "i"}
    if dataset:
        query["dataset_type"] = dataset.lower()

    articles_cursor = collection.find(query).skip(skip).limit(limit)
    articles = []
    for a in articles_cursor:
        articles.append({
            "url": a.get("url"),
            "title": a.get("title"),
            "body": a.get("body"),
            "source": a.get("source"),
            "language": a.get("language"),
            "dataset_type": a.get("dataset_type")
        })

    return jsonify({
        "page": page,
        "limit": limit,
        "count": len(articles),
        "articles": articles
    })
