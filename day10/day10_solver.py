import timeit
import math

test_data = """[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]"""

CLOSERS = {
  '(': ')',
  '[': ']',
  '<': '>',
  '{': '}'
}

BOUNTIES = {
  ')': 3,
  ']': 57,
  '}': 1197,
  '>': 25137
}

COMPLETION_BOUNTIES = {
  ')': 1,
  ']': 2,
  '}': 3,
  '>': 4
}

def main():
  t1  = timeit.timeit('part1()', number=1, globals = globals())
  t2 = timeit.timeit('part2()', number=1, globals = globals())
  print('part 1 took ' + str(t1) + ' seconds')
  print('part 2 took ' + str(t2) + ' seconds')

def part1():
  print('Part 1')
  data = read_file('input')
  score = get_score(data)
  print('score: ' + str(score))

def part2():
  print('Part 2')
  data = read_file('input')
  scores = get_completion_scores(data)
  print(scores)
  middle_index = int(len(scores)/2) # we are allowed to assume an odd number of scores
  print('length of the scores is: ' + str(len(scores)))
  print('got middle index: ' + str(middle_index))
  print('middle score is: ' + str(scores[middle_index]))

# read the input file from this directory
def read_file(filename):
  input = []
  with open(filename) as f:
    input = [x.strip() for x in f.readlines() if x] # list comprehensions are horrifying oh my god
  return input

# read the test data string
def read_test_data(input):
  return [y for y in (x.strip() for x in input.splitlines()) if y ] # I should go to jail for this

def is_opener(c):
  if c in ['[', '(', '<', '{']:
    return True
  return False


##### THE REPETITION ZONE
##### FEEL SHAME, YOU WORM
#####
def find_error(line):
  # return (index, expected, found) of error for the line
  # or if you find no errors, None, None, None
  chunk_stack = []
  for i in range(len(line)):
    if is_opener(line[i]): # does it start a new chunk?
      chunk_stack.append(line[i]) # push to stack
    else: # does it close the current chunk?
      if line[i] == CLOSERS[chunk_stack[-1]]:
        chunk_stack.pop()
      else: # it does not close the current chunk, it's an error
        return (i,CLOSERS[chunk_stack[-1]], line[i])
  return (None, None, None)

def find_completion(line):
  # return (index, expected, found) of error for the line
  # or if you find no errors, None, None, None
  chunk_stack = []
  for i in range(len(line)):
    if is_opener(line[i]): # does it start a new chunk?
      chunk_stack.append(line[i]) # push to stack
    else: # does it close the current chunk?
      if line[i] == CLOSERS[chunk_stack[-1]]:
        chunk_stack.pop()
      else: # it does not close the current chunk, it's an error
        return []
  completion = chunk_stack.copy()
  completion.reverse()
  completion = list(map(lambda x: CLOSERS[x],completion))
  return completion
####
####
#### YOU ARE NOW LEAVING THE REPETITION ZONE
#### YOU MAY CEASE FEELING SHAME


# stop at the first incorrect closing character on any line
# some lines are incomplete - we want ones that are definitely incorrect
# openers: it's a stack!
def first_illegal_characters(input):
  illegal_chars = [] # matched by index to lines in input
  for i in range(len(input)):
    illegal_chars.append((i,input[i],find_error(input[i]))) # index, input string, errors
  return list(filter(lambda x: x[2] != (None, None, None), illegal_chars))

def get_score(data):
  score = 0
  errors = first_illegal_characters(data) # index, input string, errors
  for item in errors:
    error = item[2]
    illegal_character = error[2]
    score += BOUNTIES[illegal_character]
  return score

def remove_error_lines(data):
  error_indices = sorted([x[0] for x in first_illegal_characters(data)], reverse=True) # index, input string, errors
  incomplete_lines = data.copy()
  for i in error_indices:
    del(incomplete_lines[i])
  return incomplete_lines

def compute_completion_score(completion):
  score = 0
  for i in range(len(completion)):
    score = score*5 + COMPLETION_BOUNTIES[completion[i]]
  return score

def get_completion_scores(data):
  scores = []
  for i in range(len(data)):
    completion = find_completion(data[i])
    if completion:
      scores.append(compute_completion_score(completion))
  return sorted(scores)

if __name__ == '__main__':
  main()

# opening a chunk is allowed
# when you close a chunk, it must match the stack opener

# start at index 0, read character a-open
# is it an opener?
#   yes: open with a-open, (looking for a-close)
#   no: syntax error REPORT ERROR

# move to index 1
# is it an opener?
#   yes: push b-open to the stack
#   no: is it an error or another open
#     error: REPORT ERROR
#     another open: push b-open to stack, now searching for b-open

# move to index 2
# does it close the chunk?