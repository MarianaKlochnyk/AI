import random
import math
import matplotlib.pyplot as plt

def test_function(x):
    return math.cos(x) + 1

def main_function(x):
    return math.exp(x**2)

def f(x, mode="test"):
    if mode == "test":
        return test_function(x)
    else:
        return main_function(x)

def exact_test_integral():
    return math.pi / 2 + 1

def random_point(a, b, M):
    x = random.uniform(a, b)
    y = random.uniform(0, M)
    return x, y

def monte_carlo(a, b, N, mode="test"):
    xs = [a + (b - a) * i / 5000 for i in range(5001)]
    M = max(f(x, mode) for x in xs)

    inside = 0

    x_inside = []
    y_inside = []
    x_outside = []
    y_outside = []

    rectangle_area = (b - a) * M

    for _ in range(N):
        x, y = random_point(a, b, M)

        if y <= f(x, mode):
            inside += 1
            x_inside.append(x)
            y_inside.append(y)
        else:
            x_outside.append(x)
            y_outside.append(y)

    area = (inside / N) * rectangle_area

    return area, x_inside, y_inside, x_outside, y_outside, M

def plot_result(a, b, mode, x_in, y_in, x_out, y_out):
    xs = [a + (b - a) * i / 500 for i in range(501)]
    ys = [f(x, mode) for x in xs]

    plt.figure(figsize=(8, 5))

    plt.plot(xs, ys, label="f(x)")
    plt.scatter(x_in, y_in, s=5, label="під графіком")
    plt.scatter(x_out, y_out, s=5, label="над графіком")

    plt.title("Метод Монте-Карло")
    plt.legend()
    plt.show()

N = 50000

a, b = 0, math.pi / 2

approx, xi, yi, xo, yo, M = monte_carlo(a, b, N, "test")
exact = exact_test_integral()

abs_error = abs(exact - approx)
rel_error = abs_error / exact
rel_error_percent = rel_error * 100

print("=== ТЕСТОВА ФУНКЦІЯ f(x) = cos(x) + 1 ===")
print("Оцінка інтеграла:", approx)
print("Точне значення:", exact)
print("Абсолютна похибка:", abs_error)
print(f"Відносна похибка: {rel_error_percent:.2f}%")

plot_result(a, b, "test", xi, yi, xo, yo)

a, b = 1, 2

approx, xi, yi, xo, yo, M = monte_carlo(a, b, N, "main")

print("\n=== ОСНОВНА ФУНКЦІЯ f(x) = e^(x^2) ===")
print("Оцінка інтеграла:", approx)

plot_result(a, b, "main", xi, yi, xo, yo)