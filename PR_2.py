class Game:
    def __init__(self, title, genre):
        self.title = title
        self.genre = genre
        
    def start_game(self):
        print(f"Гра {self.title} в жанрі {self.genre} запустилась.")
    
class Multiplayer:
    def __init__(self, player_count):
        self.player_count = player_count
        
    def count_players(self):
        print(f"Кількість гравців у грі: {self.player_count}")

class OnlineGame(Game, Multiplayer):
    def __init__(self, title, genre, player_count, ranking):
        super().__init__(title, genre)
        Multiplayer.__init__(self, player_count)
        self.ranking = ranking
    
    def start_game(self):
        super().start_game()
        print(f"Гра {self.title} в жанрі {self.genre} розпочалась")
        
    def check_ranking(self):
        print(f"Рейтинг гравця: {self.ranking}")
            
if __name__ == "__main__":
    game1 = OnlineGame("World of Warcraft", "fantasy", 600, 23)
    game2 = OnlineGame("Grand Theft Auto V", "RPG", 20, 13)
    game3 = OnlineGame("MInecraft", "Sandbox", 50, 99)
    
game1.start_game()
game1.count_players()
game1.check_ranking()
print("---")
game2.start_game()
game2.count_players()
game2.check_ranking()
print("---")
game3.start_game()
game3.count_players()
game3.check_ranking()
