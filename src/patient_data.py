from datetime import date
from enum import Enum
from typing import List


class PatientRecordType(Enum):
    GENERAL_RECORD = 0
    DISEASE = 1
    TREATMENT = 2


class PatientRecord:
    record_type: PatientRecordType = PatientRecordType.GENERAL_RECORD
    content: str = None

    def __init__(self, record_type: PatientRecordType, content: str):
        self.record_type = record_type
        self.content = content

    def as_dict(self):
        return {
            "record_type": self.record_type,
            "content": self.content
        }


class PatientData:
    name: str = None
    birth_date: date = None
    records: List[PatientRecord] = []

    def __init__(self, name, birth_date, records):
        self.name = name
        self.birth_date = birth_date
        self.records = records

    def as_dict(self):
        return {
            "name": self.name,
            "birth_date": self.birth_date,
            "records": [record.as_dict() for record in self.records]
        }

