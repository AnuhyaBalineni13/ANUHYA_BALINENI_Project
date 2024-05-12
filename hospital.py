# hospital.py

from datetime import datetime

class Hospital:
    def __init__(self):
        self.patients = {}

    def add_patient(self, patient):
        self.patients[patient.Patient_ID] = patient

    def remove_patient(self, patient_id):
        if patient_id in self.patients:
            del self.patients[patient_id]

    def retrieve_patient(self, patient_id):
        if patient_id in self.patients:
            return self.patients[patient_id]
        else:
            return None

    def count_visits_on_date(self, date):
        total_visits = 0
        for patient in self.patients.values():
            if patient.Visit_time and patient.Visit_time.date() == date.date():
                total_visits += 1
        return total_visits

class Patient:
    def __init__(
        self,
        Patient_ID,
        Visit_ID,
        Visit_time,
        Visit_department,
        Race,
        Gender,
        Ethnicity,
        Age,
        Zip_code,
        Insurance,
        Chief_complaint,
        Note_ID,
        Note_type,
    ):
        self.Patient_ID = Patient_ID
        self.Visit_ID = Visit_ID
        self.Visit_time = Visit_time
        self.Visit_department = Visit_department
        self.Race = Race
        self.Gender = Gender
        self.Ethnicity = Ethnicity
        self.Age = Age
        self.Zip_code = Zip_code
        self.Insurance = Insurance
        self.Chief_complaint = Chief_complaint
        self.Note_ID = Note_ID
        self.Note_type = Note_type
        self.visits = {}  # Initialize visits dictionary

    def add_visit(self, visit_id, visit_time, visit_department, chief_complaint, note_id, note_type):
        visit = Visit(visit_id, visit_time, visit_department, chief_complaint, note_id, note_type)
        self.visits[visit_id] = visit

    def to_dict(self):
        return {
            "Patient_ID": self.Patient_ID,
            "Visit_ID": self.Visit_ID,
            "Visit_time": self.Visit_time,
            "Visit_department": self.Visit_department,
            "Race": self.Race,
            "Gender": self.Gender,
            "Ethnicity": self.Ethnicity,
            "Age": self.Age,
            "Zip_code": self.Zip_code,
            "Insurance": self.Insurance,
            "Chief_complaint": self.Chief_complaint,
            "Note_ID": self.Note_ID,
            "Note_type": self.Note_type,
        }


class Visit:
    def __init__(self, visit_id, visit_time, visit_department, chief_complaint, note_id, note_type):
        self.Visit_ID = visit_id
        self.Visit_time = visit_time
        self.Visit_department = visit_department
        self.Chief_complaint = chief_complaint
        self.Note_ID = note_id
        self.Note_type = note_type
