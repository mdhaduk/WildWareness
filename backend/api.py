from flask import Flask, jsonify, request
from sqlalchemy import create_engine, func, or_, and_
from sqlalchemy.orm import sessionmaker
from models import Wildfire, Shelter, NewsReport
from models import TESTING
from flask_cors import CORS
from dotenv import load_dotenv
from datetime import datetime
from sqlalchemy.orm import joinedload
import os
from itertools import permutations
from scripts.helper_scripts import score_model

load_dotenv()

app = Flask(__name__)
app.json.sort_keys = False
CORS(app)

DATABASE_URL = ""
if TESTING:
    DATABASE_URL = "sqlite:///test.db"
else:
    username = os.getenv("DB_USERNAME")
    password = os.getenv("DB_PASSWORD")
    database_name = "wildfiredb"
    DATABASE_URL = f"postgresql+psycopg2://{username}:{password}@wildwarenessdb.czwce00s2t3z.us-east-2.rds.amazonaws.com/{database_name}"

engine = create_engine(DATABASE_URL, echo=False, future=True)
local_session = sessionmaker(bind=engine, autoflush=False, future=True)

DEFAULT_PAGE_SIZE = 10

wildfire_cache = []
shelter_cache = []
news_cache = []


def preload_all_data():
    global wildfire_cache, shelter_cache, news_cache
    with local_session() as session:
        wildfire_cache = session.query(Wildfire).options(
            joinedload(Wildfire.shelters),
            joinedload(Wildfire.newsreports)
        ).all()
        print(f"Preloaded {len(wildfire_cache)} wildfires")

        shelter_cache = session.query(Shelter).options(
            joinedload(Shelter.wildfires),
            joinedload(Shelter.newsreports)
        ).all()
        print(f"Preloaded {len(shelter_cache)} shelters")

        news_cache = session.query(NewsReport).options(
            joinedload(NewsReport.wildfires),
            joinedload(NewsReport.shelters)
        ).all()
        print(f"Preloaded {len(news_cache)} news reports")


preload_all_data()  # GET ALL THE DATA


@app.route("/wildfire_incidents", methods=["GET"])
def get_all_incidents():
    page = request.args.get("page", 1, type=int)
    size = request.args.get("size", DEFAULT_PAGE_SIZE, type=int)
    sort_by = request.args.get("sort_by", "")
    order = request.args.get("order", "")
    location = request.args.get("location")
    year = request.args.get("year")
    acres_burned = request.args.get("acres_burned")
    search = request.args.get("search", None)
    status = request.args.get("status")
    data = wildfire_cache[:]
    # Apply search terms with relevance ranking
    if search:
        term = search.lower().strip()
        data_with_scores = [(r, score_model(r, term, ["name", "county", "location", "status", "year", "acres_burned"])) for r in data]
        # Only include reports with score > 0
        data_with_scores = [d for d in data_with_scores if d[1] > 0]
        # Sort by relevance score
        data_with_scores.sort(key=lambda x: x[1], reverse=True)
        # Extract sorted reports
        data = [d[0] for d in data_with_scores]

    # Apply filters
    if location:
        data = [w for w in data if location.lower()
                in (w.location or "").lower()
                or location.lower() in (w.county or "").lower()]
    if year:
        data = [w for w in data if str(w.year or "") == str(year)]
    if acres_burned:
        # Checks that number isnt just a string by doing: 12.34 -> 1245 (is this a number?)
        data = [
            w for w in data
            if w.acres_burned and w.acres_burned.replace('.', '', 1).isdigit()
            and float(w.acres_burned) > float(acres_burned)
        ]

    if status:
        data = [w for w in data if w.status and w.status.lower() ==
                status.lower()]

    if sort_by:
        reverse = order == "desc"
        try:
            data.sort(key=lambda w: (getattr(w, sort_by)
                      or "").lower(), reverse=reverse)
        except AttributeError:
            return jsonify({"error": f"Invalid sort field '{sort_by}'"}), 400

    # Pagination
    total_items = len(data)
    total_pages = (total_items + size - 1) // size
    start = (page - 1) * size
    end = start + size
    paged_data = data[start:end]

    return jsonify({
        "incidents": [w.as_instance() for w in paged_data],
        "pagination": {
            "page": page,
            "size": size,
            "total_pages": total_pages,
            "total_items": total_items,
        },
    })


