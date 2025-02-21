import pytest
from unittest.mock import patch
from snooker_scores import SnookerScores


@pytest.fixture
def snooker_game():
    return SnookerScores()

# Shot validation tests
def test_validate_shot_valid(snooker_game):
    assert snooker_game.validate_shot("0") == 0
    assert snooker_game.validate_shot("7") == 7

def test_validate_shot_invalid(snooker_game):
    assert snooker_game.validate_shot("-1") is None
    assert snooker_game.validate_shot("8") is None
    assert snooker_game.validate_shot("100") is None
    assert snooker_game.validate_shot("abc") is None
    assert snooker_game.validate_shot("!") is None
    assert snooker_game.validate_shot("") is None

@patch("sys.exit")
def test_validate_shot_quit(mock_exit, snooker_game):
    with patch("builtins.input", return_value="q"):
        mock_exit.side_effect = SystemExit
        with pytest.raises(SystemExit):
            snooker_game.get_shot_value()

def test_validate_shot_p(snooker_game):
    with patch.object(snooker_game, "add_penalty") as mock_penalty:
        with patch("builtins.input", side_effect=["p", "1"]):
            assert snooker_game.get_shot_value() == 1
        mock_penalty.assert_called_once()

def test_validate_shot_x(snooker_game):
    initial_turn = snooker_game.player_1_turn
    with patch.object(snooker_game, "switch_players", side_effect=snooker_game.switch_players) as mock_switch:
        with patch("builtins.input", side_effect=["x", "1"]):
            assert snooker_game.get_shot_value() == 1
        mock_switch.assert_called_once()
    assert snooker_game.player_1_turn != initial_turn

def test_validate_shot_s(snooker_game):
    snooker_game.first_input = True
    with patch("builtins.input", side_effect=["s", "5", "10", "5", "1"]):
        snooker_game.get_shot_value()
        assert snooker_game.red_balls == 5
        assert snooker_game.score_player_1 == 10
        assert snooker_game.score_player_2 == 5
        assert snooker_game.available_player_1 == 67
        assert snooker_game.available_player_2 == 67

# Handle special inputs
def test_handle_special_input_q(snooker_game):
    with patch("sys.exit") as mock_exit:
        snooker_game.handle_special_input("q")
        mock_exit.assert_called_once()

def test_handle_special_input_p(snooker_game):
    # Test for 'p' which should apply penalty (mock add_penalty)
    with patch.object(snooker_game, 'add_penalty') as mock_add_penalty:
        snooker_game.handle_special_input("p")
        mock_add_penalty.assert_called_once()

def test_handle_special_input_x(snooker_game):
    # Test for 'x' which should switch players (mock switch_players)
    with patch.object(snooker_game, 'switch_players') as mock_switch_players:
        snooker_game.handle_special_input("x")
        mock_switch_players.assert_called_once()

def test_handle_special_input_s(snooker_game):
    with patch.object(snooker_game, 'set_starting_scores') as mock_set_starting_scores:
        snooker_game.handle_special_input("s")
        mock_set_starting_scores.assert_called_once()

def test_handle_invalid_input(snooker_game, capfd):
    snooker_game.handle_invalid_input()
    captured = capfd.readouterr()
    assert "Only numbers between 0 and 7 are valid!" in captured.out

# Re-spot input validation
def test_get_respot_input_valid():
    with patch('builtins.input', return_value='y'):
        game = SnookerScores()
        result = game.get_respot_input()
        assert result == 'y', f"Expected 'y', but got {result}"

    with patch('builtins.input', return_value='n'):
        game = SnookerScores()
        result = game.get_respot_input()
        assert result == 'n', f"Expected 'n', but got {result}"

def test_get_respot_input_invalid():
    with patch('builtins.input', side_effect=['a', 'y']):
        game = SnookerScores()
        result = game.get_respot_input()
        assert result == 'y', f"Expected 'y', but got {result}"

# Starting scores validation
def test_set_starting_scores_valid_input():
    with patch('builtins.input', side_effect=[16, 50, 60, 2, 50, 60]):
        game = SnookerScores()
        game.set_starting_scores()

    assert game.red_balls == 2
    assert game.score_player_1 == 50
    assert game.score_player_2 == 60
    assert game.available_player_1 == 43
    assert game.available_player_2 == 43

def test_set_starting_scores_invalid_input():
    with patch('builtins.input', side_effect=["15", "50", "60", "2", "50", "60"]):  
        game = SnookerScores()
        game.set_starting_scores()

    assert game.red_balls == 2
    assert game.score_player_1 == 50
    assert game.score_player_2 == 60
    assert game.available_player_1 == 43
    assert game.available_player_2 == 43

# Penalty input validation
def test_get_penalty_input_valid():
    with patch('builtins.input', side_effect=['5']):
        game = SnookerScores()
        penalty = game.get_penalty_input()
        assert penalty == 5

def test_get_penalty_input_invalid():
    with patch('builtins.input', side_effect=['-1', '3']):
        game = SnookerScores()
        penalty = game.get_penalty_input()
        assert penalty == 3

