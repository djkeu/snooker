class SnookerGame:
    def __init__(self):
        """Initialize the game scores state."""
        self.red_balls = 15
        self.available_points = (self.red_balls * 8) + 27
        self.red_needed_next = True
        self.player_1_turn = True
        self.score_player_1 = 0
        self.score_player_2 = 0
        self.possible_score_player_1 = self.available_points
        self.possible_score_player_2 = self.available_points
        self.yellow_ball = 2
        self.colored_balls = {
            2: "yellow",
            3: "green",
            4: "brown",
            5: "blue",
            6: "pink",
            7: "black",
        }
        self.prompt = self.initialize_prompt()

    # Ball handling
    def initialize_prompt(self):
        """Initialize the prompt message."""
        prompt = "What's the value of the shot: "
        return prompt

    def validate_shot(self, shot):
        """Validate the shot value."""
        try:
            shot = int(shot)
            if 0 <= shot <= 7:
                return True
            else:
                raise ValueError("Only numbers between 0 and 7 are valid!")
        except ValueError:
            raise ValueError("Only numbers between 0 and 7 are valid!")

    def handle_red_ball(self, shot):
        """Handle logic for when a red ball is hit."""
        if self.red_needed_next:
            self.available_points -= 1  # Decrease by 1 for the red ball
            self.red_balls -= 1
            self.red_needed_next = False
            self.update_score(shot)
        else:
            # Player failed to pot a colored ball after a red ball
            self.available_points -= 8  # Decrease by 8 (1 for red + 7 for colored)
            self.switch_players()
            self.red_needed_next = True

    def handle_color_ball(self, shot):
        """Handle logic for when a color ball is hit."""
        if self.red_needed_next:
            print("\nYou need to hit a red ball first!")
            self.switch_players()
            self.red_needed_next = True
        else:
            self.available_points -= 7
            self.red_needed_next = True
            self.update_score(shot)

    def handle_miss(self):
        """Handle logic for when a shot is missed."""
        if not self.red_needed_next:
            # Player was supposed to pot a colored ball
            self.available_points -= 7  # Decrease by 7 for the missed colored ball
        else:
            # Player was supposed to pot a red ball
            self.available_points -= 1  # Decrease by 1 for the missed red ball
        self.red_needed_next = True
        self.switch_players()

    def switch_players(self):
        """Switch turns between players."""
        self.player_1_turn = not self.player_1_turn

    # Score handling
    def set_starting_scores(self, red_balls, score_1, score_2):
        """Set starting scores and the number of red balls left."""
        self.available_points = 147

        if score_1 < 0 or score_2 < 0:
            raise ValueError("Scores cannot be negative")
        elif red_balls < 0 or red_balls > 15:
            raise ValueError("Number of red balls must be between 0 and 15.")
        elif score_1 + score_2 + (red_balls * 8) > self.available_points:
            raise ValueError("Total score must be less than 147")

        self.score_player_1 = score_1
        self.score_player_2 = score_2
        self.red_balls = red_balls
        self.available_points = (self.red_balls * 8) + 27
        self.calculate_possible_scores()

    def update_score(self, shot):
        """Update the current player's score."""
        if self.player_1_turn:
            self.score_player_1 += shot
        else:
            self.score_player_2 += shot

    def calculate_possible_scores(self):
        """Current score plus remaining available points."""
        if self.player_1_turn:
            self.possible_score_player_1 = self.score_player_1 + self.available_points
            self.possible_score_player_2 = self.score_player_2 + self.available_points
        else:
            self.possible_score_player_1 = self.score_player_1 + self.available_points
            self.possible_score_player_2 = self.score_player_2 + self.available_points

    def display_game_state(self):
        """Display the current state of the game in the desired format."""
        self.calculate_possible_scores()

        print(f"\nPlayer 1: score {self.score_player_1}, "
              f"possible score {self.possible_score_player_1}")
        print(f"Player 2: score {self.score_player_2}, "
              f"possible score {self.possible_score_player_2}")

        if self.available_points > 27:
            print(f"{self.red_balls} red balls left")
            self.display_next_ball()

    def display_next_ball(self):
        """Display which ball the current player must pot next."""
        if self.player_1_turn:
            player = "Player 1"
        else:
            player = "Player 2"

        if self.red_needed_next:
            ball = "red ball"
        else:
            ball = "colored ball"

        print(f"{player} must pot a {ball}")

    def add_penalty(self, penalty):
        """Add points to the other player's score."""
        if not (0 <= penalty <= 7):
            raise ValueError("Penalty must be between 0 and 7")

        if self.player_1_turn:
            self.score_player_2 += penalty
        else:
            self.score_player_1 += penalty

        self.switch_players()

    def respot_balls(self, respot):
        """Respot the balls after a foul."""
        if respot not in ['y', 'n']:
            raise ValueError("Invalid input. Please enter 'y' or 'n'.")

        if respot == 'y':
            self.switch_players()
        elif self.red_balls > 0:
            self.red_needed_next = True

    # Game phases
    def red_balls_phase(self, shot):
        """Take turns playing reds and colors."""
        if self.red_balls > 0:
            if shot == 0:
                self.handle_miss()
            elif shot == 1:
                self.handle_red_ball(shot)
            else:
                self.handle_color_ball(shot)

    def handle_last_colored_ball(self, shot):
        """Handle last ball before colored balls phase."""
        if shot < 2 or shot > 7:
            raise ValueError("You must pot a colored ball!")
        else:
            self.available_points -= shot
            self.update_score(shot)

    def colored_balls_phase(self, shot):
        """Simulate colored balls phase."""
        if shot != self.yellow_ball:
            raise ValueError("Wrong ball!")
        else:
            self.available_points -= self.yellow_ball
            self.update_score(shot)
            self.yellow_ball += 1

    def display_winner(self):
        """Display the winner of the game."""
        if self.score_player_1 > self.score_player_2:
            return "Player 1 wins!"
        elif self.score_player_1 < self.score_player_2:
            return "Player 2 wins!"
        else:
            return "It's a tie!"