@app.route("/wildfire_locations", methods=["GET"])
def get_wildfire_locations():
    with local_session() as ls:
        try:
            counties = ls.query(Wildfire.county).distinct().order_by(
                Wildfire.county).all()
            county_list = [c[0] for c in counties if c[0]]
            return jsonify({"locations": county_list})
        except Exception as e:
            return jsonify({"Error getting locations": str(e)}), 500


@app.route("/shelter_locations", methods=["GET"])
def get_shelter_locations():
    with local_session() as ls:
        try:
            counties = ls.query(Shelter.county).distinct().order_by(
                Shelter.county).all()
            county_list = [c[0] for c in counties if c[0]]
            return jsonify({"locations": county_list})
        except Exception as e:
            return jsonify({"Error getting locations": str(e)}), 500


@app.route("/wildfire_incidents/<int:id>", methods=["GET"])
def get_single_incident(id):
    for w in wildfire_cache:
        if w.id == id:
            return jsonify(w.as_instance())
    return jsonify({"error": "incident not found"}), 404


@app.route("/shelters", methods=["GET"])
def get_all_shelters():
    page = request.args.get("page", 1, type=int)
    size = request.args.get("size", DEFAULT_PAGE_SIZE, type=int)
    sort_by = request.args.get("sort_by", "")
    order = request.args.get("order", "")
    county = request.args.get("county")
    zipCode = request.args.get("zipCode")
    phone = request.args.get("phone")
    rating = request.args.get("rating")
    search = request.args.get("search")

    data = shelter_cache[:]
    if search:
        term = search.lower().strip()
        data_with_scores = [(r, score_model(r, term, ["name", "county", "address", "rating", "website", "phone"])) for r in data]
        # Only include reports with score > 0
        data_with_scores = [d for d in data_with_scores if d[1] > 0]
        # Sort by relevance score
        data_with_scores.sort(key=lambda x: x[1], reverse=True)
        data = [d[0] for d in data_with_scores]

    # Apply filters
    if county:
        data = [s for s in data if county.lower() in (s.address or "").lower()
                or county.lower() in (s.county or "").lower()]
    if zipCode:
        zipCode = str(zipCode)
        data = [s for s in data if zipCode.strip() in (s.address or "").lower()]

    if phone:
        cleaned_phone = ''.join(filter(str.isdigit, str(phone)))
        first_three_phone = cleaned_phone[:3]
        data = [s for s in data if first_three_phone in ''.join(
            filter(str.isdigit, s.phone or ""))[:3]]

    if rating:
        data = [s for s in data
                if s.rating and s.rating != "N/A"
                and float(s.rating.split('/')[0] or 0) >= float(rating)
                and float(s.rating.split('/')[0] or 0) < float(rating) + 1]

    if sort_by:
        reverse = order == "desc"
        try:
            data.sort(key=lambda s: (getattr(s, sort_by)
                      or "").lower(), reverse=reverse)
        except AttributeError:
            return jsonify({"error": f"Invalid sort field '{sort_by}'"}), 400

    # Pagination
    total_items = len(data)
    total_pages = (total_items + size - 1) // size
    start = (page - 1) * size
    end = start + size
    paged_data = data[start:end]

    return jsonify({
        "shelters": [s.as_instance() for s in paged_data],
        "pagination": {
            "page": page,
            "size": size,
            "total_pages": total_pages,
            "total_items": total_items,
        },
    })


@app.route("/shelters/<int:id>", methods=["GET"])
def get_single_shelter(id):
    for s in shelter_cache:
        if s.id == id:
            return jsonify(s.as_instance())
    return jsonify({"error": "shelter not found"}), 404


