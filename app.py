from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from models import db, Pregnancy, DoctorAppointment, BabyName, Symptom, PregnancySymptom, EducationalResource
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///pregnancy_tracker.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate = Migrate(app, db)
CORS(app)

@app.route("/")
def home():
    return {"message": "Pregnancy Tracker API"}

@app.route("/pregnancies", methods=["GET"])
def get_pregnancies():
    pregnancies = Pregnancy.query.all()
    return jsonify([
        {
            "id": p.id,
            "user_name": p.user_name,
            "start_date": p.start_date.strftime("%Y-%m-%d"),
            "due_date": p.due_date.strftime("%Y-%m-%d")
        } for p in pregnancies
    ])

@app.route("/pregnancies", methods=["POST"])
def create_pregnancy():
    data = request.get_json()

    start_date = datetime.strptime(data["start_date"], "%Y-%m-%d").date()
    due_date = datetime.strptime(data["due_date"], "%Y-%m-%d").date()

    new_pregnancy = Pregnancy(
        user_name=data["user_name"],
        start_date=start_date,
        due_date=due_date
    )

    db.session.add(new_pregnancy)
    db.session.commit()

    return jsonify({"message": "Pregnancy profile created!"}), 201

@app.route("/pregnancies/<int:id>", methods=["DELETE"])
def delete_pregnancy(id):
    pregnancy = Pregnancy.query.get(id)
    if not pregnancy:
        return jsonify({"error": "Pregnancy not found"}), 404
    
    db.session.delete(pregnancy)
    db.session.commit()
    return jsonify({"message": "Pregnancy deleted successfully!"})

@app.route("/pregnancies/<int:id>", methods=["PUT", "PATCH"])
def update_pregnancy(id):
    pregnancy = Pregnancy.query.get(id)
    if not pregnancy:
        return jsonify({"error": "Pregnancy not found"}), 404

    data = request.get_json()

    if "user_name" in data:
        pregnancy.user_name = data["user_name"]
    
    if "start_date" in data:
        try:
            pregnancy.start_date = datetime.strptime(data["start_date"], "%Y-%m-%d").date()
        except ValueError:
            return jsonify({"error": "Invalid start_date format. Use YYYY-MM-DD."}), 400

    if "due_date" in data:
        try:
            pregnancy.due_date = datetime.strptime(data["due_date"], "%Y-%m-%d").date()
        except ValueError:
            return jsonify({"error": "Invalid due_date format. Use YYYY-MM-DD."}), 400

    db.session.commit()
    return jsonify({"message": "Pregnancy updated successfully!"})

@app.route("/pregnancies/<int:pregnancy_id>/baby-names", methods=["GET"])
def get_baby_names(pregnancy_id):
    baby_names = BabyName.query.filter_by(pregnancy_id=pregnancy_id).all()
    return jsonify([{"id": bn.id, "name": bn.name} for bn in baby_names])

@app.route("/pregnancies/<int:pregnancy_id>/baby-names", methods=["POST"])
def add_baby_name(pregnancy_id):
    data = request.get_json()
    new_baby_name = BabyName(pregnancy_id=pregnancy_id, name=data["name"])
    db.session.add(new_baby_name)
    db.session.commit()
    return jsonify({"message": "Baby name added!"}), 201

@app.route("/baby-names/<int:id>", methods=["PUT", "PATCH"])
def update_baby_name(id):
    baby_name = BabyName.query.get(id)
    if not baby_name:
        return jsonify({"error": "Baby name not found"}), 404

    data = request.get_json()
    if "name" in data:
        baby_name.name = data["name"]

    db.session.commit()
    return jsonify({"message": "Baby name updated successfully!"})

@app.route("/appointments", methods=["GET"])
def get_appointments():
    appointments = DoctorAppointment.query.all()
    return jsonify([
        {
            "id": a.id,
            "pregnancy_id": a.pregnancy_id,
            "doctor_name": a.doctor_name,
            "date": a.date.strftime("%Y-%m-%d"),
            "time": str(a.time),
            "purpose": a.purpose,
            "notes": a.notes
        } for a in appointments
    ])

@app.route("/appointments", methods=["POST"])
def create_appointment():
    try:
        data = request.get_json(force=True)  
        print(f"📥 Received request data: {data}")  

        time_str = data["time"]
        if len(time_str) == 5: 
            time_obj = datetime.strptime(time_str, "%H:%M").time()
        else:  
            time_obj = datetime.strptime(time_str, "%H:%M:%S").time()

        new_appointment = DoctorAppointment(
            pregnancy_id=int(data["pregnancy_id"]),  
            doctor_name=data["doctor_name"],
            date=datetime.strptime(data["date"], "%Y-%m-%d").date(),
            time=time_obj,
            purpose=data.get("purpose", ""),
            notes=data.get("notes", "")
        )

        db.session.add(new_appointment)
        db.session.commit()
        return jsonify({"message": "Appointment added!"}), 201

    except Exception as e:
        print(f" POST error: {str(e)}") 
        return jsonify({"error": str(e)}), 400


