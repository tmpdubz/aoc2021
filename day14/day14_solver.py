import timeit
import math

test_data = """NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C"""


def main():
    t0 = timeit.timeit('part0()', number=1, globals=globals())
    t1 = timeit.timeit('part1()', number=1, globals=globals())
    t2 = timeit.timeit('part2()', number=1, globals=globals())
    print('part 0 took ' + str(t0) + ' seconds')
    print('part 1 took ' + str(t1) + ' seconds')
    print('part 2 took ' + str(t2) + ' seconds')


def part0():
    print('Part 0')
    data = read_test_data_lines(test_data)
    p = Polymerificator(*parse_lines(data))
    print(p)
    print(p.count_elements())
    p.tickerator(10)
    print(p)
    print(p.count_elements())
    print('mce - lce: ' + str(p.max_min_diff()))


def part1():
    print('Part 1')
    data = read_lines('input')
    p = Polymerificator(*parse_lines(data))
    p.tickerator(10)
    print('mce - lce: ' + str(p.max_min_diff()))


def part2():
    print('Part 2')
    data = read_lines('input')
    p = Polymerificator(*parse_lines(data))
    p.tickerator(40)
    print('mce - lce: ' + str(p.max_min_diff()))

# read the input file from this directory


def read_lines(filename):
    input = []
    with open(filename) as f:
        input = [x.strip() for x in f.readlines() if x]
    return input


def read_test_data_lines(input):
    return [x.strip() for x in input.splitlines() if x]


def parse_lines(lines):
    polyrules = [x for x in lines if '->' in x]
    template_map = dict()
    for rule in polyrules:
        s = rule.split(' -> ')
        template_map[s[0]] = s[1]
    init = lines[0]
    return (init, template_map)


class Polymerificator:
    def __init__(self, initial_state, template):
        self.initial_state = initial_state
        self.template = template
        self.init_state_first = initial_state[0]
        self.init_state_last = initial_state[len(initial_state) - 1]
        template_dict = dict()
        for t in template.keys():
            seed = t
            # ('CC', 'B') ====> 'CBC'
            applied = seed[0] + template[t] + seed[1]
            template_dict[seed] = [applied[0:2], applied[1:3]]
            # ('CC' -> 'B') =====>  ('CC' -> ['CB', 'BC'])
        self.template_dict = template_dict
        state_map = dict()
        for key in template.keys():
            state_map[key] = 0
        window_size = 2
        for i in range(len(self.initial_state) - window_size + 1):
            key = ''.join(self.initial_state[i:i+window_size])
            state_map[key] += 1
        self.counts = state_map

    def __repr__(self):
        return str(self.counts)

    def tick(self):
        to_grow = [key for key, value in self.counts.items() if value > 0]
        new_values = dict()
        for key in self.counts:
            new_values[key] = 0
        for key in to_grow:
            growth_factor = self.counts[key]
            inc1, inc2 = self.template_dict[key]
            new_values[inc1] += growth_factor
            new_values[inc2] += growth_factor
        self.counts = new_values

    def tickerator(self, number_of_ticks):
        for _ in range(number_of_ticks):
            self.tick()

    def count_elements(self):
        elements = list(set([element for sublist in [[char for char in key]
                                                     for key in self.template] for element in sublist]))
        element_counts = dict()
        for el in elements:
            print('counting ' + el)
            counter = 0
            for ct in self.counts:
                if self.counts[ct] > 0 and ct.count(el) == 2:
                    counter += 2 * self.counts[ct]
                elif self.counts[ct] > 0 and ct.count(el) == 1:
                    counter += self.counts[ct]
                else:
                    pass
            element_counts[el] = math.floor(counter/2)
            if el == self.init_state_first or el == self.init_state_last:
                element_counts[el] += 1
        return element_counts

    def max_min_diff(self):
        c = self.count_elements()
        return max(c.values()) - min(c.values())


if __name__ == '__main__':
    main()

# NNCB
# 1 NN
# 1 CB
# NN -> NCN
# CB -> CHB


# generate initial adjacency set:
# endponts = N,B
# NN NC CB
#
# NN -> NCN
# NC NBC
# CB CHB

# NN 1
# NC 1
# CB 1
# observed: 3xN, 2xC, 1xB
# actual: 2xN, 1xC, 1xB

# each NN creates a NC and a CN
# each NC creates a NB and a BC
# each CB creates a CH and a HB
# NCNBCHB: NC CN NB BC CH HB

# NN 0
# NC 1
# CB 0
# CN 1
# NB 1
# BC 1
# CH 1
# HB 1
# observed: 3xN, 4xC, 3xB, 2H
# actual: 2xN, 2xC, 1xH, 2xB
# hypothesis: internal polymers are /2, endpoints are /2 + 1??

# each NN creates a NC and a CN
# each NC creates a NB and a BC
# each CB creates a CH and a HB
# each CN creates a CC and a CN
# each NB creates a NB and a BB
# each BC creates a BB and a BC
# each CH creates a CB and a BH
# each HB creates a HC and a CB


# NBCCNBBBCBHCB
#
# NN: 0
# NC: 0
# CB: 2
# CN: 1
# NB: 2
# BC: 2
# CH: 0
# HB: 0
# CC: 1
# BB: 2
# BH: 1
# HC: 1
# observed: 2xN, 11xB, 9xC, 2xH
# actual: 2xN, 6xB, 4xC, 1xH
# count: .5 for each occurence in a string, add 1 for ends
