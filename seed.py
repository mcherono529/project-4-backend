from datetime import datetime
from app import app  
from models import db, Pregnancy, DoctorAppointment, BabyName, Symptom, PregnancySymptom, EducationalResource  
from sqlalchemy.exc import IntegrityError

with app.app_context():
    pregnancy1 = Pregnancy(
        user_name="Alice",
        start_date=datetime.strptime("2025-01-01", "%Y-%m-%d").date(),
        due_date=datetime.strptime("2025-07-10", "%Y-%m-%d").date()
    )

    pregnancy2 = Pregnancy(
        user_name="Bob",
        start_date=datetime.strptime("2025-02-01", "%Y-%m-%d").date(),
        due_date=datetime.strptime("2025-09-15", "%Y-%m-%d").date()
    )

    db.session.add_all([pregnancy1, pregnancy2])
    db.session.commit()  

    baby_name1 = BabyName(pregnancy_id=pregnancy1.id, name="Emma")
    baby_name2 = BabyName(pregnancy_id=pregnancy1.id, name="Oliver")
    baby_name3 = BabyName(pregnancy_id=pregnancy2.id, name="Sophia")

    db.session.add_all([baby_name1, baby_name2, baby_name3])
    db.session.commit()

    appointment1 = DoctorAppointment(
        pregnancy_id=pregnancy1.id,
        date=datetime.strptime("2025-02-20", "%Y-%m-%d").date(),
        time=datetime.strptime("10:00:00", "%H:%M:%S").time(), 
        doctor_name="Dr. Smith",
        purpose="Routine Checkup",
        notes="All vitals normal."
    )

    appointment2 = DoctorAppointment(
        pregnancy_id=pregnancy2.id,
        date=datetime.strptime("2025-03-15", "%Y-%m-%d").date(),
        time=datetime.strptime("14:30:00", "%H:%M:%S").time(),
        doctor_name="Dr. Brown",
        purpose="Ultrasound",
        notes="Baby is developing well."
    )

    db.session.add_all([appointment1, appointment2])
    db.session.commit()

    symptoms = [
        ("Morning Sickness", "Nausea and vomiting during early pregnancy."),
        ("Fatigue", "Extreme tiredness during pregnancy."),
        ("Back Pain", "Lower back pain due to weight changes.")
    ]

    for name, description in symptoms:
        existing_symptom = Symptom.query.filter_by(name=name).first()
        if not existing_symptom:
            symptom = Symptom(name=name, description=description)
            db.session.add(symptom)
        else:
            print(f"Symptom '{name}' already exists in the database.")

    db.session.commit()

    pregnancy_symptom1 = PregnancySymptom(
        pregnancy_id=pregnancy1.id,
        symptom_id=Symptom.query.filter_by(name="Morning Sickness").first().id,
        date_reported=datetime.strptime("2025-02-05", "%Y-%m-%d").date()
    )

    pregnancy_symptom2 = PregnancySymptom(
        pregnancy_id=pregnancy2.id,
        symptom_id=Symptom.query.filter_by(name="Fatigue").first().id,
        date_reported=datetime.strptime("2025-03-01", "%Y-%m-%d").date()
    )

    db.session.add_all([pregnancy_symptom1, pregnancy_symptom2])
    db.session.commit()

    resources = [
        ("Pregnancy Nutrition Guide", "A guide to healthy eating during pregnancy.", "https://www.hopkinsmedicine.org/health/wellness-and-prevention/nutrition-during-pregnancy"),
        ("Exercise During Pregnancy", "Safe exercises for pregnant women.", "https://www.betterhealth.vic.gov.au/health/healthyliving/pregnancy-and-exercise")
    ]

    for title, content, link in resources:
        resource = EducationalResource(title=title, content=content, link=link)
        db.session.add(resource)

    db.session.commit()

    print("Database seeded successfully!")
