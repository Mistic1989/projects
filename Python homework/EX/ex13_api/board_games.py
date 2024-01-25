"""Board games."""


import csv


class Statistics:
    """
    Class Statistics.

    Statistics is a required class for storing and retrieving the data.
    """

    def __init__(self, filename):
        """Initialize the Statistics class."""
        self.filename = filename
        self.data_list = []
        self.winners_results = {}
        self.losers_results = {}
        self.player_points = {}
        self.read_files()

    def read_files(self):
        """Read data from text file."""
        with open(self.filename, "r") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=";")
            for row in csv_reader:
                self.data_list.append(row)
        return self.data_list

    def get_player_names(self):
        """Return a list of player names (order is not important)."""
        all_players_list = []
        for items in self.data_list:
            split_players = items[1].split(",")
            for player in split_players:
                all_players_list.append(player)
        return list(set(all_players_list))

    def get_game_names(self):
        """Return a list of game names (order is not important)."""
        all_games_list = []
        for games in self.data_list:
            all_games_list.append(games[0])
        return list(set(all_games_list))

    def get_games_played_amount(self):
        """Return an integer, which represents the total amount of games played."""
        return len(self.data_list)

    def get_games_played_of_type(self, result_type: str):
        """Get games played by type (points, places or winner)."""
        games_played_of_type_list = []
        for items in self.data_list:
            if result_type in items:
                games_played_of_type_list.append(items[0])
        return len(games_played_of_type_list)

    def get_games_amount_played_by(self, player_name: str):
        """Return an integer, which represents the amount of games played by player_name."""
        result = 0
        for items in self.data_list:
            if player_name in items[1].split(","):
                result += 1
        return result

    def get_favourite_game(self, player_name: str):
        """Return a string representing a game name, which has been played most by player_name."""
        result = {}
        for items in self.data_list:
            if player_name in items[1].split(","):
                result.setdefault(items[0], []).append(player_name)
        count = 0
        favourite = ""
        for key, value in result.items():
            if len(value) > count:
                favourite = key
                count = len(value)
        return favourite

    def return_winner_by_points(self, row) -> str:
        """Sort players by points and return winner."""
        split_players = row[1].split(",")
        split_points = row[3].split(",")
        all_results = {}
        for index, player in enumerate(split_players):
            all_results.setdefault(player, int(split_points[index]))
        self.player_points = all_results
        highest_score = max(all_results.values())
        for key, value in all_results.items():
            if value == highest_score:
                return key

    def get_amount_of_games_won(self, player_name: str):
        """Return an integer, which represents the amount of games won by player_name."""
        count = 0
        for row in self.data_list:
            if player_name in row[1]:
                if row[2] == "points":
                    if player_name == self.return_winner_by_points(row):
                        count += 1
                if row[2] == "places":
                    places = row[3].split(",")
                    if player_name == places[0]:
                        count += 1
                if row[2] == "winner":
                    if row[3] == player_name:
                        count += 1
        return count

    def get_games_played_of_name(self, game_name: str):
        """Return an integer, which represents how many games of name game_name have been played."""
        games_played = []
        for items in self.data_list:
            if game_name == items[0]:
                games_played.append(items[0])
        return len(games_played)

    def get_amount_of_players_most_often_played_with(self, game_name: str):
        """Return an integer, which represents the most common amount of players game_name is usually played with."""
        amount_of_people = []
        for items in self.data_list:
            if game_name == items[0]:
                amount_of_people.append(len(items[1].split(",")))
        most_common = {}
        unique_sorted_list = list(set(amount_of_people))
        for persons_count in unique_sorted_list:
            most_common.setdefault(persons_count, amount_of_people.count(persons_count))
        max_value = max(most_common.values())
        for key, value in most_common.items():
            if value == max_value:
                return key

    def get_player_with_most_amount_of_wins(self, game_name: str):
        """Return a string, which represents the player name, who has the most amount of wins in game_name."""
        new = {}
        for row in self.data_list:
            if game_name == row[0]:
                if row[2] == "points":
                    new.setdefault(self.return_winner_by_points(row), []).append(1)
                if row[2] == "places":
                    places = row[3].split(",")
                    new.setdefault(places[0], []).append(1)
                if row[2] == "winner":
                    new.setdefault(row[3], []).append(1)
        self.winners_results = new
        most_wins = max(new.values())
        for person_name, result in new.items():
            if result == most_wins:
                return person_name

    def get_most_frequent_winner(self, game_name: str):
        """Return a string, which represents the player name, who has the highest win rate in game_name."""
        self.get_player_with_most_amount_of_wins(game_name)
        new_dict = {}
        for key, value in self.winners_results.items():
            wins_amount = sum(list(value))
            played_games_amount = 0
            for game in self.data_list:
                if key in game[1].split(",") and game_name == game[0]:
                    played_games_amount += 1
            calculate_percentage = wins_amount / played_games_amount * 100
            new_dict.setdefault(key, calculate_percentage)
        highest_percentage = max(new_dict.values())
        for person_name, result in new_dict.items():
            if result == highest_percentage:
                return person_name

    def get_losers_by_points_and_places(self, game_name):
        """Create a dict of losers (winning types are points and places)."""
        losers = {}
        for row in self.data_list:
            if game_name == row[0]:
                if row[2] == "points":
                    self.return_winner_by_points(row)
                    min_points = min(self.player_points.values())
                    for key, value in self.player_points.items():
                        if value == min_points:
                            losers.setdefault(key, []).append("lost one game")
                if row[2] == "places":
                    places = row[3].split(",")
                    losers.setdefault(places[-1], []).append("lost one game")
        return losers

    def get_player_with_most_amount_of_losses(self, game_name: str):
        """Return a string, which represents the player name, who has the most amount of losses in game_name."""
        losers = self.get_losers_by_points_and_places(game_name)
        self.losers_results = losers
        most_losings = 0
        for losings_amount in list(losers.values()):
            if len(losings_amount) >= most_losings:
                most_losings = len(losings_amount)
        for key, value in losers.items():
            if len(value) == most_losings:
                return key

    def get_most_frequent_loser(self, game_name: str):
        """Return a string, which represents the player name, who has the highest lose rate in game_name."""
        self.get_player_with_most_amount_of_losses(game_name)
        all_lost_players = {}
        for key, value in self.losers_results.items():
            loses_amount = len(value)
            played_games_amount = 0
            for game in self.data_list:
                if key in game[1].split(",") and game_name == game[0]:
                    played_games_amount += 1
            calculate_percentage = loses_amount / played_games_amount * 100
            all_lost_players.setdefault(key, calculate_percentage)
        highest_percentage = max(all_lost_players.values())
        for person_name, result in all_lost_players.items():
            if result == highest_percentage:
                return person_name

    def get_record_holder(self, game_name: str):
        """Return player who has gained the most amount of points in game_name in a single session."""
        winner = ""
        max_points = 0
        for row in self.data_list:
            if row[2] == "points" and row[0] == game_name:
                split_players = row[1].split(",")
                split_points = row[3].split(",")
                player_index_with_max_points = [split_points.index(x) for x in split_points if x == max(split_points)][0]
                if int(split_points[player_index_with_max_points]) > int(max_points):
                    max_points = split_points[player_index_with_max_points]
                    winner = split_players[player_index_with_max_points]
        return winner


