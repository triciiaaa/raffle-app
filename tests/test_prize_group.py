from src.prize_group import PrizeGroup 

def test_prize_group_initialisation():
    """Tests that the PrizeGroup class is initialised correctly"""
    prize_group = PrizeGroup(match_count=3, reward_percentage=10.0)
    assert prize_group.match_count == 3
    assert prize_group.reward_percentage == 10.0

def test_calculate_reward_with_winners():
    """Tests that the calculate_reward method returns the correct reward"""
    prize_group = PrizeGroup(match_count=3, reward_percentage=20.0)
    pot_size = 1000.0
    winner_count = 5
    expected_reward = (20.0 / 100) * pot_size / winner_count
    assert prize_group.calculate_reward(pot_size, winner_count) == expected_reward

def test_calculate_reward_no_winners():
    """Tests that the calculate_reward method returns 0 when there are no winners"""
    prize_group = PrizeGroup(match_count=3, reward_percentage=20.0)
    pot_size = 1000.0
    winner_count = 0
    assert prize_group.calculate_reward(pot_size, winner_count) == 0
