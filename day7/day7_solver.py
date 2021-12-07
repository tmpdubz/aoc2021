import statistics

test_data = """16,1,2,0,4,2,7,1,2,14"""

def main():
  part1()
  part2()

def part1():
  print('Part 1')
  data = read_file('input')
  print('position, fuel_cost: ' + str(determine_crabrizon(data, original_crab_cost_func)))

def part2():
  print('Part 2')
  data = read_file('input')
  print('position, fuel_cost: ' + str(determine_crabrizon(data, new_crab_cost_function)))

def read_file(filename):
  input = []
  with open(filename) as f:
    input = [x.strip() for x in f.readlines() if x]
  return [int(y) for y in input[0].split(',')]

def read_test_data(input):
  lines = [ y for y in (x.strip() for x in input.splitlines()) if y ] # list of lines
  return [int(y) for y in lines[0].split(',')]

def determine_bounds(horizontal_positions):
  # whats the biggest and whats the smallest?
  return(min(horizontal_positions), max(horizontal_positions))

def original_crab_cost_func(curr_pos, new_pos):
  return abs(curr_pos - new_pos)

def new_crab_cost_function(curr_pos, new_pos):
  # absolute value of diff
  # e.g. 1 -> 5 == 4
  # but we want it to cost 1 + 2 + 3 + 4 instead of 1 + 1 + 1 + 1
  d = abs(curr_pos - new_pos)
  return int(d*(d+1)/2)

def determine_crabrizon(data, crab_cost_func):
  potential_crabrizon_sums = {}
  bounds = determine_bounds(data)
  potential_crabrizons = range(bounds[0], bounds[1]) # we don't wanna check things twice
  for CRABRIZON in potential_crabrizons: # compute sums for potential crabrizons
    sum = 0
    for val in data: # check the sum for each crabrizon
      sum += crab_cost_func(CRABRIZON, val)
    potential_crabrizon_sums[CRABRIZON] = sum
  key = min(potential_crabrizon_sums, key=potential_crabrizon_sums.get)
  return (key, potential_crabrizon_sums[key])

if __name__ =='__main__':
  main()

# median == half below, half above
# what we really want is....

# CRABRIZON s.t. |CRABRIZON - i| for i in crab_positions is smallest
