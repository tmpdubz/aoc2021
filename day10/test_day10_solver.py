from day10_solver import *

def test_read_test_data():
  data = read_test_data(test_data)
  assert len(data) == 10
  assert data[0] == '[({(<(())[]>[[{[]{<()<>>'
  assert data[9] == '<{([{{}}[<[[[<>{}]]]>[]]'

def test_read_file():
  data = read_file('input')
  assert len(data) == 90
  assert data[0] == '{[[<[({{[<[[[[<>()]{[][]}][[<>[]]([])]]]{({[[]()]<()<>>}[[()()]<{}()>])<{<[]<>><{}{}>}[<()<>>{[]()}]>}'
  assert data[89] == '((<(([{[[<[<{({}{})<{}[]>}{[[]<>][()[]]}>[((<>{})(<><>)){<{}()>(<>{})}]]>(({({<>[]}[{}<>]]<[<>'

def test_find_error():
  line = '{([(<{}[<>[]}>{[]{[(<()>'
  err = find_error(line)
  print(err)
  assert err == (12 , ']', '}')

def test_find_no_error():
  line = '[({(<(())[]>[[{[]{<()<>>'
  err = find_error(line)
  assert err == (None, None, None)

def test_test_data():
  data = read_test_data(test_data)
  o = first_illegal_characters(data)
  print(o)
  assert len(o) == 5
  assert o == [(2, '{([(<{}[<>[]}>{[]{[(<()>', (12, ']', '}')), (4, '[[<[([]))<([[{}[[()]]]', (8, ']', ')')), (5, '[{[{({}]{}}([{[{{{}}([]', (7, ')', ']')), (7, '[<(<(<(<{}))><([]([]()', (10, '>', ')')), (8, '<{([([[(<>()){}]>(<<{{', (16, ']', '>'))]

# def test_completion():
#   data = read_test_data(test_data)

def test_completion():
  line = '[({(<(())[]>[[{[]{<()<>>'
  completion = find_completion(line)
  print(completion)
  assert completion == ['}', '}', ']', ']', ')', '}', ')', ']']

def test_completion_score():
  completion1 = [']',')','}','>']
  completion2 = [']',']','}','}',']','}',']','}','>']
  score1 = compute_completion_score(completion1)
  score2 = compute_completion_score(completion2)
  assert score1 == 294
  assert score2 == 995444

