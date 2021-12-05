
def main():
    infile = 'input'
    with open(infile) as input:
        process_file(input)


def process_file(input):
    raw_lines = input.readlines()
    parsed_lines = [line.strip() for line in raw_lines]
    # parse input
    positional_map = get_postitional_map(parsed_lines)
    frequency_map = get_frequency_map(positional_map)
    # part 1
    string_gamma = stringify_fm(frequency_map)
    gamma = int('0b' + string_gamma, 2)
    epsilon = int('0b' + invert(string_gamma), 2)
    print('gamma:' + str(gamma))
    print('epsilon:' + str(epsilon))
    print('power consumption:' + str(gamma * epsilon))
    # part 2
    ox = int(oxygen(parsed_lines), 2)
    scrubbers = int(c02(parsed_lines), 2)
    print('oxygen:' + str(ox))
    print('c02 scrubbers:' + str(scrubbers))
    print('life support:' + str(ox*scrubbers))


def diag_length(input):
    return len(input[0])


def get_postitional_map(input):
    # assume all input lines share the same length
    # get a map of position => list of all things in that position
    l = diag_length(input)
    positional_map = {k: [] for k in range(l)}
    for reading in input:
        i = 0
        while i < l:
            positional_map[i].append(reading[i])
            i = i+1
    return positional_map


def most_frequent(l):
    return max(set(l), key=l.count)


def get_frequency_map(pm):
    # given a map of position => things that occur in that position
    # determine the most frequent for each position
    return {k: most_frequent(v) for k, v in pm.items()}


def stringify_fm(fm):
    s = ""
    for _, v in fm.items():
        s = s + v
    return s


def invert(bin):
    inverted = ''
    for i in bin:
        if i == '0':
            inverted += '1'
        else:
            inverted += '0'
    return inverted


def oxygen(l):
    result = ''

    # start with a list and position 0
    pos = 0
    considering = l

    while pos < diag_length(l):
        size = len(considering)
        # get the most frequent bit at position we are looking at
        positionals = ''
        for i in considering:
            positionals += i[pos]
        splisitionals = [char for char in positionals]
        most_frequent = max(set(splisitionals), key=splisitionals.count)
        least_frequent = '0' if most_frequent == '1' else '1'

        # filter out based on positional criteria
        mf_list = list(filter(lambda n: n[pos] != least_frequent, considering))
        lf_list = list(filter(lambda n: n[pos] != most_frequent, considering))

        considering = mf_list

        # check if we need to tie-break
        if size % 2 == 0 and len(mf_list) == len(lf_list):
            # if ox, keep the one where 1s most frequent
            considering = mf_list if most_frequent == '1' else lf_list

        # how many are left?
        # if only one, done
        if len(considering) == 1:
            result = considering[0]
            break

        pos = pos + 1

    return result


def c02(l):
    # disgusting
    # you should be ashamed
    result = ''

    # start with a list and position 0
    pos = 0
    considering = l

    while pos < diag_length(l):
        size = len(considering)
        # get the most frequent bit at position we are looking at
        positionals = ''
        for i in considering:
            positionals += i[pos]
        splisitionals = [char for char in positionals]
        most_frequent = max(set(splisitionals), key=splisitionals.count)
        least_frequent = '0' if most_frequent == '1' else '1'

        # filter out based on positional criteria
        mf_list = list(filter(lambda n: n[pos] != least_frequent, considering))
        lf_list = list(filter(lambda n: n[pos] != most_frequent, considering))

        considering = lf_list

        # check if we need to tie-break
        if size % 2 == 0 and len(mf_list) == len(lf_list):
            # if ox, keep the one where 1s most frequent
            considering = mf_list if most_frequent == '0' else lf_list

        # how many are left?
        # if only one, done
        if len(considering) == 1:
            result = considering[0]
            break

        pos = pos + 1
    return result


if __name__ == "__main__":
    main()