class Controller:
    """Class Controller."""

    def __init__(self, statistics: Statistics):
        """Initialize the Controller class."""
        self.statistics = statistics

    def get_players_info(self, path: str):
        """Get players info."""
        if path == "/players":
            return self.statistics.get_player_names()
        if path[0:7] == "/player" and path != "/players":
            path_split = path.split("/")
            if path_split[3] == "amount":
                return self.statistics.get_games_amount_played_by(path_split[2])
            if path_split[3] == "favourite":
                return self.statistics.get_favourite_game(path_split[2])
            if path_split[3] == "won":
                return self.statistics.get_amount_of_games_won(path_split[2])

    def get_games_info(self, path: str):
        """Get games info."""
        if path == "/games":
            return self.statistics.get_game_names()
        if path[0:5] == "/game" and path != "/games":
            path_split = path.split("/")
            if path_split[3] == "amount":
                return self.statistics.get_games_played_of_name(path_split[2])
            if path_split[3] == "player-amount":
                return self.statistics.get_amount_of_players_most_often_played_with(path_split[2])
            if path_split[3] == "most-wins":
                return self.statistics.get_player_with_most_amount_of_wins(path_split[2])
            if path_split[3] == "most-frequent-winner":
                return self.statistics.get_most_frequent_winner(path_split[2])
            if path_split[3] == "most-losses":
                return self.statistics.get_player_with_most_amount_of_losses(path_split[2])
            if path_split[3] == "most-frequent-loser":
                return self.statistics.get_most_frequent_loser(path_split[2])
            if path_split[3] == "record-holder":
                return self.statistics.get_record_holder(path_split[2])

    def get(self, path: str):
        """
        Get data through Statistic's class methods.

        Path is a string with a specific format, which describes the type of data requested.
        """
        if path[0:7] == "/player" or path == "/players":
            return self.get_players_info(path)
        if path == "/games" or path[0:5] == "/game":
            return self.get_games_info(path)
        if path[0:6] == "/total":
            if path == "/total":
                return self.statistics.get_games_played_amount()
            if len(path) > 6:
                return self.statistics.get_games_played_of_type(path[7:])


if __name__ == '__main__':
    uus = Statistics("data.txt")
    # print(uus.data_list)
    # print(uus.get_player_names())
    # print(uus.get_game_names())
    # print(uus.get_games_played_amount())
    # print(uus.get_games_played_of_type("points"))
    # print(uus.get_games_amount_played_by("kristjan"))
    # print(uus.get_favourite_game("joosep"))
    # print(uus.get_amount_of_games_won("joosep"))
    # print(uus.get_games_played_of_name("terraforming mars"))
    # print(uus.get_amount_of_players_most_often_played_with("terraforming mars"))
    # print(uus.get_player_with_most_amount_of_wins("terraforming mars"))
    print(uus.get_most_frequent_winner("chess"))
    # print(uus.get_player_with_most_amount_of_losses("chess"))
    print(uus.get_most_frequent_loser("chess"))
    print(uus.get_record_holder("chess"))
    controller = Controller(uus)
    print(controller.get("/game/teretere/amount"))
