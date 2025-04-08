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

# Initialize lower and upper matrices
lower = [[0.0 for _ in range(mat_size)] for _ in range(mat_size)]
upper = [[0.0 for _ in range(mat_size)] for _ in range(mat_size)]

# Doolittle's algorithm: L has ones on the diagonal
for i in range(mat_size):
    lower[i][i] = 1.0

# Perform LU decomposition
for i in range(mat_size):
    # Calculate upper matrix for row i
    for j in range(i, mat_size):
        upper[i][j] = A[i][j] - sum(lower[i][k] * upper[k][j] for k in range(i))
    
    # Check for zero pivot in U
    if upper[i][i] == 0.0:
        with open(output_filename, 'w') as f_out:
            f_out.write("Factorization impossible\n")
        exit()
    
    # Calculate lower matrix for column i
    for j in range(i + 1, mat_size):
        lower[j][i] = (A[j][i] - sum(lower[j][k] * upper[k][i] for k in range(i))) / upper[i][i]

# Solve Ly = b using forward substitution
y = [0.0] * mat_size
for i in range(mat_size):
    y[i] = b[i] - sum(lower[i][k] * y[k] for k in range(i))

# Solve Ux = y using backward substitution
x = [0.0] * mat_size
for i in range(mat_size - 1, -1, -1):
    x[i] = (y[i] - sum(upper[i][k] * x[k] for k in range(i + 1, mat_size))) / upper[i][i]

# Write the results to the output file
with open(output_filename, 'w') as f_out:
    # Write L matrix
    for row in lower:
        f_out.write(' '.join(f"{val:.9f}" for val in row) + '\n')
    f_out.write('\n')
    # Write U matrix
    for row in upper:
        f_out.write(' '.join(f"{val:.9f}" for val in row) + '\n')
    f_out.write('\n')
    # Write solutions
    f_out.write("Temporary solution (y):\n" + ' '.join(f"{val:.9f}" for val in y) + '\n')
    f_out.write("Unique solution (x):\n" + ' '.join(f"{val:.9f}" for val in x) + '\n')