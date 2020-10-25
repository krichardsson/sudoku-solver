import numpy as np

src = [
    ' 6  13 89',
    '      4  ',
    '  4 9  35',
    '5  94    ',
    '6       1',
    '    72  4',
    '92  3 8  ',
    '  6      ',
    '48 62  5 '
]

symbols = '123456789'

numbers = [
]

masks = {}

def initial_populate_numbers(src, numbers):
    for line in src:
        nr_line = []
        for c in line:
            nr = c
            if c == ' ':
                nr = None
            nr_line.append(nr)
        numbers.append(nr_line)

def initial_populate_masks(masks):
    for s in symbols:
        mask = []
        for i in range(9):
            line = []
            for j in range(9):
                line.append(False)
            mask.append(line)
        masks[s] = mask


def get(array, x, y):
    return array[y][x]

def set(array, x, y, val):
    array[y][x] = val

def print_horiz():
    print('|---------+---------+---------|')

def print_array(picker):
    for line_count in range(9):
        if line_count % 3 == 0:
            print_horiz()

        for col_count in range(9):
            if col_count % 3 == 0:
                print('|', end='')
            c = picker(col_count, line_count)
            print(' ' + c + ' ', end='')
        print('|')
    print_horiz()


def print_numbers(numbers):
    def picker(col, line):
        nr = get(numbers, col, line)
        if nr:
            return nr
        else:
            return ' '

    print_array(picker)

def print_mask(numbers, masks, symbol):
    def picker(x, y):
        val = get(masks[symbol], x, y)
        if val:
            return 'X'
        else:
            if get(numbers, x, y) == symbol:
                return '+'
            return ' '

    print("Mask " + symbol + ':')
    print_array(picker)

def paint_horiz(mask, x, y):
    for i in range(9):
        if int(x / 3) != int(i / 3):
            set(mask, i, y, True)

def paint_vert(mask, x, y):
    for i in range(9):
        if int(y / 3) != int(i / 3):
            set(mask, x, i, True)

def paint_box(mask, x, y):
    bx = 3 * int(x / 3)
    by = 3 * int(y / 3)
    for i in range(bx, bx + 3):
        for j in range(by, by + 3):
            if x != i or y != j:
                set(mask, i, j, True)


# Set the mask for all locations where there is a number (except this symbol)
def mask_other_numbers(numbers, mask, symbol):
    for x in range(9):
        for y in range(9):
            s = get(numbers, x, y)
            if s and s != symbol:
                set(mask, x, y, True)

# Set the mask for all locations (except the symbol location it self) in all boxes where this symbol exists
def mask_self(numbers, mask, symbol):
    for x in range(9):
        for y in range(9):
            s = get(numbers, x, y)
            if s == symbol:
                paint_box(mask, x, y)

# Find columns where the symbol forms a single line in a box and mask out the rest of those columns
def mask_single_cols(mask):
    for i in range(3):
        yb = i * 3
        for j in range(3):
            xb = j * 3
            all_masked = [True, True, True]
            for x in range(xb, xb + 3):
                for y in range(yb, yb + 3):
                    if not get(mask, x, y):
                        all_masked[x - xb] = False

            count = 0
            last_found = -1
            for i in range(3):
                masked = all_masked[i]
                if not masked:
                    count += 1
                    last_found = i

            if count == 1:
                paint_vert(mask, last_found + xb, yb)

# Find rows where the symbol forms a single line in a box and mask out the rest of those rows
def mask_single_row(mask):
    for i in range(3):
        yb = i * 3
        for j in range(3):
            xb = j * 3
            all_masked = [True, True, True]
            for x in range(xb, xb + 3):
                for y in range(yb, yb + 3):
                    if not get(mask, x, y):
                        all_masked[y - yb] = False

            count = 0
            last_found = -1
            for i in range(3):
                masked = all_masked[i]
                if not masked:
                    count += 1
                    last_found = i

            if count == 1:
                paint_horiz(mask, xb, last_found + yb)

# Search a column to see if there is one one hole in the mask
def find_single_hole_in_col(mask, x):
    count = 0
    last_found = -1
    for y in range(9):
        if not get(mask, x, y):
            count += 1
            last_found = y

    if count == 1:
        return last_found
    else:
        return None

# Search a row to see if there is one one hole in the mask
def find_single_hole_in_row(mask, y):
    count = 0
    last_found = -1
    for x in range(9):
        if not get(mask, x, y):
            count += 1
            last_found = x

    if count == 1:
        return last_found
    else:
        return None

# Search a box to see if there is one one hole in the mask
def find_single_hole_in_box(mask, x, y):
    count = 0
    last_found_x = -1
    last_found_y = -1
    xb = 3 * int(x / 3)
    yb = 3 * int(y / 3)
    for x in range(xb, xb + 3):
        for y in range(yb, yb + 3):
            if not get(mask, x, y):
                count += 1
                last_found_x = x
                last_found_y = y

    if count == 1:
        return last_found_x, last_found_y
    else:
        return None, None

# Search all masks for a location to see if there is only one possible symbol
def find_only_sym_for_position(masks, x, y):
    found = None
    count = 0
    for symbol in symbols:
        if not get(masks[symbol], x, y):
            found = symbol
            count += 1

    if count == 1:
        return found

    return None


def iterate_mask(numbers, masks, symbol):
    mask = masks[symbol]
    mask_other_numbers(numbers, mask, symbol)
    mask_self(numbers, mask, symbol)

    mask_single_cols(mask)
    mask_single_row(mask)

def iterate_number(numbers, masks, symbol):
    mask = masks[symbol]

    # Columns
    for x in range(9):
        y = find_single_hole_in_col(mask, x)
        if y and get(numbers, x, y) != symbol:
            print('found', symbol, 'in col @ ', x, y)
            set(numbers, x, y, symbol)

    # Rows
    for y in range(9):
        x = find_single_hole_in_row(mask, y)
        if x and get(numbers, x, y) != symbol:
            print('found', symbol, 'in row @ ', x, y)
            set(numbers, x, y, symbol)

    # Boxes
    for i in range(3):
        for j in range(3):
            x, y = find_single_hole_in_box(mask, i * 3, j * 3)
            if x and y and get(numbers, x, y) != symbol:
                print('found', symbol, 'in box @ ', x, y)
                set(numbers, x, y, symbol)


def iterate_single_fit(numbers, masks):
    for x in range(9):
        for y in range(9):
            symbol = find_only_sym_for_position(masks, x, y)
            if symbol and get(numbers, x, y) != symbol:
                print('found', symbol, 'as single fit @ ', x, y)
                set(numbers, x, y, symbol)


def count_reminder(numbers):
    count = 0
    for line in numbers:
        for sym in line:
            if sym == None:
                count += 1

    return count


initial_populate_numbers(src, numbers)
initial_populate_masks(masks)
print_numbers(numbers)

last_remains = 100000;
for i in range(30):
    for symbol in symbols:
        iterate_mask(numbers, masks, symbol)
        # print_mask(numbers, masks, symbol)
        iterate_number(numbers, masks, symbol)
    iterate_single_fit(numbers, masks)

    remains = count_reminder(numbers)
    print_numbers(numbers)
    print(remains, 'unsolved')
    if remains == 0 or remains == last_remains:
        break
    last_remains = remains

print()

# for symbol in symbols:
#     print_mask(numbers, masks, symbol)
