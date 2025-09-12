from flask import Blueprint, request, jsonify
from pymongo import MongoClient, TEXT

articles_bp = Blueprint("articles", __name__)

# ---------------- MongoDB Connection ----------------
client = MongoClient(
    "mongodb+srv://muskankamran3369:muskurahat2328U@cluster0.fxk1min.mongodb.net/insightbot_db?retryWrites=true&w=majority&appName=Cluster0"
)
db = client.insightbot_db
collection = db.articles

# ---------------- Multilingual Index Setup ----------------
# Drop old indexes to avoid conflicts
collection.drop_indexes()

# Normalize languages
collection.update_many(
    {"language": {"$nin": ["EN", "AR", "RU", "FR"]}},
    {"$set": {"language": "none"}}
)
collection.update_many(
    {"language": "AR"},
    {"$set": {"language": "none"}}
)

# Create multilingual text index
collection.create_index(
    [("title", TEXT), ("body", TEXT)],
    default_language="none",
    name="multilang_text_index"
)

print("✅ Multilingual text index created successfully!")


# ---------------- Routes ----------------
from datetime import datetime

@articles_bp.route("/", methods=["GET"])
def get_articles():
    """
    Fetch articles with optional filters + multilingual keyword search + date filter:
    Example:
    /articles/?language=EN&dataset=training&search=climate&start_date=2025-01-01&end_date=2025-01-31&page=1&limit=10
    """
    language = request.args.get("language")
    dataset = request.args.get("dataset")
    search = request.args.get("search")
    start_date = request.args.get("start_date")  # format: YYYY-MM-DD
    end_date = request.args.get("end_date")      # format: YYYY-MM-DD
    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 10))
    skip = (page - 1) * limit

    query = {}

    # Language filter
    if language:
        query["language"] = {"$regex": f"^{language}$", "$options": "i"}

    # Dataset filter
    if dataset:
        query["dataset_type"] = dataset.lower()

    # Date filter
    if start_date or end_date:
        date_filter = {}
        if start_date:
            date_filter["$gte"] = datetime.strptime(start_date, "%Y-%m-%d")
        if end_date:
            date_filter["$lte"] = datetime.strptime(end_date, "%Y-%m-%d")
        query["publication_date"] = date_filter

    # Text search
    if search:
        query["$text"] = {"$search": search}

    # ---------------- Count total docs ----------------
    total_count = collection.count_documents(query)

    # ---------------- Fetch articles ----------------
    if search:
        articles_cursor = collection.find(
            query, {"score": {"$meta": "textScore"}}
        ).sort([("score", {"$meta": "textScore"})]).skip(skip).limit(limit)
    else:
        articles_cursor = collection.find(query).skip(skip).limit(limit)

    # Prepare response
    articles = []
    for a in articles_cursor:
        articles.append({
            "url": a.get("url"),
            "title": a.get("title"),
            "body": a.get("body"),
            "source": a.get("source"),
            "language": a.get("language"),
            "dataset_type": a.get("dataset_type"),
            "publication_date": a.get("publication_date")
        })

    return jsonify({
        "page": page,
        "limit": limit,
        "total": total_count,
        "count": len(articles),
        "articles": articles
    })
