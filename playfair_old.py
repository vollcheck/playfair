#!/usr/bin/python3

import cgi

# -- CGI definitions
print("Content-Type: text/plain")

# -- Constants
DEBUG = False
WIDTH = 5
R_CHAR = "x"
LETTERS = "abcdefghiklmnopqrstuvwxyz"

# -- List functions
def get_rowal(board, x, y, decrypt = False):
    move = 1 if not decrypt else -1

    for row in board:
        try:
            x_idx = row.index(x)
            y_idx = row.index(y)
        except ValueError:
            continue

        if x_idx >= 0 and y_idx >= 0:
            return (row[(x_idx + move) % WIDTH] +
                    row[(y_idx + move) % WIDTH])

    else:
        return False


def transpose(board):
    return [[row[i] for row in board]
            for i in range(len(board[0]))]

# prolly that function might be merged and simplified
# with get_rowal
def get_columnar(board, x, y, decrypt = False):
    move = 1 if not decrypt else -1

    transposed = transpose(board)
    for row in transposed:
        try:
            x_idx = row.index(x)
            y_idx = row.index(y)
        except ValueError:
            continue

        if x_idx >= 0 and y_idx >= 0:
            return (row[(x_idx + move) % WIDTH] +
                    row[(y_idx + move) % WIDTH])

    else:
        return False

def get_coords(board, char):
    for row_idx, row in enumerate(board):
        for c_idx, c in enumerate(row):
            if c == char:
                return [row_idx, c_idx]

def get_contrary(board, x, y):
    if DEBUG:
        print("Processing " + x + " and " + y)

    x_row, x_col = get_coords(board, x)
    y_row, y_col = get_coords(board, y)

    return board[x_row][y_col] + board[y_row][x_col]

def make_diags(content):
    content = content.replace(" ", "")
    content = content.replace("j", "i")

    output = []

    for i in range(0, len(content), 2):
        try:
            f = content[i]
            s = content[i+1]
        except IndexError:
            print(f"last letter '{f}' has no pair")
            # if there is no second letter
            s = R_CHAR

        # if both letters are the same, add "x" and move cursor back
        if f == s:
            print(f"found the same: {f}")
            s = R_CHAR
            i -= 1

        output.append(f + s)

    return output


def make_board(keyword):
    keyword = keyword.replace("j", "i")
    ordered = "".join(list(dict.fromkeys(keyword)))
    board_content = "".join(list(dict.fromkeys(ordered + LETTERS)))

    board = [["x"]*WIDTH for _ in range(WIDTH)]
    for x in range(WIDTH):
        for y in range(WIDTH):
            board[x][y] = board_content[x * WIDTH + y]

    return board

def pp_board(board):
    for row in board:
        print(" ".join(row))

def encrypt(keyword, content):
    board = make_board(keyword)
    diags = make_diags(content)

    output = ""

    for diag in diags:
        f, s = diag
        output += (get_rowal(board, f, s)
                   or get_columnar(board, f, s)
                   or get_contrary(board, f, s))

    return output

def decrypt(keyword, content):
    board = make_board(keyword)
    diags = make_diags(content)

    output = ""

    for diag in diags:
        f, s = diag
        output += (get_rowal(board, *diag, False)
                   or get_columnar(board, *diag, False)
                   or get_contrary(board, *diag))

    return output


# -- Input handling
# args = cgi.parse()

args = {"keyword": "szyfr",
        "content": "wikipedia jest najlepsza",
        "decrypt": False}

keyword = args["keyword"]
content = args["content"]
decrypt = bool(args["decrypt"])

if not decrypt:
    print(encrypt(keyword, content))
else:
    print(decrypt(keyword, content))
