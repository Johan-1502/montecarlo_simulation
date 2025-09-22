import sys
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QFrame,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QScrollArea,
    QMainWindow,
    QSizePolicy,
)
from PyQt5.QtCore import Qt
from simulation import Tournament
import constants
import time
from datetime import timedelta
import math
from matplotlib.figure import Figure
import matplotlib
import numpy as np
from matplotlib.ticker import MaxNLocator
import threading

matplotlib.use("Qt5Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.execution_time = 0
        self.execute_tournament()
        self.setWindowTitle("Arquersim")
        self.setGeometry(100, 100, 1700, 900)
        self.setStyleSheet("background-color: #E2E8F0;")

        # ---- HEADER ----
        header_widget = self.create_header()

        initial_val_widget = QWidget()
        initial_layout = QHBoxLayout(initial_val_widget)
        table_gender = self.archers_by_gender()
        initial_layout.addWidget(table_gender)
        

        # -----Primer fila de componentes----
        row1_widget = self.create_first_row()

        row2_widget = QWidget()
        row2_layout = QHBoxLayout(row2_widget)
        row2_layout.setSpacing(0)
        row2_layout.setContentsMargins(0, 0, 0, 0)

        statistics_content = QWidget()
        statistics_content.setFixedHeight(435)
        statistics_layout = QVBoxLayout(statistics_content)
        statistics_layout.setSpacing(0)
        statistics_layout.setContentsMargins(0, 0, 0, 0)
        table = self.table_teams()

        lateral_widget = QWidget()
        lateral_layout = QHBoxLayout(lateral_widget)
        gender_winner = create_component(
            "Género con más rondas ganadas (global)",
            f"{self.tournament.winning_genre()}",
            f"M:{self.tournament.male_wins} rondas, F:{self.tournament.female_wins} rondas",
            240,
            500,
        )
        tied_rounds = create_component(
            "Cantidad de rondas empatadas (global)",
            f"{self.tournament.tied_rounds} rondas empatadas",
            f"Frecuencia relativa: {self.tournament.tied_rounds_frequency:.2f} %",
            240,
            500,
        )

        lateral_layout.addWidget(table)
        lateral_layout.addWidget(gender_winner)
        lateral_layout.addWidget(tied_rounds)

        # row2_layout.addWidget(table)
        row2_layout.addWidget(lateral_widget)

        statistics_layout.addWidget(row1_widget)
        statistics_layout.addWidget(row2_widget)

        points_archers = self.tournament.points_by_archer()
        chart_widget = AccumulatedPointsChart(
            points_archers,
            "Rendimiento acumulado de jugadores",
            "Rendimiento acumulado de jugadores",
        )
        chart_widget.setMinimumHeight(600)
        chart_widget.setStyleSheet("background: transparent;")

        points_by_team = self.tournament.points_by_team()

        chart_container = self.create_graphic(chart_widget)

        chart2 = TeamsBoxplotChart(points_by_team)
        chart2_container = self.create_graphic(chart2)

        canvas = QWidget()
        canvas_layout = QHBoxLayout(canvas)
        canvas_layout.addWidget(chart_container)
        canvas_layout.addWidget(chart2_container)

        table_games = self.create_table_games()

        specials = self.tournament.teams[0].special_shots_by_game
        experience = self.tournament.teams[0].experience_by_game

        special_experience_chart = SpecialsExperienceChart(specials, experience)
        special_chart_container = self.create_graphic(special_experience_chart)

        chart_experience_gender = AccumulatedPointsChart(
            self.tournament.experience_by_gender(),
            "Experiencia acumulada por género",
            "Experiencia acumulada",
        )
        chart_experience_gender_container = self.create_graphic(chart_experience_gender)

        canvas2 = QWidget()
        canvas2_layout = QHBoxLayout(canvas2)
        canvas2_layout.addWidget(special_chart_container)
        canvas2_layout.addWidget(chart_experience_gender_container)

        tied_rounds = self.tournament.tied_rounds
        total_rounds = constants.QUANTITY_OF_ROUNDS * constants.QUANTITY_OF_GAMES

        pie_chart = TiedRoundsPieChart(tied_rounds, total_rounds)
        pie_chart_container = self.create_graphic(pie_chart)

        canvas3 = QWidget()
        canvas3_layout = QHBoxLayout(canvas3)
        canvas3_layout.addWidget(pie_chart_container)

        # ---- Ensamblar todo ----
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        main_layout.addWidget(header_widget)
        main_layout.addWidget(initial_val_widget)
        main_layout.addWidget(statistics_content)
        main_layout.addWidget(table_games)
        main_layout.addWidget(canvas)
        main_layout.addWidget(canvas2)
        main_layout.addWidget(canvas3)
        main_layout.addStretch()

        main_widget.setMinimumSize(1600, 3400)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(main_widget)

        self.setCentralWidget(scroll)

    def create_graphic(self, chart):
        chart_container = QWidget()
        chart_container.setFixedHeight(650)
        chart_container.setFixedWidth(800)
        chart_container_layout = QHBoxLayout(chart_container)
        chart_container_layout.addWidget(chart)
        chart_container.setStyleSheet(
            """
                background-color: white;  
                border: 2px solid #444;   
                border-radius: 15px;      
            """
        )
        return chart_container

    def create_table_games(self):
        table = QWidget()
        table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        table_layout = QVBoxLayout(table)
        table.setStyleSheet(
            """
            background-color: #0F1730;
            color: lightgray;
            border-radius: 20px;
        """
        )

        title_table = QLabel(
            f"Equipo ganador por juego (primeros {constants.QUANTITY_OF_GAMES_TO_SHOW} juegos)"
        )
        title_table.setStyleSheet(
            """
            font-family: Arial, sans-serif;
            background: none;
            color: #9AA5B3;
            font-size: 19px;
            font-weight: bold;
            padding: 10px 10px 10px 5px;
        """
        )
        table_layout.addWidget(title_table)

        table_content = QTableWidget()
        table_content.setFixedHeight(400)
        header = table_content.horizontalHeader()
        header.setDefaultAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        table_content.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        table_content.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        table_content.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        table_content.verticalHeader().setVisible(False)
        table_layout.addWidget(table_content)

        table_content.setColumnCount(3)
        table_content.setHorizontalHeaderLabels(
            ["# Juego", "Equipo ganador", "Rondas ganadas"]
        )

        table_content.setRowCount(constants.QUANTITY_OF_GAMES_TO_SHOW)

        for r in range(constants.QUANTITY_OF_GAMES_TO_SHOW):
            for c in range(3):
                item = None
                if c == 0:
                    item = QTableWidgetItem(str(self.tournament.games[r].id))
                if c == 1:
                    if self.tournament.games[r].bestTeam:
                        item = QTableWidgetItem(
                            str(
                                self.tournament.games[r].bestTeam[
                                    constants.NAME_ATRIBUTE
                                ]
                            )
                        )
                    else:
                        item = QTableWidgetItem(str("Empate"))
                if c == 2:
                    if self.tournament.games[r].bestTeam:
                        item = QTableWidgetItem(
                            str(self.tournament.games[r].bestTeam[constants.ROUNDS_WON])
                        )
                    else:
                        item = QTableWidgetItem(str("Empate"))
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                table_content.setItem(r, c, item)

        table_content.setShowGrid(False)
        table_content.setStyleSheet(
            """
            QTableView {
                background-color: transparent;
                border: none;
                color: lightgray;
                font-size: 20px;
            }
            QTableView::item {
                border-bottom: 1px solid #E6EEF6;
                padding: 8px;
            }
            QHeaderView::section {
                background: #0F1730;
                color: #9AA5B3;
                font-weight: bold;
                font-size:30px;
                padding: 6px;
                border: none;
            }
            QScrollBar:vertical {
                background: #0F1730;
                width: 14px;
                margin: 15px 0 15px 0;
                border-radius: 7px;
            }
            QScrollBar::handle:vertical {
                background: #3C4A6E;
                min-height: 30px;
                border-radius: 7px;
            }
            QScrollBar::handle:vertical:hover {
                background: #5A6E99;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                background: none;
                border: none;
                height: 0px;
            }
            QScrollBar:horizontal {
                background: #0F1730;
                height: 14px;
                margin: 0 15px 0 15px;
                border-radius: 7px;
            }
            QScrollBar::handle:horizontal {
                background: #3C4A6E;
                min-width: 30px;
                border-radius: 7px;
            }
            QScrollBar::handle:horizontal:hover {
                background: #5A6E99;
            }
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
                background: none;
                border: none;
                width: 0px;
            }
        """
        )
        table_content.clearSelection()
        try:
            table_content.setCurrentCell(-1, -1)
        except Exception:
            pass
        table_content.setFocusPolicy(Qt.NoFocus)
        return table

    def table_teams(self):
        table = QWidget()
        table.setFixedSize(560, 240)
        table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        table_layout = QVBoxLayout(table)
        table.setStyleSheet(
            """
            background-color: #0F1730;
            color: lightgray;
            border-radius: 20px;
        """
        )

        title_table = QLabel("Juegos ganados por equipo")
        title_table.setStyleSheet(
            """
            font-family: Arial, sans-serif;
            background: none;
            color: #9AA5B3;
            font-size: 22px;
            font-weight: bold;
            padding: 10px 10px 10px 5px;
        """
        )
        table_layout.addWidget(title_table)

        table_content = QTableWidget()
        header = table_content.horizontalHeader()
        header.setDefaultAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        table_content.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        table_content.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        table_content.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        table_content.verticalHeader().setVisible(False)
        table_layout.addWidget(table_content)

        table_content.setColumnCount(2)
        table_content.setHorizontalHeaderLabels(["Equipo", "Juegos ganados"])

        quantity_of_games = len(self.tournament.teams)
        table_content.setRowCount(quantity_of_games)

        sorted_teams = sorted(
            self.tournament.teams, key=lambda t: t.quantity_games_won, reverse=True
        )

        for r in range(quantity_of_games):
            for c in range(2):
                item = None
                if c == 0:
                    item = QTableWidgetItem(str(sorted_teams[r].name))
                if c == 1:
                    item = QTableWidgetItem(str(sorted_teams[r].quantity_games_won))
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                table_content.setItem(r, c, item)

        table_content.setShowGrid(False)
        table_content.setStyleSheet(
            """
            QTableView {
                background-color: transparent;
                border: none;
                color: lightgray;
                font-size: 20px;
            }
            QTableView::item {
                border-bottom: 1px solid #E6EEF6;
                padding: 8px;
            }
            QHeaderView::section {
                background: #0F1730;
                color: #9AA5B3;
                font-weight: bold;
                font-size:30px;
                padding: 6px;
                border: none;
            }
            QScrollBar:vertical {
                background: #0F1730;
                width: 14px;
                margin: 15px 0 15px 0;
                border-radius: 7px;
            }
            QScrollBar::handle:vertical {
                background: #3C4A6E;
                min-height: 30px;
                border-radius: 7px;
            }
            QScrollBar::handle:vertical:hover {
                background: #5A6E99;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                background: none;
                border: none;
                height: 0px;
            }
            QScrollBar:horizontal {
                background: #0F1730;
                height: 14px;
                margin: 0 15px 0 15px;
                border-radius: 7px;
            }
            QScrollBar::handle:horizontal {
                background: #3C4A6E;
                min-width: 30px;
                border-radius: 7px;
            }
            QScrollBar::handle:horizontal:hover {
                background: #5A6E99;
            }
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
                background: none;
                border: none;
                width: 0px;
            }
        """
        )
        table_content.clearSelection()
        try:
            table_content.setCurrentCell(-1, -1)
        except Exception:
            pass
        table_content.setFocusPolicy(Qt.NoFocus)
        return table

    def archers_by_gender(self):
        table = QWidget()
        table.setFixedSize(560, 240)
        table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        table_layout = QVBoxLayout(table)
        table.setStyleSheet(
            """
            background-color: #0F1730;
            color: lightgray;
            border-radius: 20px;
        """
        )

        title_table = QLabel("Cantidad de arqueros por género")
        title_table.setStyleSheet(
            """
            font-family: Arial, sans-serif;
            background: none;
            color: #9AA5B3;
            font-size: 22px;
            font-weight: bold;
            padding: 10px 10px 10px 5px;
        """
        )
        table_layout.addWidget(title_table)

        table_content = QTableWidget()
        header = table_content.horizontalHeader()
        header.setDefaultAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        table_content.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        table_content.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        table_content.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        table_content.verticalHeader().setVisible(False)
        table_layout.addWidget(table_content)

        table_content.setColumnCount(2)
        table_content.setHorizontalHeaderLabels(["Género", "Cantidad de arqueros"])

        archers_by_gender = self.tournament.archers_by_gender()
        quantity_of_games = len(archers_by_gender)
        table_content.setRowCount(quantity_of_games)

        for r in range(quantity_of_games):
            for c in range(2):
                item = None
                if c == 0:
                    item = QTableWidgetItem(str(archers_by_gender[r]["gender"].value))
                if c == 1:
                    item = QTableWidgetItem(str(archers_by_gender[r]["quantity"]))
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                table_content.setItem(r, c, item)

        table_content.setShowGrid(False)
        table_content.setStyleSheet(
            """
            QTableView {
                background-color: transparent;
                border: none;
                color: lightgray;
                font-size: 20px;
            }
            QTableView::item {
                border-bottom: 1px solid #E6EEF6;
                padding: 8px;
            }
            QHeaderView::section {
                background: #0F1730;
                color: #9AA5B3;
                font-weight: bold;
                font-size:30px;
                padding: 6px;
                border: none;
            }
            QScrollBar:vertical {
                background: #0F1730;
                width: 14px;
                margin: 15px 0 15px 0;
                border-radius: 7px;
            }
            QScrollBar::handle:vertical {
                background: #3C4A6E;
                min-height: 30px;
                border-radius: 7px;
            }
            QScrollBar::handle:vertical:hover {
                background: #5A6E99;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                background: none;
                border: none;
                height: 0px;
            }
            QScrollBar:horizontal {
                background: #0F1730;
                height: 14px;
                margin: 0 15px 0 15px;
                border-radius: 7px;
            }
            QScrollBar::handle:horizontal {
                background: #3C4A6E;
                min-width: 30px;
                border-radius: 7px;
            }
            QScrollBar::handle:horizontal:hover {
                background: #5A6E99;
            }
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
                background: none;
                border: none;
                width: 0px;
            }
        """
        )
        table_content.clearSelection()
        try:
            table_content.setCurrentCell(-1, -1)
        except Exception:
            pass
        table_content.setFocusPolicy(Qt.NoFocus)
        return table

    def execute_tournament(self):
        print("Ejecución iniciada")
        start_time = time.time()
        stop_flag = {"stop": False}

        # Lanzamos el hilo
        thread = threading.Thread(target=mostrar_tiempo, args=(start_time, stop_flag))
        thread.start()
        
        self.tournament = Tournament()
        self.tournament.execute()

        stop_flag["stop"] = True
        thread.join()

        end_time = time.time()
        execution_time = end_time - start_time
        hours, rem = divmod(execution_time, 3600)
        minutes, seconds = divmod(rem, 60)
        tiempo_formateado = f"{int(hours):02}:{int(minutes):02}:{seconds:05.2f}"
        #first_part = tiempo_formateado.split(".")[0]
        #second_part = tiempo_formateado.split(".")[1]
        
        
        self.execution_time = tiempo_formateado
        print(execution_time)
        print(f"\nTiempo de ejecución: {tiempo_formateado}")

        print("Ejecución terminada")
        print(
            f"cantidad de veces con arquero especial repetido equipo 1: {self.tournament.teams[0].repeated_special_archer}"
        )
        print(
            f"cantidad de veces con arquero especial repetido equipo 2: {self.tournament.teams[1].repeated_special_archer}"
        )

    def create_header(self):
        header_widget = QWidget()
        header_layout = QVBoxLayout(header_widget)
        header_layout.setSpacing(0)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_widget.setStyleSheet(
            """border-top-left-radius: 10px;
    border-top-right-radius: 10px;
    border-bottom-left-radius: 0px;
    border-bottom-right-radius: 0px;"""
        )

        self.title = QLabel("Arquersim — Panel de Resultados")
        self.title.setStyleSheet(
            """
            background-color: #071029;
            color: lightgray;
            font-size: 30px;
            font-weight: bold;
            padding: 5px 10px 3px 7px;
        """
        )
        header_layout.addWidget(self.title)

        self.subtitle = QLabel(
            "Simulación Montecarlo de un torneo de arquería adaptativa multironda"
        )
        self.subtitle.setStyleSheet(
            """
            font-family: Arial, sans-serif;
            background-color: #071029;
            color: lightgray;
            font-size: 22px;
            padding: 0px 10px 10px 10px;
            border-top-left-radius: 0px;
            border-top-right-radius: 0px;
            border-bottom-left-radius: 10px;
            border-bottom-right-radius: 10px;
        """
        )
        header_layout.addWidget(self.subtitle)

        header_widget.setFixedHeight(100)
        return header_widget

    def create_first_row(self):
        row1_widget = QWidget()
        row1_layout = QHBoxLayout(row1_widget)

        abbreviated_number = abbreviate_number(constants.QUANTITY_OF_GAMES)

        luckiest_component = create_component(
            f"Jugador más afortunado (conteo en {abbreviated_number} juegos)",
            f"{self.tournament.luckiest_archer.name}",
            f"Veces como más afortunado: {self.tournament.luckiest_archer.quantity_luckiest_games}",
            150,
            540,
        )
        row1_layout.addWidget(luckiest_component)

        experienced_component = create_component(
            f"Jugador con más experiencia (conteo en {abbreviated_number} juegos)",
            f"{self.tournament.the_most_experienced_archer.name}",
            f"Veces con más experiencia:  {self.tournament.luckiest_archer.quantity_experienced_games}",
            150,
            540,
        )
        row1_layout.addWidget(experienced_component)

        time_component = create_component(
            "Tiempo total de simulación",
            self.execution_time,
            #f"{self.execution_time:.2f} s",
            None,
            150,
            540,
        )
        row1_layout.addWidget(time_component)

        return row1_widget

def mostrar_tiempo(start_time, stop_flag):
    while not stop_flag["stop"]:
        elapsed = time.time() - start_time
        print(f"Tiempo transcurrido: {elapsed:.1f} s", end="\r") 
        time.sleep(0.1) 

class TiedRoundsPieChart(QWidget):
    def __init__(self, tied_rounds, total_rounds, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)

        # Crear figura y canvas
        self.figure = Figure(figsize=(6, 6))
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        # Dibujar gráfico
        self.plot(tied_rounds, total_rounds)

    def plot(self, tied_rounds, total_rounds):
        ax = self.figure.add_subplot(111)
        ax.clear()

        # Datos
        rondas_no_empatadas = total_rounds - tied_rounds
        valores = [tied_rounds, rondas_no_empatadas]
        etiquetas = ["Empatadas", "No empatadas"]
        colores = ["skyblue", "lightcoral"]

        # Gráfico circular
        ax.pie(
            valores,
            labels=etiquetas,
            autopct="%1.1f%%",
            colors=colores,
            startangle=90,
            explode=(0.05, 0),
            shadow=True,
        )

        ax.set_title("Porcentaje de rondas empatadas vs no empatadas")
        self.canvas.draw()


class AccumulatedPointsChart(QWidget):
    def __init__(self, points_data, title: str, y_label: str, parent=None):
        super().__init__(parent)

        self.title = title
        self.y_label = y_label

        layout = QVBoxLayout(self)

        # Crear figura y canvas
        self.figure, self.ax = plt.subplots(figsize=(8, 5))
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        # Estado de líneas activas
        self.lines = []  # todas las líneas
        self.active_lines = set()  # las seleccionadas

        # Dibujar gráfico
        self.plot(points_data)

        # Conectar evento de click
        self.canvas.mpl_connect("pick_event", self.on_pick)

    def plot(self, points_data):
        self.ax.clear()
        self.lines.clear()
        self.active_lines.clear()

        # Dibujar cada jugador
        for name, acumulados in points_data.items():
            (line,) = self.ax.plot(
                range(1, len(acumulados) + 1), acumulados, label=name, picker=True
            )
            self.lines.append(line)

        # Leyenda
        legend = self.ax.legend(
            loc="upper left",
            fontsize=12,
            markerscale=4.0,
            handlelength=3,
            borderpad=1.2,
        )
        for legline, origline in zip(legend.get_lines(), self.lines):
            legline.set_picker(True)
            legline._associated_line = origline

        self.ax.set_title(self.title)
        self.ax.set_xlabel("Rondas")
        self.ax.set_ylabel(self.y_label)
        self.ax.grid(True, alpha=0.3)

        self.canvas.draw()

    def on_pick(self, event):
        legline = event.artist
        if not hasattr(legline, "_associated_line"):
            return  # ignorar clicks fuera de la leyenda

        origline = legline._associated_line

        if origline in self.active_lines:
            # Si ya estaba seleccionada → la quitamos
            self.active_lines.remove(origline)
        else:
            # Si no estaba → la añadimos
            self.active_lines.add(origline)

        if self.active_lines:
            # Mostrar solo las seleccionadas
            for line in self.lines:
                line.set_visible(line in self.active_lines)
        else:
            # Si no hay ninguna seleccionada → mostrar todas
            for line in self.lines:
                line.set_visible(True)

        self.canvas.draw()


class SpecialsExperienceChart(QWidget):
    def __init__(self, specials, experience, parent=None):
        super().__init__(parent)

        # Layout principal
        layout = QVBoxLayout(self)

        # Crear figura y canvas
        self.figure = Figure(figsize=(6, 4))
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        # Guardar datos y dibujar
        self.specials = specials
        self.experience = experience
        self.plot()

    def plot(self):
        ax = self.figure.add_subplot(111)
        ax.clear()

        # Puntos de dispersión
        ax.scatter(
            self.specials, self.experience, color="blue", alpha=0.6, label="Juegos"
        )

        # Ajuste lineal (recta de tendencia)
        m, b = np.polyfit(self.specials, self.experience, 1)
        ax.plot(
            self.specials,
            [m * x + b for x in self.specials],
            color="red",
            label="Tendencia",
        )

        # Etiquetas y título
        ax.set_xlabel("Lanzamientos especiales por equipo")
        ax.set_ylabel("Experiencia ganada por equipo")
        ax.set_title("Correlación entre lanzamientos especiales y experiencia")
        ax.legend()

        ax.grid(alpha=0.3)

        # Dibujar en canvas
        self.canvas.draw()


class TeamsBoxplotChart(QWidget):
    def __init__(self, points_by_team, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        self.figure = Figure(figsize=(6, 4))
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        self.points_by_team = points_by_team
        self.plot(points_by_team)

        # Conectar evento de movimiento del mouse
        self.canvas.mpl_connect("motion_notify_event", self.on_hover)

    def plot(self, points_by_team):
        self.ax = self.figure.add_subplot(111)
        self.ax.clear()

        # Dibujar boxplot y guardar referencias
        bp = self.ax.boxplot(
            points_by_team.values(),
            tick_labels=points_by_team.keys(),
            showmeans=True,
            meanline=True,
            patch_artist=True,
        )

        # Dibujar puntos individuales encima
        self.scatter_points = []
        for i, values in enumerate(points_by_team.values(), start=1):
            sc = self.ax.scatter([i] * len(values), values, alpha=0.6)
            self.scatter_points.append(sc)

        self.ax.set_title("Dispersión de puntajes por equipo")
        self.ax.set_xlabel("Equipo")
        self.ax.set_ylabel("Puntaje por ronda")
        self.ax.grid(alpha=0.3)
        self.ax.yaxis.set_major_locator(MaxNLocator(nbins=15))

        # === Añadir texto de cuartiles y mediana ===
        for i, (team, values) in enumerate(points_by_team.items(), start=1):
            q1, med, q3 = (
                np.percentile(values, 25),
                np.median(values),
                np.percentile(values, 75),
            )

            self.ax.text(
                i + 0.1, q1, f"Q1={q1:.1f}", va="center", fontsize=8, color="blue"
            )
            self.ax.text(
                i + 0.1, med, f"Med={med:.1f}", va="center", fontsize=8, color="red"
            )
            self.ax.text(
                i + 0.1, q3, f"Q3={q3:.1f}", va="center", fontsize=8, color="green"
            )

        # Crear anotación (tooltip oculto inicialmente)
        self.annotation = self.ax.annotate(
            "",
            xy=(0, 0),
            xytext=(15, 15),
            textcoords="offset points",
            bbox=dict(boxstyle="round", fc="w"),
            arrowprops=dict(arrowstyle="->"),
        )
        self.annotation.set_visible(False)

        self.canvas.draw()

    def update_annotation(self, x, y, text):
        """Actualiza el tooltip con la posición y texto"""
        self.annotation.xy = (x, y)
        self.annotation.set_text(text)
        self.annotation.set_visible(True)
        self.canvas.draw_idle()

    def on_hover(self, event):
        """Detecta cuando el mouse pasa sobre un punto"""
        vis = self.annotation.get_visible()
        if event.inaxes == self.ax:
            for sc in self.scatter_points:
                cont, ind = sc.contains(event)
                if cont:
                    idx = ind["ind"][0]
                    x, y = sc.get_offsets()[idx]
                    self.update_annotation(x, y, f"Puntaje: {y:.1f}")
                    return
        if vis:
            self.annotation.set_visible(False)
            self.canvas.draw_idle()


def create_component(
    title: str, central_text: str, bottom_text: str, height: int, width: int
):
    component = QWidget()
    component.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
    component.setFixedHeight(height)

    component.setStyleSheet(
        """
        background-color: #0F1730;
        color: lightgray;
        border-radius: 20px;
    """
    )

    layout = QVBoxLayout(component)
    layout.setSpacing(0)

    title_component = QLabel(title)
    title_component.setStyleSheet(
        """
        font-family: Arial, sans-serif;
        background: none;
        color: #9AA5B3;
        font-size: 21px;
        font-weight: bold;
        padding: 10px 10px 10px 5px;
    """
    )
    layout.addWidget(title_component)

    central_component = QLabel(central_text)
    central_component.setStyleSheet(
        """
        background: none;
        color: lightgray;
        font-size: 30px;
        font-weight: bold;
        padding: 0px 10px 10px 5px;
    """
    )
    layout.addWidget(central_component)

    if bottom_text:
        bottom_component = QLabel(bottom_text)
        bottom_component.setStyleSheet(
            """
            font-family: Arial, sans-serif;
            background: none;
            color: #9AA5B3;
            font-size: 21px;
            padding: 0px 10px 10px 5px;
        """
        )
        layout.addWidget(bottom_component)

    return component


def abbreviate_number(num: int) -> str:
    if num >= 1_000_000_000_000:
        return f"{num/1_000_000_000_000:.1f}B"
    elif num >= 1_000_000:
        return f"{num/1_000_000:.1f}M"
    elif num >= 1_000:
        return f"{num/1_000:.1f}k"
    else:
        return str(num)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
