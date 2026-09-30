from enum import Enum


class StatusDocument(Enum):
    UPLOAD = "upload"
    Processing = "processing"
    REJECTED = "rejected"
    SUCCESS = "success"