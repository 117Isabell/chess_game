# import pytest
from chess_puzzle import *


def test_locatio2index1():
    assert location2index("e2") == (5,2)  
def test_locatio2index2():
    assert location2index("a1") == (1,1)
def test_locatio2index3():
    assert location2index("b3") == (2,3)   
def test_locatio2index4():
    assert location2index("c5") == (3,5) 
def test_locatio2index5():
    assert location2index("d3") == (4,3)

def test_index2location1():
    assert index2location(5,2) == "e2"
def test_index2location2():
    assert index2location(1,1) == "a1"
def test_index2location3():
    assert index2location(2,3) == "b3"
def test_index2location4():
    assert index2location(3,5) == "c5"
def test_index2location5():
    assert index2location(4,3) == "d3"
    
wn1 = Knight(1,2,True)
wn2 = Knight(5,2,True)
wn3 = Knight(5,4, True)
wk1 = King(3,5, True)

bn1 = Knight(1,1,False)
bk1 = King(2,3, False)
bn2 = Knight(2,4, False)

B1 = (5, [wn1, bn1, wn2, bn2, wn3, wk1, bk1])
'''
  ♔  
 ♞  ♘
 ♚   
♘   ♘
♞    
'''

def test_is_piece_at1():
    assert is_piece_at(2,2, B1) == False
def test_is_piece_at2():
    assert is_piece_at(2,4, B1) == True
def test_is_piece_at3():
    assert is_piece_at(1,2, B1) == True
def test_is_piece_at4():
    assert is_piece_at(5,2, B1) == True
    
def test_piece_side1():
    assert piece_side(1, 1, B1) == False
def test_piece_side2():
    assert piece_side(2, 3, B1) == False
def test_piece_side3():
    assert piece_side(3, 5, B1) == True
def test_piece_side4():
    assert piece_side(5, 4, B1) == True
def test_piece_side5():
    assert piece_side(2, 4, B1) == False

def test_piece_at1():
    assert piece_at(1,1, B1) == bn1
def test_piece_at2():
    assert piece_at(1,2, B1) == wn1
def test_piece_at3():
    assert piece_at(2,3, B1) == bk1
def test_piece_at4():
    assert piece_at(3,5, B1) == wk1
def test_piece_at5():
    assert piece_at(5,4, B1) == wn3

def test_can_reach1():
    assert bn1.can_reach(2,2, B1) == False
    assert wn3.can_reach(7,5, B1) == False
    assert wn3.can_reach(3,5, B1) == False
    assert wn1.can_reach(2,4, B1) == True
    assert bn1.can_reach(2,3,B1) == False
    assert wn2.can_reach(3, 5, B1) == False
    
def test_can_reach_bk1():
    assert bk1.can_reach(1, 3, B1) == True
def test_can_reach_bk2():
    assert bk1.can_reach(1, 4, B1) == True
def test_can_reach_bk3():
    assert bk1.can_reach(2, 4, B1) == False
def test_can_reach_bk4():
    assert bk1.can_reach(3, 4, B1) == True
def test_can_reach_wk5():
    assert wk1.can_reach(2, 4, B1) == True
def test_can_reach_wk6():
    assert wk1.can_reach(2, 5, B1) == True
def test_can_reach_wk7():
    assert wk1.can_reach(4, 4, B1) == True
def test_can_reach_wk8():
    assert wk1.can_reach(5, 4, B1) == False
    
def test_can_move_to1():
    assert wk1.can_move_to(4,5, B1) == False
def test_can_move_to2():
    assert wn3.can_move_to(3,5, B1) == False
def test_can_move_to3():
    assert bk1.can_move_to(3,4, B1) == False
def test_can_move_to4():
    assert bn2.can_move_to(4,3, B1) == True
def test_can_move_to5():
    assert wn2.can_move_to(4,2, B1) == False
    
    
def test_move_to1(): 
    wn1 = Knight(2, 4, True)
    bn1 = Knight(4, 4, False)
    wn2 = Knight(3, 2, True)
    wn3 = Knight(2, 3, True)
    wk1 = King(1, 1, True)
    bk1 = King(3, 3, False)
    B1 = (5, [wn1, bn1, wn2, wn3, wk1, bk1])
    Expected_B = (5, [wn1, bn1, wn2, wn3, wk1, bk1])
    Actual_B = wn1.move_to(2, 4, B1)
    '''
      ♔   
     ♘  ♘
     ♚   
        ♘
    ♞    
    '''

    #check if actual board has same contents as expected 
    assert Actual_B[0] == 5

    for piece1 in Actual_B[1]: #we check if every piece in Actual_B is also present in Expected_B; if not, the test will fail
        found = False
        for piece in Expected_B[1]:
            if piece.pos_x == piece1.pos_x and piece.pos_y == piece1.pos_y and piece.side == piece1.side and type(piece) == type(piece1):
                found = True
        assert found


    for piece in Expected_B[1]:  #we check if every piece in Expected_B is also present in Actual_B; if not, the test will fail
        found = False
        for piece1 in Actual_B[1]:
            if piece.pos_x == piece1.pos_x and piece.pos_y == piece1.pos_y and piece.side == piece1.side and type(piece) == type(piece1):
                found = True
        assert found
