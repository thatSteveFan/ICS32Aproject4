"""This defines the game of columns"""
import enum



class Game_State(enum.Enum):
    """An enum for the state of the game"""
    READY = enum.auto()
    FALLING = enum.auto()
    LANDED = enum.auto()#landed but not frozen
    FROZEN = enum.auto()#frozen but not cleared
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
        self.contents.rotate(1)
class Game:
    """A class represeting an instance of the game"""
    
    def __init__(self, board:[[ int]]):
        self.state = Game_State.READY  
        self.board = [[Space(element) for element in row] for row in board]
        self.column = None
        
    def make_column(self, column:[int]) -> None:
        if(self.state != Game_State.READY):
            raise ArgumentException("Not ready for a column")
        if(len(column) != 3):
            raise ArgumentException("Wrong length")
        self.column = Column(column)
    
    def move_col_right(self) -> None:
        if(self.state != Game_State.FALLING):
            raise ArgumentException("No column to shift right")
        if(self.column.column == len(board)):
            return
        if(self.column.fallen == 1):
            if(board[0][column.column + 1].content != None):
                return
            else:
                self.column.column = self.column.column + 1
        elif(self.column.fallen == 2):
            if(board[0][column.column + 1].content != None or board[1][column.column + 1].content != None):
                return
            else:
                self.column.column = self.column.column + 1
        else:
            pass
    def move_col_left(self) -> None:
        if(self.state != Game_State.FALLING):
            raise ArgumentException("No column to shift left")
        if(self.column.column == len(board)):
            return
        if(self.column.fallen == 1):
            if(board[0][column.column - 1].content != None):
                return
            else:
                self.column.column = self.column.column + 1
        elif(self.column.fallen == 2):
            if(board[0][column.column - 1].content != None or board[1][column.column - 1].content != None):
                return
            else:
                self.column.column = self.column.column + 1
        else:
            pass
    
    def tick(self):
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
            
    def fall(self):
        pass
    def landed(self):
        pass
    def frozen(self):
        pass
    def matched(self):
        pass
    
def make_game(rows:int, cols:int) -> Game:
    return Game([[0 for y in range(cols)] for x in range(rows)])#passes an empty board to the constructor