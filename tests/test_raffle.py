import io
import pytest 
from contextlib import redirect_stdout
from unittest.mock import patch, call, MagicMock
from src.raffle import Raffle
from src.user import User
from src.exception.invalid_input_exception import InvalidInputException

def test_raffle_initialisation():
    """Tests that the Raffle class is initialised correctly"""
    raffle = Raffle()
    
    assert raffle.pot_size == 0
    assert raffle.users == []
    assert raffle.winning_numbers == []
    assert raffle.is_active is False
    assert raffle.raffle_results == {}

def test_get_draw_status_inactive():
    """Tests that the get_draw_status method returns the correct status message when there are no active draws"""
    raffle = Raffle()
    assert raffle.get_draw_status() == "Status: Draw has not started"
    
def test_get_draw_status_active():
    """Tests that the get_draw_status method returns the correct status message when there is an active draw"""
    raffle = Raffle()
    raffle.is_active = True
    raffle.pot_size = 150
    assert raffle.get_draw_status() == "Status: Draw is ongoing. Raffle pot size is $150"

def test_start_new_draw():
    """Tests that the start_new_draw method initialises a new raffle draw"""
    raffle = Raffle()

    output_buffer = io.StringIO()
    with redirect_stdout(output_buffer):
        raffle.start_new_draw()
    
    printed_output = output_buffer.getvalue().strip() 
    expected_output = "New Raffle draw has been started. Initial pot size: $100"

    assert raffle.is_active is True
    assert raffle.pot_size == 100
    assert printed_output == expected_output
    
def test_get_existing_user_by_name():
    """Tests that the get_user_by_name method returns the correct user instance"""
    raffle = Raffle()
    
    user1 = User("Alice")
    user2 = User("Bob")
    user3 = User("Charlie")
    
    raffle.users.extend([user1, user2, user3])
    result = raffle.get_user_by_name("Bob")
    
    assert result is not None
    assert result.name == "Bob"  
    assert result == user2  

def test_get_non_existing_user_by_name():
    """Tests that the get_user_by_name method returns None when the user does not exist"""
    raffle = Raffle()
    
    raffle.users.append(User("Alice"))
    result = raffle.get_user_by_name("Bob")
    
    assert result is None 

def test_verify_buy_tickets_valid_input():
    """Tests that the verify_buy_tickets method correctly validates user input for buying tickets"""
    raffle = Raffle()
    
    result = raffle.verify_buy_tickets_input("Alice, 3")
    assert result == ("Alice", 3)

def test_verify_buy_tickets_invalid_input_single_detail():
    """Tests that the verify_buy_tickets method correctly handles invalid user input for buying tickets"""
    raffle = Raffle()
    
    with pytest.raises(InvalidInputException, match="Invalid input. Input must contain a single comma separating the name and ticket count."):
        result = raffle.verify_buy_tickets_input("Alice")

def test_verify_buy_tickets_invalid_input_missing_name():
    """Tests that the verify_buy_tickets method correctly handles invalid user input for buying tickets"""
    raffle = Raffle()

    with pytest.raises(InvalidInputException, match="Invalid input. Name cannot be empty."):
        result = raffle.verify_buy_tickets_input(", 3")

def test_verify_buy_tickets_invalid_input_missing_ticket_count():
    """Tests that the verify_buy_tickets method correctly handles invalid user input for buying tickets"""
    raffle = Raffle()
    
    with pytest.raises(InvalidInputException, match="Invalid input. Ticket count must be a positive integer."):
        result = raffle.verify_buy_tickets_input("Alice,")

def test_verify_buy_tickets_invalid_input_negative_ticket_count():
    """Tests that the verify_buy_tickets method correctly handles invalid user input for buying tickets"""
    raffle = Raffle()
    
    with pytest.raises(InvalidInputException, match="Invalid input. Ticket count must be a positive integer."):
        result = raffle.verify_buy_tickets_input("Alice, -3")

def test_add_user():
    """Tests that the add_user method correctly adds a new user to the raffle"""
    raffle = Raffle()
    raffle.add_user("Alice")

    assert len(raffle.users) == 1
    assert raffle.users[0].name == "Alice"

def test_increase_pot_size():
    """Tests that the increase_pot_size method correctly increases the pot size based on the number of tickets purchased"""
    raffle = Raffle()
    raffle.pot_size = 100
    raffle.increase_pot_size(3)
    
    assert raffle.pot_size == 115

