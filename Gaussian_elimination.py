def row_interchange(matrix, p, i):
    matrix[p], matrix[i] = matrix[i], matrix[p]
    return matrix

def gaussian_elimination_step(matrix, j, i, m):
    for col in range(len(matrix[j])):
        matrix[j][col] -= m * matrix[i][col]
    return matrix

input_filename = 'input.txt'
output_filename = 'output.txt'

# Read the augmented matrix from input file
matrix = []

with open(input_filename, 'r') as f_in:
    for line in f_in:
        stripped_line = line.strip()
        if stripped_line:
            row = [float(val) for val in stripped_line.replace(',', ' ').split()]
            matrix.append(row)

n_rows = len(matrix)
if n_rows == 0:
    with open(output_filename, 'w') as f_out:
        f_out.write("No entry")
    exit()

n_cols = len(matrix[0]) if n_rows > 0 else 0
if n_cols == 0:
    with open(output_filename, 'w') as f_out:
        f_out.write("No entry")
    exit()

current_row = 0
current_col = 0
n = n_rows
m_vars = n_cols - 1  # Number of variables (excluding augmented column)

# Perform Gaussian elimination
while current_row < n and current_col < m_vars:
    # Find the pivot in current_col starting from current_row
    pivot_row = None
    for r in range(current_row, n):
        if matrix[r][current_col] != 0:
            pivot_row = r
            break
    if pivot_row is None:
        current_col += 1
        continue
    # Swap current_row with pivot_row
    if pivot_row != current_row:
        matrix = row_interchange(matrix, current_row, pivot_row)
    # Eliminate entries below current_row in current_col
    pivot_val = matrix[current_row][current_col]
    for r in range(current_row + 1, n):
        factor = matrix[r][current_col] / pivot_val
        matrix = gaussian_elimination_step(matrix, r, current_row, factor)
    current_row += 1
    current_col += 1

# Check for no solution
no_solution = False
for row in matrix:
    coeff = row[:-1]
    aug = row[-1]
    if all(x == 0 for x in coeff) and aug != 0:
        no_solution = True
        break

infinite_solution = False
if not no_solution:
    # Determine the rank (number of non-zero rows in coefficient part)
    rank = current_row  # Since current_row is the number of pivots found
    if rank < m_vars:
        infinite_solution = True

with open(output_filename, 'w') as f_out:
    if no_solution:
        f_out.write("No solution")
    elif infinite_solution:
        f_out.write("Infinite solution")
    else:
        for row in matrix:
            formatted_row = ' '.join([f"{x:.9f}".rstrip('0').rstrip('.') if '.' in f"{x:.9f}" else f"{x:.9f}" for x in row])
            f_out.write(formatted_row + "\n")

        solution = [0.0] * m_vars
        for row in range(n_rows - 1, -1, -1):
            solution[row] = matrix[row][- 1]
            for temp in range(row + 1, n_rows):
                solution[row] -= matrix[row][temp] * solution[temp]
            solution[row] = solution[row] / matrix[row][row]
        f_out.write("Unique solution:\n" + ' '.join(f"{val:.9f}" for val in solution) + "\n")
