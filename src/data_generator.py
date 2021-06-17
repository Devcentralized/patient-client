import random
from typing import List
from patient_data import PatientRecordType, PatientData, PatientRecord
from faker import Faker
from faker.providers import BaseProvider

faker = Faker()

class RecordsProvider(BaseProvider):

    general_words = [
        "patient", "check", "noticed", "weight", "height", "normal", "levels", "high", "low", "blood", "sugar"
    ]

    treatment_words = [
        "prescribed", "medicine", "exercise", "sleep", "should", "sport", "food", "eating", "drink water"
    ]

    disease_words = [
        "suffers", ""
    ]

    def disease_data(self) -> str:
        return faker.text(ext_word_list=self.general_words + self.disease_words)

    def treatment_data(self) -> str:
        return faker.text(ext_word_list=self.general_words + self.treatment_words)

    def general_record_data(self) -> str:
        return faker.text(ext_word_list=self.general_words)

    def record(self, record_type: PatientRecordType) -> str:
        if record_type == PatientRecordType.DISEASE:
            return self.disease_data()
        elif record_type == PatientRecordType.TREATMENT:
            return self.treatment_data()
        else:
            return self.general_record_data()


class DataGenerator:

    def __init__(self):
        faker.add_provider(RecordsProvider)

    def generate_patients_data(self, patients_count: int = 100, records_per_patient: int = 10) -> List[PatientData]:
        return [self.generate_patient_data(records_per_patient) for p in range(patients_count)]

    def generate_patient_data(self, records_count: int = 10) -> PatientData:
        name = faker.name()
        birth_date = faker.date_of_birth()
        records = []
        for i in range(records_count):
            records.append(self.generate_record())
        patient_data = PatientData(name, birth_date, records)
        return patient_data.as_dict()

    def generate_record(self) -> PatientRecord:
        record_type = random.choice(list(PatientRecordType))
        content = faker.record(record_type)
        record = PatientRecord(record_type, content)
        return record