def test_move_to2():
    Actual_B = wn3.move_to(1, 2, B1)
    Expected_B = (5, [wn1, bn1, wn2, bn2, wn3, wk1, bk1])
    assert Actual_B[0] == Expected_B[0]
    for piece1 in Actual_B[1]:
        found = False
        for piece in Expected_B[1]:
            if (piece.pos_x == piece1.pos_x and
                piece.pos_y == piece1.pos_y and
                piece.side == piece1.side and
                type(piece) == type(piece1)):
                found = True
        assert found
    for piece in Expected_B[1]:
        found = False
        for piece1 in Actual_B[1]:
            if (piece.pos_x == piece1.pos_x and
                piece.pos_y == piece1.pos_y and
                piece.side == piece1.side and
                type(piece) == type(piece1)):
                found = True
        assert found
def test_move_to3():
    wn2 = Knight(3, 2, True)
    bn1 = Knight(4, 4, False)
    B1 = (5, [wn1, bn1, wn2, wn3, wk1, bk1])
    Actual_B = wn2.move_to(4, 4, B1)
    wn2_new = Knight(4, 4, True)  
    Expected_B = (5, [wn1, wn2_new, wn3, wk1, bk1])
    assert Actual_B[0] == Expected_B[0]
    for piece1 in Actual_B[1]:
        found = False
        for piece in Expected_B[1]:
            if (piece.pos_x == piece1.pos_x and
                piece.pos_y == piece1.pos_y and
                piece.side == piece1.side and
                type(piece) == type(piece1)):
                found = True
        assert found
    for piece in Expected_B[1]:
        found = False
        for piece1 in Actual_B[1]:
            if (piece.pos_x == piece1.pos_x and
                piece.pos_y == piece1.pos_y and
                piece.side == piece1.side and
                type(piece) == type(piece1)):
                found = True
        assert found
def test_move_to4():
    wn3 = Knight(2, 3, True)
    B1 = (5, [wn1, bn1, wn2, wn3, wk1, bk1])
    Actual_B = wn3.move_to(4, 4, B1)
    wn3_new = Knight(4, 4, True)  
    Expected_B = (5, [wn1, bn1, wn2, wn3_new, wk1, bk1])
    assert Actual_B[0] == Expected_B[0]
    for piece1 in Actual_B[1]:
        found = False
        for piece in Expected_B[1]:
            if (piece.pos_x == piece1.pos_x and
                piece.pos_y == piece1.pos_y and
                piece.side == piece1.side and
                type(piece) == type(piece1)):
                found = True
        assert found
    for piece in Expected_B[1]:
        found = False
        for piece1 in Actual_B[1]:
            if (piece.pos_x == piece1.pos_x and
                piece.pos_y == piece1.pos_y and
                piece.side == piece1.side and
                type(piece) == type(piece1)):
                found = True
        assert found

def test_is_check1():
    wk1a = King(4,5,True)
    B2 = (5, [wn1, bn1, wn2, bn2, wn3, wk1a, bk1])
    '''
       ♔  
     ♞  ♘
     ♚   
    ♘   ♘
    ♞    
    '''
    
    assert is_check(True, B2) == True

def test_is_check2():
    bk1a = King(3,3,False)
    B2 = (5, [wn1, bn1, wn2, bn2, wn3, bk1a, bk1])
    '''
       ♔  
     ♞  ♘
     ♚   
    ♘   ♘
    ♞    
    '''
    
    assert is_check(False, B2) == True

def test_is_checkmate1():
    wk1a = King(1,5,True)
    bn2a = Knight(3,4, False)
    bn3 = Knight(4,4,False)
    B2 = (5, [wn1, wn2, wn3, wk1a, bn1, bk1, bn2a, bn3]) 
    '''
    ♔    
      ♞♞♘
     ♚   
    ♘   ♘
    ♞    
    '''
    assert is_checkmate(True, B2) == False
def test_is_checkmate2():
    wk1a = King(1, 5, True)
    bn2a = Knight(3, 4, False)
    bn3 = Knight(4, 4, False)
    wn1 = Knight(4, 1, True)  
    wn2 = Knight(2, 5, True)
    wn3 = Knight(1, 1, True)
    bn1 = Knight(1, 3, False)  
    bk1 = King(3, 3, False)
    B2 = (5, [wn1, wn2, wn3, wk1a, bn1, bk1, bn2a, bn3])
    assert is_checkmate(True, B2) == False
    
