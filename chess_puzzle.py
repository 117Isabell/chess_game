import random
import sys

def location2index(loc: str) -> tuple[int, int]:
    '''converts chess location to corresponding x and y coordinates'''
    first_coord = ord(loc[0].lower())-ord('a') + 1
    second_coord = int(loc[1])
    return (first_coord,second_coord)
    
	
def index2location(x: int, y: int) -> str:
    '''converts  pair of coordinates to corresponding location'''
    first_char = chr(ord('a') + x - 1)  
    second_char = str(y)               
    return first_char + second_char

class Piece:
    pos_x : int	
    pos_y : int
    side : bool #True for White and False for Black
    def __init__(self, pos_X : int, pos_Y : int, side_ : bool):
        '''sets initial values'''
        self.pos_x= pos_X
        self.pos_y = pos_Y
        self.side = side_


Board = tuple[int, list[Piece]]


def is_piece_at(pos_X : int, pos_Y : int, B: Board) -> bool:
    '''checks if there is piece at coordinates pox_X, pos_Y of board B''' 
    for piece in B[1]:
        if piece.pos_x == pos_X and piece.pos_y == pos_Y:
            return True
    return False

def piece_side(pos_X : int, pos_Y : int, B: Board) -> bool:
    ''' Returns the side (True for white, False for black) of the piece at the given coordinates on the board B.''' 
    for piece in B[1]:
        if (piece.pos_x ,piece.pos_y) == (pos_X, pos_Y):
            return piece.side        

def piece_at(pos_X : int, pos_Y : int, B: Board) -> Piece:
    '''
    returns the piece at coordinates pox_X, pos_Y of board B 
    assumes some piece at coordinates pox_X, pos_Y of board B is present
    '''
    for piece in B[1]:
        if piece.pos_x == pos_X and piece.pos_y == pos_Y:
            return piece
        
class Knight(Piece):
    def __init__(self, pos_X : int, pos_Y : int, side_ : bool):
        '''sets initial values by calling the constructor of Piece'''
        super().__init__(pos_X, pos_Y, side_)
	
    def can_reach(self, pos_X : int, pos_Y : int, B: Board) -> bool:
        '''
        checks if this Knight can move to coordinates pos_X, pos_Y
        on board B according to rule [Rule1] and [Rule3] (see section Intro)
        Hint: use is_piece_at
        '''
        size_of_board, pieces = B
        knight_moves = [
            (self.pos_x + 2, self.pos_y + 1),
            (self.pos_x + 2, self.pos_y - 1),
            (self.pos_x - 2, self.pos_y + 1),
            (self.pos_x - 2, self.pos_y - 1),
            (self.pos_x + 1, self.pos_y + 2),
            (self.pos_x + 1, self.pos_y - 2),
            (self.pos_x - 1, self.pos_y + 2),
            (self.pos_x - 1, self.pos_y - 2)
        ]
        if (pos_X, pos_Y) not in knight_moves:
            return False
        if is_piece_at(pos_X, pos_Y, B):
            return (pos_X, pos_Y) in knight_moves and self.side is not piece_side(pos_X, pos_Y, B)
        if pos_X >= size_of_board or pos_Y >= size_of_board or pos_X < 1 or pos_Y < 1 :
            return False
        return True

    def can_move_to(self, pos_X : int, pos_Y : int, B: Board) -> bool:
        '''
        checks if this Knight can move to coordinates pos_X, pos_Y
        on board B according to all chess rules
        
        Hints:
        - firstly, check [Rule1] and [Rule3] using can_reach
        - secondly, check if result of move is capture using is_piece_at
        - if yes, find the piece captured using piece_at
        - thirdly, construct new board resulting from move
        - finally, to check [Rule4], use is_check on new board

        Is there a piece?
        If that piece is an enemy, we need to remove it
        We need to move our piece,
        We have to check for check
        if there is a check
        * move our piece back
        * re-add the enemy piece
        '''
        if not self.can_reach(pos_X, pos_Y, B):
            return False
        old_pos_x = self.pos_x
        old_pos_y = self.pos_y
        self.pos_x = pos_X
        self.pos_y = pos_Y

        if is_check(self.side, B):
            self.pos_x = old_pos_x
            self.pos_y = old_pos_y
            return False

        self.pos_x = old_pos_x
        self.pos_y = old_pos_y
        return True
    def move_to(self, pos_X : int, pos_Y : int, B: Board) -> Board:
        '''
        returns new board resulting from move of this knight to coordinates pos_X, pos_Y on board B 
        assumes this move is valid according to chess rules
        '''
        # new_pieces = B[1][:]
        new_pieces = [piece for piece in new_pieces if not (piece.pos_x == pos_X and piece.pos_y == pos_Y)]
        new_pieces = [piece for piece in new_pieces if piece != self]
        self.pos_x = pos_X
        self.pos_y = pos_Y
        new_pieces.append(self)
        return (B[0], new_pieces)
    