@app.route("/news", methods=["GET"])
def get_all_reports():
    page = request.args.get("page", 1, type=int)
    size = request.args.get("size", DEFAULT_PAGE_SIZE, type=int)
    source = request.args.get("source", None)
    author = request.args.get("author", None)
    date = request.args.get("date", None)
    categories = request.args.get('categories', '')
    sort_by = request.args.get("sort_by", "")  # Default to 'title'
    order = request.args.get("order", "")  # Default to ascending order
    search = request.args.get("search", None)
    # Copy the cache to filter/sort
    data = news_cache[:]

    if search:
        term = search.lower().strip()
        data_with_scores = [(r, score_model(model=r, term=term, attributes=["title", "source", "author", "published_at", "categories"])) for r in data]
        # Only include reports with score > 0
        data_with_scores = [d for d in data_with_scores if d[1] > 0]
        # Sort by relevance score
        data_with_scores.sort(key=lambda x: x[1], reverse=True)

        # Extract sorted reports
        data = [d[0] for d in data_with_scores]

    # Apply filters
    if source:
        data = [r for r in data if source.lower()
                in (r.source or "").lower()]
    if author:
        data = [r for r in data if author.lower().strip()
                in (r.author or "").lower()]
    if date:
        date_obj = datetime.strptime(date, '%Y-%m-%d').date()
        date_string = date_obj.strftime('%Y-%m-%d')
        data = [
            r for r in data
            if r.published_at == date_string]
    if categories:
        category_list = categories.split(",")
        print(categories.split(","))
        data = [
            r for r in data
            if all(cat in r.categories for cat in category_list)
        ]
    if sort_by:
        reverse = order == "desc"
        # Handle sorting for text fields (title, author, source)
        if sort_by == "published_at":
            data.sort(
                key=lambda r: datetime.strptime(
                    r.published_at, "%Y-%m-%d") if r.published_at else datetime.min,
                reverse=reverse
            )
        else:
            data.sort(
                key=lambda r: (getattr(r, sort_by, "") or "").lower(),
                reverse=reverse
            )

    # Pagination
    total_items = len(data)
    total_pages = (total_items + size - 1) // size
    start = (page - 1) * size
    end = start + size
    paged_data = data[start:end]

    return jsonify({
        "reports": [r.as_instance() for r in paged_data],
        "pagination": {
            "page": page,
            "size": size,
            "total_pages": total_pages,
            "total_items": total_items,
        },
    })


@app.route("/news/<int:id>", methods=["GET"])
def get_single_report(id):
    for r in news_cache:
        if r.id == id:
            return jsonify(r.as_instance())
    return jsonify({"error": "incident not found"}), 404


@app.route("/search", methods=["GET"])
def search_all_cards():
    page = request.args.get("page", 1, type=int)
    size = request.args.get("size", DEFAULT_PAGE_SIZE, type=int)
    text = request.args.get("text", None)

    # Copy the cache to filter/sort
    global data
    data = []
    if text:
        data = [*wildfire_cache, *shelter_cache, *news_cache]

    # Apply search terms
    if text:
        term = text.lower().strip()
        data_with_scores = []
        def match_search(obj):
            if isinstance(obj, Wildfire):
                return score_model(obj, term, ["name", "county", "location", "status", "year", "acres_burned"])
            elif isinstance(obj, NewsReport):
                return score_model(model=obj, term=term, attributes=["title", "source", "author", "published_at", "categories"])
            elif isinstance(obj, Shelter):
                return score_model(obj, term, ["name", "county", "address", "rating", "website", "phone"])
        # Only include reports with score > 0
        data_with_scores = [(obj, match_search(obj)) for obj in data]
        data_with_scores = [d for d in data_with_scores if d[1] > 0]
        data_with_scores.sort(key=lambda x: x[1], reverse=True)
        data = [item[0] for item in data_with_scores]

    # Pagination
    total_items = len(data)
    total_pages = (total_items + size - 1) // size
    start = (page - 1) * size
    end = start + size
    paged_data = data[start:end]

    return jsonify({
        "instances": [r.as_instance() for r in paged_data],
        "pagination": {
            "page": page,
            "size": size,
            "total_pages": total_pages,
            "total_items": total_items,
        },
    })


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3000, debug=True)
