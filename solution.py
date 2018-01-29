import sys
print('Python version:', sys.version)

import nqueens as nq

try:
	solver=nq.Solver_8_queens()
	best_fit, epoch_num, visualization = solver.solve()
	print("Best solution:")
	print("Fitness:", best_fit)
	print("Iterations:", epoch_num)
	print(visualization)

except Exception as e:
	print('exception:', e)

input()