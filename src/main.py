from src.raffle import Raffle

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
    return input("\nSelect an option: ")

def handle_menu_choice(raffle, choice):
    """
    Handles the menu choice and perform actions based on the user's selection.

    Parameters:
        raffle (Raffle): The raffle instance to interact with.
        choice (str): The option selected by the user.
    """
    if choice == '1':
        raffle.start_new_draw()
    elif choice == '2':
        name_and_ticket_count = input("\nEnter your name, no of tickets to purchase: ")
        name, ticket_count = name_and_ticket_count.split(",")
        name = name.strip()
        ticket_count = int(ticket_count.strip())
        raffle.add_user(name, ticket_count)
    elif choice == '3':
        raffle.generate_winning_numbers()
        raffle.calculate_raffle_results()
        raffle.display_winners(raffle.raffle_results)
        raffle.end_draw()
    else:
        print("Invalid choice, please select again.")

def main():
    """
    Main function to control the raffle application flow.
    """
    raffle = Raffle()
    while True:
        choice = display_menu(raffle)
        handle_menu_choice(raffle, choice)

if __name__ == "__main__":
    main()
