import io 
from contextlib import redirect_stdout
from src.user import User
from src.ticket import Ticket

def test_user_initialisation():
    """Tests that the User class is initialised correctly"""
    user = User("Alice")
    assert user.name == "Alice"
    assert user.tickets == []

def test_buy_tickets_within_limit():
    """Tests that the buy_tickets method adds the correct number of tickets to the user"""
    user = User("Alice")
    user.buy_tickets(3)

    assert len(user.tickets) == 3 
    assert all(isinstance(ticket, Ticket) for ticket in user.tickets)

def test_buy_tickets_exceeding_limit():
    """Tests that the buy_tickets method does not allow the user to buy more tickets than the limit"""
    user = User("Bob")
    user.buy_tickets(10) 

    assert len(user.tickets) == User.MAX_TICKETS

def test_buy_tickets_after_reaching_limit():
    """Tests that the buy_tickets method does not allow the user to buy more tickets after reaching the limit"""
    user = User("Charlie")
    user.buy_tickets(User.MAX_TICKETS)

    output_buffer = io.StringIO()
    with redirect_stdout(output_buffer):
        user.buy_tickets(1) 

    assert len(user.tickets) == User.MAX_TICKETS
    
    printed_output = output_buffer.getvalue().strip()
    expected_message = f"Charlie has already purchased the maximum of {User.MAX_TICKETS} tickets and cannot buy more."
    
    assert printed_output == expected_message
