import timeit

test_data = """6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5"""


def main():
    t0 = timeit.timeit('sanity()', number=1, globals=globals())
    t1 = timeit.timeit('part1()', number=1, globals=globals())
    t2 = timeit.timeit('part2()', number=1, globals=globals())
    print('part 0 took ' + str(t0) + ' seconds')
    print('part 1 took ' + str(t1) + ' seconds')
    print('part 2 took ' + str(t2) + ' seconds')


def sanity():
    print('Part 0: Sanity Check')
    data = read_test_data_lines(test_data)
    paper = Paper(*parse_lines(data))
    paper.print_grid()
    print('-----')
    paper.fold(paper.instructions[0])
    paper.print_grid()
    print('-----')
    paper.fold(paper.instructions[1])
    paper.print_grid()
    print(paper)


def part1():
    print('Part 1')
    data = read_lines('input')
    paper = Paper(*parse_lines(data))
    paper.fold(paper.instructions[0])
    print('Visible points after first fold:' + str(len(paper.points)))


def part2():
    print('Part 2')
    data = read_lines('input')
    paper = Paper(*parse_lines(data))
    for i in range(len(paper.instructions)):
        paper.fold(paper.instructions[i])
    paper.print_grid()


# read the input file from this directory


def read_lines(filename):
    input = []
    with open(filename) as f:
        input = [x.strip() for x in f.readlines() if x]
    return input


def read_test_data_lines(input):
    return [x.strip() for x in input.splitlines() if x]


class Paper:
    def __init__(self, grid, instruction):
        self.points, self.instructions = (grid, instruction)

    def __repr__(self):
        return str({'points': self.points, 'instructions': self.instructions, 'grid': self.build_grid()})

    def get_grid_size(self):
        max_x = max([p[0] for p in self.points])
        max_y = max([p[1] for p in self.points])
        return (max_x, max_y)

    def build_grid(self):
        max_x, max_y = self.get_grid_size()
        print(max_x, max_y)
        # make a dot grid
        # fill in hash tags
        grid = [['.' for _ in range(max_x + 1)] for _ in range(max_y + 1)]
        [['.'] * (max_x + 1)] * (max_y + 1)
        for p in self.points:
            grid[p[1]][p[0]] = '#'
        joined_rows = [''.join(x) for x in grid]
        gridstring = '\n'.join(joined_rows)
        return gridstring

    def print_grid(self):
        print(self.build_grid())

    def fold(self, instruction):
        axis, fold_point = instruction
        vertical = axis == 'x'
        if vertical:
            to_reflect = [p for p in self.points if p[0] > fold_point]
            reflected = []
            for p in to_reflect:
                dist_from_fold = abs(p[0] - fold_point)
                reflected.append((fold_point - dist_from_fold, p[1]))
                self.points.remove(p)
        else:
            to_reflect = [p for p in self.points if p[1] > fold_point]
            reflected = []
            for p in to_reflect:
                dist_from_fold = abs(p[1] - fold_point)
                reflected.append((p[0], fold_point - dist_from_fold))
                self.points.remove(p)
        self.points = list(set(self.points + reflected))


def format_instruction(line):
    t = tuple(line.split(' ')[2].split('='))
    return (t[0], int(t[1]))


def parse_lines(lines):
    folds = [format_instruction(line)
             for line in lines if "fold along" in line]
    points = [tuple([int(p) for p in line.split(',')])
              for line in lines if ',' in line]
    return (points, folds)


if __name__ == '__main__':
    main()


# 10 -> 4 when folded about 7
# 10-7 = 3
# 7-4 = 3
#
