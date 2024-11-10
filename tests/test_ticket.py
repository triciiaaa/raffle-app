from src.ticket import Ticket

def test_ticket_initialisation():
    """Tests that a ticket is initialised with 5 numbers"""
    ticket = Ticket()
    
    assert len(ticket.numbers) == 5
    assert len(set(ticket.numbers)) == 5

    for number in ticket.numbers:
        assert 1 <= number <= 15
    
    assert ticket.numbers == sorted(ticket.numbers)

def test_count_matching_numbers():
    """Tests that the count_matching_numbers method counts the number of matching numbers between the ticket and the winning numbers"""
    ticket = Ticket()
    
    winning_numbers = [1, 2, 3, 4, 5]
    expected_matches = len(set(ticket.numbers) & set(winning_numbers))
    assert ticket.count_matching_numbers(winning_numbers) == expected_matches

def test_display_numbers():
    """Tests that the display_numbers method returns a string of the ticket numbers"""
    ticket = Ticket()
    
    displayed_numbers = ticket.display_numbers().split()
    assert displayed_numbers == list(map(str, ticket.numbers))
