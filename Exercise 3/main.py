import matplotlib.pyplot as plt
import generator
import time

t_0 = time.time()

level = 3
L     = 1
points = generator.boks(level, L)
t_fractal_done = time.time() 







t_lattice = time.time()
lattice = generator.make_lattice(points, level, L)

t_plot = time.time()
plt.plot(*zip(*points))
plt.matshow(lattice)

print(f"""time to make fractal:       {t_fractal_done - t_0}
time to make lattice:       {t_plot - t_lattice}
time to plot it all:        {time.time() - t_plot}
time of total simulation:   {time.time() - t_0}""") 

plt.show()

