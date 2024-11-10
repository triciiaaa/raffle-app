class PrizeGroup:
    """
    Represents a prize group in the raffle, defined by the number of matching numbers
    required to win and the percentage of the pot allocated as the reward.
    """

    def __init__(self, match_count, reward_percentage):
        """
        Initialises a PrizeGroup instance with the required match count and reward percentage.

        Parameters:
            match_count (int): The number of matching numbers required to win in this prize group.
            reward_percentage (float): The percentage of the pot allocated as the reward for this prize group.
        """
        self.match_count = match_count
        self.reward_percentage = reward_percentage

    def calculate_reward(self, pot_size, winner_count):
        """
        Calculates the reward for each winning ticket in this prize group.

        Parameters:
            pot_size (float): The total pot size available for distribution.
            winner_count (int): The number of winning tickets in this prize group.

        Returns:
            float: The reward per winning ticket. If there are no winners, returns 0.
        """
        if winner_count == 0:
            return 0
        return (self.reward_percentage / 100) * pot_size / winner_count
