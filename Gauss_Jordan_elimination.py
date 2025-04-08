def row_interchange(matrix, p, i):
    matrix[p], matrix[i] = matrix[i], matrix[p]
    return matrix

def gaussian_elimination_step(matrix, target_row, pivot_row, factor, start_col):
    for col in range(start_col, len(matrix[target_row])):
        matrix[target_row][col] -= factor * matrix[pivot_row][col]
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

# Forward Elimination (Gaussian) with normalization
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
    # Normalize the pivot row
    pivot_val = matrix[current_row][current_col]
    if pivot_val != 0:
        matrix[current_row] = [x / pivot_val for x in matrix[current_row]]
    # Eliminate entries below the pivot
    for r in range(current_row + 1, n):
        factor = matrix[r][current_col]
        matrix = gaussian_elimination_step(matrix, r, current_row, factor, current_col)
    current_row += 1
    current_col += 1

# Backward Elimination (Gauss-Jordan)
for i in reversed(range(current_row)):
    # Find the pivot column for row i
    pivot_col = None
    for j in range(m_vars):
        if matrix[i][j] != 0:
            pivot_col = j
            break
    if pivot_col is None:
        continue
    # Eliminate entries above the pivot
    for k in range(i-1, -1, -1):
        factor = matrix[k][pivot_col]
        matrix = gaussian_elimination_step(matrix, k, i, factor, pivot_col)

# Check for no solution
no_solution = False
for row in matrix:
    coeff = row[:-1]
    aug = row[-1]
    if all(x == 0 for x in coeff) and aug != 0:
        no_solution = True
        break

# Check for infinite solutions
infinite_solution = False
if not no_solution:
    rank = current_row
    if rank < m_vars:
        infinite_solution = True

# Prepare output

with open(output_filename, 'w') as f_out:
    # Write the augmented matrix in RREF
    for row in matrix:
        formatted_row = []
        for x in row:
            s = f"{x:.9f}"
            if '.' in s:
                s = s.rstrip('0').rstrip('.')
            formatted_row.append(s)
        f_out.write(' '.join(formatted_row) + "\n")

    # Write the solution status or solution vector   
    if no_solution:
        f_out.write("No solution")
    elif infinite_solution:
        f_out.write("Infinite solution")
    else:
        # Extract solution vector
        solution = [0.0] * m_vars
        for sol in range(m_vars):
            solution[sol] = matrix[sol][-1]

        # Format the solution
        f_out.write("Unique solution:\n" + ' '.join(f"{val:.9f}" for val in solution) + "\n")