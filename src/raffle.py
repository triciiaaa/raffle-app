import random
from src.user import User
from src.prize_group import PrizeGroup
from src.exception.invalid_input_exception import InvalidInputException

class Raffle:
    """
    Represents a raffle draw with a pot size, list of users, winning numbers,
    """
    def __init__(self):
        """
        Initialises a Raffle instance with default values for pot size, user list,
        winning numbers, draw status, and raffle results.
        """
        self.pot_size = 0
        self.users = []
        self.winning_numbers = []
        self.is_active = False
        self.raffle_results = {}

    def get_draw_status(self):
        """
        Retrieves the current draw status.
        
        Returns:
            str: Message indicating if a draw is active and the current pot size.
        """
        if self.is_active:
            return f"Status: Draw is ongoing. Raffle pot size is ${self.pot_size}"
        else:
            return "Status: Draw has not started"

    def start_new_draw(self):
        """
        Starts a new raffle draw by setting the draw to active, increasing the pot size,
        and prompting the user to return to the main menu.
        """
        self.is_active = True
        self.pot_size += 100
        print(f"\nNew Raffle draw has been started. Initial pot size: ${self.pot_size}")
        print("Press any key to return to the main menu.")
        return input()

    def get_user_by_name(self, name):
        """
        Retrieves a user by their name.

        Parameters:
            name (str): The name of the user.

        Returns:
            User: The user instance if found, otherwise None.
        """
        for user in self.users:
            if user.name == name:
                return user
        return None

    def verify_buy_tickets_input(self, name_and_ticket_count):
        if ',' not in name_and_ticket_count or name_and_ticket_count.count(',') != 1:
            raise InvalidInputException("Invalid input. Input must contain a single comma separating the name and ticket count.")

        name, ticket_count = name_and_ticket_count.split(',', 1)

        if not name.strip():
            raise InvalidInputException("Invalid input. Name cannot be empty.")

        if not ticket_count.strip().isdigit() or int(ticket_count.strip()) <= 0:
            raise InvalidInputException("Invalid input. Ticket count must be a positive integer.")

        return name.strip(), int(ticket_count.strip())

    def add_user(self, name, ticket_count):
        """
        Adds a user to the raffle and allow them to purchase tickets.

        Parameters:
            name (str): The user's name.
            ticket_count (int): The number of tickets the user wishes to buy.
        """
        user = self.get_user_by_name(name)
        
        if user is None:
            user = User(name)
            self.users.append(user)

        initial_ticket_count = len(user.tickets)
        user.buy_tickets(ticket_count)
        new_ticket_count = len(user.tickets) - initial_ticket_count

        self.pot_size += new_ticket_count * 5 

    def generate_winning_numbers(self):
        """
        Generates a set of five unique winning numbers between 1 and 15,
        sort them, and display the result.
        """
        print("\nRunning Raffle...")
        self.winning_numbers = sorted(random.sample(range(1, 16), 5))
        print(f"Winning Ticket is {' '.join(map(str, self.winning_numbers))}", end="\n")

    def calculate_raffle_results(self):
        """
        Calculates the results of the raffle by determining winning tickets
        based on matching numbers. Distribute rewards according to prize groups.
        """
        rewards = {"Group 2": {}, "Group 3": {}, "Group 4": {}, "Group 5 (Jackpot)": {}}
        prize_groups = {
            2: PrizeGroup(2, 10),  # 2 matches = 10% of pot
            3: PrizeGroup(3, 15),  # 3 matches = 15% of pot
            4: PrizeGroup(4, 25),  # 4 matches = 25% of pot
            5: PrizeGroup(5, 50)   # 5 matches = 50% of pot (Jackpot)
        }

        group_winner_counts = {2: {}, 3: {}, 4: {}, 5: {}}

        # Count matches for each user's tickets
        for user in self.users:
            for ticket in user.tickets:
                match_count = ticket.count_matching_numbers(self.winning_numbers)
                if match_count in prize_groups:
                    if user.name in group_winner_counts[match_count]:
                        group_winner_counts[match_count][user.name]['count'] += 1
                    else:
                        group_winner_counts[match_count][user.name] = {'count': 1}

        # Calculate rewards for each prize group
        for match_count, winners in group_winner_counts.items():
            group_name = f"Group {match_count}"
            winner_count = sum(winner_data['count'] for winner_data in winners.values())  # Total number of winning tickets in the group

            if winner_count > 0:
                reward_per_ticket = prize_groups[match_count].calculate_reward(self.pot_size, winner_count)

                for user_name, data in winners.items():
                    ticket_count = data['count']
                    total_reward = round(ticket_count * reward_per_ticket, 2)
                    rewards[group_name][user_name] = {'count': ticket_count, 'total_reward': total_reward}

        self.raffle_results = rewards

    def display_winners(self, rewards):
        """
        Displays the winners of the raffle for each prize group.

        Parameters:
            rewards (dict): Dictionary of rewards for each prize group and user.
        """
        for group, winners in rewards.items():
            print(f"\n{group} Winners:")

            if not winners:
                print("Nil")
            else:
                for user, data in winners.items():
                    ticket_count = data['count']
                    total_reward = round(data['total_reward'], 2)
                    print(f"{user} with {ticket_count} winning ticket(s) - ${total_reward}")

        print("\nPress any key to return to the main menu.")
        return input()
    
    def calculate_total_winnings(self, rewards):
        """
        Calculates the total amount of winnings to be distributed.

        Parameters:
            rewards (dict): Dictionary of rewards for each prize group and user.

        Returns:
            float: Total winnings to be deducted from the pot.
        """
        return sum(data['total_reward'] for group_rewards in rewards.values() for data in group_rewards.values())

    def reset_draw(self):
        """
        Resets the draw by clearing users, winning numbers, and setting the draw as inactive.
        """
        self.is_active = False
        self.users = []
        self.winning_numbers = []

    def end_draw(self):
        """
        Ends the current raffle draw, distribute winnings, and reset for the next round.
        """
        total_winnings = self.calculate_total_winnings(self.raffle_results)
        self.pot_size = max(0, self.pot_size - total_winnings)
        self.reset_draw()

    
