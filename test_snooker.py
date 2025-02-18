import pytest
from unittest.mock import patch, MagicMock
from snooker_gui import SnookerGUI
from snooker_game import SnookerGame


def create_mock_root():
    """Create a mock root object for the SnookerGUI."""
    return MagicMock()


def test_initial_state():
    """Test the initial state of the SnookerGUI class."""
    root = create_mock_root()
    game = SnookerGUI(root)
    assert game.game.available_points == 147
    assert game.game.red_balls == 15
    assert game.game.red_needed_next is True
    assert game.game.player_1_turn is True
    assert game.game.score_player_1 == 0
    assert game.game.score_player_2 == 0
    assert game.game.possible_score_player_1 == 147
    assert game.game.possible_score_player_2 == 147
    assert game.game.yellow_ball == 2
    assert game.game.colored_balls == {
        2: "yellow",
        3: "green",
        4: "brown",
        5: "blue",
        6: "pink",
        7: "black",
    }
    assert game.game.prompt == "What's the value of the shot: "


def test_initialize_prompt():
    root = create_mock_root()
    game = SnookerGUI(root)

    expected_prompt = "What's the value of the shot: "
    assert game.game.initialize_prompt() == expected_prompt

    expected_prompt = "What's the value of the shot: "
    assert game.game.initialize_prompt() == expected_prompt


def test_set_starting_scores_valid_input():
    """Test valid input for set_starting_scores."""
    root = create_mock_root()
    game = SnookerGUI(root)

    with patch('builtins.input', side_effect=["3", "50", "60"]):
        game.game.set_starting_scores(3, 50, 60)

    assert game.game.red_balls == 3
    assert game.game.score_player_1 == 50
    assert game.game.score_player_2 == 60
    assert game.game.available_points == game.game.red_balls * 8 + 27


def test_set_starting_scores_negative_scores():
    """Test negative scores input."""
    root = create_mock_root()
    game = SnookerGUI(root)

    with patch('builtins.input', side_effect=["3", "-10", "20", "3", "50", "60"]):
        game.game.set_starting_scores(3, 50, 60)

    assert game.game.red_balls == 3
    assert game.game.score_player_1 == 50
    assert game.game.score_player_2 == 60
    assert game.game.available_points == game.game.red_balls * 8 + 27


def test_set_starting_scores_total_score_exceeds_147():
    """Test total score exceeding 147."""
    root = create_mock_root()
    game = SnookerGUI(root)

    with patch('builtins.input', side_effect=["3", "100", "50", "3", "50", "60"]):
        game.game.set_starting_scores(3, 50, 60)

    assert game.game.red_balls == 3
    assert game.game.score_player_1 == 50
    assert game.game.score_player_2 == 60
    assert game.game.available_points == game.game.red_balls * 8 + 27


def test_set_starting_scores_invalid_red_balls():
    """Test invalid number of red balls."""
    root = create_mock_root()
    game = SnookerGUI(root)

    # Mock the StartingScoresDialog to simulate invalid input
    with patch('snooker_gui.StartingScoresDialog') as mock_dialog:
        # Mock the show method to return invalid input (20 red balls)
        mock_dialog.return_value.show.return_value = (20, 50, 60)

        # Mock messagebox.showerror to verify the error message
        with patch('tkinter.messagebox.showerror') as mock_showerror:
            # Call the set_starting_scores method
            game.set_starting_scores()

            # Verify that messagebox.showerror was called with the correct arguments
            mock_showerror.assert_called_once_with(
                "Invalid Input", "Number of red balls must be between 0 and 15."
            )


def test_set_starting_scores_non_numeric_input():
    """Test non-numeric input."""
    root = create_mock_root()
    game = SnookerGUI(root)

    with patch('builtins.input', side_effect=["abc", "3", "50", "60"]):
        game.game.set_starting_scores(3, 50, 60)

    assert game.game.red_balls == 3
    assert game.game.score_player_1 == 50
    assert game.game.score_player_2 == 60
    assert game.game.available_points == game.game.red_balls * 8 + 27


def test_get_shot_value_quit():
    """Test quitting the game using 'q'."""
    root = create_mock_root()
    game = SnookerGUI(root)
    with patch.object(game.root, 'quit') as mock_quit:
        game.entry_shot.get = MagicMock(return_value="q")
        game.submit_shot()
        mock_quit.assert_called_once()


