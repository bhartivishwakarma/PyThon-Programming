import random

# ---------------- GAME BASE CLASS ----------------
class Game:
    def __init__(self, name):
        self.name = name

    def play(self, bet):
        pass

    def __repr__(self):
        return f"Game(name='{self.name}')"


# ---------------- GAME TYPES ----------------
class SlotMachine(Game):
    def __init__(self):
        super().__init__("Slot Machine")

    def play(self, bet):
        if random.choice([True, False]):
            return bet * 2
        else:
            return -bet


class DiceGame(Game):
    def __init__(self):
        super().__init__("Dice Game")

    def play(self, bet):
        roll = random.randint(1, 6)
        if roll >= 4:
            return bet
        else:
            return -bet


class CoinToss(Game):
    def __init__(self):
        super().__init__("Coin Toss")

    def play(self, bet):
        if random.choice(["heads", "tails"]) == "heads":
            return bet
        else:
            return -bet


class NumberGuess(Game):
    def __init__(self):
        super().__init__("Number Guess Game")

    def play(self, bet):
        secret = random.randint(1, 5)
        guess = random.randint(1, 5)
        if guess == secret:
            return bet * 3
        else:
            return -bet


class HighCard(Game):
    def __init__(self):
        super().__init__("High Card Game")

    def play(self, bet):
        if random.randint(1, 13) > random.randint(1, 13):
            return bet
        else:
            return -bet


class RockPaperScissors(Game):
    def __init__(self):
        super().__init__("Rock Paper Scissors")

    def play(self, bet):
        choices = ["rock", "paper", "scissors"]
        player = random.choice(choices)
        computer = random.choice(choices)

        if player == computer:
            return 0
        elif (
            (player == "rock" and computer == "scissors") or
            (player == "paper" and computer == "rock") or
            (player == "scissors" and computer == "paper")
        ):
            return bet
        else:
            return -bet


# ---------------- PLAYER ----------------
class Player:
    def __init__(self, name, money):
        self.name = name
        self.money = money

    def play_game(self, game, bet):
        if bet > self.money:
            return
        self.money += game.play(bet)

    def __repr__(self):
        return f"Player(name='{self.name}', money={self.money})"


# ---------------- CASINO ----------------
class Casino:
    def __init__(self):
        self.games = []

    def add_game(self, game):
        self.games.append(game)

    def __repr__(self):
        return f"Casino(games={self.games})"


# ---------------- RUN PROGRAM ----------------
casino = Casino()
casino.add_game(SlotMachine())
casino.add_game(DiceGame())
casino.add_game(CoinToss())
casino.add_game(NumberGuess())
casino.add_game(HighCard())
casino.add_game(RockPaperScissors())

player = Player("Bharti", 100)

print(casino)   # uses __repr__
print(player)   # uses __repr__

player.play_game(casino.games[0], 20)
player.play_game(casino.games[3], 10)

print(player)   # updated attributes
