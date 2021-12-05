from collections import Counter

test_data = """0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2"""

def main():
  raw_file = read_file_lines('input')
  line_data = parse_lines(raw_file)
  part1(line_data)
  part2(line_data)

def part1(line_data):
  gridsize = determine_grid_size(line_data)
  print('Got grid size: ' + str(gridsize))
  overlaps = get_overlapping_vent_coords(line_data)
  print('Number of overlaps > 1: ' + str(len(overlaps)))

def part2(line_data):
  gridsize = determine_grid_size(line_data)
  print('Got grid size: ' + str(gridsize))
  overlaps = get_overlapping_vent_coords(line_data, allow_diag=True)
  print('Number of overlaps > 1: ' + str(len(overlaps)))

def read_file_lines(filename):
  input = []
  with open(filename) as f:
    input = [x.strip() for x in f.readlines() if x]
  return input

def read_test_data(input):
  return [ y for y in (x.strip() for x in input.splitlines()) if y ] # list of lines

def parse_lines(lines):
  # absolutely digusting
  split = [ x.split('->') for x in lines ] # split on arrow, list od strings [['0,9', '5,9']]
  tuples = [ list(map(lambda x: tuple(x.strip().split(',')), pair)) for pair in split ] # parse into tuples [[('0','9'), ('5','9')]]
  int_tuples = []
  for pair in tuples:
    int_pair = [tuple(list(map(lambda n: int(n), list(tup)))) for tup in pair] # unpack the tuples, convert to ints and repack [(0,9),(5,9)]
    int_tuples.append(int_pair)
  return [Line(x[0], x[1]) for x in int_tuples]

def determine_grid_size(lines):
  x_coords = [[l.p1[0], l.p2[0]] for l in lines]
  y_coords = [[l.p1[1], l.p2[1]] for l in lines]
  biggest_x = max([item for sublist in x_coords for item in sublist])
  biggest_y = max([item for sublist in y_coords for item in sublist])
  return (biggest_x, biggest_y)

def get_hor_ver_lines(lines):
  return [l for l in lines if l.p1[0] == l.p2[0] or l.p1[1] == l.p2[1]]

def get_overlapping_vent_coords(lines, allow_diag=False):
  coords = []
  for line in lines:
    print(line.p1, line.p2, line.get_points_hor_ver_line(allow_diag), line.is_diag())
    coords.append(line.get_points_hor_ver_line(allow_diag=allow_diag))
  flat_coords = [item for sublist in coords for item in sublist]
  print(flat_coords)
  counts = dict(Counter(flat_coords))
  print(counts)
  overlapping_points = dict()
  for key, value in counts.items():
    if value > 1:
      overlapping_points[key] = value
  print(overlapping_points)
  return overlapping_points


class Line:
  def __init__(self, p1, p2):
    self.p1 = p1
    self.p2 = p2

  def show(self):
    print(self.p1, self.p2)

  def equals(self, line):
    return self.p1 == line.p1 and self.p2 == line.p2

  def is_horizontal(self):
    return self.p1[1] == self.p2[1]

  def is_vertical(self):
    return self.p1[0] == self.p2[0]

  def is_diag(self):
    return abs(self.p1[0] - self.p2[0]) == abs(self.p1[1] - self.p2[1])

  def get_points_hor_ver_line(self, allow_diag=False):
    int_points = []
    if self.is_horizontal():
      rh = range(self.p1[0], self.p2[0] + 1) if self.p2[0] > self.p1[0] else range(self.p2[0], self.p1[0] + 1)
      for v in rh:
        int_points.append((v, self.p1[1]))
    if self.is_vertical():
      rv = range(self.p1[1], self.p2[1] + 1) if self.p2[1] > self.p1[1] else range(self.p2[1], self.p1[1] + 1)
      for v in rv:
        int_points.append((self.p1[0],v))
    if allow_diag:
      if self.is_diag():
        moves = range(abs(self.p1[0] - self.p2[0]) + 1)
        for i in moves:
          # reference chart for my brain
          #
          # 00 10 20 30 40 50 60 70 80 90
          # 01 11 21 31 41 51 61 71 81 91
          # 02 12 22 32 42 52 62 72 82 92
          # 03 13 23 33 43 53 63 73 83 93
          # 04 14 24 34 44 54 64 74 84 94
          # 05 15 25 35 45 55 65 75 85 95
          # 06 16 26 36 46 56 66 76 86 96
          # 07 17 27 37 47 57 67 77 87 97
          # 08 18 28 38 48 58 68 78 88 98
          # 09 19 29 39 49 59 69 79 98 99
          if self.p1[0] < self.p2[0] and self.p1[1] < self.p2[1]: # upleft to downright
            int_points.append((self.p1[0] + i, self.p1[1] + i))
          elif self.p2[0] < self.p1[0] and self.p1[1] < self.p2[1]: # upright to downleft
            int_points.append((self.p1[0] - i, self.p1[1] + i))
          elif self.p1[0] < self.p2[0] and self.p2[1] < self.p1[1]: # downleft to upright
            int_points.append((self.p1[0] + i, self.p1[1] - i))
          elif self.p2[0] < self.p1[0] and self.p2[1] < self.p1[1]: # downright to upleft
            int_points.append((self.p1[0] - i, self.p1[1] - i))
    return int_points


if __name__ == "__main__":
  main()
