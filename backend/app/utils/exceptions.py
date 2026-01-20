class EmailClassifierException(Exception):
    pass


class InvalidFileException(EmailClassifierException):
    pass


class InvalidTextException(EmailClassifierException):
    pass


class NLPProcessingException(EmailClassifierException):
    pass


class AIAPIException(EmailClassifierException):
    pass
