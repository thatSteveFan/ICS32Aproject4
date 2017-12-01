"""This defines the game of columns"""
import enum



class Game_State(enum.Enum):
    """An enum for the state of the game"""
    READY = enum.auto()
    FALLING = enum.auto()
    LANDED = enum.auto()#landed but not frozen
    MATCHED = enum.auto()
    OVER = enum.auto()
    
    
class Space():
    """a class representing a space in the game"""
    def __init__(self, value:int = None, matched:bool = False):
        self.content = value
        self.matched = matched
    
class Column():
    def __init__(self, column:int = 1, contents:[int] = [1,1,1]):
        self.contents = contents
        self.column = column
        self.fallen = 1#the distance this column has fallen
    def rotate(self) -> None:
        self.contents = self.contents[1:] + [self.contents[0]]
class Game:
    """A class represeting an instance of the game"""
    
    def __init__(self, board:[[ int]]):
        self.state = Game_State.READY  
        self.board = [[Space(element) for element in row] for row in board]
        self.column = None
        
    def make_column(self, content:[int], column) -> None:
        if(self.state != Game_State.READY):
            raise ArgumentException("Not ready for a column")
        if(len(content) != 3):
            raise ArgumentException("Wrong length")
        self.column = Column(column, content)
        self.state = Game_State.FALLING
    
    def move_col_right(self) -> None:
        print(self.column.column)
        if(self.state != Game_State.FALLING):
            raise ArgumentException("No column to shift right")
        if(self.column.column == len(self.board[0])-1):
            return
        if(self.column.fallen == 1):
            if(self.board[0][self.column.column + 1].content != 0):
                print("moving blocked")
                return
            else:
                self.column.column = self.column.column + 1
        elif(self.column.fallen == 2):
            if(self.board[0][self.column.column + 1].content != 0 or self.board[1][self.column.column + 1].content != 0):
                print("moving blocked")
                return
            else:
                self.column.column = self.column.column + 1
        else:
            pass
    def move_col_left(self) -> None:
        if(self.state != Game_State.FALLING):
            raise ArgumentException("No column to shift left")
        if(self.column.column == 0):
            return
        if(self.column.fallen == 1):
            if(self.board[0][self.column.column - 1].content != None):
                return
            else:
                self.column.column = self.column.column - 1
        elif(self.column.fallen == 2):
            if(self.board[0][self.column.column - 1].content != None or self.board[1][self.column.column - 1].content != None):
                return
            else:
                self.column.column = self.column.column - 1
        else:
            pass
    
    def tick(self) -> None:
        if(self.state == Game_State.READY):
            pass
        elif(self.state == Game_State.FALLING):
            self.fall()
        elif(self.state == Game_State.LANDED):
            self.landed()
        elif(self.state == Game_State.FROZEN):
            self.frozen()
        elif(self.state == Game_State.MATCHED):
            self.matched()

    def rotate(self) -> None:
        self.column.rotate()
    def fall(self) -> None:
        print("fallen: " + str(self.column.fallen))
        print(self.column.fallen < len(self.board))
        if((self.column.fallen < len(self.board)) and ((self.board[self.column.fallen][self.column.column].content == 0) or (self.board[self.column.fallen][self.column.column].content == None))):
            self.column.fallen = self.column.fallen + 1
        else:
            if(self.column.fallen < 3):
                self.state = Game_State.OVER
            else:
                self.state = Game_State.LANDED
    def landed(self) -> None:
        changed_spaces = []
        for i in range(3):
            self.board[self.column.fallen-3 + i][self.column.column] = Space(self.column.contents[1])
            changed_spaces.append((self.column.fallen-3 + i, self.column.column))
        #matching code
        for coord in changed_spaces:
            self.check_matches(coord)


        


        self.column = None
        if(matches):
            self.state = Game_State.MATCHED
        else:
            self.state = Game_State.READY
    def matched(self):
        pass


    def check_matches(self, coord: ()) -> None:
        pass
    
def make_game(rows:int, cols:int) -> Game:
    return Game([[0 for y in range(cols)] for x in range(rows)])#passes an empty board to the constructor
