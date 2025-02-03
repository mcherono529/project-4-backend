from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Pregnancy(db.Model):
    __tablename__ = "pregnancies"

    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(100), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    due_date = db.Column(db.Date, nullable=False)

    baby_names = db.relationship("BabyName", backref="pregnancy", lazy=True, cascade="all, delete")
    doctor_appointments = db.relationship("DoctorAppointment", backref="pregnancy", lazy=True, cascade="all, delete")
    symptoms = db.relationship("PregnancySymptom", backref="pregnancy", lazy=True, cascade="all, delete")

class BabyName(db.Model):
    __tablename__ = "baby_names"

    id = db.Column(db.Integer, primary_key=True)
    pregnancy_id = db.Column(db.Integer, db.ForeignKey("pregnancies.id", ondelete="CASCADE"), nullable=False)
    name = db.Column(db.String(100), nullable=False)

class DoctorAppointment(db.Model):
    __tablename__ = "doctor_appointments"

    id = db.Column(db.Integer, primary_key=True)
    pregnancy_id = db.Column(db.Integer, db.ForeignKey("pregnancies.id", ondelete="CASCADE"), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    doctor_name = db.Column(db.String(100), nullable=False)
    purpose = db.Column(db.String(200))
    notes = db.Column(db.Text)

class Symptom(db.Model):
    __tablename__ = "symptoms"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)

class PregnancySymptom(db.Model):
    __tablename__ = "pregnancy_symptoms"

    id = db.Column(db.Integer, primary_key=True)
    pregnancy_id = db.Column(db.Integer, db.ForeignKey("pregnancies.id", ondelete="CASCADE"), nullable=False)
    symptom_id = db.Column(db.Integer, db.ForeignKey("symptoms.id", ondelete="CASCADE"), nullable=False)
    date_reported = db.Column(db.Date, nullable=False)

class EducationalResource(db.Model):
    __tablename__ = "educational_resources"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=True)
    link = db.Column(db.String(300), nullable=True)
