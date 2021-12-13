from day12_solver import *

def test_read_test_data1():
  data = read_test_data(test_data1)
  assert data[0] == ['dc','end']
  assert len(data) == 10
  assert data[9] == ['kj','dc']

def test_read_test_data2():
  data = read_test_data(test_data2)
  assert data[0] == ['fs','end']
  assert len(data) == 18
  assert data[17] == ['start','RW']

def test_read_file():
  data = read_file('input')
  assert len(data) == 23
  assert data[0] == ['QF','bw']
  assert data[22] == ['XL','po']

def test_init():
  data = read_test_data(test_data1)
  g = CaveGraph(data)
  node = g.get_node('start').get_node_rep()
  assert node == {'adjacent': ['kj', 'dc', 'HN'], 'name': 'start'}