def test_generate_winning_numbers():
    """Tests that the generate_winning_numbers method sets the winning numbers correctly"""
    raffle = Raffle()
    raffle.generate_winning_numbers()
    
    assert len(raffle.winning_numbers) == 5, "Winning numbers must contain exactly 5 numbers."
    assert len(set(raffle.winning_numbers)) == 5, "Winning numbers must be unique."
    assert all(1 <= num <= 15 for num in raffle.winning_numbers), "Winning numbers must be between 1 and 15."
    assert raffle.winning_numbers == sorted(raffle.winning_numbers), "Winning numbers must be sorted."

def test_calculate_raffle_results_for_single_win():
    """Tests that the calculate_raffle_results method correctly calculates the raffle results for a single winner"""
    raffle = Raffle()
    mock_user = MagicMock(spec=User)
    mock_user.name = "Alice"
    mock_user.tickets = [MagicMock()]
    mock_user.tickets[0].count_matching_numbers = MagicMock(return_value=3)
    
    raffle.users.append(mock_user)
    raffle.pot_size = 1000
    raffle.calculate_raffle_results()
    
    assert "Group 3" in raffle.raffle_results
    assert "Alice" in raffle.raffle_results["Group 3"]
    assert raffle.raffle_results["Group 3"]["Alice"]["count"] == 1 
    assert raffle.raffle_results["Group 3"]["Alice"]["total_reward"] > 0

def test_calculate_raffle_results_for_multiple_wins_same_group():
    """Tests that the calculate_raffle_results method correctly calculates the raffle results for multiple winners in the same prize group"""
    raffle = Raffle()
    raffle.pot_size = 1000

    user = MagicMock(spec=User)
    user.name = "Alice"
    user.tickets = [MagicMock(), MagicMock()]

    user.tickets[0].count_matching_numbers = MagicMock(return_value=2)
    user.tickets[1].count_matching_numbers = MagicMock(return_value=2)

    raffle.users.append(user)    
    raffle.calculate_raffle_results()
    
    assert "Group 2" in raffle.raffle_results
    assert "Alice" in raffle.raffle_results["Group 2"]
    
    assert raffle.raffle_results["Group 2"]["Alice"]["count"] == 2
    
    total_reward = raffle.raffle_results["Group 2"]["Alice"]["total_reward"]
    assert total_reward > 0

def test_display_winners():
    """Tests that the display_winners method correctly prints the raffle winners"""
    raffle = Raffle()
    
    rewards = {
        "Group 2": {
            "Alice": {"count": 2, "total_reward": 50.0}
        },
        "Group 3": {
            "Bob": {"count": 1, "total_reward": 75.0}
        },
        "Group 5 (Jackpot)": {}
    }

    expected_output = (
        "\nGroup 2 Winners:\n"
        "Alice with 2 winning ticket(s) - $50.0\n"
        "\nGroup 3 Winners:\n"
        "Bob with 1 winning ticket(s) - $75.0\n"
        "\nGroup 5 (Jackpot) Winners:\n"
        "Nil\n"
    )

    output_buffer = io.StringIO()
    with redirect_stdout(output_buffer):
        raffle.display_winners(rewards)

    printed_output = output_buffer.getvalue()

    assert printed_output == expected_output
    
def test_calculate_total_winnings():
    """Tests that the calculate_total_winnings method correctly calculates the total winnings from the raffle results"""
    raffle = Raffle()
    raffle.raffle_results = {
        "Group 2": {"Alice": {"total_reward": 50}},
        "Group 3": {"Bob": {"total_reward": 75}},
        "Group 4": {},
        "Group 5 (Jackpot)": {"Charlie": {"total_reward": 500}}
    }
    total_winnings = raffle.calculate_total_winnings(raffle.raffle_results)
    assert total_winnings == 625

def test_reset_draw():
    """Tests that the reset_draw method resets the raffle draw state"""
    raffle = Raffle()
    raffle.is_active = True
    raffle.users = [MagicMock(spec=User)]
    raffle.winning_numbers = [1, 2, 3, 4, 5]
    
    raffle.reset_draw()
    
    assert raffle.is_active is False
    assert raffle.users == []
    assert raffle.winning_numbers == []

def test_end_draw():
    """Tests that the end_draw method correctly ends the raffle draw and updates the pot size"""
    raffle = Raffle()
    raffle.pot_size = 1000
    raffle.raffle_results = {
        "Group 2": {"Alice": {"total_reward": 50}},
        "Group 3": {"Bob": {"total_reward": 75}}
    }
    
    with patch.object(raffle, 'reset_draw') as mock_reset:
        raffle.end_draw()

    assert raffle.pot_size == 875  
    mock_reset.assert_called_once()