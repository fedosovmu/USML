import sys
import time
print('Python version:', sys.version)

import nqueens as nq

start_time = time.time()
solver = nq.Solver_8_queens()
best_fit, epoch_num, visualization = solver.solve()
end_time = time.time()
time = end_time - start_time
print("Best solution:")
print("Fitness:", best_fit)
print("Iterations:", epoch_num)
print("time:", time)
print(visualization)
