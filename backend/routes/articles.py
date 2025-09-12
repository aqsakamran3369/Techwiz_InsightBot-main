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
# Drop all old indexes and recreate fresh multilingual index
collection.drop_indexes()

# Create a multilingual text index on title + body
collection.create_index(
    [("title", TEXT), ("body", TEXT)],
    default_language="none",   # neutral → all langs work
    name="multilang_text_index"
)

print("✅ Multilingual text index created successfully!")


# ---------------- Routes ----------------
@articles_bp.route("/", methods=["GET"])
def get_articles():
    language = request.args.get("language")
    dataset = request.args.get("dataset")
    search = request.args.get("search")
    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 40))
    skip = (page - 1) * limit

    # Build query dynamically
    query = {}
    if language:
        query["language"] = {"$regex": f"^{language}$", "$options": "i"}
    if dataset:
        query["dataset_type"] = dataset.lower()
    if search:
        query["$text"] = {"$search": search}

    # Count total matching docs
    total = collection.count_documents(query)

    # Fetch docs with pagination
    if search:
        articles_cursor = collection.find(query, {"score": {"$meta": "textScore"}}) \
                                    .sort([("score", {"$meta": "textScore"})]) \
                                    .skip(skip).limit(limit)
    else:
        articles_cursor = collection.find(query).skip(skip).limit(limit)

    # Format results for frontend
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
        "total": total,   # total docs for pagination frontend
        "articles": articles
    })
