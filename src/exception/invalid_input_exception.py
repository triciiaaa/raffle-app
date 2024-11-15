from src.exception.raffle_app_exception import RaffleAppException

class InvalidInputException(RaffleAppException):
    """
    Exception raised for invalid user input.

    Attributes:
        message (str): Explanation of the error.
    """
    pass