def test_get_shot_value_invalid():
    """Test entering an invalid shot value."""
    root = create_mock_root()
    game = SnookerGUI(root)

    # Mock the entry widget to simulate invalid input
    with patch.object(game.entry_shot, 'get', return_value="8"):
        # Mock messagebox.showerror to verify the error message
        with patch('tkinter.messagebox.showerror') as mock_showerror:
            # Call the submit_shot method
            game.submit_shot()

            # Verify that messagebox.showerror was called with the correct arguments
            mock_showerror.assert_called_once_with(
                "Invalid Input", "Only numbers between 0 and 7 are valid!"
            )


def test_get_shot_value_non_numeric():
    """Test entering a non-numeric shot value."""
    root = create_mock_root()
    game = SnookerGUI(root)

    # Mock the entry widget to simulate non-numeric input
    with patch.object(game.entry_shot, 'get', return_value="abc"):
        # Mock messagebox.showerror to verify the error message
        with patch('tkinter.messagebox.showerror') as mock_showerror:
            # Call the submit_shot method
            game.submit_shot()

            # Verify that messagebox.showerror was called with the correct arguments
            mock_showerror.assert_called_once_with(
                "Invalid Input", "Only numbers between 0 and 7 are valid!"
            )


def test_handle_red_ball():
    """Test handling a red ball."""
    root = create_mock_root()
    game = SnookerGUI(root)
    game.game.handle_red_ball(1)
    assert game.game.score_player_1 == 1
    assert game.game.red_balls == 14
    assert game.game.red_needed_next is False


def test_handle_red_ball_reduces_available_points():
    """Test that handle_red_ball reduces available points correctly."""
    root = create_mock_root()
    game = SnookerGUI(root)
    game.game.handle_red_ball(1)
    assert game.game.available_points == 146


def test_handle_color_ball():
    """Test handling a colored ball."""
    root = create_mock_root()
    game = SnookerGUI(root)
    game.game.red_needed_next = False
    game.game.handle_color_ball(2)
    assert game.game.score_player_1 == 2
    assert game.game.red_needed_next is True


def test_handle_color_ball_reduces_available_points():
    """Test that handle_color_ball reduces available points correctly."""
    root = create_mock_root()
    game = SnookerGUI(root)
    game.game.red_balls = 13
    game.game.available_points = 138  # 147 - 1 - 7 - 1
    game.game.red_needed_next = False
    game.game.handle_color_ball(3)  # green ball
    assert game.game.available_points == 131  # 138 - 7


def test_handle_miss():
    """Test handling a missed shot."""
    root = create_mock_root()
    game = SnookerGUI(root)
    game.game.handle_miss()
    assert game.game.red_needed_next is True
    assert game.game.player_1_turn is False


def test_update_score():
    """Test updating player scores."""
    root = create_mock_root()
    game = SnookerGUI(root)
    game.game.update_score(5)
    assert game.game.score_player_1 == 5
    game.game.switch_players()
    game.game.update_score(3)
    assert game.game.score_player_2 == 3


def test_switch_players():
    """Test switching turns between players."""
    root = create_mock_root()
    game = SnookerGUI(root)
    assert game.game.player_1_turn is True
    game.game.switch_players()
    assert game.game.player_1_turn is False
    game.game.switch_players()
    assert game.game.player_1_turn is True


import pytest
from snooker_game import SnookerGame


def test_calculate_possible_scores_player_1_turn_red_needed_next():
    """Test possible scores when it's Player 1's turn and a red ball is needed next."""
    game = SnookerGame()
    game.player_1_turn = True
    game.red_needed_next = True
    game.score_player_1 = 10
    game.score_player_2 = 20
    game.available_points = 100

    game.calculate_possible_scores()

    assert game.possible_score_player_1 == 110  # 10 + 100
    assert game.possible_score_player_2 == 120  # 20 + 100


def test_calculate_possible_scores_player_1_turn_colored_needed_next():
    """Test possible scores when it's Player 1's turn and a colored ball is needed next."""
    game = SnookerGame()
    game.player_1_turn = True
    game.red_needed_next = False
    game.score_player_1 = 10
    game.score_player_2 = 20
    game.available_points = 100

    game.calculate_possible_scores()

    assert game.possible_score_player_1 == 110  # 10 + 100
    assert game.possible_score_player_2 == 113  # 20 + 100 - 7


def test_calculate_possible_scores_player_2_turn_red_needed_next():
    """Test possible scores when it's Player 2's turn and a red ball is needed next."""
    game = SnookerGame()
    game.player_1_turn = False
    game.red_needed_next = True
    game.score_player_1 = 10
    game.score_player_2 = 20
    game.available_points = 100

    game.calculate_possible_scores()

    assert game.possible_score_player_1 == 110  # 10 + 100
    assert game.possible_score_player_2 == 120  # 20 + 100


