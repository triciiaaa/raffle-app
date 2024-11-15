from src.ticket import Ticket

class User:
    """
    Represents a user participating in the raffle. Each user has a name and can purchase up to a maximum number of tickets.
    """

    MAX_TICKETS = 5

    def __init__(self, name):
        """
        Initialiases a User instance with a given name and an empty ticket list.

        Parameters:
            name (str): The name of the user.
        """
        self.name = name
        self.tickets = []

    def buy_tickets(self, ticket_count):
        """
        Allows the user to purchase raffle tickets, limited to the maximum ticket count.

        Parameters:
            ticket_count (int): The number of tickets the user wants to purchase.
        """
        remaining_tickets = User.MAX_TICKETS - len(self.tickets)
        
        # Check if user has already reached the maximum ticket purchase limit
        if remaining_tickets <= 0:
            print(f"{self.name} has already purchased the maximum of {User.MAX_TICKETS} tickets and cannot buy more.")
            return
        
        # Adjust ticket count if the request exceeds the remaining allowance
        if ticket_count > remaining_tickets:
            print(f"{self.name} requested {ticket_count} tickets, but only {remaining_tickets} more ticket(s) can be purchased.")
            ticket_count = remaining_tickets

        print(f"\nHi {self.name}, you are purchasing {ticket_count} ticket(s).")
        
        # Generate and display each ticket purchased
        for i in range(ticket_count):
            ticket = Ticket()
            self.tickets.append(ticket)
            print(f"Ticket {i + 1}: {ticket.display_numbers()}")