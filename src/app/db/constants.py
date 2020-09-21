import enum


MAXIMUM_EMAIL_LENGTH = 320
MAXIMUM_PHONE_NUMBER_LENGTH = 50

DEFAULT_EMPLOYER_TYPE = "outsourcing"
DEFAULT_USER_TYPE = "viewer"


class ApplyStatus(enum.Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"