def test_calculate_possible_scores_player_2_turn_colored_needed_next():
    """Test possible scores when it's Player 2's turn and a colored ball is needed next."""
    game = SnookerGame()
    game.player_1_turn = False
    game.red_needed_next = False
    game.score_player_1 = 10
    game.score_player_2 = 20
    game.available_points = 100

    game.calculate_possible_scores()

    assert game.possible_score_player_1 == 103  # 10 + 100 - 7
    assert game.possible_score_player_2 == 120  # 20 + 100


def test_calculate_possible_scores_edge_case_zero_available_points():
    """Test possible scores when available_points is 0."""
    game = SnookerGame()
    game.player_1_turn = True
    game.red_needed_next = False
    game.score_player_1 = 10
    game.score_player_2 = 20
    game.available_points = 0

    game.calculate_possible_scores()

    assert game.possible_score_player_1 == 10  # 10 + 0
    assert game.possible_score_player_2 == 13  # 20 + 0 - 7


def test_calculate_possible_scores_edge_case_negative_scores():
    """Test possible scores when scores are negative."""
    game = SnookerGame()
    game.player_1_turn = False
    game.red_needed_next = False
    game.score_player_1 = -10
    game.score_player_2 = -20
    game.available_points = 100

    game.calculate_possible_scores()

    assert game.possible_score_player_1 == 83  # -10 + 100 - 7
    assert game.possible_score_player_2 == 80  # -20 + 100


def test_add_penalty():
    root = create_mock_root()
    game = SnookerGUI(root)

    with patch('builtins.input', side_effect=['4', 'n']):
        game.game.player_1_turn = True
        game.game.add_penalty(4)
        assert game.game.score_player_2 == 4
        assert game.game.player_1_turn is False

    # Input out of range
    with patch('builtins.input', side_effect=['8', '4', 'n']):
        game.game.player_1_turn = False
        game.game.add_penalty(4)
        assert game.game.score_player_1 == 4
        assert game.game.player_1_turn is True

    # Non-numeric input
    with patch('builtins.input', side_effect=['a', '3', 'n']):
        game.game.player_1_turn = True
        game.game.add_penalty(3)
        assert game.game.score_player_2 == 7
        assert game.game.player_1_turn is False

    # Respot balls with 'y'
    with patch('builtins.input', side_effect=['3', 'y']):
        game.game.player_1_turn = False
        game.game.add_penalty(3)
        assert game.game.score_player_1 == 7
        assert game.game.player_1_turn is False

    # Respot balls with 'n'
    with patch('builtins.input', side_effect=['3', 'n']):
        game.game.player_1_turn = True
        game.game.add_penalty(3)
        assert game.game.score_player_2 == 10
        assert game.game.red_needed_next is True


def test_red_balls_phase():
    """Test the red balls phase."""
    root = create_mock_root()
    game = SnookerGUI(root)
    with patch("builtins.input", side_effect=["1", "2"] * 14 + ["1", "5"]):
        # (14 * 1) + (14 * 2) + 1 + 5 (last blue)
        with patch("builtins.print") as mocked_print:
            game.game.red_balls_phase(1)
            assert game.game.red_balls == 0
            assert game.game.score_player_1 == 48
            assert game.game.available_points == 29
            # 147 - (15) - (98) - 5 (last blue ball)
            mocked_print.assert_any_call(
                "\nNo more red balls left! "
                "Pot a colored ball to start the endgame."
            )


def test_colored_balls_phase():
    """Test the colored balls phase."""
    root = create_mock_root()
    game = SnookerGUI(root)
    game.game.red_balls = 0
    game.game.available_points = 27
    game.game.score_player_1 = 0
    game.game.score_player_2 = 0
    game.game.yellow_ball = 2

    with patch("builtins.input", side_effect=["2", "3", "4", "5", "6", "7"]):
        with patch("builtins.print") as mocked_print:
            game.game.colored_balls_phase(2)
            assert game.game.score_player_1 == 27
            assert game.game.score_player_2 == 0
            assert game.game.available_points == 0
            assert game.game.yellow_ball == 8
            mocked_print.assert_any_call("\nEntering colored balls endgame!\n")
            mocked_print.assert_any_call("Available for endgame: 27")
            mocked_print.assert_any_call("Next ball to pot: yellow (2 points)")
            mocked_print.assert_any_call("Next ball to pot: green (3 points)")
            mocked_print.assert_any_call("Next ball to pot: brown (4 points)")
            mocked_print.assert_any_call("Next ball to pot: blue (5 points)")
            mocked_print.assert_any_call("Next ball to pot: pink (6 points)")
            mocked_print.assert_any_call("Next ball to pot: black (7 points)")
            mocked_print.assert_any_call("\nNo more balls to play!")


if __name__ == "__main__":
    pytest.main()
