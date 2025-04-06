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

mat_size = len(matrix)

# Initialize upper and lower matrices with zeros
upper = [[0.0 for _ in range(mat_size)] for _ in range(mat_size)]
lower = [[0.0 for _ in range(mat_size)] for _ in range(mat_size)]

# Set the diagonal of L to 1
for i in range(mat_size):
    lower[i][i] = 1.0

# Check if the first pivot is zero
upper[0][0] = matrix[0][0]
if lower[0][0] * upper[0][0] == 0:
    with open(output_filename, 'w') as f_out:
        f_out.write('Factorization impossible')
    exit()

# Compute first row of U and first column of L
for j in range(1, mat_size):
    upper[0][j] = matrix[0][j] / lower[0][0]
    lower[j][0] = matrix[j][0] / upper[0][0]

for i in range(1, mat_size - 1):
    upper[i][i] = matrix[i][i]
    for k in range(i):  # Corrected range to start from 0
        upper[i][i] -= lower[i][k] * upper[k][i]
    
    if lower[i][i] * upper[i][i] == 0:
        with open(output_filename, 'w') as f_out:
            f_out.write('Factorization impossible')
        exit()
    
    for j in range(i + 1, mat_size):  # Corrected 'n' to 'mat_size'
        upper[i][j] = matrix[i][j]
        lower[j][i] = matrix[j][i]
        for k in range(i):  # Corrected range to start from 0
            upper[i][j] -= lower[i][k] * upper[k][j]
            lower[j][i] -= lower[j][k] * upper[k][i]
        upper[i][j] /= lower[i][i]
        lower[j][i] /= upper[i][i]

# Compute the last element of U
upper[mat_size-1][mat_size-1] = matrix[mat_size-1][mat_size-1]
for k in range(mat_size-1):
    upper[mat_size-1][mat_size-1] -= lower[mat_size-1][k] * upper[k][mat_size-1]

# Check if the last pivot is valid
if lower[mat_size-1][mat_size-1] * upper[mat_size-1][mat_size-1] == 0:
    with open(output_filename, 'w') as f_out:
        f_out.write('Factorization impossible')
    exit()

# Write the results
with open(output_filename, 'w') as f_out:
    for row in lower:
        f_out.write(' '.join(f"{val:.9f}" for val in row) + '\n')
    f_out.write('\n')
    for row in upper:
        f_out.write(' '.join(f"{val:.9f}" for val in row) + '\n')