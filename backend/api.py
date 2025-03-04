from flask import Flask, jsonify, request
from sqlalchemy import create_engine
from flask_cors import CORS
from sqlalchemy.orm import sessionmaker
from models import Wildfire
from models import TESTING
import os
import awsgi


app = Flask(__name__)
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

if __name__ == '__main__':
    app.run(debug=False)
