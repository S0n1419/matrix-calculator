def row_interchange(matrix, p, i):
    matrix[i], matrix[p] = matrix[p], matrix[i]
    return matrix

def gaussian_elimination_step(matrix, j, i, m):
    for col in range(i, len(matrix[j])):
        matrix[j][col] -= m * matrix[i][col]
    return matrix

input_filename = 'input.txt'
output_filename = 'output.txt'

# Read matrix from input file
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
        f_out.write("No unique solution")
    exit()

n_cols = len(matrix[0])
unique_solution = True

i = 0
while i < n_rows and i < n_cols - 1:  # Assuming augmented matrix (n_cols includes RHS)
    # Find pivot row
    p = i
    while p < n_rows and matrix[p][i] == 0:
        p += 1
    
    if p >= n_rows:
        unique_solution = False
        break
    
    if p != i:
        matrix = row_interchange(matrix, p, i)
    
    pivot_val = matrix[i][i]
    if pivot_val == 0:
        unique_solution = False
        break
    
    # Eliminate below
    for j in range(i + 1, n_rows):
        m = matrix[j][i] / pivot_val
        matrix = gaussian_elimination_step(matrix, j, i, m)
    
    i += 1

# Check for zero on diagonal in RREF
if unique_solution:
    for i in range(min(n_rows, n_cols - 1)):
        if matrix[i][i] == 0:
            unique_solution = False
            break

# Write output
with open(output_filename, 'w') as f_out:
    if not unique_solution:
        f_out.write("No unique solution")
    else:
        for row in matrix:
            f_out.write(' '.join(f"{val:.9f}" for val in row) + '\n')