import numpy as np

def make_data_himmelblau(p_X, p_Y):
    x = np.linspace(-p_X, p_X, 100)
    y = np.linspace(-p_Y, p_Y, 100)

    x_grid, y_grid = np.meshgrid(x, y)

    z = himmelblau(np.array([x_grid, y_grid]))
    return x_grid, y_grid, z

def himmelblau(x):
    return (x[0]**2+x[1]-11)**2 + (x[0]+x[1]**2-7)**2

def himmelblau_2(x, y):
    return (x**2+y-11)**2 + (x+y**2-7)**2

def make_data_rosenbrock(p_X, p_Y):
    x = np.linspace(-p_X, p_X, 100)
    y = np.linspace(-p_Y, p_Y, 100)

    x_grid, y_grid = np.meshgrid(x, y)

    z = rosenbrock(np.array([x_grid, y_grid]))
    return x_grid, y_grid, z

def rosenbrock(x):
    return np.sum(100.0 * (x[1:] - x[:-1] ** 2.0) ** 2.0 + (1 - x[:-1]) ** 2.0, axis=0)

def rosenbrock_2(x, y):
    return (1.0 - x) ** 2 + 100.0 * (y - x * x) ** 2



