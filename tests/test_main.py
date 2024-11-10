from unittest.mock import patch, call
from src.raffle import Raffle
from src.main import display_menu, handle_menu_choice

def test_display_menu():
    """Tests that the display_menu function prints the menu options correctly"""
    raffle = Raffle()
    raffle.get_draw_status = lambda: "Status: Draw not started"  # Mock get_draw_status output
    
    # Simulate user input '1' to select "Start a New Draw"
    with patch("builtins.input", return_value="1"), patch("builtins.print") as mock_print:
        choice = display_menu(raffle)
    
    # Verify that menu output was printed correctly
    expected_calls = [
        call("\nWelcome to My Raffle App"),
        call("Status: Draw not started"),
        call("\n[1] Start a New Draw"),
        call("[2] Buy Tickets"),
        call("[3] Run Raffle")
    ]
    mock_print.assert_has_calls(expected_calls)

    # Verify that the returned choice is '1'
    assert choice == "1"

def test_handle_menu_choice_start_new_draw():
    """Tests that the handle_menu_choice function calls start_new_draw when user selects '1'"""
    raffle = Raffle()
    
    with patch.object(raffle, "start_new_draw") as mock_start_new_draw:
        handle_menu_choice(raffle, '1')
        
        mock_start_new_draw.assert_called_once()

def test_handle_menu_choice_buy_tickets():
    """Tests that the handle_menu_choice function calls add_user when user selects '2'"""
    raffle = Raffle()
    
    with patch.object(raffle, "add_user") as mock_add_user, \
         patch("builtins.input", return_value="Alice, 3"):
        
        handle_menu_choice(raffle, '2')
        
        mock_add_user.assert_called_once_with("Alice", 3)

def test_handle_menu_choice_run_raffle():
    """Tests that the handle_menu_choice function calls the necessary methods when user selects '3'"""
    raffle = Raffle()
    
    with patch.object(raffle, "generate_winning_numbers") as mock_generate_winning_numbers, \
         patch.object(raffle, "calculate_raffle_results") as mock_calculate_raffle_results, \
         patch.object(raffle, "display_winners") as mock_display_winners, \
         patch.object(raffle, "end_draw") as mock_end_draw:
        
        handle_menu_choice(raffle, '3')
        
        mock_generate_winning_numbers.assert_called_once()
        mock_calculate_raffle_results.assert_called_once()
        mock_display_winners.assert_called_once_with(raffle.raffle_results)
        mock_end_draw.assert_called_once()

def test_handle_menu_choice_invalid_option():
    """Tests that the handle_menu_choice function prints an error message for invalid choices"""
    raffle = Raffle()
    
    with patch("builtins.print") as mock_print:
        handle_menu_choice(raffle, '4')
        
        mock_print.assert_called_once_with("Invalid choice, please select again.")