class King(Piece):
    def __init__(self, pos_X : int, pos_Y : int, side_ : bool):
        '''sets initial values by calling the constructor of Piece'''
        super().__init__(pos_X, pos_Y, side_)
    def can_reach(self, pos_X : int, pos_Y : int, B: Board) -> bool:
        '''checks if this king can move to coordinates pos_X, pos_Y on board B according to rule [Rule2] and [Rule3]'''
        board_size = B[0]
        if pos_X < 0 or pos_X > board_size or pos_Y < 0 or pos_Y > board_size:
           return False
        rule2_x = abs(self.pos_x - pos_X) <= 1
        rule2_y = abs(self.pos_y - pos_Y) <= 1
# The king must move at least one square, but not more than one in any direction
        size_of_board, _ = B
        if pos_X > size_of_board or pos_Y > size_of_board or pos_X < 1 or pos_Y < 1:
            return False
        rule2_x = abs(self.pos_x - pos_X) <= 1
        rule2_y = abs(self.pos_y - pos_Y) <= 1
        could_move = rule2_x and rule2_y and (self.pos_x != pos_X or self.pos_y != pos_Y)
        if is_piece_at(pos_X, pos_Y, B):
            return could_move and self.side != piece_side(pos_X, pos_Y, B)
        else:
            return could_move
    
    def can_move_to(self, pos_X : int, pos_Y : int, B: Board) -> bool:
        '''checks if this king can move to coordinates pos_X, pos_Y on board B according to all chess rules'''
        if not self.can_reach(pos_X, pos_Y, B):
            return False

        # Check if there's a piece at the target position
        if is_piece_at(pos_X, pos_Y, B):
            capture_piece = piece_at(pos_X, pos_Y, B)
            if capture_piece.side == self.side:
                return False  # Cannot capture own piece
            # Remove the captured piece temporarily to test for check
            B[1].remove(capture_piece)
        
        # Simulate the move
        old_pos_x = self.pos_x
        old_pos_y = self.pos_y
        self.pos_x = pos_X
        self.pos_y = pos_Y

        # Check if this move results in putting the king's own side in check
        if is_check(self.side, B):
            # Move puts the king's side in check, revert the move
            self.pos_x = old_pos_x
            self.pos_y = old_pos_y
            if is_piece_at(pos_X, pos_Y, B):
                B[1].append(capture_piece)  # Restore the captured piece
            return False
        
        # Move doesn't result in check, revert the move and finalize
        self.pos_x = old_pos_x
        self.pos_y = old_pos_y
        if is_piece_at(pos_X, pos_Y, B):
            B[1].append(capture_piece)  # Restore the captured piece
        return True

    def move_to(self, pos_X : int, pos_Y : int, B: Board) -> Board:
        '''
        returns new board resulting from move of this king to coordinates pos_X, pos_Y on board B 
        assumes this move is valid according to chess rules
        '''
        # size_of_board, pieces = B
        new_pieces = [piece for piece in B[1] if not (piece.pos_x == pos_X and piece.pos_y == pos_Y)]
        self.pos_x = pos_X
        self.pos_y = pos_Y
        new_pieces.append(self) 
        return (B[0], new_pieces)
    
def is_check(side: bool, B: Board) -> bool:
    '''
    checks if configuration of B is check for side
    Hint: use can_reach
    '''
    king = None
    for piece in B[1]:
        if isinstance(piece, King) and piece.side == side:
            king = piece
            break
    if not king:
        return False
    for piece in B[1]:
        if piece.side != side:
            if piece.can_reach(king.pos_x, king.pos_y, B):
                return True
    return False

