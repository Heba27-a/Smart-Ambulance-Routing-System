import sys
from PyQt5.QtWidgets import QApplication
from graph_model import CityGraph
from algorithms import bfs, dfs, uniform_cost, greedy_best_first, a_star
from ui_main import MainWindow

ALGO_MAP = {
    "BFS": bfs,
    "DFS": dfs,
    "Uniform Cost": uniform_cost,
    "Greedy Best-First": greedy_best_first,
    "A*": a_star
}

def main():
    city = CityGraph()
    city.load_from_json("data/city.json")

    app = QApplication(sys.argv)
    window = MainWindow(city, ALGO_MAP)
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()