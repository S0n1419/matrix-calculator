def row_interchange(matrix, p, i):
    matrix[i], matrix[p] = matrix[p], matrix[i]
    return matrix

def gaussian_elimination_step(matrix, j, i, m):
    for col in range(i, len(matrix[j])):
        matrix[j][col] -= m * matrix[i][col]
    return matrix

input_filename = 'input.txt'
output_filename = 'output.txt'

# Read augmented matrix from input file
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

n_cols = len(matrix[0])
if n_cols == 0:
    with open(output_filename, 'w') as f_out:
        f_out.write("No entry")
    exit()

unique_solution = True

i = 0
while i < n_rows and i < n_cols - 1:  # Process each column (variable)
    # Find pivot row
    p = i
    while p < n_rows and matrix[p][i] == 0:
        p += 1
    
    if p >= n_rows:  # No pivot found in this column
        unique_solution = False
        break
    
    if p != i:
        matrix = row_interchange(matrix, p, i)
    
    pivot_val = matrix[i][i]
    # Eliminate below
    for j in range(i + 1, n_rows):
        m = matrix[j][i] / pivot_val
        matrix = gaussian_elimination_step(matrix, j, i, m)
    
    i += 1

# Check if all variables have a pivot (i.e., number of pivots equals number of variables)
if i < (n_cols - 1):
    unique_solution = False

# Write output
with open(output_filename, 'w') as f_out:
    if not unique_solution:
        f_out.write("No unique solution")
    else:
        n = n_rows
        solution = [0.0] * n
        
        # Start from last row (backward substitution)
        solution[n-1] = matrix[n-1][n] / matrix[n-1][n-1]
        
        # Iterate upward from n-2 to 0
        for i in range(n-2, -1, -1):
            sum_ax = 0.0
            # Sum known solutions multiplied by their coefficients
            for j in range(i+1, n):
                sum_ax += matrix[i][j] * solution[j]
            # Calculate current variable
            solution[i] = (matrix[i][n] - sum_ax) / matrix[i][i]
        
        # Format output with 9 decimal places
        f_out.write(' '.join(f"{x:.9f}" for x in solution))
