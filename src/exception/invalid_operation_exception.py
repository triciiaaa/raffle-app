from src.exception.raffle_app_exception import RaffleAppException

class InvalidOperationException(RaffleAppException):
    """
    Exception raised when an invalid operation is performed on the raffle application.
    """
    pass