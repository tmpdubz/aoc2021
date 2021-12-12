from day11_solver import *

def test_read_test_data():
  data = read_test_data(test_data)
  assert data[0] == [5,4,8,3,1,4,3,2,2,3]
  assert len(data) == 10
  assert data[9] == [5,2,8,3,7,5,1,5,2,6]

def test_read_file():
  data = read_file('input')
  assert len(data) == 10
  assert data[0] == [1,2,5,4,1,1,7,2,2,8]
  assert data[9] == [5,2,5,4,2,6,6,3,4,7]