@app.route("/appointments/<int:id>", methods=["DELETE"])
def delete_appointment(id):
    appointment = DoctorAppointment.query.get(id)
    if not appointment:
        return jsonify({"error": "Appointment not found"}), 404

    db.session.delete(appointment)
    db.session.commit()
    return jsonify({"message": "Appointment deleted successfully!"})

@app.route("/appointments/<int:id>", methods=["PUT", "PATCH"])
def update_appointment(id):
    print(f"Received request data: {request.get_json()}")  

    appointment = DoctorAppointment.query.get(id)
    if not appointment:
        return jsonify({"error": "Appointment not found"}), 404

    try:
        data = request.get_json(force=True)  
        print(f"Parsed JSON data: {data}")

        if "pregnancy_id" in data:
            del data["pregnancy_id"]

        if "doctor_name" in data:
            appointment.doctor_name = data["doctor_name"]
        if "date" in data:
            appointment.date = datetime.strptime(data["date"], "%Y-%m-%d").date()
        if "time" in data:
            appointment.time = datetime.strptime(data["time"], "%H:%M:%S").time()
        if "purpose" in data:
            appointment.purpose = data["purpose"]
        if "notes" in data:
            appointment.notes = data["notes"]

        db.session.commit()
        return jsonify({"message": "Appointment updated successfully!"})
    
    except Exception as e:
        print(f"Update error: {str(e)}")  
        return jsonify({"error": str(e)}), 400

@app.route("/symptoms", methods=["GET"])
def get_symptoms():
    symptoms = Symptom.query.all()
    return jsonify([
        {"id": s.id, "name": s.name, "description": s.description}
        for s in symptoms
    ])

@app.route("/symptoms", methods=["POST"])
def add_symptom():
    data = request.get_json()
    new_symptom = Symptom(name=data["name"], description=data["description"])
    db.session.add(new_symptom)
    db.session.commit()
    return jsonify({"message": "Symptom added!"}), 201

@app.route("/symptoms/<int:id>", methods=["PUT", "PATCH"])
def update_symptom(id):
    symptom = Symptom.query.get(id)
    if not symptom:
        return jsonify({"error": "Symptom not found"}), 404

    data = request.get_json()
    
    if "name" in data:
        symptom.name = data["name"]
    if "description" in data:
        symptom.description = data["description"]

    db.session.commit()
    return jsonify({"message": "Symptom updated successfully!"})

@app.route("/pregnancies/<int:pregnancy_id>/symptoms", methods=["POST"])
def add_pregnancy_symptom(pregnancy_id):
    data = request.get_json()
    new_pregnancy_symptom = PregnancySymptom(
        pregnancy_id=pregnancy_id,
        symptom_id=data["symptom_id"],
        date_reported=data["date_reported"]
    )
    db.session.add(new_pregnancy_symptom)
    db.session.commit()
    return jsonify({"message": "Symptom reported for pregnancy!"}), 201

@app.route("/pregnancies/<int:pregnancy_id>/symptoms", methods=["GET"])
def get_pregnancy_symptoms(pregnancy_id):
    pregnancy_symptoms = PregnancySymptom.query.filter_by(pregnancy_id=pregnancy_id).all()
    return jsonify([
        {
            "id": ps.id,
            "symptom_name": ps.symptom.name,
            "date_reported": ps.date_reported.strftime("%Y-%m-%d")
        } for ps in pregnancy_symptoms
    ])

@app.route("/pregnancies/<int:pregnancy_id>/symptoms/<int:symptom_id>", methods=["PUT", "PATCH"])
def update_pregnancy_symptom(pregnancy_id, symptom_id):
    pregnancy_symptom = PregnancySymptom.query.filter_by(pregnancy_id=pregnancy_id, symptom_id=symptom_id).first()
    if not pregnancy_symptom:
        return jsonify({"error": "Pregnancy symptom not found"}), 404

    data = request.get_json()
    
    if "date_reported" in data:
        pregnancy_symptom.date_reported = data["date_reported"]

    db.session.commit()
    return jsonify({"message": "Pregnancy symptom updated successfully!"})

@app.route("/resources", methods=["GET"])
def get_resources():
    resources = EducationalResource.query.all()
    return jsonify([
        {"id": r.id, "title": r.title, "content": r.content, "link": r.link}
        for r in resources
    ])

@app.route("/resources", methods=["POST"])
def add_resource():
    data = request.get_json()
    new_resource = EducationalResource(
        title=data["title"],
        content=data.get("content", ""),
        link=data.get("link", "")
    )
    db.session.add(new_resource)
    db.session.commit()
    return jsonify({"message": "Educational resource added!"}), 201

if __name__ == "__main__":
    app.run(debug=True)
