from unittest.mock import patch, MagicMock
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
    
    # Mock the Ticket creation to avoid generating random numbers
    with patch("src.user.Ticket", return_value=MagicMock(spec=Ticket)) as mock_ticket:
        with patch("builtins.input", return_value=""):  # Mock input to avoid waiting for user input
            user.buy_tickets(3)

    assert len(user.tickets) == 3  # User should have 3 tickets
    assert all(isinstance(ticket, Ticket) for ticket in user.tickets)
    assert mock_ticket.call_count == 3  # Ticket should be created 3 times

def test_buy_tickets_exceeding_limit():
    """Tests that the buy_tickets method does not allow the user to buy more tickets than the limit"""
    user = User("Bob")
    
    with patch("src.user.Ticket", return_value=MagicMock(spec=Ticket)) as mock_ticket:
        with patch("builtins.input", return_value=""):
            user.buy_tickets(10)  # Request more than MAX_TICKETS

    # User should only have MAX_TICKETS tickets
    assert len(user.tickets) == User.MAX_TICKETS
    assert mock_ticket.call_count == User.MAX_TICKETS

def test_buy_tickets_after_reaching_limit():
    """Tests that the buy_tickets method does not allow the user to buy more tickets after reaching the limit"""
    user = User("Charlie")
    
    # Fill up to MAX_TICKETS first
    with patch("src.user.Ticket", return_value=MagicMock(spec=Ticket)):
        with patch("builtins.input", return_value=""):
            user.buy_tickets(User.MAX_TICKETS)

    assert len(user.tickets) == User.MAX_TICKETS

    # Attempt to buy more tickets, which should not be allowed
    with patch("src.user.Ticket", return_value=MagicMock(spec=Ticket)) as mock_ticket:
        with patch("builtins.print") as mock_print, patch("builtins.input", return_value=""):
            user.buy_tickets(2)  # Try to buy more tickets after reaching limit

    # Confirm no new tickets were added and appropriate message was printed
    assert len(user.tickets) == User.MAX_TICKETS
    mock_ticket.assert_not_called()  # No new Ticket instance should be created
    mock_print.assert_any_call(f"{user.name} has already purchased the maximum of {User.MAX_TICKETS} tickets and cannot buy more.")
