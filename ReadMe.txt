Description:
The program is a Hospital Management System implemented in Python using Tkinter for the GUI. It allows users with different roles (admin, management, clinician, nurse) to log in and perform various tasks such as retrieving patient information, adding or removing patients, and generating key statistics like temporal trends in visits and demographics. The system also logs user actions for auditing purposes.

How to run: 
-> python, tinker,  matplotlib should be installed in your computer. 
    If you don't have them installed, run the following command one by one to get them installed:
    For Python: Search python online and download it from Python.org
    For tinker:  python -m tkinter
    For  matplotlib: pip install Matplotlib
-> Once you have all of the above installed go to the command prompt and run this command: python main.py <credentials_file> <patients_file> . Replace main.py, credentials file and patients file with
    the actual paths. 
-> That's all you will be able to see the User Interface which will ask you to enter username, password and upon credential validation it will show the menu based on the role. 

For your Information:
->program.py:
   This file contains the main program logic for the Hospital Management System.
    It provides functionalities for user login, menu display based on user roles, patient management, and generation of key statistics.
    The program is implemented using Tkinter for the GUI.
->credentials.py:
    This file defines the CredentialManager class, responsible for managing user credentials.
     It provides methods for validating user login credentials.
-> hospital.py:
    This file contains the definitions for the Hospital, Patient, and Visit classes.
    The Hospital class manages patient data and provides methods for adding, removing, and retrieving patients.
     The Patient class represents individual patients, while the Visit class represents patient visits.
->interface.py:
   This file contains functions to manage the GUI, specifically to clear the screen by destroying all widgets.
   The clear_screen function takes the root window as an argument and removes all widgets from it, effectively clearing the screen.
->  Main.py
    serves as the entry point for the Hospital Management System application. It initializes the program by passing necessary files and resources, such as credential and patient data files
->All the log actions are stored in usage_statistics.csv which will be created by program, user don't have to create it.

