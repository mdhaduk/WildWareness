from flask import Flask, jsonify, request
from sqlalchemy import create_engine, func
from flask_cors import CORS
from sqlalchemy.orm import sessionmaker
from models import Wildfire, Shelter, NewsReport
from models import TESTING
from scripts import ca_fire_gov
from flask import render_template_string
import os
import awsgi
from datetime import datetime


app = Flask(__name__)
# app.config["DEBUG"] = True
app.json.sort_keys = False
CORS(app)

DATABASE_URL = ""
if TESTING:
    DATABASE_URL = "sqlite:///test.db"
else:
    username = os.getenv("DB_USERNAME")
    password = os.getenv("DB_PASSWORD")
    database_name = "homelessaid"
    DATABASE_URL = f"postgresql+psycopg2://{username}:{password}@homelessaid-database.ctc8886awsgr.us-east-2.rds.amazonaws.com:5432/{database_name}"

engine = create_engine(DATABASE_URL, echo=True, future=True)
local_session = sessionmaker(bind=engine, autoflush=False, future=True)

DEFAULT_PAGE_SIZE = 10


@app.route("/wildfire_incidents", methods=["GET"])
def get_all_incidents():
    page = request.args.get("page", 1, type=int)
    size = request.args.get("size", DEFAULT_PAGE_SIZE, type=int)
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
    size = request.args.get("size", DEFAULT_PAGE_SIZE, type=int)

    # sort_by = request.args.get("sortBy", "title")  # Default sorting by name
    # order = request.args.get("order", "asc")  # Default ordering by ascending
    source = request.args.get("source", None)
    # author = request.args.get("author", None)
    # date = request.args.get("date", None)


    with local_session() as ls:
        try:
            query = ls.query(NewsReport)
            print(source)
            if source:
                query = query.filter(func.lower(NewsReport.source) == source.lower())


            # if author:
            #     query = query.filter(NewsReport.author.ilike(f"%{author}%"))

            # if date:
            #     date_obj = datetime.strptime(date, '%Y-%m-%d')
            #     query = query.filter(NewsReport.published_at == date_obj)


            # Sorting logic
            # if sort_by == "date":
            #     if order == "desc":
            #         query = query.order_by(NewsReport.published_at.desc())
            #     else:
            #         query = query.order_by(NewsReport.published_at.asc())
            # elif sort_by == "title":
            #     if order == "asc":
            #         query = query.order_by(NewsReport.title.lower().asc())
            #     else:
            #         query = query.order_by(NewsReport.title.lower().desc())


            incidents = query.limit(size).offset((page - 1) * size).all()
            print(incidents)
            incident_cards = [incident.as_instance() for incident in incidents]
            total_incidents = query.count()
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
