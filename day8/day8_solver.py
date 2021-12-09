import timeit
import statistics

test_data = """be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb |
fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec |
fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef |
cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega |
efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga |
gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf |
gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf |
cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd |
ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg |
gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc |
fgae cfgab fg bagce"""

DIGIT_SEGMENT_MAP = {
  0: 6,
  1: 2,
  2: 5,
  3: 5,
  4: 4,
  5: 5,
  6: 6,
  7: 3,
  8: 7,
  9: 6
}

flipped = {}
for k,v in DIGIT_SEGMENT_MAP.items():
  if v not in flipped:
    flipped[v] = [k]
  else:
    flipped[v].append(k)
UNIQUE_SEGMENTS = [y for sublist in (v for k,v in flipped.items() if len(v) < 2) for y in sublist]
UNIQUE_SEGMENT_MAP = { us: DIGIT_SEGMENT_MAP[us] for us in UNIQUE_SEGMENTS }
UNIQUE_SEGMENT_LENGTHS = [v for _,v in UNIQUE_SEGMENT_MAP.items()]

# difference between the key and (1,4,7,8)
# allows us to uniquely identify each of these by XOring them against 1,4,7 and 8
DIFFERENCE_MAP = {
  (2,3,3,6): 0,
  (1,2,2,5): 2,
  (2,3,3,5): 3,
  (1,3,2,5): 5,
  (1,3,2,6): 6,
  (2,4,3,6): 9
}

def main():
  t1  = timeit.timeit('part1()', number=1, globals = globals())
  t2 = timeit.timeit('part2()', number=1, globals = globals())
  print('part 1 took ' + str(t1) + ' seconds')
  print('part 2 took ' + str(t2) + ' seconds')

def part1():
  print('Part 1')
  data = read_file('input')
  ov = output_values(data)
  counts = count_unique_digits(ov)
  print('Occurences of digits with unqiue segment patterns: ' + str(counts))


def part2():
  print('Part 2')
  data = read_file('input')
  iv = input_values(data) # inputs, indices correspond to outputs
  ov = output_values(data) # outputs with correspdonding indices
  print(ov[:10])
  # get the decode keys - indices still match with inputs/outputs
  sum = 0
  for i in range(len(iv)):
    key = determine_new_mapping(iv[i])
    sum += decode(ov[i], key)
  print('decoded sum: ' + str(sum))


# read the input file from this directory
def read_file(filename):
  input = []
  with open(filename) as f:
    input = [x.strip() for x in f.readlines() if x]
  return input

# read the test data string
def read_test_data(input):
  return [ y for y in (x.strip() for x in input.splitlines()) if y ] # list of lines

# parse the inputs from the data (before the |)
def input_values(data):
  in_out = [ x.split('|') for x in data]
  unpacked = [y.strip() for y in (item for sublist in in_out for item in sublist) if y]
  inputs = [y for y in (x.split(' ') for x in unpacked[0::2]) if y]
  sorted_input = [list(map(lambda y: ''.join(sorted(y)),t)) for t in inputs]
  return sorted_input

# parse the outputs from the data (after the |)
def output_values(data):
  in_out = [ x.split('|') for x in data]
  unpacked = [y.strip() for y in (item for sublist in in_out for item in sublist) if y]
  outputs = [y for y in (x.split(' ') for x in unpacked[1::2]) if y]
  sorted_output = [list(map(lambda y: ''.join(sorted(y)),t)) for t in outputs]
  return sorted_output

# just count how many 1,4,7,8's we have in the output set
def count_unique_digits(list_of_signals):
  count = 0
  lengths = [list(map(lambda x: len(x), numberset)) for numberset in list_of_signals]
  searchset = [item for sublist in lengths for item in sublist]
  for item in searchset:
    if item in UNIQUE_SEGMENT_LENGTHS:
      count += 1
  return count

def determine_new_mapping(inputs):
  known_keys = {}
  remaining_input = []
  for i in inputs:
    if len(i) in UNIQUE_SEGMENT_MAP.values():
      key = list(UNIQUE_SEGMENT_MAP.keys())[list(UNIQUE_SEGMENT_MAP.values()).index(len(i))]
      known_keys[key] = i
    else:
      remaining_input.append(i)
  for i in remaining_input:
    sig = (
      len(set(known_keys[1]).intersection(set(i))),
      len(set(known_keys[4]).intersection(set(i))),
      len(set(known_keys[7]).intersection(set(i))),
      len(set(known_keys[8]).intersection(set(i)))
    )
    known_keys[DIFFERENCE_MAP[sig]] = i
  return known_keys

def decode(output, keys):
  no = ''
  flipped = {}
  for k,v in keys.items():
    if v not in flipped:
      flipped[v] = k
    else:
      flipped[v].append(k)
  for i in output:
    k = list(set(flipped.keys()).intersection(set([i]))).pop()
    no += str(flipped[k])
  # print(no)
  return int(no)


if __name__ == '__main__':
  main()



# let's look at the numbers we have and think of the others relative to them

#      a
#      a
#
#      b
#      b

# e    a
# e    a
#  ffff
#      b
#      b

#  dddd
#      a
#      a
#
#      b
#      b

#  dddd
# e    a
# e    a
#  ffff
# g    b
# g    b
#  cccc

# 1 we have
# 2 shares 1 with 1, 2 with 4, 2 with 7, 5 with 8 (1,2,2,5)
# 3 shares 2 with 1, 3 with 4, 3 with 7, 5 with 8 (2,3,3,5)
# 4 we have
# 5 shares 1 with 1, 3 with 4, 2 with 7, 5 with 8 (1,3,2,5)
# 6 shares 1 with 1, 3 with 4, 2 with 7, 6 with 8 (1,3,2,6)
# 7 we have
# 8 we have
# 9 shares 2 with 1, 4 with 4, 3 with 7, 6 with 8 (2,4,3,6)
# 0 shares 2 with 1, 3 with 4, 3 with 7, 6 with 8 (2,3,3,6)

