import os

class Patient:
    def __init__(self, name, surname, date_of_birth, diagnosis="", status=True):
        self.name = name
        self.surname = surname
        self.date_of_birth = date_of_birth
        self.diagnosis = diagnosis
        self.status = status

    def __str__(self):
        return f"{self.name} {self.surname} ({self.date_of_birth}) — {self.diagnosis or 'Без діагнозу'} — {'Хворий' if self.status else 'Виписаний'}"

    def to_line(self):
        return f"{self.name}|{self.surname}|{self.date_of_birth}|{self.diagnosis}|{self.status}\n"

    @staticmethod
    def from_line(line):
        name, surname, date_of_birth, diagnosis, status = line.strip().split("|")
        return Patient(name, surname, date_of_birth, diagnosis, status == "True")

class Doctor:
    def __init__(self, name, surname, specialization):
        self.name = name
        self.surname = surname
        self.specialization = specialization
        self.patients = []

    def __str__(self):
        return f"{self.name} {self.surname} — {self.specialization}, пацієнтів: {len(self.patients)}"

    def assign_patient(self, patient):
        self.patients.append(f"{patient.name} {patient.surname}")

    def to_line(self):
        patient_str = ",".join(self.patients)
        return f"{self.name}|{self.surname}|{self.specialization}|{patient_str}\n"

    @staticmethod
    def from_line(line):
        parts = line.strip().split("|")
        name, surname, specialization = parts[:3]
        patients = parts[3].split(",") if len(parts) > 3 and parts[3] else []
        d = Doctor(name, surname, specialization)
        d.patients = patients
        return d

class MedicalRecord:
    def __init__(self, patient_name, doctor_name, diagnosis, treatment):
        self.patient_name = patient_name
        self.doctor_name = doctor_name
        self.diagnosis = diagnosis
        self.treatment = treatment

    def __str__(self):
        return f"Пацієнт: {self.patient_name} | Лікар: {self.doctor_name} | Діагноз: {self.diagnosis} | Лікування: {self.treatment}"

    def to_line(self):
        return f"{self.patient_name}|{self.doctor_name}|{self.diagnosis}|{self.treatment}\n"

    @staticmethod
    def from_line(line):
        patient_name, doctor_name, diagnosis, treatment = line.strip().split("|")
        return MedicalRecord(patient_name, doctor_name, diagnosis, treatment)

class Hospital:
    def __init__(self, patients_file="patients.txt", doctors_file="doctors.txt", records_file="records.txt"):
        self.patients_file = patients_file
        self.doctors_file = doctors_file
        self.records_file = records_file
        self.patients = []
        self.doctors = []
        self.records = []
        self.load_data()

    def add_patient(self, patient):
        self.patients.append(patient)
        self.save_data()

    def add_doctor(self, doctor):
        self.doctors.append(doctor)
        self.save_data()

    def assign_patient_to_doctor(self, patient_name, doctor_name):
        patient = next((p for p in self.patients if f"{p.name} {p.surname}" == patient_name), None)
        doctor = next((d for d in self.doctors if f"{d.name} {d.surname}" == doctor_name), None)
        if patient and doctor:
            doctor.assign_patient(patient)
            print(f"Пацієнта {patient_name} закріплено за лікарем {doctor_name}")
            self.save_data()
        else:
            print("Пацієнта або лікаря не знайдено")

    def add_record(self, record):
        self.records.append(record)
        self.save_data()

    def list_patients(self):
        print("\n=== Пацієнти ===")
        for p in self.patients:
            print(p)

    def list_doctors(self):
        print("\n=== Лікарі ===")
        for d in self.doctors:
            print(d)

    def list_records(self):
        print("\n=== Історії хвороб ===")
        for r in self.records:
            print(r)

    def save_data(self):
        with open(self.patients_file, "w", encoding="utf-8") as f:
            for p in self.patients:
                f.write(p.to_line())
        with open(self.doctors_file, "w", encoding="utf-8") as f:
            for d in self.doctors:
                f.write(d.to_line())
        with open(self.records_file, "w", encoding="utf-8") as f:
            for r in self.records:
                f.write(r.to_line())

    def load_data(self):
        if os.path.exists(self.patients_file):
            with open(self.patients_file, "r", encoding="utf-8") as f:
                self.patients = [Patient.from_line(line) for line in f]
        if os.path.exists(self.doctors_file):
            with open(self.doctors_file, "r", encoding="utf-8") as f:
                self.doctors = [Doctor.from_line(line) for line in f]
        if os.path.exists(self.records_file):
            with open(self.records_file, "r", encoding="utf-8") as f:
                self.records = [MedicalRecord.from_line(line) for line in f]


if __name__ == "__main__":
    hospital = Hospital()

    while True:
        print("\n Система обліку пацієнтів")
        print("1. Додати пацієнта")
        print("2. Додати лікаря")
        print("3. Призначити пацієнта лікарю")
        print("4. Додати історію хвороби")
        print("5. Переглянути пацієнтів")
        print("6. Переглянути лікарів")
        print("7. Переглянути історії хвороб")
        print("8. Вийти")

        choice = input("Виберіть опцію: ")

        if choice == "1":
            name = input("Ім'я: ")
            surname = input("Прізвище: ")
            dob = input("Дата народження: ")
            diagnosis = input("Діагноз: ")
            hospital.add_patient(Patient(name, surname, dob, diagnosis))
        elif choice == "2":
            name = input("Ім'я лікаря: ")
            surname = input("Прізвище: ")
            specialization = input("Спеціалізація: ")
            hospital.add_doctor(Doctor(name, surname, specialization))
        elif choice == "3":
            patient_name = input("Пацієнт (Ім'я Прізвище): ")
            doctor_name = input("Лікар (Ім'я Прізвище): ")
            hospital.assign_patient_to_doctor(patient_name, doctor_name)
        elif choice == "4":
            patient_name = input("Пацієнт (Ім'я Прізвище): ")
            doctor_name = input("Лікар (Ім'я Прізвище): ")
            diagnosis = input("Діагноз: ")
            treatment = input("Лікування: ")
            hospital.add_record(MedicalRecord(patient_name, doctor_name, diagnosis, treatment))
        elif choice == "5":
            hospital.list_patients()
        elif choice == "6":
            hospital.list_doctors()
        elif choice == "7":
            hospital.list_records()
        elif choice == "8":
            print("Вихід із системи...")
            break
        else:
            print("Невірний вибір!")
