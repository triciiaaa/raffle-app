import io
import pytest 
from contextlib import redirect_stdout
from unittest.mock import patch
from src.raffle import Raffle
from src.main import display_menu, handle_menu_choice
from src.exception.invalid_operation_exception import InvalidOperationException
from src.exception.invalid_input_exception import InvalidInputException

def test_display_menu():
    """Tests that the display_menu function prints the menu options correctly"""
    raffle = Raffle()
    output_buffer = io.StringIO()
    with redirect_stdout(output_buffer):
        display_menu(raffle)
    
    printed_output = output_buffer.getvalue()
    
    expected_output = (
        "\nWelcome to My Raffle App\n"
        "Status: Draw has not started\n"
        "\n[1] Start a New Draw\n"
        "[2] Buy Tickets\n"
        "[3] Run Raffle\n"
    )
    
    assert printed_output == expected_output

def test_handle_menu_choice_start_new_draw():
    """Tests that the handle_menu_choice function calls start_new_draw when user selects '1'"""
    raffle = Raffle()
    
    with patch.object(raffle, "start_new_draw") as mock_start_new_draw, \
         patch("builtins.input", return_value=""):
        handle_menu_choice(raffle, '1')
        
        mock_start_new_draw.assert_called_once()

def test_handle_menu_choice_start_new_draw_with_existing_draw():
    """Tests that the handle_menu_choice function raises an exception when user selects '1' with an active draw"""
    raffle = Raffle()

    with patch.object(raffle, "is_active", return_value=True), \
        pytest.raises(InvalidOperationException, match="Raffle draw is already active. Please end the current draw."):
        handle_menu_choice(raffle, '1')

def test_handle_menu_choice_buy_tickets_existing_draw():
    """Tests that the handle_menu_choice function calls add_user when user selects '2'"""
    raffle = Raffle()
    
    with patch.object(raffle, "is_active", return_value=True), \
         patch.object(raffle, "add_user") as mock_add_user, \
         patch("builtins.input", return_value="Alice, 3"):
        
        handle_menu_choice(raffle, '2')
        
        mock_add_user.assert_called_once_with("Alice")

def test_handle_menu_choice_buy_tickets_no_draw():
    """Tests that the handle_menu_choice function raises an exception when user selects '2' without starting a draw"""
    raffle = Raffle()

    with patch("builtins.input", return_value="Alice, 3"):
        with pytest.raises(InvalidOperationException, match="Raffle draw has not started. Please start a new draw."):
            handle_menu_choice(raffle, '2')

def test_handle_menu_choice_run_raffle_existing_draw():
    """Tests that the handle_menu_choice function calls the necessary methods when user selects '3'"""
    raffle = Raffle()
    
    with patch.object(raffle, "is_active", return_value=True), \
         patch.object(raffle, "generate_winning_numbers") as mock_generate_winning_numbers, \
         patch.object(raffle, "calculate_raffle_results") as mock_calculate_raffle_results, \
         patch.object(raffle, "display_winners") as mock_display_winners, \
         patch.object(raffle, "end_draw") as mock_end_draw, \
         patch("builtins.input", return_value=""):
        
        handle_menu_choice(raffle, '3')
        
        mock_generate_winning_numbers.assert_called_once()
        mock_calculate_raffle_results.assert_called_once()
        mock_display_winners.assert_called_once_with(raffle.raffle_results)
        mock_end_draw.assert_called_once()

def test_handle_menu_choice_run_raffle_no_draw():
    """Tests that the handle_menu_choice function raises an exception when user selects '3' without starting a draw"""
    raffle = Raffle()

    with pytest.raises(InvalidOperationException, match="Raffle draw has not started. Please start a new draw."):
        handle_menu_choice(raffle, '3')

def test_handle_menu_choice_invalid_option():
    """Tests that the handle_menu_choice function prints an error message for invalid choices"""
    raffle = Raffle()
    
    with pytest.raises(InvalidInputException, match="Invalid choice, please select again."):
        handle_menu_choice(raffle, '4')
