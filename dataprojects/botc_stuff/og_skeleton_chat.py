import random

class Player:
    def __init__(self, name, alignment):
        self.name = name
        self.alignment = alignment  # "good" or "evil"
        self.alive = True

    def __repr__(self):
        status = "alive" if self.alive else "dead"
        return f"{self.name} ({self.alignment}, {status})"


class GameState:
    def __init__(self, players):
        self.players = players
        self.day = 1
        self.phase = "night"

    def alive_players(self):
        return [p for p in self.players if p.alive]

    def check_win(self):
        good = [p for p in self.alive_players() if p.alignment == "good"]
        evil = [p for p in self.alive_players() if p.alignment == "evil"]

        if not evil:
            return "Good wins!"
        if len(evil) >= len(good):
            return "Evil wins!"
        return None


def create_game(num_players=5):
    players = []
    evil_index = random.randint(0, num_players - 1)

    for i in range(num_players):
        alignment = "evil" if i == evil_index else "good"
        players.append(Player(f"Player {i+1}", alignment))

    return GameState(players)


def night_phase(game):
    print("Night phase")

    evil_players = [p for p in game.alive_players() if p.alignment == "evil"]
    targets = [p for p in game.alive_players() if p.alignment == "good"]

    if evil_players and targets:
        victim = random.choice(targets)
        victim.alive = False
        print(f"{victim.name} was killed during the night.")


def day_phase(game):
    print("Day phase")

    alive = game.alive_players()
    for p in alive:
        print(p)

    # Random voting (you will improve this later)
    votes = {}
    for voter in alive:
        target = random.choice([p for p in alive if p != voter])
        votes[target] = votes.get(target, 0) + 1

    # Execute player with most votes
    executed = max(votes, key=votes.get)
    executed.alive = False
    print(f"{executed.name} was executed by vote.")


def run_game():
    game = create_game()

    while True:
        night_phase(game)
        result = game.check_win()
        if result:
            print(result)
            break

        day_phase(game)
        result = game.check_win()
        if result:
            print(result)
            break

        game.day += 1


if __name__ == "__main__":
    run_game()