def is_checkmate(side: bool, B: Board) -> bool:
    '''
    checks if configuration of B is checkmate for side

    Hints: 
    - use is_check
    - use can_reach 
    '''
    if not is_check(side, B):
        return False
    for piece in B[1]:
        if piece.side == side:
            for x in range(1, B[0] + 1):
                for y in range(1, B[0] + 1):
                    if piece.can_reach(x, y, B):
                        print(f"{piece} can reach ({x}, {y}) to evade check")
                        return False
    return True
    

def is_stalemate(side: bool, B: Board) -> bool:
    '''
    checks if configuration of B is stalemate for side

    Hints: 
    - use is_check
    - use can_move_to 
    '''
    # if the king is not in check
    if is_check(side, B):
        return False
    for piece in B[1]:
        if piece.side is not side:
            continue
        for x in range(1,6):
            for y in range(1,6):
                if x == piece.pos_x and y ==piece.pos_y:
                    continue
                if piece.can_move_to(x, y, B):
                    return False
    else:
        return True        
        
def parse_line(line: str, side_: bool) -> list[Piece]:
    line = line.strip()
    elments = line.split(',')
    pieces =[]
    for element in elments:
        element = element.strip()
        role_of_chess = element[0]
        location_of_the_role = element[1:3]
        x,y = location2index(location_of_the_role)
        if role_of_chess == 'N':
            piece = Knight(pos_X = x, pos_Y = y, side_ = side_)
        else:
            piece = King(pos_X = x, pos_Y = y, side_ = side_)
        pieces.append(piece)
    return pieces

def read_board(filename: str) -> Board:
    '''
    reads board configuration from file in current directory in plain format
    raises IOError exception if file is not valid (see section Plain board configurations)
    '''
    f = open(filename, "r")
    size_of_board = int(f.readline())
    white_side = f.readline()
    white_pieces = parse_line(white_side, True)
    black_side = f.readline()
    balck_pieces = parse_line(black_side, False)
    pieces = white_pieces + balck_pieces
    f.close()
    return tuple([size_of_board, pieces])


def save_board(filename: str, B: Board) -> None:
    '''saves board configuration into file in current directory in plain format'''
    size_of_board, pieces = B
    f = open(filename, "w")
    f.write(str(size_of_board) + '\n')
    white_pieces = [piece for piece in pieces if piece.side]
   # Write pieces for the white player
    for i, piece in enumerate(pieces):
            if piece.side:  # White pieces
                role = 'K' if isinstance(piece, King) else 'N'
                location = index2location(piece.pos_x, piece.pos_y)
                f.write(f'{role}{location}')
                if i < len(white_pieces) - 1:  # If not the last piece, add a comma
                    f.write(',')
     
  #Start a new line for the black player's pieces
    f.write('\n')
    black_pieces = [piece for piece in pieces if not piece.side]
        # Write pieces for the black player
    for i, piece in enumerate(black_pieces):
            if not piece.side:  # Black pieces
                role = 'K' if isinstance(piece, King) else 'N'
                location = index2location(piece.pos_x, piece.pos_y)
                f.write(f'{role}{location}')
                if i < len(black_pieces) - 1:  
                    f.write(',')
    f.close()        
    
        
def find_black_move(B: Board) -> tuple[Piece, int, int]:
    '''
    returns (P, x, y) where a Black piece P can move on B to coordinates x,y according to chess rules 
    assumes there is at least one black piece that can move somewhere

    Hints: 
    - use methods of random library
    - use can_move_to
    '''
    black_pieces = [p for p in B[1] if p.side == False]
    random.shuffle(black_pieces)
    for piece in black_pieces:
        for x in range(1,6):
            for y in range(1,6):
                if x == piece.pos_x and y ==piece.pos_y:
                    continue
                if piece.can_move_to(x, y, B):
                    return (piece,x, y)
                
def valid_move(move: str, side: bool, B: Board) -> bool:
    '''
    checks if the move provided is valid for the side in the current board configuration B.
    '''
    if len(move) != 4:
        return False
    start_loc = move[0:2]
    end_loc = move[2:4]
    start_x, start_y = location2index(start_loc)
    end_x, end_y = location2index(end_loc)

    if not is_piece_at(start_x, start_y, B):
        return False
    piece = piece_at(start_x, start_y, B)
    if piece.side != side:
        return False
    if not piece.can_move_to(end_x, end_y, B):
        return False
    return True

