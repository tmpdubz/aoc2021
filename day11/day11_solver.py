import timeit

test_data = """5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526"""

def main():
  t1  = timeit.timeit('part1()', number=1, globals = globals())
  t2 = timeit.timeit('part2()', number=1, globals = globals())
  print('part 1 took ' + str(t1) + ' seconds')
  print('part 2 took ' + str(t2) + ' seconds')

def part1():
  print('Part 1')
  data = read_file('input')
  # data = read_test_data(test_data)
  og = Octogrid(data)
  og.do(100)

def part2():
  print('Part 2')
  data = read_file('input')
  # data = read_test_data(test_data)
  og = Octogrid(data)
  og.stepper()


class Octo:
  def __init__(self, energy):
    self.energy_level = energy
    self.flashed = False

  def energize(self):
    if not self.flashed:
      self.energy_level += 1
    if self.energy_level > 9 and not self.flashed:
      self.flashed = True
      self.energy_level = 0
      return True # send a signal saying 'I just flashed'
    return False # send a signal saying 'I energized but didn't flash'

  def reset(self):
    self.flashed = False

class Octogrid:
  def __init__(self, data):
    self.grid = [[Octo(energy_level) for energy_level in row] for row in data]
    self.flash_count = 0
    self.step_no = 0
    self.synchronicity_achieved = False

  def display_grid(self):
    for row in self.grid:
      print(''.join([str(x.energy_level) for x in row]))

  def get_neighbs(self,i,j):
    indices = [(i-1,j-1),(i,j-1),(i+1,j-1),(i-1,j),(i+1,j),(i-1,j+1),(i,j+1),(i+1,j+1)]
    filter_set = []
    if i == 0:
      filter_set.extend([(i-1,j-1),(i-1,j),(i-1,j+1)])
    if j == 0:
      filter_set.extend([(i-1,j-1),(i,j-1),(i+1,j-1)])
    if i == len(self.grid) - 1:
      filter_set.extend([(i+1,j-1),(i+1,j),(i+1,j+1)])
    if j == len(self.grid[0]) - 1:
      filter_set.extend([(i-1,j+1),(i,j+1),(i+1,j+1)])
    return [x for x in indices if x not in filter_set]

  # adjacent bois flash -- ?? -- what happens if we just don't. The example specifies 8 surroudning a 1, which requires no additional logic
  def energize(self,i,j):
    octo = self.grid[i][j]
    if octo.energize(): # energize it and it flashes or it doesn't -- if it does - energize the nighbs
      self.flash_count += 1
      neighbs = self.get_neighbs(i,j)
      for n in neighbs:
        self.energize(n[0],n[1])

  def step(self):
    synchronicity = True
    rows = len(self.grid)
    columns = len(self.grid[0])
    # blink 'em
    for row in range(rows):
      for column in range(columns):
        self.energize(row,column)
    # check if we sync 'em
    for row in range(rows):
      for column in range(columns):
        synchronicity = synchronicity and self.grid[row][column].flashed
    self.synchronicity_achieved = synchronicity
    # ready the next step
    for row in range(rows):
      for column in range(columns):
        self.grid[row][column].reset()

  def stepper(self):
    while not self.synchronicity_achieved:
      self.step()
      self.step_no +=1
    print('stopped at step: ' + str(self.step_no + 1))

  def do(self,its):
    while self.step_no < its:
      self.step()
      self.step_no +=1
    print(str(self.flash_count))



# read the input file from this directory
def read_file(filename):
  input = []
  with open(filename) as f:
    input = [[int(char) for char in x.strip()] for x in f.readlines() if x] # list comprehensions are horrifying oh my god
  return input

# read the test data string
def read_test_data(input):
  return [y for y in ([int(char) for char in x.strip()] for x in input.splitlines()) if y ] # I should go to jail for this

if __name__ == '__main__':
  main()
