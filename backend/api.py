from flask import Flask, jsonify, request
from sqlalchemy import create_engine
from flask_cors import CORS
from sqlalchemy.orm import sessionmaker
from models import Wildfire, Shelter, NewsReport
from models import TESTING
from scripts import ca_fire_gov
from flask import render_template_string
from dotenv import load_dotenv
import os
import awsgi
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

engine = create_engine(DATABASE_URL, echo=True, future=True)
local_session = sessionmaker(bind=engine, autoflush=False, future=True)

DEFAULT_PAGE_SIZE = 10

def searchModels(search_text, query, MODEL):
    phrase_tsquery = func.plainto_tsquery('english', search_text)
    words_tsquery_input = ' | '.join(search_text.split())
    words_tsquery = func.to_tsquery('english', words_tsquery_input)
    conditions = []
    columns = ['name', 'description', 'city', 'target', 'eligibility', 'counties_served', 'main_services', 'detailed_target', 'detailed_hours', 'operating_hours']
    for column_name in columns:
        if not hasattr(MODEL, column_name):
            continue
        column = getattr(MODEL, column_name)      
        phrase_match = func.to_tsvector('english', column).op('@@')(phrase_tsquery)
        words_match = func.to_tsvector('english', column).op('@@')(words_tsquery)
        conditions.append(or_(phrase_match, words_match))

    # Combine all conditions with OR, so any match on any specified field will be included
    if conditions:
        query = query.filter(or_(*conditions))
    
    return query

@app.route("/wildfire_incidents", methods=["GET"])
def get_all_incidents():
    page = request.args.get("page", 1, type=int)
    size = request.args.get("size", DEFAULT_PAGE_SIZE, type=int)
    sort_by = request.args.get('sort_by', 'city')
    order = request.args.get('order', 'asc')
    hours = request.args.get('hours', None)
    county = request.args.get('county', None)
    search = request.args.get('search', None)
    eligibility = request.args.get('eligibility' , None)
    valid_sort_columns = {'name', 'city'}
    if sort_by not in valid_sort_columns:
        return jsonify({'error': f"Invalid sort column '{sort_by}'"}), 400
    with local_session() as ls:
        try:
            incidents = ls.query(Wildfire).limit(size).offset((page - 1) * size).all()
            incident_cards = [incident.as_instance() for incident in incidents]
            total_incidents = ls.query(Wildfire).count()
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

@app.route("/wildfire_incidents/<int:id>", methods=["GET"])
def get_single_incident(id):
    with local_session() as ls:
        try:
            incident = ls.query(Wildfire).get(id)
            if incident:
                return jsonify(incident.as_instance())
            else:
                return jsonify({"error": "incident not found"}), 404
        except:
            return jsonify({"error": "issue getting data"}), 500

@app.route("/shelters", methods=["GET"])
def get_all_shelters():
    page = request.args.get("page", 1, type=int)
    size = request.args.get("size", DEFAULT_PAGE_SIZE, type=int)
    with local_session() as ls:
        try:
            shelters = ls.query(Shelter).limit(size).offset((page - 1) * size).all()
            shelter_cards = [shelter.as_instance() for shelter in shelters]
            total_shelters = ls.query(Shelter).count()
            total_pages = (total_shelters + size - 1) // size
            return jsonify(
                {
                    "shelters": shelter_cards,
                    "pagination": {
                        "page": page,
                        "size": size,
                        "total_pages": total_pages,
                        "total_items": total_shelters,
                    },
                }
            )
        except Exception as e:
            return jsonify({"error": str(e)}), 500

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
    app.run(host="0.0.0.0", port=5000)
