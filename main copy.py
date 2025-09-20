import sys
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Tabla de resultados")
        self.setGeometry(100, 100, 600, 400)

        # Crear un layout vertical
        layout = QVBoxLayout()

        # Crear el QTableWidget
        self.table = QTableWidget()
        layout.addWidget(self.table)

        # Configurar el número de columnas
        self.table.setColumnCount(3)  # # Juego, Equipo ganador, Puntaje
        self.table.setHorizontalHeaderLabels(["# Juego", "Equipo ganador", "Puntaje"])

        # Agregar algunas filas de ejemplo
        data = [
            [1, 'A', 109],
            [2, 'B', 91],
            [3, 'A', 100],
            [3, 'A', 100],
            [3, 'A', 100],
            [3, 'A', 100],
            [3, 'A', 100],
            [3, 'A', 100],
            [3, 'A', 100],
            [3, 'A', 100],
            [3, 'A', 100],
            [3, 'A', 100],
            [3, 'A', 100],
            [3, 'A', 100],
            [3, 'A', 100],
            [3, 'A', 100],
            [3, 'A', 100],
            [3, 'A', 100],
            [3, 'A', 100],
            [3, 'A', 100],
            [3, 'A', 100],
            [4, 'A', 94]
        ]
        self.table.setRowCount(len(data))

        for row in range(len(data)):
            for col in range(3):
                self.table.setItem(row, col, QTableWidgetItem(str(data[row][col])))

        # Establecer el layout de la ventana
        self.setLayout(layout)

# Inicializar la aplicación
app = QApplication(sys.argv)

# Crear y mostrar la ventana
window = MyWindow()
window.show()

# Ejecutar el bucle de eventos
sys.exit(app.exec_())
