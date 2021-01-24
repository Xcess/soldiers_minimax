import sys
import csv
import math


def possible_moves(state, player):
    moves = []
    rows = len(state)
    columns = len(state[0])
    for i, row in enumerate(state):
        for j, cell in enumerate(row):
            if cell != player:
                continue

            enemy = -1 * player
            next_row = i + 1 * player
            attack_col_right = j + 1
            attack_col_left = j - 1

            if next_row > rows - 1 or next_row < 0:
                continue

            if state[next_row][j] == 0:
                moves.append(((i, j), (next_row, j)))

            if attack_col_right < columns - 1 and attack_col_right > 0:
                if state[next_row][attack_col_right] == enemy:
                    moves.append(((i, j), (next_row, attack_col_right)))

            if attack_col_left < columns - 1 and attack_col_left > 0:
                if state[next_row][attack_col_left] == enemy:
                    moves.append(((i, j), (next_row, attack_col_left)))
    return moves


def game_over(state, player):
    return len(possible_moves(state, player)) == 0


def evaluate(state):
    score = 0
    for cell in state[-1]:
        if cell == 1:
            score += 1
    for cell in state[0]:
        if cell == -1:
            score += -1
    return score


def apply_move(state, move):
    src = move[0]
    dst = move[1]
    state[dst[0]][dst[1]] = state[src[0]][src[1]]
    state[src[0]][src[1]] = 0


def from_csv(filename):
    data = csv.reader(open(filename))
    data = [list(map(int, row)) for row in data]

    return data


def to_csv(state, file=sys.stdout):
    writer = csv.writer(file)
    writer.writerows(state)


def stats(state, best):
    print(f"{best[0]}->{best[1]}\n")
    new_state = state.copy()
    apply_move(new_state, best)
    to_csv(new_state)
    print()


def minimax(state, depth, player):
    if player == 1:
        best = [None, None, -math.inf]
    else:
        best = [None, None, +math.inf]

    if depth == 0 or game_over(state, player):
        score = evaluate(state)
        return [None, None, score]

    for move in possible_moves(state, player):
        new_state = [x[:] for x in state]
        apply_move(new_state, move)
        score = minimax(new_state, depth - 1, -player)
        score[0], score[1] = move[0], move[1]

        if player == 1:
            if score[2] > best[2]:
                best = score
        else:
            if score[2] < best[2]:
                best = score
    return best


def main():
    if len(sys.argv) != 3:
        print("Usage: ./p3.py map.csv moves.txt")
        sys.exit(1)
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    state = from_csv(input_path)
    score = minimax(state, math.inf, 1)

    print(f"Finished with score {score[2]}\nLast Move: {score[0]}->{score[1]}")

    with open(input_path, "w") as f:
        apply_move(state, score)
        to_csv(state, f)

    with open(output_path, "a") as f:
        f.write(
            "[{},{}]->[{},{}]\n".format(
                score[0][0], score[0][1], score[1][0], score[1][1]
            )
        )


if __name__ == "__main__":
    main()
