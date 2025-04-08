import math

input_filename = 'input.txt'
output_filename = 'output.txt'

# Read the augmented matrix from the input file
augmented_matrix = []
with open(input_filename, 'r') as f_in:
    for line in f_in:
        stripped_line = line.strip()
        if stripped_line:
            row = [float(val) for val in stripped_line.replace(',', ' ').split()]
            augmented_matrix.append(row)

mat_size = len(augmented_matrix)
if mat_size == 0:
    with open(output_filename, 'w') as f_out:
        f_out.write("Empty input.\n")
    exit()

# Validate each row has exactly mat_size + 1 elements
for row in augmented_matrix:
    if len(row) != mat_size + 1:
        with open(output_filename, 'w') as f_out:
            f_out.write("Invalid input: each row must have n+1 elements for an n x n system.\n")
        exit()

# Split into coefficient matrix A and constants vector b
A = [row[:-1] for row in augmented_matrix]
b = [row[-1] for row in augmented_matrix]

# Check if the matrix is symmetric
is_symmetric = True
for i in range(mat_size):
    for j in range(mat_size):
        if A[i][j] != A[j][i]:
            is_symmetric = False
            break
    if not is_symmetric:
        break
if not is_symmetric:
    with open(output_filename, 'w') as f_out:
        f_out.write("Matrix is not symmetric\n")
    exit()

# Initialize the lower triangular matrix
lower = [[0.0 for _ in range(mat_size)] for _ in range(mat_size)]

# Perform Cholesky factorization
try:
    for i in range(mat_size):
        for j in range(i+1):
            sum_val = sum(lower[i][k] * lower[j][k] for k in range(j))
            if i == j:
                if A[i][i] - sum_val <= 0:
                    raise ValueError("Matrix is not positive definite")
                lower[i][j] = math.sqrt(A[i][i] - sum_val)
            else:
                lower[i][j] = (A[i][j] - sum_val) / lower[j][j]
except ValueError as e:
    with open(output_filename, 'w') as f_out:
        f_out.write(f"Factorization impossible: {e}\n")
    exit()

# Upper triangular matrix is the transpose of lower
upper = [[lower[j][i] for j in range(mat_size)] for i in range(mat_size)]

# Solve Ly = b using forward substitution
y = [0.0] * mat_size
for i in range(mat_size):
    sum_val = sum(lower[i][k] * y[k] for k in range(i))
    y[i] = (b[i] - sum_val) / lower[i][i]

# Solve Ux = y using backward substitution
x = [0.0] * mat_size
for i in range(mat_size-1, -1, -1):
    sum_val = sum(upper[i][k] * x[k] for k in range(i+1, mat_size))
    x[i] = (y[i] - sum_val) / upper[i][i]

# Write results to the output file
with open(output_filename, 'w') as f_out:
    for row in lower:
        f_out.write(' '.join(f"{val:.9f}" for val in row) + '\n')
    for row in upper:
        f_out.write(' '.join(f"{val:.9f}" for val in row) + '\n')
    f_out.write("\nTemporary solution (y):\n" + ' '.join(f"{val:.9f}" for val in y) + '\n')
    f_out.write("Unique solution (x):\n" + ' '.join(f"{val:.9f}" for val in x) + '\n')