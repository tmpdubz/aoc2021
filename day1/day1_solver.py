import sys
import getopt

# Open the file, do the thing


def main():
    infile = 'input'
    with open(infile) as input:
        process_file(input)

# Parse into integers
# Generate windowed list


def process_file(input):
    raw_lines = input.readlines()
    parsed_lines = [int(line.strip()) for line in raw_lines]
    sums = compute_sums(parsed_lines, 3)
    evaluated_windows = evaluate_window(sums)
    print(evaluated_windows.count(True))

# Generate windowed list
# True if the values in the list is greater than the previous
# False if the value in the list is smaller than the previous
# None for the initial value that has no previous value


def evaluate_window(sums):
    eval_window = [None]
    i = 1
    while i < len(sums):
        eval_window.append(sums[i - 1] < sums[i])
        i = i+1
    return eval_window


def compute_sums(list, window_size):
    sums = []
    i = 0
    while i < len(list) - window_size + 1:
        sums.append(sum(list[i:i+window_size]))
        i = i+1
    print(sums)
    return sums


    # Run the thing
if __name__ == "__main__":
    main()
