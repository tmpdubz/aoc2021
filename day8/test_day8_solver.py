from day8_solver import *

def test_read_td():
  data = read_test_data(test_data)
  ov = output_values(data)
  assert ov == [['fdgacbe', 'cefdb', 'cefbgd', 'gcbe'], ['fcgedb', 'cgb', 'dgebacf', 'gc'], ['cg', 'cg', 'fdcagb', 'cbg'], ['efabcd', 'cedba', 'gadfec', 'cb'], ['gecf', 'egdcabf', 'bgf', 'bfgea'], ['gebdcfa', 'ecba', 'ca', 'fadegcb'], ['cefg', 'dcbef', 'fcge', 'gbcadfe'], ['ed' ,'bcgafe', 'cdgba', 'cbgef'], ['gbdfcae' ,'bgc', 'cg', 'cgb'], ['fgae', 'cfgab', 'fg', 'bagce']]
  assert len(ov) == 10

def test_read_file():
  data = read_file('input')
  ov = output_values(data)
  assert ov[0] == ['gcdfbe', 'cbea', 'bc', 'gbc']
  assert ov[199] == ['becadf', 'facdeb', 'dg', 'agbdcf']
  assert len(ov) == 200

def test_count_uniques():
  data = read_test_data(test_data)
  ov = output_values(data)
  counts = count_unique_digits(ov)
  assert counts == 26

