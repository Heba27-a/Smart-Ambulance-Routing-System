from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QComboBox, QTableWidget, QTableWidgetItem,
    QGraphicsScene, QGraphicsView, QGraphicsLineItem, QGraphicsEllipseItem,
    QMessageBox
)
from PyQt5.QtGui import QPen, QColor, QPixmap
from PyQt5.QtCore import Qt
import sys
import os


class MainWindow(QMainWindow):
    def __init__(self, city, algorithms):
        super().__init__()

        self.city = city
        self.algorithms = algorithms
        self.setWindowTitle("🚑 Smart Ambulance Routing")
        self.setGeometry(100, 100, 1000, 700)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout()
        central.setLayout(layout)

        # Top bar
        top_bar = QHBoxLayout()
        self.start_combo = QComboBox()
        self.goal_combo = QComboBox()
        self.algo_combo = QComboBox()
        self.calc_btn = QPushButton("Calculate Route")

        top_bar.addWidget(QLabel("Start:"))
        top_bar.addWidget(self.start_combo)
        top_bar.addWidget(QLabel("Goal:"))
        top_bar.addWidget(self.goal_combo)
        top_bar.addWidget(QLabel("Algorithm:"))
        top_bar.addWidget(self.algo_combo)
        top_bar.addWidget(self.calc_btn)

        layout.addLayout(top_bar)

        # Graph area
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        layout.addWidget(self.view)

        # Table (added Status column)
        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["Route", "Distance", "Traffic", "Status"])
        layout.addWidget(self.table)

        self.statusBar().showMessage("Ready")

        # Assets directory
        base_dir = os.path.dirname(os.path.abspath(__file__))
        # تأكدي إن اسم المجلد assets
        self.assets_dir = os.path.join(base_dir, 'assets')

        self._setup_data()

        # Actions
        self.calc_btn.clicked.connect(self._compute_route)
        # إعادة الرسم تلقائيًا عند تغيير Start/Goal
        self.start_combo.currentTextChanged.connect(lambda _: self._draw_graph())
        self.goal_combo.currentTextChanged.connect(lambda _: self._draw_graph())

    def _setup_data(self):
        nodes = list(self.city.G.nodes)
        self.start_combo.addItems(nodes)
        self.goal_combo.addItems(nodes)
        self.algo_combo.addItems(list(self.algorithms.keys()))

        # Fill table
        self.table.setRowCount(0)
        for u, v, data in self.city.G.edges(data=True):
            row = self.table.rowCount()
            self.table.insertRow(row)

            # Route
            route_item = QTableWidgetItem(f"{u}-{v}")
            self.table.setItem(row, 0, route_item)

            # Distance
            dist = float(data.get('distance', 0))
            dist_item = QTableWidgetItem(str(dist))
            self.table.setItem(row, 1, dist_item)

            # Traffic
            traffic = float(data.get('traffic', 0))
            traffic_item = QTableWidgetItem(str(traffic))
            self.table.setItem(row, 2, traffic_item)

            # Status
            is_closed = bool(data.get("closed", False))
            status = "Closed" if is_closed else "Open"
            status_item = QTableWidgetItem(status)

            # Highlighting in table
            if is_closed:
                # Closed: red background
                status_item.setBackground(QColor("red"))
                status_item.setForeground(QColor("white"))
                # Optional: also tint route cell red for clarity
                route_item.setBackground(QColor(255, 200, 200))
            elif traffic > 0.4:
                # High traffic: yellow background
                traffic_item.setBackground(QColor(255, 245, 157))  # soft yellow
            if dist > 5:
                # Long distance: orange hint
                dist_item.setBackground(QColor(255, 213, 128))  # soft orange

            self.table.setItem(row, 3, status_item)

        # Draw graph initially
        self._draw_graph()

    def _draw_graph(self, path=None):
        self.scene.clear()

        # Get current Start and Goal selections
        start = self.start_combo.currentText()
        goal = self.goal_combo.currentText()

        # Draw edges (roads)
        for u, v, data in self.city.G.edges(data=True):
            x1, y1 = self.city.positions[u]
            x2, y2 = self.city.positions[v]
            line = QGraphicsLineItem(x1*100, y1*100, x2*100, y2*100)

            # Default color
            color = QColor("red") if data.get("closed", False) else QColor("green")
            # If path provided, highlight edges that belong to the path in blue
            if path:
                # edge belongs to path if u-v are consecutive in path
                for i in range(len(path) - 1):
                    if (path[i] == u and path[i+1] == v) or (path[i] == v and path[i+1] == u):
                        color = QColor("blue")
                        break

            line.setPen(QPen(color, 3))
            self.scene.addItem(line)

            # Add traffic light icon if traffic is high
            if float(data.get("traffic", 0)) > 0.4:
                pixmap = QPixmap(os.path.join(self.assets_dir, "traffic_light.png")).scaled(25, 25, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                icon_item = self.scene.addPixmap(pixmap)
                mid_x = (x1 + x2) / 2 * 100
                mid_y = (y1 + y2) / 2 * 100
                icon_item.setPos(mid_x - 12, mid_y - 12)

            # Add barrier icon if road is closed
            if bool(data.get("closed", False)):
                pixmap = QPixmap(os.path.join(self.assets_dir, "barrier.png")).scaled(25, 25, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                icon_item = self.scene.addPixmap(pixmap)
                mid_x = (x1 + x2) / 2 * 100
                mid_y = (y1 + y2) / 2 * 100
                icon_item.setPos(mid_x + 12, mid_y + 12)

        # Draw nodes
        for n, (x, y) in self.city.positions.items():
            ellipse = QGraphicsEllipseItem(x*100-10, y*100-10, 20, 20)
            ellipse.setBrush(QColor("black"))
            self.scene.addItem(ellipse)

            label = self.scene.addText(n)
            label.setPos(x*100-10, y*100-30)

            # Icon for Start node (Ambulance)
            if n == start:
                pixmap = QPixmap(os.path.join(self.assets_dir, "ambulance.png")).scaled(30, 30, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                item = self.scene.addPixmap(pixmap)
                item.setPos(x*100-20, y*100-20)

            # Icon for Goal node (Hospital)
            if n == goal:
                pixmap = QPixmap(os.path.join(self.assets_dir, "hospital.png")).scaled(30, 30, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                item = self.scene.addPixmap(pixmap)
                item.setPos(x*100-20, y*100-20)

    def _compute_route(self):
        start = self.start_combo.currentText()
        goal = self.goal_combo.currentText()
        algo_name = self.algo_combo.currentText()
        algo = self.algorithms[algo_name]

        path, cost = algo(self.city, start, goal)
        if path is None:
            QMessageBox.warning(self, "No Route Found", "There is no available path.")
            # still redraw to update icons if Start/Goal changed
            self._draw_graph()
            return

        self._draw_graph(path)
        self.statusBar().showMessage(f"Path: {' -> '.join(path)} | Cost: {round(cost, 2)}")