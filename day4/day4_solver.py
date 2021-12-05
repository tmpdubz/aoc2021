# https://adventofcode.com/2021/day/4

test_data = """7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7"""

"""
How to model this:
- each board is a matrix
- a matrix is a list of lists
  [[first row], [second row], etc]
- first line o an input is the draws
"""

def main():
  data = read_file('input')
  part1(data)
  part2(data)

def part1(data):
  boards = get_boards(data)
  draws = get_draws(data)
  result = determine_winning_boards(draws, boards)
  # lets assume 1 winner and only take the top of the winners list
  windex = result['winners'][0]
  assumed_winning_board = result['resulting_boards'][windex]
  winning_number = result['winning_number']
  score = determine_winning_board_score(assumed_winning_board, winning_number)
  print('winning board: ' + str(assumed_winning_board))
  print('winning number: ' + winning_number)
  print('winning score: ' + str(score))

def part2(data):
  boards = get_boards(data)
  draws = get_draws(data)
  result = determine_last_winning_board(draws, boards)
  print(result)
  score = determine_winning_board_score(result[1][0], result[0])
  print('score of last winning board: ' + str(score))


def read_file(filename):
  input = ""
  with open(filename) as f:
    input = [x.strip() for x in f.readlines()]
  no_empties = list(filter(lambda x: x != '', input))
  return no_empties

def read_test_data(input):
  return [y for y in (x.strip() for x in input.splitlines()) if y]

def get_draws(input):
  return input[0].split(',')

def get_boards(input):
  boards = []
  # slice out the line that has draws
  cut_input = input[1:]
  # roll over every 5 lines as a matrix/board
  i = 0
  roller = 0
  current_board = []
  while i < len(cut_input):
    if roller != 5:
      current_board.append(cut_input[i].split())
      roller = roller+1
      i = i+1
    else:
      boards.append(current_board)
      current_board = []
      roller = 0
  # missed a board because i'm bad at loops - gotta get that last one in
  boards.append(current_board)
  return boards

def cross_off(draw, board):
  # like in bingo, take in a draw and cross it off on the boards
  # modelled by replacing the number with an 'X'
  i = 0
  while i < len(board):
    board[i] = ['X' if number == draw else number for number in board[i]]
    i = i+1
  return board

def check_win_condition(board):
  winner = False
  # are there X's in one row or column?
  # return a boolean telling us if its a winning board or not
  columns = [0,0,0,0,0]
  for row in board:
    if row.count('X') == 5:
      winner = True
      break
    column_hits = [index for index, element in enumerate(row) if element == 'X']
    for hit in column_hits:
      columns[hit] = columns[hit]+1
    if 5 in columns:
      winner = True
      break
  # check columns
  return winner


def determine_winning_boards(draws, boards):
  winners = []
  winner_detected = False
  winning_number = -1
  # start running through all the draws and check every board
  for draw in draws:
    # if we found winners on the last draw, don't iterate
    if winner_detected:
      break
    else:
      # if we found no winners yet, check all the boards and append winners to the winner index list
      for i in range(len(boards)):
        boards[i] = cross_off(draw, boards[i])
        if check_win_condition(boards[i]):
          winners.append(i)
          winning_number = draw
          winner_detected = True
  return {'resulting_boards': boards, 'winners': winners, 'winning_number': winning_number}

def determine_last_winning_board(draws, boards):
  rounds = []
  check_against = boards.copy()
  for draw in draws:
    winners = []
    for i in range(len(boards)):
      boards[i] = cross_off(draw, boards[i])
      if check_win_condition(boards[i]) and check_against[i] != 'ALREADY_WON':
          winners.append(boards[i].copy())
          check_against[i] = 'ALREADY_WON'
    rounds.append((draw, winners))
  print(rounds)
  rounds.reverse()
  last_winner = next(round for round in rounds if round[1] != [])
  return last_winner


def determine_winning_board_score(board, winning_number):
  running = 0
  for row in board:
    no_cross = [x for x in row if x != 'X']
    converted = [int(x) for x in no_cross]
    running = running + sum(converted)
  return running * int(winning_number)

if __name__ == '__main__':
  main()
