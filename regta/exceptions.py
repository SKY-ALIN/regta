class RegtaException(Exception):
    pass


class StopService(RegtaException):
    pass


class IncorrectJobType(RegtaException):
    def __init__(self, job, scheduler):
        message = f"{job.__class__.__name__} is incorrect job type for {scheduler.__class__.__name__}"
        super().__init__(message)
