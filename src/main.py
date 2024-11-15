from src.raffle import Raffle
from src.exception.invalid_operation_exception import InvalidOperationException
from src.exception.invalid_input_exception import InvalidInputException

def display_menu(raffle):
    """
    Displays the main menu of the raffle application and prompt user input.

    Parameters:
        raffle (Raffle): The raffle instance to retrieve current draw status.

    Returns:
        str: The option selected by the user.
    """
    print("\nWelcome to My Raffle App")
    print(raffle.get_draw_status())  
    print("\n[1] Start a New Draw")
    print("[2] Buy Tickets")
    print("[3] Run Raffle")

def handle_menu_choice(raffle, choice):
    """
    Handles the menu choice and perform actions based on the user's selection.

    Parameters:
        raffle (Raffle): The raffle instance to interact with.
        choice (str): The option selected by the user.
    """
    if choice == '1':
        if raffle.is_active:
            raise InvalidOperationException("Raffle draw is already active. Please end the current draw.")
        else:
            raffle.start_new_draw()
            print("Press any key to return to the main menu.")
            input()
    elif choice == '2':
        if raffle.is_active:
            name_and_ticket_count = input("\nEnter your name, no of tickets to purchase: ")

            try:
                name, ticket_count = raffle.verify_buy_tickets_input(name_and_ticket_count)
            except InvalidInputException as e:
                print(e)

            if name and ticket_count:
                user = raffle.add_user(name)
                
                initial_ticket_count = len(user.tickets)
                user.buy_tickets(ticket_count)

                print("\nPress any key to return to the main menu.")
                input()
                
                new_ticket_count = len(user.tickets) - initial_ticket_count
                raffle.increase_pot_size(new_ticket_count)
        else:
            raise InvalidOperationException("Raffle draw has not started. Please start a new draw.")
    elif choice == '3':
        if raffle.is_active:
            print("\nRunning Raffle...")
            raffle.generate_winning_numbers()
            print(f"Winning Ticket is {' '.join(map(str, raffle.winning_numbers))}\n")
            raffle.calculate_raffle_results()
            raffle.display_winners(raffle.raffle_results)
            print("\nPress any key to return to the main menu.")
            input()
            raffle.end_draw()
        else:
            raise InvalidOperationException("Raffle draw has not started. Please start a new draw.")
    else:
        raise InvalidInputException("Invalid choice, please select again.")
    
def main():
    """
    Main function to control the raffle application flow.
    """
    raffle = Raffle()
    while True:
        display_menu(raffle)
        choice = input("\nSelect an option: ")
        
        try:
            handle_menu_choice(raffle, choice)
        except (InvalidOperationException, InvalidInputException) as e:
            print(e)

if __name__ == "__main__":
    main()
