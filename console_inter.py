"""defines the interface between the game and the console"""
import game as game_py
import re

def main():
    """The main method containing the main loop."""
    rows = int(input())
    cols = int(input())
    
    start = input()
    if(start == "EMPTY"):
        game = game_py.make_game(rows, cols)
    elif(start == "CONTENTS"):
        requested_array = []
        for i in range(rows):
            requested_array.append(list(input()))
        translated_array = [[(ord(char) - 64) for char in row] for row in requested_array]
        game = game_py.Game(translated_array)
    
    while(1):
        print(game_to_str(game))
        if(game.state == game_py.Game_State.OVER):
            print("GAME OVER")
            break
        input_str = input()
        if(input_str == ""):
            game.tick()
        elif(input_str == "<"):
            game.move_col_left()
        elif(input_str == ">"):
            game.move_col_right()
        elif(input_str == "Q"):
            break
        elif(input_str == "R"):
            game.rotate()
        elif(re.match(r"F \d [A-J] [A-J] [A-J]", input_str)):
            game.make_column([ord(input_str[4]) - 64,ord(input_str[6]) - 64,ord(input_str[8]) - 64], int(input_str[2]) - 1)
            
        
    
        
def game_to_str(game: game_py.Game) -> str:
    """Changes the internal integer representation of the board to an array of strings"""
    board_stringed = [(["|"] + [(space_to_str(space)) for space in row] + ["|"]) for row in game.board]
    board_stringed.append([" "] + ["---" for n in range(len(game.board[0]))]+ [" "])

    if(game.column != None):
        colstrs = col_to_strs(game.column, game.state)
        if(game.column.fallen == 1):
            board_stringed[0][game.column.column + 1] = colstrs[2]
        elif(game.column.fallen == 2):
            board_stringed[0][game.column.column + 1] = colstrs[1]
            board_stringed[1][game.column.column + 1] = colstrs[2]
        else:
            for i in range(3):
                board_stringed[i + game.column.fallen - 3][game.column.column + 1] = colstrs[i]
    
    return "\n".join(["".join(row) for row in board_stringed])
def space_to_str(space: game_py.Space) -> str:
    """Changes a space from the game into a string representation"""
    if(space.content == None or space.content == 0):
        return "   "
    else:
        if(space.matched):
            around = "*"
        else:
            around = " "
        return around + chr(space.content + 64) + around

STATE_TO_SURROUNDING_CHR = {game_py.Game_State.FALLING: ("[", "]"), game_py.Game_State.LANDED: ("|", "|"), game_py.Game_State.OVER: ("|", "|")}
def col_to_strs(col: game_py.Column, state: game_py.Game_State) -> [str]:
    """Turns the falling column into an array of strings"""
    return ["" + (STATE_TO_SURROUNDING_CHR[state][0] + chr(gem + 64) + STATE_TO_SURROUNDING_CHR[state][1]) for gem in col.contents]
