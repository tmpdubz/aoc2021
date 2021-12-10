import timeit

test_data = """2199943210
3987894921
9856789892
8767896789
9899965678"""


def main():
  t1  = timeit.timeit('part1()', number=1, globals = globals())
  t2 = timeit.timeit('part2()', number=1, globals = globals())
  print('part 1 took ' + str(t1) + ' seconds')
  print('part 2 took ' + str(t2) + ' seconds')

def part1():
  print('Part 1')
  data = read_file('input')
  lps = get_low_points(data, ignore_basins=True)
  risksum = sum(list(map(lambda x: x+1,lps)))
  print('risksum: ' + str(risksum))


def part2():
  print('Part 2')
  data = read_file('input')
  tb = find_top3_basin_size(data)
  print('product of top 3 basins: ' + str(tb[0]*tb[1]*tb[2]))


# read the input file from this directory
def read_file(filename):
  input = []
  with open(filename) as f:
    input = [[int(char) for char in x.strip()] for x in f.readlines() if x] # list comprehensions are horrifying oh my god
  return input

# read the test data string
def read_test_data(input):
  return [[int(char) for char in y] for y in (x.strip() for x in input.splitlines()) if y ] # I should go to jail for this

# return a sorted array of adjacencies for a matrix element
def determine_adjacencies(i, j, matrix, ignore_basins=False):
  pings = ping(i,j, matrix, ignore_basins=ignore_basins)
  adjacent_values = []
  for p in pings:
    adjacent_values.append(matrix[p[0]][p[1]])
  return sorted(adjacent_values)

def is_low_point(i,j, matrix, ignore_basins=False): # i == row, j == column -- standard matrix notation
  adjacencies = determine_adjacencies(i, j, matrix, ignore_basins=ignore_basins)
  if matrix[i][j] < min(adjacencies):
    return True
  return False

def get_low_points(matrix, ignore_basins=False):
  lps = []
  column_length = len(matrix)
  row_length = len(matrix[0])
  for i in range(column_length):
    for j in range(row_length):
      if is_low_point(i,j,matrix,ignore_basins=ignore_basins):
        lps.append(matrix[i][j])
  return sorted(lps)

def get_low_points_coords(matrix, ignore_basins=False):
  lps = []
  column_length = len(matrix)
  row_length = len(matrix[0])
  for i in range(column_length):
    for j in range(row_length):
      if is_low_point(i,j,matrix,ignore_basins=ignore_basins):
        lps.append((i,j))
  return sorted(lps)

# what do we need as an input to ping?
# current point, matrix
# what do we output?
# adjacent points inside the basin that we append to the next exploration set
def ping(i,j, matrix, ignore_basins=False):
  max_row = len(matrix) - 1
  max_column = len(matrix[0]) - 1 # assumption: all rows are same length
  adjacencies = []
  if i == 0: # don't look above it, just below
    if ignore_basins or matrix[i+1][j] != 9: adjacencies.append((i+1,j))
  elif i == max_row: # don't look below it, just above
    if ignore_basins or matrix[i-1][j] != 9: adjacencies.append((i-1,j))
  else: # look above and below
    if ignore_basins or matrix[i+1][j] != 9: adjacencies.append((i+1,j))
    if ignore_basins or matrix[i-1][j] != 9: adjacencies.append((i-1,j))

  if j == 0:
    if ignore_basins or matrix[i][j+1] != 9: adjacencies.append((i,j+1))
  elif j == max_column:
    if ignore_basins or matrix[i][j-1] != 9: adjacencies.append((i,j-1))
  else:
    if ignore_basins or not matrix[i][j+1] == 9: adjacencies.append((i,j+1))
    if ignore_basins or not matrix[i][j-1] == 9: adjacencies.append((i,j-1))
  return set(adjacencies)

def get_basin_size(lowpoint_i, lowpoint_j, matrix):
  basin = set([(lowpoint_i, lowpoint_j)])
  to_explore = [(lowpoint_i, lowpoint_j)]
  i=0
  while len(to_explore) > 0:
    new_exploration = []
    for pt in to_explore:
      found_in_ping = ping(pt[0], pt[1], matrix)
      new_exploration = new_exploration + list(found_in_ping.difference(basin))
      basin |= found_in_ping.difference(basin)
    to_explore = new_exploration
    i += 1
  return len(basin)

def find_top3_basin_size(matrix):
  # every low point is at the bottom of a basin
  # 9s are not in basins
  basins = []
  lps = get_low_points_coords(matrix, ignore_basins=True)
  for lp in lps:
    basins.append(get_basin_size(lp[0], lp[1], matrix))
  return sorted(basins)[-3:]



# LOW POINT = lower than its adjacent numbers
# LOW POINT if point < min(get_adjacent_numbers)
# getting adjacent numbers means:
# if the number is in the top or bottom row, don't look up or down respectively
# if the number is in the left or rightmost row, don't look left or right respectively
# risk level = 1 + lowpoint
# WANT: sum of risk levels


# ok now cut out all the 9s to draw out basins
#
# 21...43210
# 3.878.4.21
# .85678.8.2
# 87678.678.
# .8...65678

# What if we were to start at the low point and "PING" outwards
#     ^
#     |
# <-- . -->
#     |
#     v
# We only want to know the size of the basin, so let's track set((i,j))
# each valid (i,j) gets added to a set, then we ping outwards from there

# NEXT IDEA
# start a a low point
# go out in each direction and add i,j to the list
# initial index = LP, basin = set[LP]
# first_exploration = valid points 1 away from LP
# second_exploration = valid points 1 away from points in first_exploration

# Let's use the visible basin as an example
# XX...43210
# X.XXX.4.21
# .XXXXX.X.2
# XXXXX.XXX.
# .X...XXXXX
#
# (0,5)(0,6)(0,7)(0,8)(0,9)
#
#
# LP = 1,
# to explore = LP = (0,9)
# while there is something to explore....
# explore LP yields 2 points, (0,8), (1,9)
# to_explore = (0,8), (1,9)
#   ping (0,8) to get (0,7), (1,8)
#   ping (1,9) to get (1,8), (2,9)
# to_explore = (0,7),(1,8),(2,9)
  # ping(0,7) to get (0,6)

if __name__ == '__main__':
  main()
