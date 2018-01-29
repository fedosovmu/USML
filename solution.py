import sys
import time
import math
print('Python version:', sys.version)

import nqueens as nq


for i in range(92):
    print("Solution:", i+1)
    start_time = time.time()
    solver = nq.Solver_8_queens()
    best_fit, epoch_num, visualization = solver.solve()
    end_time = time.time()
    runtime = end_time - start_time
    print("Best solution:")
    print("Fitness: " + str(best_fit), end = ' ')
    if (best_fit == 1):
        print("TRUE")
    else:
        print("FALSE")
    print("Iterations:", epoch_num)
    print("runtime:", runtime)
    print(visualization)
