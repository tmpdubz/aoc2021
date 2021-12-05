from day5_solver import *

def test_read_td():
  lines = read_test_data(test_data)
  data = parse_lines(lines)
  assert data[0].equals(Line((0,9), (5,9)))
  assert len(data) == 10
  assert data[9].equals(Line((5,5), (8,2)))

def test_read_file():
  lines = read_file_lines('input')
  data = parse_lines(lines)
  assert data[0].equals(Line((976,35),(24,987)))
  assert len(data) == 500
  assert data[499].equals(Line((154,131),(154,210)))

def test_get_grid_size():
  lines = read_test_data(test_data)
  data = parse_lines(lines)
  gridsize = determine_grid_size(data)
  assert gridsize == (9,9)

def test_hor_ver_count():
  lines = read_test_data(test_data)
  data = parse_lines(lines)
  hor_ver_lines = get_hor_ver_lines(data)
  assert len(hor_ver_lines) == 6

def test_hor_ver_lattice_count():
  l = Line((0,9), (5,9))
  integral_solutions = l.get_points_hor_ver_line()
  assert len(integral_solutions) == 6

def test_overlapping_points():
  lines = read_test_data(test_data)
  data = parse_lines(lines)
  ovc = get_overlapping_vent_coords(data)
  assert len(ovc) == 5

def test_overlapping_points():
  lines = read_test_data(test_data)
  data = parse_lines(lines)
  ovc = get_overlapping_vent_coords(data, allow_diag=True)
  assert len(ovc) == 12