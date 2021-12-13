import timeit
from collections import deque

test_data1 = """start-A
start-b
A-c
A-b
b-d
A-end
b-end"""

test_data2 = """fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW"""

def main():
  t1  = timeit.timeit('part1()', number=1, globals = globals())
  t2 = timeit.timeit('part2()', number=1, globals = globals())
  print('part 1 took ' + str(t1) + ' seconds')
  print('part 2 took ' + str(t2) + ' seconds')

def part1():
  print('Part 1')
  data = read_file('input')
  data = read_test_data(test_data1)
  g = CaveGraph(data)
  g.traverse()
  print(len(g.paths))

def part2():
  print('Part 2')
  data = read_file('input')
  # data = read_test_data(test_data1)
  g = CaveGraph(data)
  g.traverse_with_doubles()
  print(len(g.paths))

# read the input file from this directory
def read_file(filename):
  input = []
  with open(filename) as f:
    input = [x.strip().split('-') for x in f.readlines() if x]
  return input

class Node:
  def __init__(self, name):
    self.name = name
    self.adjacent_nodes = set()
    self.little = not name.isupper() # little nodes can only be visited once
    self.is_terminus = name == 'end' # terminus ends a traversal

  def add_adjacency(self,node):
    self.adjacent_nodes.add(node)

  def __str__(self):
    # return str({'name': self.name, 'adjacent': [node.name for node in self.adjacent_nodes]})
    return self.name

  def __repr__(self):
    # return str({'name': self.name, 'adjacent': [node.name for node in self.adjacent_nodes]})
    return self.name

  def print_node(self):
    print(self.get_node_rep())

class CaveGraph:
  def __init__(self, adjacency_list):
    self.paths = []
    nodes = set([n for adj in adjacency_list for n in adj])
    self.nodes = [Node(n) for n in nodes]
    for node in self.nodes:
      adjacencies = [[i for i in adj if i != node.name] for adj in adjacency_list if node.name in adj]
      nodes_to_add = [n for adj in adjacencies for n in adj]
      for n in nodes_to_add:
        node.add_adjacency(self.get_node(n))

  def get_node(self, name):
    return next(node for node in self.nodes if node.name == name)

  def display(self):
    for node in self.nodes:
      node.print_node()

  def traverse(self, allow_double=None): # let's do a BFS for funsies BFFS with BFS!
    source = self.get_node('start') # source
    current_path = []
    queue = deque()
    # initilize
    current_path.append(source) # initialize the path
    queue.append(current_path.copy()) # create the queue, in which we store the paths to keep track of them as we go
    while queue:
      current_path = queue.popleft()
      last = current_path[len(current_path) - 1]
      if last.is_terminus:
        if current_path not in self.paths: self.paths.append(current_path)
      for node in last.adjacent_nodes:
        # try all nodes that are uppercase or lowercase and not in the current path AND not the start node
        if allow_double and node.name == allow_double.name:
          condition = node.name != 'start' and (node.little and len([x.name for x in current_path if x.name == allow_double.name]) < 2 and not node.is_terminus) or not node.little
        else:
          condition = node.name != 'start' and (node.little and node.name not in [x.name for x in current_path]) or not node.little
        if condition:
          new_path = current_path.copy()
          new_path.append(node)
          queue.append(new_path)

  def traverse_with_doubles(self): # This is crazy slow -- figure out a better way, ideally not when you have had a lot of wine
    littles = [node for node in self.nodes if node.little]
    print('doing ' + str(len(littles)) + ' traversals')
    for node in littles:
      self.traverse(allow_double=node)
      print('traversal complete: ' + str(littles.index(node)))

# read the test data string
def read_test_data(input):
  return [y for y in (x.strip().split('-') for x in input.splitlines()) if y]

if __name__ == '__main__':
  main()


#     start
#     /   \
# c--A-----b--d
#     \   /
#      end

# INITIALIZE QUEUE
# path = [start]
# queue = [[start]]

# START MOVING THROUGH IT
# queue.popleft(): [start]
# is the last item in this list the terminus? if yes, stop and add to the paths
# last = start
# queue.append()

# queue = [[start,A],[start,b]]
# queue.popleft(): [start,A]

# queue = [[start,A,c],[start,A,end],[start,A,b],[start,b,end],[start,b,A],[start,b,d]]
#