def parse_move(move_str: str) -> tuple[int, int, int, int]:
    '''
    parses a move string (e.g., 'e4d2') into starting and ending coordinates.
    '''
    start_loc = move_str[:2]
    end_loc = move_str[2:]
    start_x, start_y = location2index(start_loc)
    end_x, end_y = location2index(end_loc)
    return start_x, start_y, end_x, end_y

# def conf2unicode(B: Board) -> str: 
#     '''converts board cofiguration B to unicode format string (see section Unicode board configurations)'''
#     size, pieces = B
#     board = [['\u2001' for _ in range(size)] for _ in range(size)]
#     for piece in pieces:
#         if isinstance(piece, King):
#             if piece.side:
#                 board[piece.pos_y - 1][piece.pos_x - 1] = '♔'  
#             else:
#                 board[piece.pos_y - 1][piece.pos_x - 1] = '♚'  
#         elif isinstance(piece, Knight):
#             if piece.side:
#                 board[piece.pos_y - 1][piece.pos_x - 1] = '♘' 
#             else:
#                 board[piece.pos_y - 1][piece.pos_x - 1] = '♞' 
#     unicode_board = '\n'.join([''.join(row) for row in board])
#     return unicode_board

def conf2unicode(B: Board) -> str:
    '''converts board configuration B to unicode format string with column and row labels'''
    size, pieces = B
    board = [['\u2001' for _ in range(size)] for _ in range(size)]

    # Place pieces on the board
    for piece in pieces:
        if isinstance(piece, King):
            if piece.side:
                board[size - piece.pos_y][piece.pos_x - 1] = '♔'  # White king
            else:
                board[size - piece.pos_y][piece.pos_x - 1] = '♚'  # Black king
        elif isinstance(piece, Knight):
            if piece.side:
                board[size - piece.pos_y][piece.pos_x - 1] = '♘'  # White knight
            else:
                board[size - piece.pos_y][piece.pos_x - 1] = '♞'  # Black knight

    # Create the Unicode representation with column and row labels
    unicode_board = ' a b c d e\n'  # Unicode space character (\u2001) for indentation

    for i in range(size):
        unicode_board += f'{size - i} '  # Row label (5, 4, 3, 2, 1)
        for j in range(size):
            unicode_board += board[i][j] + ' '
        unicode_board += '\n'

    return unicode_board

def main() -> None:
    '''
    Main function to run the chess game.
    '''
    import sys
    while True:
        filename = input("File name for initial configuration: ")
        if filename.upper() == "QUIT":
            print("Program terminated.")
            sys.exit(0)
        try:
            board = read_board(filename)
            break
        except IOError:
            print("This is not a valid file.")
    
    print("The initial configuration is:")
    print(conf2unicode(board))
    current_side = True  # True for White, False for Black
    while True:
        if current_side:  # White's turn
            print("Next move of White:")
            move_input = input().strip()
            
            if move_input.upper() == "QUIT":
                filename_to_save = input("File name to store the configuration: ")
                save_board(filename_to_save, board)
                print("The game configuration saved.")
                break
            
            if not valid_move(move_input, current_side, board):
                print("This is not a valid move. Next move of White:")
                continue
            
            pos_X, pos_Y, new_X, new_Y = parse_move(move_input)
            piece = piece_at(pos_X, pos_Y, board)
            if piece.can_move_to(new_X, new_Y, board):
                board = piece.move_to(new_X, new_Y, board)
                print("The configuration after White's move is:")
                print(conf2unicode(board))
                
                if is_checkmate(not current_side, board):
                    print("Game over. White wins.")
                    break
                elif is_stalemate(not current_side, board):
                    print("Game over. Stalemate.")
                    break
            
                current_side = False  # Switch to Black's turn
        # Black's turn
        else:  
            print("Next move of Black:")
            black_piece, new_X, new_Y = find_black_move(board)
            # print(f"{black_piece} can reach ({new_X}, {new_Y}) to evade check")
            board = black_piece.move_to(new_X, new_Y, board)
            print("The configuration after Black's move is:")
            print(conf2unicode(board))
            
            if is_checkmate(not current_side, board):
                print("Game over. Black wins.")
                break
            elif is_stalemate(not current_side, board):
                print("Game over. Stalemate.")
                break
            current_side = True  # Switch to White's turn

if __name__ == '__main__':
    main()

