

def main():
    infile = 'input'
    with open(infile) as input:
        process_file(input)


def process_file(input):
    raw_lines = input.readlines()
    parsed_instructions = [line.strip().split() for line in raw_lines]
    position = determine_position(parsed_instructions)
    print(position)
    print(position[0]*position[1])


def determine_position(movements):
    horizontal = 0
    depth = 0
    # down is up, so aiming down is encoded positive, aiming up encoded negative
    aim = 0
    for command in movements:
        instruction, movement = command
        movement = int(movement)
        if instruction == 'forward':
            horizontal = horizontal + movement
            depth = depth + aim * movement
        elif instruction == 'down':
            aim = aim + movement
        elif instruction == 'up':
            aim = aim - movement
        else:
            pass
    return (horizontal, depth)


if __name__ == "__main__":
    main()
