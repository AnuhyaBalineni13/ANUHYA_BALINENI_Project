# program.py
import csv
import tkinter as tk
from tkinter import messagebox, simpledialog
import pandas as pd
import matplotlib.pyplot as plt
from credentials import CredentialManager
from hospital import Hospital, Patient
from datetime import datetime


class Program:
    def __init__(self, credential_file, patients_file):
        self.credential_manager = CredentialManager(credential_file)
        self.patients_file = patients_file
        self.hospital = Hospital()
        self.load_patient_data(patients_file)

    def load_patient_data(self, file_path):
        with open(file_path, "r") as file:
           reader = csv.DictReader(file)
           for row in reader:
                patient_id = row["Patient_ID"]
                visit_id = row["Visit_ID"]
                visit_time_str = row["Visit_time"]
                visit_time = self.parse_date(visit_time_str)
        
                visit_department = row["Visit_department"]
                race = row["Race"]
                gender = row["Gender"]
                ethnicity = row["Ethnicity"]
                age_str = row["Age"]
                age = int(float(age_str)) if age_str else None
                zip_code = row["Zip_code"]
                insurance = row["Insurance"]
                chief_complaint = row["Chief_complaint"]
                note_id = row["Note_ID"]
                note_type = row["Note_type"]
            
            # Check if the patient already exists
                if patient_id in self.hospital.patients:
                   patient = self.hospital.patients[patient_id]
                else:
                   patient = Patient(
                        Patient_ID=patient_id,
                        Visit_ID=visit_id,
                        Visit_time=visit_time,
                        Visit_department=visit_department,
                         Race=race,
                         Gender=gender,
                         Ethnicity=ethnicity,
                         Age=age,
                         Zip_code=zip_code,
                         Insurance=insurance,
                         Chief_complaint=chief_complaint,
                         Note_ID=note_id,
                         Note_type=note_type
                   )
                   self.hospital.add_patient(patient)

                
            # Add visit information to the patient
                patient.add_visit(
                    visit_id,
                    visit_time,
                    visit_department,
                    chief_complaint,
                    note_id,
                    note_type,
            )

    def parse_date(self, date_str):
    	if not date_str:  # Check if the string is empty
        	return None
    	formats_to_try = [
        	"%Y-%m-%d %H:%M:%S", "%Y-%m-%d %I:%M:%S %p",
        	"%m-%d-%Y %H:%M:%S", "%m-%d-%Y %I:%M:%S %p",
        	"%d-%m-%Y %H:%M:%S", "%d-%m-%Y %I:%M:%S %p",
        	"%Y-%m-%d %H:%M", "%Y-%m-%d %I:%M %p",
        	"%m-%d-%Y %H:%M", "%m-%d-%Y %I:%M %p",
        	"%d-%m-%Y %H:%M", "%d-%m-%Y %I:%M %p",
        	"%Y-%m-%d", "%m-%d-%Y", "%d-%m-%Y",
    	]
    	for format_str in formats_to_try:
        	try:
            		return datetime.strptime(date_str, format_str)
        	except ValueError:
            		pass
    
    	raise ValueError(f"Unable to parse date: {date_str}")

    def start(self):
        self.root = tk.Tk()
        self.root.title("Hospital Management System")
        self.login_page()
        self.root.mainloop()

    def login_page(self):
        self.clear_screen()
        self.username_label = tk.Label(self.root, text="Username:")
        self.username_label.pack()
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack()

        self.password_label = tk.Label(self.root, text="Password:")
        self.password_label.pack()
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack()

        self.login_button = tk.Button(self.root, text="Log In", command=self.login)
        self.login_button.pack()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        user = self.credential_manager.validate_user(username, password)
        if user:
            self.user = user
            self.show_menu()
        else:
            messagebox.showerror(
                "Error", "Invalid username or password. Please try again."
            )

    def show_menu(self):
        self.clear_screen()
        if self.user.role == "admin":
            self.log_usage("Admin login")
            self.admin_menu()
        elif self.user.role == "management":
            self.log_usage("Management login")
            self.management_menu()
        elif self.user.role in ["clinician", "nurse"]:
            self.log_usage("Clinician/Nurse login")
            self.clinician_nurse_menu()

    def admin_menu(self):
        self.count_visits_button = tk.Button(
            self.root, text="Count Visits", command=self.count_visits
        )
        self.count_visits_button.pack()
        self.exit_button = tk.Button(self.root, text="Exit", command=self.exit_program)
        self.exit_button.pack()

    def management_menu(self):
        self.generate_statistics_button = tk.Button(
            self.root,
            text="Generate Key Statistics",
            command=self.generate_key_statistics,
        )
        self.generate_statistics_button.pack()
        self.exit_button = tk.Button(self.root, text="Exit", command=self.exit_program)
        self.exit_button.pack()

    def clinician_nurse_menu(self):
        self.retrieve_patient_button = tk.Button(
            self.root, text="Retrieve Patient", command=self.retrieve_patient
        )
        self.retrieve_patient_button.pack()
        self.add_patient_button = tk.Button(
            self.root, text="Add Patient", command=self.add_patient
        )
        self.add_patient_button.pack()
        self.remove_patient_button = tk.Button(
            self.root, text="Remove Patient", command=self.remove_patient
        )
        self.remove_patient_button.pack()
        self.count_visits_button = tk.Button(
            self.root, text="Count Visits", command=self.count_visits
        )
        self.count_visits_button.pack()
        self.exit_button = tk.Button(self.root, text="Exit", command=self.exit_program)
        self.exit_button.pack()

    def retrieve_patient(self):
        patient_id = simpledialog.askstring("Retrieve Patient", "Enter Patient ID:")
        if patient_id:
            patient = self.hospital.retrieve_patient(patient_id)
            if patient:
                self.show_patient_info(patient)
            else:
                messagebox.showerror("Error", "Patient not found.")

    def show_patient_info(self, patient):
        info_window = tk.Toplevel(self.root)
        info_window.title("Patient Information")

        info_label = tk.Label(
            info_window, text="Patient Information", font=("Helvetica", 16, "bold")
        )
        info_label.pack()

        patient_info = tk.Label(
            info_window,
            text=f"Patient ID: {patient.Patient_ID}\n"
            f"Gender: {patient.Gender}\n"
            f"Race: {patient.Race}\n"
            f"Age: {patient.Age}\n"
            f"Ethnicity: {patient.Ethnicity}\n"
            f"Insurance: {patient.Insurance}\n"
            f"Zip code: {patient.Zip_code}\n",
        )
        patient_info.pack()

        visits_label = tk.Label(
            info_window, text="Visits:", font=("Helvetica", 14, "bold")
        )
        visits_label.pack()

        for visit_id, visit in patient.visits.items():
            visit_info = tk.Label(
                info_window,
                text=f"Visit ID: {visit_id}\n"
                f"Visit time: {visit.Visit_time.strftime('%Y-%m-%d')}\n"
                f"Department: {visit.Visit_department}\n"
                f"Chief complaint: {visit.Chief_complaint}\n"
                f"Note ID: {visit.Note_ID}\n"
                f"Note type: {visit.Note_type}\n",
            )
            visit_info.pack()

        close_button = tk.Button(info_window, text="Close", command=info_window.destroy)
        close_button.pack()

    def add_patient(self):
    	fields = [
        	"Patient_ID",
        	"Visit_ID",
        	"Visit_time",
        	"Visit_department",
        	"Race",
        	"Gender",
        	"Ethnicity",
        	"Age",
        	"Zip_code",
        	"Insurance",
        	"Chief_complaint",
        	"Note_ID",
        	"Note_type",
    	]
    	data = {}
    	for field in fields:
        	data[field] = simpledialog.askstring("Add Patient", f"Enter {field}:")

    	patient_id = data["Patient_ID"]
    	visit_id = data["Visit_ID"]
    	visit_time = self.parse_date(data["Visit_time"])
    	visit_department = data["Visit_department"]
    	chief_complaint = data["Chief_complaint"]
    	note_id = data["Note_ID"]
    	note_type = data["Note_type"]
    	patient = Patient(**data)
    	patient.add_visit(visit_id, visit_time, visit_department, chief_complaint, note_id, note_type)
    	self.hospital.add_patient(patient)
    	self.update_patients_file()


    def remove_patient(self):
        patient_id = simpledialog.askstring("Remove Patient", "Enter Patient ID:")
        if patient_id in self.hospital.patients:
            self.hospital.remove_patient(patient_id)
            self.update_patients_file()
            messagebox.showinfo("Success", "Patient removed successfully.")
        else:
            messagebox.showerror("Error", "Patient not found.")

    def count_visits(self):
    	if self.user.role == "admin":
        # Admin can count visits for any date
        	self.count_visits_for_date()
    	elif self.user.role in ["clinician", "nurse"]:
        	# Clinician and Nurse can count visits for any date
        	self.count_visits_for_date()
    	else:
        	messagebox.showerror("Error", "You don't have permission to count visits.")

    def count_visits_for_date(self):
    	date_str = simpledialog.askstring("Count Visits", "Enter date (YYYY-MM-DD):")
    	try:
        	date = datetime.strptime(date_str, "%Y-%m-%d")
        	total_visits = self.hospital.count_visits_on_date(date)
        	messagebox.showinfo(
            	"Total Visits",
            	f"Total visits on {date.strftime('%Y-%m-%d')}: {total_visits}",
        	)
    	except ValueError:
        	messagebox.showerror("Error", "Invalid date format.")

    def generate_key_statistics(self):
        self.generate_temporal_trend_total_visits()
        self.generate_temporal_trend_insurance()
        self.generate_temporal_trend_demographics()

    def generate_temporal_trend_total_visits(self):
        # Extract visit dates
        visit_dates = [patient.Visit_time.date() for patient in self.hospital.patients.values() if patient.Visit_time]

        # Count visits per day
        visit_counts = {}
        for date in visit_dates:
            visit_counts[date] = visit_counts.get(date, 0) + 1

        # Plotting
        plt.figure(figsize=(10, 6))
        plt.plot(visit_counts.keys(), visit_counts.values(), marker='o')
        plt.title('Temporal Trend of Total Visits')
        plt.xlabel('Date')
        plt.ylabel('Number of Visits')
        plt.grid(True)
        plt.show()

    def generate_temporal_trend_insurance(self):
        # Extract insurance types
        insurance_types = set(patient.Insurance for patient in self.hospital.patients.values())

        # Count visits per insurance type per day
        insurance_counts = {insurance: {} for insurance in insurance_types}
        for patient in self.hospital.patients.values():
            if patient.Visit_time:
                date = patient.Visit_time.date()
                insurance_counts[patient.Insurance][date] = insurance_counts[patient.Insurance].get(date, 0) + 1

        # Plotting
        plt.figure(figsize=(10, 6))
        for insurance, counts in insurance_counts.items():
            plt.plot(counts.keys(), counts.values(), marker='o', label=insurance)
        plt.title('Temporal Trend of Visits by Insurance Type')
        plt.xlabel('Date')
        plt.ylabel('Number of Visits')
        plt.legend()
        plt.grid(True)
        plt.show()

    def generate_temporal_trend_demographics(self):
        # Extract demographic information
        demographics = ['Age', 'Race', 'Gender', 'Ethnicity']

        # Count visits per demographic group per day
        demographic_counts = {demo: {value: {} for value in set(getattr(patient, demo) for patient in self.hospital.patients.values() if patient.Visit_time)} for demo in demographics}
        for patient in self.hospital.patients.values():
            if patient.Visit_time:
                date = patient.Visit_time.date()
                for demo in demographics:
                    value = getattr(patient, demo)
                    demographic_counts[demo][value][date] = demographic_counts[demo][value].get(date, 0) + 1

        # Plotting
        for demo, counts in demographic_counts.items():
            plt.figure(figsize=(10, 6))
            for value, value_counts in counts.items():
                plt.plot(value_counts.keys(), value_counts.values(), marker='o', label=value)
            plt.title(f'Temporal Trend of Visits by {demo}')
            plt.xlabel('Date')
            plt.ylabel('Number of Visits')
            plt.legend()
            plt.grid(True)
            plt.show()

    def exit_program(self):
        self.root.destroy()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def update_patients_file(self):
        self.patients_df = pd.DataFrame(
            [patient.to_dict() for patient in self.hospital.patients.values()]
        )
        self.patients_df.to_csv(self.patients_file, index=False)
    
    def log_usage(self, action):
        # Define the file path for the usage statistics file
        usage_file = "usage_statistics.csv"

        # Define the fields for the CSV file
        fields = ["Timestamp", "Username", "Role", "Action"]

        # Get the current timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Get the username and role of the current user
        username = self.user.username
        role = self.user.role

        # Write the data to the CSV file, creating it if necessary
        try:
            with open(usage_file, "a", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=fields)
                # Write the header if the file is empty
                if file.tell() == 0:
                    writer.writeheader()
                writer.writerow({"Timestamp": timestamp, "Username": username, "Role": role, "Action": action})
                print("Usage data logged successfully.")
        except Exception as e:
            print(f"Error occurred while logging usage data: {str(e)}")
