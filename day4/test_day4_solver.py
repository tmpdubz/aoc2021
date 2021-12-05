from day4_solver import *

def test_get_draws():
  data = read_test_data(test_data)
  assert get_draws(data) == ['7','4','9','5','11','17','23','2','0','14','21','24','10','16','13','6','15','25','12','22','18','20','8','19','3','26','1']

def test_get_boards():
  data = read_test_data(test_data)
  bs = get_boards(data)
  assert bs[0] == [['22', '13', '17', '11', '0'],['8',  '2', '23',  '4', '24'],['21',  '9', '14', '16',  '7'],['6', '10',  '3', '18',  '5'],['1', '12', '20', '15', '19']]
  assert bs[1] == [['3', '15',  '0',  '2', '22'],['9', '18', '13', '17',  '5'],['19',  '8',  '7', '25', '23'],['20', '11', '10', '24',  '4'],['14', '21', '16', '12',  '6']]
  assert len(get_boards(data)) == 3

def test_read_file_boards():
  data = read_file('input')
  boards = get_boards(data)
  assert boards[0:5] == [[['92', '3', '88', '13', '50'], ['90', '70', '24', '28', '52'], ['15', '98', '10', '26', '5'], ['84', '34', '37', '73', '87'], ['25', '36', '74', '33', '63']], [['66', '64', '50', '75', '53'], ['73', '24', '80', '84', '5'], ['72', '20', '68', '1', '99'], ['83', '57', '44', '60', '52'], ['32', '15', '59', '48', '98']], [['33', '51', '85', '92', '89'], ['38', '22', '93', '62', '75'], ['24', '76', '50', '90', '25'], ['69', '6', '52', '77', '3'], ['47', '9', '88', '53', '63']], [['78', '75', '29', '32', '73'], ['22', '85', '42', '1', '23'], ['80', '98', '81', '58', '9'], ['61', '76', '69', '83', '53'], ['71', '7', '15', '11', '95']], [['33', '57', '76', '73', '26'], ['6', '71', '35', '39', '85'], ['54', '77', '36', '14', '87'], ['66', '79', '8', '64', '32'], ['2', '84', '98', '34', '13']]]

def test_cross_off():
  data = read_test_data(test_data)
  first_board = get_boards(data)[0]
  first_board = cross_off('22', first_board)
  assert first_board[0][0] == 'X'

def test_column_win():
  data = read_test_data(test_data)
  first_board = get_boards(data)[0]
  column_win = ['22', '8', '21', '6', '1']
  for no in column_win:
    first_board = cross_off(no, first_board)
  assert check_win_condition(first_board) == True

def test_row_win():
  data = read_test_data(test_data)
  first_board = get_boards(data)[0]
  column_win = ['22', '13', '17', '11', '0']
  for no in column_win:
    first_board = cross_off(no, first_board)
  assert check_win_condition(first_board) == True

def test_not_win():
  data = read_test_data(test_data)
  first_board = get_boards(data)[0]
  assert check_win_condition(first_board) == False

def test_winner_ix0():
  data = read_test_data(test_data)
  draws = get_draws(data)
  boards = get_boards(data)
  result = determine_winning_boards(draws, boards)
  assert result['winning_number'] == '24'
  assert result['winners'] == [2]


def test_winning_score():
  data = read_test_data(test_data)
  draws = get_draws(data)
  boards = get_boards(data)
  result = determine_winning_boards(draws, boards)
  known_winner = result['winners'][0]
  winning_board = result['resulting_boards'][known_winner]
  score = determine_winning_board_score(winning_board, result['winning_number'])
  assert score == 4512

def test_last_winner():
  data = read_test_data(test_data)
  draws = get_draws(data)
  boards = get_boards(data)
  result = determine_last_winning_board(draws, boards)
  last_winning_board = result[1][0]
  last_winning_number = result[0]
  score = determine_winning_board_score(last_winning_board, last_winning_number)
  assert score == 1924