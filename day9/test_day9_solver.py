from day9_solver import *

def test_read_test_data():
  data = read_test_data(test_data)
  assert len(data) == 5
  assert data[0] == [2,1,9,9,9,4,3,2,1,0]
  assert data[4] == [9,8,9,9,9,6,5,6,7,8]

def test_read_file():
  data = read_file('input')
  assert len(data) == 100
  assert data[0] == [8,6,5,4,4,3,4,7,8,9,4,3,2,4,4,6,9,8,7,6,5,4,3,2,1,0,5,6,7,8,9,2,3,5,6,7,8,9,5,3,2,4,5,7,9,8,7,6,4,2,1,2,4,5,6,7,8,9,6,5,6,5,6,8,9,7,7,6,5,4,2,3,2,4,5,7,8,9,8,7,5,4,5,6,7,8,9,8,7,6,5,4,3,1,3,3,5,9,9,9]
  assert data[99] == [9,9,6,5,4,1,0,9,8,7,3,2,1,0,2,4,5,8,9,9,9,9,8,9,9,9,9,8,7,6,5,6,7,6,8,9,1,2,9,9,8,7,6,5,3,5,6,7,8,9,7,5,3,2,4,6,6,7,8,9,7,6,4,3,2,4,5,6,9,8,8,6,7,6,8,6,7,8,9,2,1,0,1,2,3,4,5,6,8,9,2,3,7,8,9,5,4,4,6,7]

def test_adjcency():
  data = read_test_data(test_data)
  adj = determine_adjacencies(0,1, data, ignore_basins=True)
  assert adj == sorted([9,2,9])

def test_low_point():
  data = read_test_data(test_data)
  assert is_low_point(0,1, data) == True

def test_lps():
  data = read_test_data(test_data)
  lps = get_low_points(data, ignore_basins=True)
  assert lps == sorted([1,0,5,5])

def test_ping():
  data = read_test_data(test_data)
  p = ping(0,9,data)
  assert p == set([(0,8), (1,9)])

def test_ping2():
  data = read_test_data(test_data)
  p = ping(0,1,data,ignore_basins=True)
  assert p == set([(0,0),(1,1), (0,2)])

def test_ping2():
  data = read_test_data(test_data)
  p = ping(2,9,data)
  assert p == set([(1,9)])

def test_basin():
  data = read_test_data(test_data)
  assert get_basin_size(0, 9, data) == 9