def test_is_checkmate3():
    wk1a = King(1, 1, True)
    wn1 = Knight(2, 3, True)
    bn1 = Knight(3, 3, False)
    bn2 = Knight(3, 1, False)
    B4 = (5, [wk1a, wn1, bn1, bn2])
    '''
    ♔    
      ♞  
     ♘ ♞ 
         
         
    '''
    assert is_checkmate(True, B4) == False
def test_read_board1():
    B = read_board("board_examp.txt")
    assert B[0] == 5

    for piece in B[1]:  #we check if every piece in B is also present in B1; if not, the test will fail
        found = False
        for piece1 in B1[1]:
            if piece.pos_x == piece1.pos_x and piece.pos_y == piece1.pos_y and piece.side == piece1.side and type(piece) == type(piece1):
                found = True
        assert found

    for piece1 in B1[1]: #we check if every piece in B1 is also present in B; if not, the test will fail
        found = False
        for piece in B[1]:
            if piece.pos_x == piece1.pos_x and piece.pos_y == piece1.pos_y and piece.side == piece1.side and type(piece) == type(piece1):
                found = True
          
        assert found

# def test_conf2unicode1():
#     size_of_board = 5
#     pieces = [
#             King(3, 1, True), Knight(2, 2, False), Knight(5, 2, True),
#             King(3, 3, False), Knight(1, 4, True), Knight(5, 4, True),
#             Knight(1, 5, False)
#         ]
#     board = (size_of_board, pieces)
#     expected_result = '  ♔  \n ♞  ♘\n  ♚  \n♘   ♘\n♞    '
#     assert conf2unicode(board) == expected_result 

def test_valid_move1():
    move = "b4c"
    assert valid_move(move, True, B1) == False
def test_valid_move2():
    move = "b3d4"
    assert valid_move(move, True, B1) == False
def test_valid_move3_wn3():
    move = "e2c3"
    assert valid_move(move, True, B1) == False
def test_valid_move4():
    move = "a1c2"
    assert valid_move(move, True, B1) == False
def test_valid_move5_bk1():
    move = "b3c2"
    assert valid_move(move, False, B1) == True

def test_parse_move1():
    move_str = "a2c3"
    assert parse_move(move_str) == (1, 2, 3, 3)
def test_parse_move2():
    move_str = "b4d2"
    assert parse_move(move_str) == (2, 4, 4, 2)
def test_parse_move3():
    move_str = "d1d3"
    assert parse_move(move_str) == (4, 1, 4, 3)
def test_parse_move4():
    move_str = "a3e3"
    assert parse_move(move_str) == (1, 3, 5, 3)
def test_parse_move5():
    move_str = "e5a1"
    assert parse_move(move_str) == (5, 5, 1, 1)
       
def test_conf2unicode():
   tests = [
        #Empty board
        ((5, []), ('\u2001' * 5 + '\n') * 4 + '\u2001' * 5),
        #With one single piece (King or Knight)
        ((5, [King(4, 4, True)]), ('\u2001' * 5 + '\n') * 3 + '\u2001' * 3 + '♔' + '\u2001' + '\n' + '\u2001' * 5),
        ((5, [Knight(4, 4, True)]), ('\u2001' * 5 + '\n') * 3 + '\u2001' * 3 + '♘' + '\u2001' + '\n' + '\u2001' * 5),
        #Multiple pieces
        ((5, [King(3, 1, True), Knight(2, 2, False), Knight(5, 2, True),
              King(3, 3, False), Knight(1, 4, True), Knight(5, 4, True),
              Knight(1, 5, False)]), 
         ('\u2001' * 2 + '♔'+ '\u2001' * 2 + '\n' + '\u2001' + '♞' + '\u2001' * 2 + '♘' + '\n' +'\u2001' * 2 + '♚' + '\u2001' * 2 + '\n' + '♘' + '\u2001' * 3 + '♘' + '\n' + '♞' + '\u2001' * 4)
        )
        #Input with different board sizes
    ]
   for (input_data, expected) in tests:
        result = conf2unicode(input_data)
        assert result == expected, f"Test failed for input {input_data}: expected {expected}, got {result}"


def test_save_board():
    # Create a test board configuration
    board = (5, [Knight(1, 2, True), Knight(2, 1, True), Knight(4, 3, True), King(3, 5, True),
                 Knight(1, 1, False), Knight(2, 3, False), Knight(3, 4, False)])
    
    # Call the save_board function
    filename = "test_board.txt"
    save_board(filename, board)
    
    # Read the content of the saved file
    with open(filename, "r") as f:
        content = f.readlines()
    
    # Check if the content matches the expected output
    assert content[0].strip() == "5"  # Check the size of the board
    assert content[1].strip() == "Na2,Nb1,Nd3,Kc5"  # Check the locations of the white pieces
    assert content[2].strip() == "Na1,Nb3,Nc4"  # Check the locations of the black pieces
