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



@app.route("/wildfire_incidents", methods=["GET"])
def get_all_incidents():
    page = request.args.get("page", 1, type=int)
    size = request.args.get("size", DEFAULT_PAGE_SIZE, type=int)
    sort_by = request.args.get("sort_by", "county")
    order = request.args.get("order", "asc")
    location = request.args.get("location")
    year = request.args.get("year")
    acres_burned = request.args.get("acres_burned")
    search = request.args.get("search")

    valid_sort_columns = {"name", "county"}
    if sort_by not in valid_sort_columns:
        return jsonify({"error": f"Invalid sort column '{sort_by}'"}), 400

    # Copy the cache to filter/sort
    data = wildfire_cache[:]

    # Apply search terms
    if search:
        term = search.lower()

        def match_search(wildfire):
            if (
                term in (wildfire.name or "").lower()
                or term in (wildfire.county or "").lower()
                or term in (wildfire.location or "").lower()
                or term in str(wildfire.year or "")
                or term in str(wildfire.acres_burned or "")
                or term in (wildfire.status or "").lower()
            ):
                return True
            return False

        data = [w for w in data if match_search(w)]


    # Apply filters
    if location:
        data = [w for w in data if location.lower()
        in (w.location or "").lower()
        or location.lower() in (w.county or "").lower()]
    if year:
        data = [w for w in data if str(w.year or "") == str(year)]
    if acres_burned:
        #Checks that number isnt just a string by doing: 12.34 -> 1245 (is this a number?)
        data = [
            w for w in data
            if w.acres_burned and w.acres_burned.replace('.', '', 1).isdigit()
            and float(w.acres_burned) > float(acres_burned)
        ]

    # Sorting
    reverse = order == "desc"
    try:
        data.sort(key=lambda w: (getattr(w, sort_by) or "").lower(), reverse=reverse)
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
            counties = ls.query(Wildfire.county).distinct().order_by(Wildfire.county).all()
            county_list = [c[0] for c in counties if c[0]]
            return jsonify({"locations": county_list})
        except Exception as e:
            return jsonify({"Error getting locations": str(e)}), 500

@app.route("/shelter_locations", methods=["GET"])
def get_shelter_locations():
    with local_session() as ls:
        try:
            counties = ls.query(Shelter.county).distinct().order_by(Shelter.county).all()
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
    sort_by = request.args.get("sort_by", "county")
    order = request.args.get("order", "asc")
    address = request.args.get("address")
    rating = request.args.get("rating")
    search = request.args.get("search")

    valid_sort_columns = {"name", "county"}
    if sort_by not in valid_sort_columns:
        return jsonify({"error": f"Invalid sort column '{sort_by}'"}), 400

    # Copy the cache to filter/sort
    data = shelter_cache[:]

    # Apply search terms
    if search:
        term = search.lower()

        def match_search(shelter):
            if (
                term in (shelter.name or "").lower()
                or term in (shelter.county or "").lower()
                or term in (shelter.address or "").lower()
                or term in str(shelter.rating or "")
                or term in (shelter.phone or "").lower()
            ):
                return True
            return False

        data = [s for s in data if match_search(s)]


    # Apply filters
    if address:
        data = [s for s in data if address.lower() in (s.address or "").lower()
        or address.lower() in (s.county or "").lower()]
    if rating:
        data = [s for s in data 
        if s.rating and s.rating!="N/A"
        and float(s.rating.split('/')[0] or 0) >= float(rating)
        and float(s.rating.split('/')[0] or 0) < float(rating) + 1]

    # Sorting
    reverse = order == "desc"
    try:
        data.sort(key=lambda s: (getattr(s, sort_by) or "").lower(), reverse=reverse)
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
    size = request.args.get("size", 2, type=int)
    source = request.args.get("source", None)
    author = request.args.get("author", None)
    date = request.args.get("date", None)
    categories = request.args.get('categories', '') 
    sortBy = request.args.get("sortBy", "title")  # Default to 'title'
    order = request.args.get("order", "asc")  # Default to ascending order
    search = request.args.get("search", None)


    valid_sort_columns = {"title", "published_at", "author", "source"}
    if sortBy not in valid_sort_columns:
        return jsonify({"error": f"Invalid sort column '{sortBy}'"}), 400

    # Copy the cache to filter/sort
    data = news_cache[:]

    # Apply search terms
    if search:
        term = search.lower()

        def match_search(report):
            if (
                term in (report.title or "").lower()
                or term in (report.source or "").lower()
                or term in (report.published_at or "").lower()
                or term in (report.author or "").lower()
                or term in (report.categories or "").lower()
            ):
                return True
            return False

        data = [r for r in data if match_search(r)]


    # Apply filters
    if source:
        data = [r for r in data if source.lower()
        in (r.source or "").lower()]
    if author:
        data = [r for r in data if author.lower() 
        in (r.author or "").lower()]
    if date:
        date_obj = datetime.strptime(date,'%Y-%m-%d').date()
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
    # Sorting
    reverse = order == "desc"

    try:
        if sortBy == "date":
            # Assuming published_at is a string like '2023-12-01'
            data.sort(
                key=lambda r: datetime.strptime(getattr(r, "published_at", ""), "%Y-%m-%d"),
                reverse=reverse
            )
        else:
            data.sort(
                key=lambda r: (getattr(r, sortBy) or "").lower(),
                reverse=reverse
            )

    except AttributeError:
        return jsonify({"error": f"Invalid sort field '{sortBy}'"}), 400
    except ValueError:
        return jsonify({"error": "Date format should be YYYY-MM-DD"}), 400

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

@app.before_first_request
def load_data_once():
    preload_all_data()
    
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3000)
