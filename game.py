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
    def __init__(self, value:int = 0, matched:bool = False):
        self.content = value
        self.matched = matched
class Column():
    def __init__(self, column:int = 1, contents:[int] = [1,1,1]):
        self.contents = contents
        self.column = column
        self.fallen = 1#the distance this column has fallen
    def rotate(self) -> None:
        """Rotates the column by one"""
        self.contents = self.contents[1:] + [self.contents[0]]
class Game:
    """A class represeting an instance of the game"""
    
    def __init__(self, board:[[ int]]):
        self.state = Game_State.READY  
        self.board = [[Space(element) for element in row] for row in board]
        self.column = None
        
    def make_column(self, content:[int], column) -> None:
        """Makes a new column with the given contents in the given column of the board."""
        if(self.state != Game_State.READY):
            raise ArgumentException("Not ready for a column")
        if(len(content) != 3):
            raise ArgumentException("Wrong length")
        self.column = Column(column, content)
        self.state = Game_State.FALLING
    
    def move_col_right(self) -> None:
        """Moves the column one to the right, returning if not possible because of the board, and raising an ArgumentException if there is no column"""
        if(self.state != Game_State.FALLING):
            raise ArgumentException("No column to shift right")
        if(self.column.column == len(self.board[0])-1):
            return
        if(self.column.fallen == 1):
            if(self.board[0][self.column.column + 1].content != 0):
                return
            else:
                self.column.column = self.column.column + 1
        elif(self.column.fallen == 2):
            if(self.board[0][self.column.column + 1].content != 0 or self.board[1][self.column.column + 1].content != 0):
                return
            else:
                self.column.column = self.column.column + 1
        else:
            for i in range(3):
                if(self.board[self.column.fallen - 3 + i][self.column.column + 1].content != 0):
                    return
            self.column.column = self.column.column + 1
    def move_col_left(self) -> None:
        """Moves the column one to the left, returning if not possible because of the board, and raising an ArgumentException if there is no column"""
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
            for i in range(3):
                if(self.board[self.column.fallen - 3 + i][self.column.column - 1].content != 0):
                    return
            self.column.column = self.column.column + 1
    
    def tick(self) -> None:
        """Acts as a tick in the game, calling the approprate method based on state"""
        if(self.state == Game_State.READY):
            pass
        elif(self.state == Game_State.FALLING):
            self.fall()
        elif(self.state == Game_State.LANDED):
            self.landed()
        elif(self.state == Game_State.MATCHED):
            self.matched()

    def rotate(self) -> None:
        """Rotates the faling column"""
        self.column.rotate()
    def fall(self) -> None:
        """What to do if the current state is FALLING. tries to fall the column one, and lands if it's not possible"""
        if((self.column.fallen < len(self.board)) and ((self.board[self.column.fallen][self.column.column].content == 0) or (self.board[self.column.fallen][self.column.column].content == None))):
            self.column.fallen = self.column.fallen + 1
        else:
            if(self.column.fallen < 3):
                self.state = Game_State.OVER
            else:
                self.state = Game_State.LANDED
    def landed(self) -> None:
        """What to do if the current state is LANDED. Takes the spaces in the column and commits them to the board"""
        changed_spaces = []
        for i in range(3):
            self.board[self.column.fallen-3 + i][self.column.column] = Space(self.column.contents[i])
            changed_spaces.append((self.column.fallen-3 + i, self.column.column))
        #matching code
        for coord in changed_spaces:#stored in row, col format
            self.check_matches(coord)


        

        matches = False
        for space in changed_spaces:
            matches = self.check_matches(space) or matches # if placed the other way, it would short-circuit and not check matches properly
        
        
        self.column = None
        if(matches):
            self.state = Game_State.MATCHED
        else:
            self.state = Game_State.READY
    def matched(self):
        """What to do if the current state is MATCHED. removes matches and has pieces fall"""
        removed_gems = []
        for row in range(len(self.board)):#note that the iteration is from top to bottom. This is very important for later
            for col in range(len(self.board[0])):
                if(self.board[row][col].matched):
                    removed_gems.append((row, col))
                    self.board[row][col].content = 0
                    self.board[row][col].matched = False
                    
        for row, col in removed_gems:
            for i in range(row, 0, -1):
                self.board[i][col].content = self.board[i-1][col].content # replaces the content of every box at or above the matched spot with the one above it
                self.board[i-1][col].content = 0
                
        self.state = Game_State.READY
                    
        
    DIRECTIONS = [(1,1), (1,0), (1,-1), (0,1)] # defines the four dirctions to check in. Then check in the opposite direction. R,C format
    def check_matches(self, coord: ()) -> bool:
        """Checks the coordinate for any match in any direction. coords expected in row, col format"""
        gem_to_search = self.board[coord[0]][coord[1]].content
        returned = False
        for direction in Game.DIRECTIONS:
            matched_coords = []
            i = 0
            row = coord[0]
            col = coord[1]
            while(row < len(self.board) and row >= 0 and col >= 0 and col < len(self.board[0]) and self.board[row][col].content == gem_to_search):
                matched_coords.append((row, col))
                i = i+1
                row = coord[0] + i*direction[0]
                col = coord[1] + i*direction[1]
            
            
            i = 1# this ignores the spot itself the second time around
            row = coord[0] - i*direction[0]
            col = coord[1] - i*direction[1]
            while(row < len(self.board) and row >= 0 and col >= 0 and col < len(self.board[0]) and self.board[row][col].content == gem_to_search):
                matched_coords.append((row, col))
                i = i+1
                row = coord[0] - i*direction[0]
                col = coord[1] - i*direction[1]
            
            if(len(matched_coords) > 2):
                returned = True
                for row, col in matched_coords:
                    self.board[row][col].matched = True
                
        return returned
def make_game(rows:int, cols:int) -> Game:
    """A factory function to make a Game"""
    return Game([[0 for y in range(cols)] for x in range(rows)])#passes an empty board to the constructor
