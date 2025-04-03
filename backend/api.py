from flask import Flask, jsonify, request
from sqlalchemy import create_engine, func, or_, and_
from sqlalchemy.orm import sessionmaker
from models import Wildfire, Shelter, NewsReport
from models import TESTING
from flask_cors import CORS
from dotenv import load_dotenv
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

from sqlalchemy.orm import joinedload

def preload_all_data():
    global wildfire_cache, shelter_cache, news_cache
    with local_session() as session:
        # wildfire_cache = session.query(Wildfire).options(
        #     joinedload(Wildfire.shelters),
        #     joinedload(Wildfire.newsreports)
        # ).all()
        # print(f"Preloaded {len(wildfire_cache)} wildfires")

        shelter_cache = session.query(Shelter).options(
            joinedload(Shelter.wildfires),
            joinedload(Shelter.newsreports)
        ).all()
        print(f"Preloaded {len(shelter_cache)} shelters")

        # news_cache = session.query(NewsReport).options(
        #     joinedload(NewsReport.wildfires),
        #     joinedload(NewsReport.shelters)
        # ).all()
        # print(f"Preloaded {len(news_cache)} news reports")



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
    global wildfire_cache
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
    with local_session() as ls:
        try:
            shelter = ls.query(Shelter).get(id)
            if shelter:
                return jsonify(shelter.as_instance())
            else:
                return jsonify({"error": "shelter not found"}), 404
        except:
            return jsonify({"error": "issue getting data"}), 500

@app.route("/news", methods=["GET"])
def get_all_reports():
    page = request.args.get("page", 1, type=int)
    size = request.args.get("size", 2, type=int)
    with local_session() as ls:
        try:
            incidents = ls.query(NewsReport).limit(size).offset((page - 1) * size).all()
            incident_cards = [incident.as_instance() for incident in incidents]
            total_incidents = ls.query(NewsReport).count()
            total_pages = (total_incidents + size - 1) // size
            return jsonify(
                {
                    "incidents": incident_cards,
                    "pagination": {
                        "page": page,
                        "size": size,
                        "total_pages": total_pages,
                        "total_items": total_incidents,
                    },
                }
            )
        except:
            return jsonify({"error": "issue getting data"}), 500

@app.route("/news/<int:id>", methods=["GET"])
def get_single_report(id):
    with local_session() as ls:
        try:
            incident = ls.query(NewsReport).get(id)
            if incident:
                return jsonify(incident.as_instance())
            else:
                return jsonify({"error": "report not found"}), 404
        except:
            return jsonify({"error": "issue getting data"}), 500

if __name__ == '__main__':
    preload_all_data()
    app.run(host="0.0.0.0", port=3000, debug = True)
