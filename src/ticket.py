import random

class Ticket:
    """
    Represents a raffle ticket with a unique set of randomly generated numbers.
    Each ticket contains five numbers between 1 and 15.
    """
    def __init__(self):
        """
        Initialises a Ticket instance with five unique random numbers
        between 1 and 15, sorted in ascending order.
        """
        self.numbers = sorted(random.sample(range(1, 16), 5))

    def count_matching_numbers(self, winning_numbers):
        """
        Counts the number of matching numbers between this ticket and the winning numbers.

        Parameters:
            winning_numbers (list of int): The list of winning numbers to compare with.

        Returns:
            int: The count of matching numbers between this ticket and the winning numbers.
        """
        return len(set(self.numbers) & set(winning_numbers))

    def display_numbers(self):
        """
        Displays the numbers on the ticket as a formatted string.

        Returns:
            str: A space-separated string of numbers on the ticket.
        """
        return ' '.join(map(str, self.numbers))