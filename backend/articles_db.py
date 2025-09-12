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
@articles_bp.route("/", methods=["GET"])
def get_articles():
    """
    Fetch articles with optional filters + multilingual keyword search:
    Example:
    /articles/?language=EN&dataset=training&search=climate&page=1&limit=10
    """
    language = request.args.get("language")
    dataset = request.args.get("dataset")
    search = request.args.get("search")
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

    # Text search
    if search:
        query["$text"] = {"$search": search}

    # ---------------- Count total docs ----------------
    total_count = collection.count_documents(query)

    # ---------------- Fetch articles ----------------
    if search:
        articles_cursor = collection.find(query, {"score": {"$meta": "textScore"}}) \
                                    .sort([("score", {"$meta": "textScore"})]) \
                                    .skip(skip).limit(limit)
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
            "dataset_type": a.get("dataset_type")
        })

    return jsonify({
        "page": page,
        "limit": limit,
        "total": total_count,   # <-- proper total count for frontend pagination
        "count": len(articles),
        "articles": articles
    })
