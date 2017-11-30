"""defines the interface between the game and the console"""
import game as game_py


def main():
    rows = int(input())
    cols = int(input())
    
    game = game_py.make_game(rows, cols)
    while(1):
        input_str = input()
        
        
def game_to_str(game: game_py.Game)