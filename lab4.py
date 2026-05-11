import numpy as np
import random
import json
import matplotlib.pyplot as plt

def generate_map():
    N = random.randint(25, 35)

    coords = np.random.randint(0, 500, size=(N, 2))
    distances = np.zeros((N, N))

    for i in range(N):
        for j in range(i + 1, N):
            dist = np.linalg.norm(coords[i] - coords[j])
            distances[i][j] = distances[j][i] = dist / 5 + 10

    return distances, coords


def save_data(distances, coords, filename="map_data.json"):
    with open(filename, "w") as f:
        json.dump({
            "distances": distances.tolist(),
            "coords": coords.tolist()
        }, f)


def load_data(filename="map_data.json"):
    with open(filename, "r") as f:
        data = json.load(f)
        return np.array(data["distances"]), np.array(data["coords"])

class AntColony:

    def __init__(self,
                 distances,
                 n_ants=20,
                 n_iterations=50,
                 alpha=1,
                 beta=5,
                 rho=0.5):

        self.distances = distances
        self.N = len(distances)

        self.n_ants = n_ants
        self.n_iterations = n_iterations

        self.alpha = alpha
        self.beta = beta
        self.rho = rho

        self.pheromone = np.ones((self.N, self.N))

        dist_inv = 1.0 / (self.distances + np.eye(self.N) * 1e-9)
        self.eta = dist_inv ** self.beta

    def calculate_length(self, route):
        length = sum(
            self.distances[route[i], route[i + 1]]
            for i in range(len(route) - 1)
        )
        length += self.distances[route[-1], route[0]]
        return length

    def construct_solution(self, move_probs):

        route = [random.randint(0, self.N - 1)]
        visited = {route[0]}

        while len(route) < self.N:
            curr = route[-1]

            probs = np.copy(move_probs[curr])
            probs[list(visited)] = 0

            probs /= probs.sum()

            next_city = np.random.choice(self.N, p=probs)

            route.append(next_city)
            visited.add(next_city)

        return route

    def run(self):

        best_route = None
        best_len = float('inf')

        for _ in range(self.n_iterations):

            move_probs = (self.pheromone ** self.alpha) * self.eta
            routes = []

            for _ in range(self.n_ants):

                route = self.construct_solution(move_probs)
                length = self.calculate_length(route)

                routes.append((route, length))

                if length < best_len:
                    best_len = length
                    best_route = route

            self.pheromone *= (1 - self.rho)

            for r, l in routes:
                deposit = 100 / l

                for i in range(len(r) - 1):
                    a, b = r[i], r[i + 1]
                    self.pheromone[a][b] += deposit
                    self.pheromone[b][a] += deposit

        return best_route, best_len

if __name__ == "__main__":

    try:
        distances, coords = load_data()
        print("Карту завантажено з файлу.")
    except:
        distances, coords = generate_map()
        save_data(distances, coords)
        print("Згенеровано нову карту.")

    ants_list = [10, 30]
    rho_list = [0.3, 0.7]
    alpha_beta = [(1, 3), (1, 5)]

    print("\nЗАПУСК СИМУЛЯЦІЙ:")

    for ants in ants_list:
        for rho in rho_list:
            for a, b in alpha_beta:

                lengths = []

                for _ in range(10):
                    colony = AntColony(
                        distances,
                        n_ants=ants,
                        rho=rho,
                        alpha=a,
                        beta=b,
                        n_iterations=40
                    )

                    _, l = colony.run()
                    lengths.append(l)

                avg = np.mean(lengths)

                print(
                    f"Ants:{ants} | Rho:{rho} | a/b:{a}/{b} -> Avg Length: {avg:.2f}"
                )

    print("\nБудуємо фінальний маршрут...")

    final_colony = AntColony(
        distances,
        n_ants=40,
        n_iterations=100
    )

    best_path, best_dist = final_colony.run()

    plt.figure(figsize=(10, 7))

    plt.scatter(coords[:, 0], coords[:, 1],
                c='red',
                edgecolors='black',
                s=100,
                zorder=3)

    for i, (x, y) in enumerate(coords):
        plt.text(x + 5, y + 5, str(i),
                 fontsize=12,
                 fontweight='bold')

    for i in range(len(best_path)):
        p1 = best_path[i]
        p2 = best_path[(i + 1) % len(best_path)]

        x1, y1 = coords[p1]
        x2, y2 = coords[p2]

        plt.arrow(
            x1, y1,
            x2 - x1,
            y2 - y1,
            length_includes_head=True,
            head_width=8,
            head_length=12,
            fc='blue',
            ec='blue',
            alpha=0.7
        )

    start_city = best_path[0]
    plt.scatter(coords[start_city, 0],
                coords[start_city, 1],
                c='green',
                s=250,
                label="START",
                zorder=5)

    finish_city = best_path[-1]
    plt.scatter(coords[finish_city, 0],
                coords[finish_city, 1],
                c='purple',
                s=250,
                label="FINISH",
                zorder=5)

    plt.title(f"Найкращий маршрут (довжина: {best_dist:.2f})")
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.5)

    plt.show()