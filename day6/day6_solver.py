from collections import Counter

ITERATIONS = 80
test_data = """3,4,3,1,2"""

def main():
  data = read_file('input')
  part1(data)
  part2(data)

def part1(data):
  simulate_fish(80, data)

def part2(data):
  simulate_fish(256, data)

def read_file(filename):
  input = []
  with open(filename) as f:
    input = [x.strip() for x in f.readlines() if x]
  return [int(y) for y in input[0].split(',')]

def read_test_data(input):
  lines = [ y for y in (x.strip() for x in input.splitlines()) if y ] # list of lines
  return [int(y) for y in lines[0].split(',')]

def simulate_fish(iterations, data):
  fish_ages = range(9)
  fish_by_age = Counter()
  fish_by_age.update({x:0 for x in fish_ages}) # initialize fish by age with 0 counts
  fish_by_age.update(data) # count fish by age
  fish_age_array = list(dict(fish_by_age).values()) # model it as an array so we can pop
  fish_counter = len(data)
  for _ in range(iterations):
    spawn = fish_age_array.pop(0) # anything that hit 0 gives birth
    fish_counter += spawn
    fish_age_array.append(spawn)
    fish_age_array[6] = fish_age_array[6] + spawn
  print(fish_counter)

if __name__ == '__main__':
  main()
