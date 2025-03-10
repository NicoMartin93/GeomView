
import os
import sys
import re
import numpy as np
import time
import shutil
import subprocess
import plotly.graph_objects as go
import plotly.express as px
from julia.api import Julia
Julia(compiled_modules=False)
from julia import Main

from PySide6.QtCore import QUrl, QPoint, Qt
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import *
from PySide6.QtGui import QGuiApplication, QSurfaceFormat, QAction, QIcon
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtAxContainer import QAxSelect, QAxWidget
from PySide6.QtQuick3D import QQuick3D
from PySide6.QtQuick import QQuickView, QQuickWindow, QSGRendererInterface
from PySide6.QtQuickWidgets import QQuickWidget

from PyQt5.QtGui import QPixmap

import matplotlib.pyplot as plt
import matplotlib
import matplotlib.gridspec as gridspec
from mpl_toolkits.mplot3d import Axes3D
# from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.image as mpimg
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import matplotlib.ticker as mtick
from matplotlib import cm
from matplotlib.colors import Normalize
from matplotlib.widgets import Slider, Button, CheckButtons
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection

import itertools
from itertools import groupby

from MonteCarlo.Utils.utils import option_list, print_list_columns
from GeomView.PS_Simulation import GeomGenerator

# # GUI PARA CINTURON DE DETECTORES


def class_name(o):
    return o.metaObject().className()

def init_widget(w, name):
    """Init a widget for the gallery, give it a tooltip showing the
       class name"""
    w.setObjectName(name)
    w.setToolTip(class_name(w))

def style_names(list_name):
    """Return a list of styles, default platform style first"""

    if list_name == 'plane':
        style_list = ['XY', 'XZ', 'YZ']
    if list_name == 'materials':
        style_list = ['CdTe', 'Ge', 'Si']
    if list_name == 'angles':
        style_list = ['Rotación completa', 'Media rotación']
    if list_name == 'shapes':
        style_list = ['Paralelepipedo', 'Cilíndrico']
    if list_name == 'type_data':
        style_list = ['Espectro antes del detector', 'Espectro despues del detector', 'Espacio de fase', 'Fluencia antes del detector']
    if list_name == 'type_plot1':
        style_list = ['','Densidad de probabilidades', 'Densidad electrones', 'Densidad fotones', 'Densidad positrones']
    if list_name == 'type_plot2':
        style_list = ['Energía depositada']
    if list_name == 'type_plot3':
        style_list = ['Fluencia total', ' Fluencia de electrones', 'Fluencia de fotones', 'Fluencia de positrones']

    result = []
    for style in style_list:
        if style.lower() == style_list:
            result.insert(0, style)
        else:
            result.append(style)
    return result

class plotsTools(QWidget):

    def __init__(self):
        super().__init__()

        # Seleccionamos la carpeta con los resultados.
        pathfolder = self.load_file()

        # Cargamos en una lista todos los path de datos.
        list_pathfiles = [os.path.join(pathfolder,pathfile) for pathfile in os.listdir(pathfolder) if os.path.isfile(os.path.join(pathfolder,pathfile)) and pathfile.endswith('.dat')]

        # Cargamos todos los resultados y los separamos en base datos.
        spc_enddet = {}
        spc_impdet = {}
        psf_impdet = {}
        fln_impdet = {}

        for pathfile in list_pathfiles:

            data = LoadDataResults(pathfile)

            if data.TypeDataFile == 'spc-enddet':
                spc_enddet.update({data.Body:data.GetData})

            if data.TypeDataFile == 'spc-impdet':
                spc_impdet.update({data.Body:data.GetData})

            if data.TypeDataFile == 'psf-impdet':
                psf_impdet.update({data.Body:data.GetData})

            if data.TypeDataFile == 'fln-impdet':
                fln_impdet.update({data.Body:data.GetData})

        self.database = {'spc-enddet':spc_enddet, 'spc-impdet':spc_impdet, 'psf-impdet':psf_impdet, 'fln-impdet':fln_impdet}

        # Definimos el número de detectores
        self.num_bodys = len(list(self.database['spc-enddet'].keys()))

        # self.__detectores_opuestos()
        # Iniciamos la pantalla
        self.__Layaout_Principal()

        layout_plots = QHBoxLayout()
        layout_plots.addLayout(self.llayout, 25)
        layout_plots.addLayout(self.rlayout, 75)
        self.setLayout(layout_plots)

    def load_file(self):

        # Creamos la ventana emergente para que se pueda seleccionar el archivo.
        opciones = QFileDialog.Options()
        opciones |= QFileDialog.DontUseNativeDialog
        pathfolder = QFileDialog.getExistingDirectory(self, "Select Directory")

        return pathfolder

    def save_file(self):
        opciones = QFileDialog.Options()
        opciones |= QFileDialog.DontUseNativeDialog
        archivo, _ = QFileDialog.getSaveFileName(self, "Guardar archivo", "",
                                                  "Archivos de texto (*.txt);;Todos los archivos (*)",
                                                  options=opciones)
        if archivo:
            print(f'Se guardará el archivo en: {archivo}')

    def __Layaout_Principal(self):

        # --------------------------------------------------
        # # Panel IZQUIERDO - Configuraciones

        # Tipo de datos para visualizar
        self._type_data = QComboBox()
        init_widget(self._type_data, "styleComboBox")
        self._type_data.addItems(style_names(list_name='type_data'))

        # Tipo de columnas para visualizar
        self._type_plot1 = QComboBox()
        init_widget(self._type_plot1, "styleComboBox")
        self._type_plot1.addItems(style_names(list_name='type_plot1'))
        self._type_plot1.setVisible(False)

        self._type_plot2 = QComboBox()
        init_widget(self._type_plot2, "styleComboBox")
        self._type_plot2.addItems(style_names(list_name='type_plot2'))
        self._type_plot2.setVisible(False)

        self._type_plot3 = QComboBox()
        init_widget(self._type_plot3, "styleComboBox")
        self._type_plot3.addItems(style_names(list_name='type_plot3'))
        self._type_plot3.setVisible(False)

        # Detector para visualizar
        self._nbody = QDoubleSpinBox()
        self._nbody.setPrefix("Detector: ")
        self._nbody.setValue(1)
        self._nbody.setRange(1, self.num_bodys)
        init_widget(self._nbody, "nbody")

        # Boton de ejecución para visualizar el plot elegido
        self.button_view = QPushButton("Ver")
        init_widget(self.button_view, "view_label")

        # ------
        # # Agregamos el layout
        self.llayout = QVBoxLayout()
        self.llayout.setContentsMargins(1, 1, 1, 1)

        self.label1 = QLabel("                      PLOTS DE DATOS")
        self.label1.setStyleSheet("border: 2px solid gray; position: center;")
        self.llayout.addWidget(self.label1)

        self.llayout.addWidget(QLabel("Datos para visualizar:"))
        self.llayout.addWidget(self._type_data)

        self.label2 = QLabel("Columna de datos para visualizar:")
        self.llayout.addWidget(self._type_plot1)
        self.llayout.addWidget(self._type_plot2)
        self.llayout.addWidget(self._type_plot3)

        self.llayout.addWidget(QLabel("Detector:"))
        self.llayout.addWidget(self._nbody)

        self.llayout.addWidget(self.button_view)

        self.llayout.addStretch()

        # # Agregamos las Conexiones
        self.button_view.clicked.connect(self.__ViewPlot)
        self._type_data.currentIndexChanged.connect(self.__OptionsPut)

        # --------------------------------------------------
        # # Panel DERECHO - PLOTS

        self.rlayout = QVBoxLayout()
        self.rlayout.setContentsMargins(1, 1, 1, 1)
        self.fig = Figure(figsize=(2, 2))
        self.can = FigureCanvasQTAgg(self.fig)
        self.rlayout.addWidget(self.can)

    def __OptionsPut(self, state):

        if str(self._type_data.currentText())=='Espectro antes del detector':
            self._type_plot1.setVisible(True)
            self._type_plot2.setVisible(False)
            self._type_plot3.setVisible(False)

        if str(self._type_data.currentText())=='Espectro despues del detector':
            self._type_plot1.setVisible(False)
            self._type_plot2.setVisible(True)
            self._type_plot3.setVisible(False)


        if str(self._type_data.currentText())=='Fluencia antes del detector':
            self._type_plot1.setVisible(False)
            self._type_plot2.setVisible(False)
            self._type_plot3.setVisible(True)

        if str(self._type_data.currentText())=='':
            self._type_plot1.setVisible(False)
            self._type_plot2.setVisible(False)
            self._type_plot3.setVisible(False)


    def __func(self,label):
        index = self.__labels.index(label)
        self.__plots[index].set_visible(not self.__plots[index].get_visible())
        self.can.draw()

    def __ViewPlot(self):

        # (1) Extraemos los datos
        print(self.database)
        ibody = str(self._nbody.value()).split('.')[0]
        if len(ibody) < 2:
            ibody = '0'+ibody
        type_data = str(self._type_data.currentText())

        if type_data == 'Espectro antes del detector':

            # (1) --- SEPARAMOS LOS DATOS
            # Separamos los datos
            column = self.database['spc-impdet'][ibody].GetTitlesColumns
            data = self.database['spc-impdet'][ibody].GetDataColumns
            units = self.database['spc-impdet'][ibody].GetUnits
            title = self.database['spc-impdet'][ibody].GetTitle

            energy = np.array(data[column[0]])
            den_prob = np.array(data[column[1]])
            su_den_prob = data[column[2]]
            dp_electron = data[column[3]]
            su_dp_electron = data[column[4]]
            dp_fotones = data[column[5]]
            su_dp_fotones = data[column[6]]
            dp_positrons = data[column[7]]
            su_dp_positrons = data[column[8]]

            # (2) --- PLOTEAMOS
            # Eliminamos la figura anterior
            self.can.deleteLater()
            # Creamos una nueva figura
            self.fig = Figure(figsize=(2, 2))
            self.can = FigureCanvasQTAgg(self.fig)
            self.rlayout.addWidget(self.can)

            # here you can set up your figure/axis
            self.ax = self.can.figure.add_subplot(111)
            matplotlib.rcParams.update({'font.size': 8})

            # q25, q75 = np.percentile(den_prob, [25, 75])
            # bin_width = 2 * (q75 - q25) * len(den_prob) ** (-1/3)
            # bins = round((den_prob.max() - den_prob.min()) / bin_width)
            # print("Freedman–Diaconis number of bins:", bins)
            # plt.hist(x, bins=bins);
            bins = 300
            self.ax.hist(den_prob, bins=bins, label='Data')

            self.ax.legend(loc="upper left", fontsize=10)
            self.ax.set_xlabel('{}'.format(units[0]))
            self.ax.set_ylabel('{}'.format(units[1]))
            self.ax.set_title('{}'.format(title))

            self.can.draw()

        if type_data == 'Espectro despues del detector':

            self.can.deleteLater()

            self.fig = Figure(figsize=(2, 2))
            self.can = FigureCanvasQTAgg(self.fig)
            self.rlayout.addWidget(self.can)

            # here you can set up your figure/axis
            self.ax = self.can.figure.add_subplot(111)
            matplotlib.rcParams.update({'font.size': 8})

            # Separamos los datos
            column = self.database['spc-enddet'][ibody].GetTitlesColumns
            data = self.database['spc-enddet'][ibody].GetDataColumns
            units = self.database['spc-enddet'][ibody].GetUnits
            title = self.database['spc-enddet'][ibody].GetTitle

            # Ploteamos los resultados
            bins=200
            self.ax.hist(data[column[1]],bins=200)

            self.ax.legend(loc="upper left", fontsize=10)
            self.ax.set_xlabel('{}'.format(units[0]))
            self.ax.set_ylabel('{}'.format(units[1]))
            self.ax.set_title('{}'.format(title))

            self.can.draw()

        if type_data == 'Fluencia del espacio de fase':

            self.can.deleteLater()

            self.fig = Figure(figsize=(2, 2))
            self.can = FigureCanvasQTAgg(self.fig)
            self.rlayout.addWidget(self.can)

            # here you can set up your figure/axis
            self.ax = self.can.figure.add_subplot(111)
            matplotlib.rcParams.update({'font.size': 8})
            print(ibody)
            print(self.database['psf-impdet'])
            # Separamos los datos
            column = self.database['psf-impdet'][ibody].GetTitlesColumns
            data = self.database['psf-impdet'][ibody].GetDataColumns
            units = self.database['psf-impdet'][ibody].GetUnits
            title = self.database['psf-impdet'][ibody].GetTitle

            # Ploteamos los resultados
            self.ax.plot(data[column[0]], data[column[1]])

            self.ax.legend(loc="upper left", fontsize=10)
            self.ax.set_xlabel('{}'.format(units[0]))
            self.ax.set_ylabel('{}'.format(units[1]))
            self.ax.set_title('{}'.format(title))

            self.can.draw()

        if type_data == 'Fluencia antes del detector':

            self.can.deleteLater()

            self.fig = Figure(figsize=(2, 2))
            self.can = FigureCanvasQTAgg(self.fig)
            self.rlayout.addWidget(self.can)

            # here you can set up your figure/axis
            self.ax = self.can.figure.add_subplot(111)
            matplotlib.rcParams.update({'font.size': 8})

            # Separamos los datos
            column = self.database['fln-impdet'][ibody].GetTitlesColumns
            data = self.database['fln-impdet'][ibody].GetDataColumns
            units = self.database['fln-impdet'][ibody].GetUnits
            title = self.database['fln-impdet'][ibody].GetTitle

            # Ploteamos los resultados
            self.ax.plot(data[column[0]], data[column[1]])

            self.ax.legend(loc="upper left", fontsize=10)
            self.ax.set_xlabel('{}'.format(units[0]))
            self.ax.set_ylabel('{}'.format(units[1]))
            self.ax.set_title('{}'.format(title))

            self.can.draw()

    def __detectores_opuestos(self):

        num_bodys = len(list(self.database['spc-enddet'].keys()))

        # Si hay un numero par de detectores.
        # Agrupamos los puestos
        self.detectors_groups = []
        # if num_bodys % 2 == 0:
        #     for body in self.database.keys():
        #         body = int(body)
        #         self.detectors_groups.append([self.database[body], self.database[body+num_bodys/2]])
        # else:
        #     msgBox = QMessageBox()
        #     msgBox.setText("Necesita que el número de detectores sea par, para que existan detectores opuestos.")
        #     msgBox.setStandardButtons(QMessageBox.Cancel)
        #     ret = msgBox.exec()

        for body in self.database['spc-enddet'].keys():
            # body = int(body)
            self.detectors_groups.append([self.database['spc-enddet'][body], self.database['spc-enddet'][body+num_bodys/2]])

class SimulateRayTracing(QWidget):

    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.setup_layout()

    def setup_layout(self):
        """
        Configura el diseño principal de la ventana.
        """
        # Configuración del panel izquierdo
        self.setup_left_panel()

        # Configuración del panel derecho
        self.setup_right_panel()

        # Layout principal
        main_layout = QHBoxLayout()
        main_layout.addLayout(self.llayout, 30)
        main_layout.addLayout(self.cllayout, 70)
        self.setLayout(main_layout)

    def setup_left_panel(self):
        """
        Configura los widgets y diseño del panel izquierdo.
        """

        # Widgets para configuración visual
        # Botones

        # Diseño del panel izquierdo
        self.llayout = QVBoxLayout()
        self.llayout.setContentsMargins(1, 1, 1, 1)

        # Geometría y archivo input
        self.add_section_label("ARCHIVO DE GEOMETRIA", self.llayout)
        self.button_geometry = self.create_button("Cargar geometría de detectores", "view_label", self.setData)
        self.llayout.addWidget(self.button_geometry)
        self.add_section_label("ARCHIVO DE ESPACIO DE FASE", self.llayout)
        self.button_phaseSpace = self.create_button("Cargar espacio de fase", "view_label", self.__loadPhaseSpace)
        self.llayout.addWidget(self.button_phaseSpace)

        self.button_start = self.create_button("INICIAR", "view_label", self.startSimulation)
        self.add_section_label("SIMULACION", self.llayout)
        self.llayout.addWidget(self.button_start)

        self.add_section_label("Visualizar", self.llayout)
        self.nF = self.create_spinbox("Fila: ", 1, "xdim", 0, 100)
        self.llayout.addWidget(self.nF)
        self.button_viewResult = self.create_button("VER", "view_label", self.viewDistribution)
        self.llayout.addWidget(self.button_viewResult)

        self.llayout.addStretch()

    def setup_right_panel(self):
        """
        Configura el diseño del panel derecho.
        """
        self.cllayout = QVBoxLayout()
        self.cllayout.setContentsMargins(1, 1, 1, 1)
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.cllayout.addWidget(self.canvas)

    def create_combobox(self, label, style):
        combo = QComboBox()
        init_widget(combo, "styleComboBox")
        combo.addItems(style_names(list_name=style))
        return combo

    def create_spinbox(self, prefix, value, style, min_val=-100, max_val=100, visible=True):
        spinbox = QDoubleSpinBox()
        spinbox.setPrefix(prefix)
        spinbox.setValue(value)
        spinbox.setRange(min_val, max_val)
        spinbox.setVisible(visible)
        init_widget(spinbox, style)
        return spinbox

    def create_button(self, text, style, callback):
        button = QPushButton(text)
        init_widget(button, style)
        button.clicked.connect(callback)
        return button

    def add_section_label(self, text, layout):
        label = QLabel(text)
        label.setStyleSheet("border: 2px solid gray; position: center;")
        layout.addWidget(label)

    def add_widgets_to_layout(self, layout, widgets):
        for item in widgets:
            if isinstance(item, tuple):
                layout.addWidget(QLabel(item[0]))
                if isinstance(item[1], list):
                    h_layout = QHBoxLayout()
                    for widget in item[1]:
                        h_layout.addWidget(widget)
                    layout.addLayout(h_layout)
                else:
                    layout.addWidget(item[1])
            else:
                layout.addWidget(item)

    def startSimulation(self):

        # DATOS DE LA GEOMETRIA DE LOS DETECTORES
        vertices, origins, directions, nCols, nRows = self.setData()
        vertices = np.array(vertices)
        directions = np.array(directions)
        numDetectors = len(vertices)


        Main.include(".\GeomView\geometry.jl")
        Geometry = Main.Geometry

        # DATOS DEL SCATTERING DEL ESPACIO DE FASE
        dataPhaseSpace = np.load(self.pathFilePS, allow_pickle=True)[()]
        pathFilePS = 'D:\Proyectos_Investigacion\Proyectos_de_Doctorado\Proyectos\SimulationXF_Detectors\Code\Estudios\ModelosBasicos\Phantom_Cilindro_1\Resultados\Mat_Au\Det9-Dist6-Length4\dataPhaseSpace.npy'
        dataPhaseSpace = np.load(pathFilePS, allow_pickle=True)[()]
        scattering = dataPhaseSpace['Scattering-PhaseSpace']
        points = np.array([scattering['x'], scattering['y'], scattering['z']]).T
        dirPoints = np.array([scattering['u'], scattering['v'], scattering['w']]).T
        ee = np.array(scattering['energy'])

        self.numDetectors = len(vertices)
        self.points = points
        self.dirPoints = dirPoints
        self.ee = ee
        self.filterAngle = False
        alpha = 1
        theta = 3
        prolongacion = 6

        self.alpha = alpha
        self.theta = theta
        self.prolongacion = prolongacion
        self.nCols = nCols
        self.nRows = nRows

        countersDetectors = {}

        start_time = time.time()
        self.__printProgressBar(0, numDetectors - 1, prefix='Detecting impact', suffix='Completo', decimals=1, length=30, start_time=start_time)

        # (2) ==========================================================
        # EXTRAEMOS DE CADA DETECTOR SUS DATOS.
        for det in range(numDetectors):
            verts = vertices[det]
            direction = directions[det] #if self.shape == 'Line' else -self.boundsDetectors.detectors_directions[det]
            direction = np.concatenate((direction, np.array([[0], [0]])), axis=1)

            # PUNTO CENTRAL DEL DETECTOR
            vertices_to_expand = np.array([verts[7], verts[2], verts[4], verts[0]])
            center = np.mean(vertices_to_expand, axis=0)

            # Centro del paralelepípedo y vector normal
            center_x, center_y, center_z = np.mean(verts, axis=0)
            normal_vector = direction[0] / np.linalg.norm(direction[0])
            normal_line_end = np.array([center_x, center_y, center_z]) + prolongacion * normal_vector  # Línea normal extendida

            # Expande el rectángulo a partir de los cuatro vértices
            expanded_vertices = Geometry.expand_rectangle(center, vertices_to_expand, normal_vector, prolongacion, theta)

            expanded_vertices_Paralelepide = np.array([verts[7], verts[2], verts[4], verts[0],
                                                       expanded_vertices[0], expanded_vertices[1],
                                                       expanded_vertices[2], expanded_vertices[3]])

            points_parallelepiped_boolean = Geometry.points_inside_parallelepiped(points, expanded_vertices_Paralelepide)
            points_parallelepiped = points[points_parallelepiped_boolean]
            dirPoints_parallelepiped = dirPoints[points_parallelepiped_boolean]
            ee_parallelepiped = ee[points_parallelepiped_boolean]

            if self.filterAngle:
                # Ángulo entre la dirección de los puntos y el detector
                # Vectores de dispersión en el espacio de fase
                unit_vectors = dirPoints_parallelepiped / np.linalg.norm(dirPoints_parallelepiped, axis=1, keepdims=True)
                dot_products = np.dot(normal_vector, unit_vectors.T)
                angles = np.arccos(np.clip(dot_products, -1.0, 1.0))

                # Umbral para seleccionar direcciones cercanas a 180 grados (hacia el detector)
                delta = self.alpha * np.pi / 180  # 1 grado en radianes
                mask = (angles >= (np.pi - delta)) & (angles <= np.pi)

                # Filtra solo los puntos que cumplen con la condición angular
                xt, yt, zt = points_parallelepiped.T
                xdt, ydt, zdt = dirPoints_parallelepiped.T

                pos = np.column_stack((xt[mask], yt[mask], zt[mask]))
                dir = np.column_stack((xdt[mask], ydt[mask], zdt[mask]))
                ene = ee_parallelepiped[mask]

                # Normalizar todas las direcciones a la vez
                dir_norms = np.linalg.norm(dir, axis=1, keepdims=True)
                dir = dir / dir_norms  # Normalización vectorial

                # Calcular las intersecciones con el plano del detector
                intersections = line_plane_intersection_vectorized(pos, dir, center, normal_vector)

                # Filtrar intersecciones válidas que caigan dentro del área del detector
                valid_intersections = (intersections is not None) & point_in_rectangle_vectorized(intersections, vertices_to_expand)

                # Crear la matriz de booleanos
                intersection_matrix = valid_intersections.astype(bool)
                countersDetectors[det] = ene[intersection_matrix]

            else:

                # Normalizar todas las direcciones a la vez
                dir_norms = np.linalg.norm(dirPoints_parallelepiped, axis=1, keepdims=True)
                dirPoints_parallelepiped = dirPoints_parallelepiped / dir_norms  # Normalización vectorial

                # Calcular las intersecciones con el plano del detector
                intersections = Geometry.line_plane_intersection_vectorized(points_parallelepiped, dirPoints_parallelepiped, center, normal_vector)

                # Filtrar intersecciones válidas que caigan dentro del área del detector
                valid_intersections = (intersections is not None) & Geometry.point_in_rectangle_vectorized(intersections, vertices_to_expand)

                # Crear la matriz de booleanos
                intersection_matrix = valid_intersections.astype(bool)[:,0]

                # print(f"ee_parallelepiped shape: {ee_parallelepiped.shape}")
                # print(f"intersection_matrix shape: {intersection_matrix.shape}")

                countersDetectors[det] = ee_parallelepiped[intersection_matrix]

            if det % 5 == 0 or det == numDetectors - 1:
                self.__printProgressBar(det, numDetectors - 1, prefix='Detecting impact', suffix='Completo', decimals=1, length=30, start_time=start_time)

        self.spectrumDetectors = countersDetectors
        organized_by_rows_and_angles = self.organizeDetectorsByRowsAndAngles()
        self.organized_by_rows_and_angles = organized_by_rows_and_angles
        # return countersDetectors

    def organizeDetectorsByRowsAndAngles(self):
        """
        Reorganiza los detectores de un diccionario donde las claves son índices únicos.
        Agrupa los detectores por filas y dentro de cada fila por ángulo.

        Parámetros:
        - detectors (dict): Diccionario de detectores donde las claves son índices únicos.
        - rows (int): Número de filas en la matriz de detectores por ángulo.
        - cols (int): Número de columnas en la matriz de detectores por ángulo.

        Retorno:
        - organized_by_rows_and_angles (list): Lista donde cada elemento representa una fila. Dentro de cada fila,
                                               los detectores están separados por ángulo.
        """
        # Convertir las claves del diccionario en una lista ordenada
        rows = self.nRows
        cols = self.nCols
        sorted_keys = sorted(self.spectrumDetectors.keys())
        total_detectors = len(sorted_keys)
        detectors_per_angle = rows * cols
        total_angles = total_detectors // detectors_per_angle
        self.total_angles = total_angles
        # Crear la estructura para filas y ángulos
        organized_by_rows_and_angles = [[[] for _ in range(total_angles)] for _ in range(rows)]

        # Iterar sobre los ángulos
        for angle_idx in range(total_angles):
            start_idx = angle_idx * detectors_per_angle

            # Iterar sobre las filas
            for row in range(rows):
                row_start = start_idx + row * cols
                row_end = row_start + cols
                organized_by_rows_and_angles[row][angle_idx] = [
                    self.spectrumDetectors[key] for key in sorted_keys[row_start:row_end]
                ]

        # self.organized_by_rows_and_angles = organized_by_rows_and_angles
        return organized_by_rows_and_angles

    def setData(self):
        data = self.parent.getDataDetectors()
        return data

    def __loadPhaseSpace(self):

        # Creamos la ventana emergente para que se pueda seleccionar el archivo.
        opciones = QFileDialog.Options()
        opciones |= QFileDialog.DontUseNativeDialog
        pathfile, _ = QFileDialog.getOpenFileName(self, "Seleccionar archivo de Espacio de Fase", "",
                                                  "Archivos de entrada (*.dat);;Archivos Numpy (*.npy);;Todos los archivos (*)",
                                                  options=opciones)
        basename = os.path.basename(pathfile)
        self.__basenameSuffix = basename.split('.')[-1]
        if basename.split('.')[-1] != "dat" and basename.split('.')[-1] != "npy":
            msgBox = QMessageBox()
            msgBox.setText("No se puede cargar ese tipo de archivos.")
            msgBox.setStandardButtons(QMessageBox.Cancel)
            ret = msgBox.exec()
        else:
            # Cargamos el archivo seleccionado.
            self.pathFilePS = pathfile
            # self.textbox_input.setText(os.path.basename(self.pathFilePS))

    def __printProgressBar(self, iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█', start_time=None):
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + ' ' * (length - filledLength)

        # Calcular tiempo restante
        if start_time is not None and iteration > 0:
            elapsed_time = time.time() - start_time
            estimated_total_time = elapsed_time / iteration * total
            remaining_time = estimated_total_time - elapsed_time
            time_format = time.strftime("%H:%M:%S", time.gmtime(remaining_time))
            time_display = f" - ETA: {time_format}"
        else:
            time_display = ""

        print(f'\r{prefix} |{bar}| {percent}% {suffix}{time_display}', end='\r')
        if iteration == total:
            print()

    def viewDistribution(self):

        counts = self.organized_by_rows_and_angles[int(self.nF), int(self.total_angles)]

        ax = self.figure.add_subplot(111)

        # Dibujar la gráfica
        ax.plot(counts, marker='o', linestyle='-', color='b')
        ax.set_title("Distribución de cuentas")
        ax.set_xlabel("Índice de posición")
        ax.set_ylabel("Cuentas detectadas")
        # ax.legend()
        ax.grid(True)

        # Actualizar el lienzo
        self.canvas.draw()





class DetSystemGen(QWidget):
    def __init__(self):
        super().__init__()

        self.__basenameSuffix = ''
        # Configuramos la pantalla principal
        self.setup_layout()

    def update_data(self, data):
        self.data = data

    def setup_layout(self):
        """
        Configura el diseño principal de la ventana.
        """
        # Configuración del panel izquierdo
        self.setup_left_panel()

        # Configuración del panel derecho
        self.setup_right_panel()

        # Layout principal
        main_layout = QHBoxLayout()
        main_layout.addLayout(self.llayout, 14)
        main_layout.addLayout(self.cllayout, 84)
        self.setLayout(main_layout)

    def setup_left_panel(self):
        """
        Configura los widgets y diseño del panel izquierdo.
        """

        # Widgets para configuración visual
        self._plane = self.create_combobox("Plano", "plane")
        self._materials = self.create_combobox("Material", "materials")
        self._nCols = self.create_spinbox("Detectores por fila: ", 9, "ndetect")
        self._nRows = self.create_spinbox("Detectores por columna: ", 3, "ndetect")
        self._distance = self.create_spinbox("Distancia: ", 5, "distance")
        self._translate = self.create_spinbox("Trasladar detectores: ", 0, "translate", 0, 100)
        self._angles = self.create_combobox("Dispoción angular", "angles")
        self._stepAngle = self.create_spinbox("Paso angular: ", 90, "step", 0, 360)

        # Dimensiones de los detectores
        self._xdim = self.create_spinbox("X: ", 0.1, "xdim", 0, 100)
        self._ydim = self.create_spinbox("Y: ", 0.5, "ydim", 0, 100)
        self._zdim = self.create_spinbox("Z: ", 0.5, "zdim", 0, 100)
        self._shape = self.create_combobox("Forma", "shapes")
        # Espaciado detectores
        self._widtSample = self.create_spinbox("Ancho: ", 4, "xdim", 0, 100)
        self._heightSample = self.create_spinbox("Alto: ", 1.5, "xdim", 0, 100)

        # Botones
        self.button_view = self.create_button("Visualizar geometría", "view_label", self.__ViewPlanes)
        self.button_phaseSpace = self.create_button("Cargar espacio de fase", "view_label", self.__loadPhaseSpace)

        # Diseño del panel izquierdo
        self.llayout = QVBoxLayout()
        self.llayout.setContentsMargins(1, 1, 1, 1)

        # Geometría y archivo input
        self.add_section_label("ARCHIVO DE ESPACIO DE FASE", self.llayout)
        self.llayout.addWidget(self.button_phaseSpace)
        # self.add_widgets_to_layout(self.llayout, [
            # ("Cargar archivo", self.button_phaseSpace),
        # ])

        self.llayout.addStretch()
        # Configuración visual
        self.add_section_label("CONFIGURACIÓN VISUAL DE ANILLOS DETECTORES", self.llayout)
        self.add_widgets_to_layout(self.llayout, [
            ("Plano:", self._plane),
            ("Detectores por fila y columna: ", [self._nCols, self._nRows]),
            ("Material: ", self._materials),
            ("Distancia de la muestra: ", self._distance),
            ("Rotación: ", self._angles),
            ("Paso angular: ", self._stepAngle),
            ("Dimensiones de los detectores: ", [self._xdim, self._ydim, self._zdim]),
            ("Ancho y alto de la muestra: ", [self._widtSample, self._heightSample]),
            ("Forma del detector: ", self._shape),
            ("Trasladar detectores: ", self._translate),
            ("Visualizar geometría", self.button_view),
        ])


    def setup_right_panel(self):
        """
        Configura el diseño del panel derecho.
        """
        self.cllayout = QVBoxLayout()
        self.cllayout.setContentsMargins(1, 1, 1, 1)
        self.browser = QWebEngineView(self)
        self.cllayout.addWidget(self.browser)

    def create_combobox(self, label, style):
        combo = QComboBox()
        init_widget(combo, "styleComboBox")
        combo.addItems(style_names(list_name=style))
        return combo

    def create_spinbox(self, prefix, value, style, min_val=-100, max_val=100, visible=True):
        spinbox = QDoubleSpinBox()
        spinbox.setPrefix(prefix)
        spinbox.setValue(value)
        spinbox.setRange(min_val, max_val)
        spinbox.setVisible(visible)
        init_widget(spinbox, style)
        return spinbox

    def create_button(self, text, style, callback):
        button = QPushButton(text)
        init_widget(button, style)
        button.clicked.connect(callback)
        return button

    def add_section_label(self, text, layout):
        label = QLabel(text)
        label.setStyleSheet("border: 2px solid gray; position: center;")
        layout.addWidget(label)

    def add_widgets_to_layout(self, layout, widgets):
        for item in widgets:
            if isinstance(item, tuple):
                layout.addWidget(QLabel(item[0]))
                if isinstance(item[1], list):
                    h_layout = QHBoxLayout()
                    for widget in item[1]:
                        h_layout.addWidget(widget)
                    layout.addLayout(h_layout)
                else:
                    layout.addWidget(item[1])
            else:
                layout.addWidget(item)

    # ======== Phase Space Load =========

    def __loadPhaseSpace(self):

        # Creamos la ventana emergente para que se pueda seleccionar el archivo.
        opciones = QFileDialog.Options()
        opciones |= QFileDialog.DontUseNativeDialog
        pathfile, _ = QFileDialog.getOpenFileName(self, "Seleccionar archivo de Espacio de Fase", "",
                                                  "Archivos de entrada (*.dat);;Archivos Numpy (*.npy);;Todos los archivos (*)",
                                                  options=opciones)
        basename = os.path.basename(pathfile)
        self.__basenameSuffix = basename.split('.')[-1]
        if basename.split('.')[-1] != "dat" and basename.split('.')[-1] != "npy":
            msgBox = QMessageBox()
            msgBox.setText("No se puede cargar ese tipo de archivos.")
            msgBox.setStandardButtons(QMessageBox.Cancel)
            ret = msgBox.exec()
        else:
            # Cargamos el archivo seleccionado.
            self.pathFilePS = pathfile
            # self.textbox_input.setText(os.path.basename(self.pathFilePS))

    # ======== Get Data ========

    def getDataDetectors(self):

        plane = str(self._plane.currentText())
        nCols = int(self._nCols.value())
        nRows = int(self._nRows.value())
        nplanes = nCols * nRows
        translate = int(self._translate.value())
        distance = self._distance.value()
        dimensions = np.array([self._xdim.value(),self._ydim.value(),self._zdim.value()])
        widthSample = self._widtSample.value()
        heightSample = self._heightSample.value()
        anglesStr = str(self._angles.currentText())

        stepAngle = self._stepAngle.value()
        if anglesStr == 'Rotación completa':
            angles = np.arange(0, 360, stepAngle)
        elif anglesStr == 'Media rotación':
            angles = np.arange(0, 180, stepAngle)

        forma =  str(self._shape.currentText())
        if forma == 'Paralelepipedo':
            shape = 'parallelepiped'
        else:
            shape = 'cylinder'

        # plane='XY'
        # dimensions = np.array([0.1,0.5,0.5])
        # distance = 6
        # translate = 0
        # angles =  np.arange(0, 360, 2)
        # nplanes = 3*9
        # widthSample=0.5
        # heightSample = 4
        # shape = 'parallelepiped'
        # nCols=3
        # nRows=9

        geom = GeomGenerator()
        geom.genDetectors.set_parameters(plane = plane,
                                         dimensions = dimensions,
                                         distance = distance,
                                         translate = translate,
                                         angles = angles,
                                         nplanes = nplanes,
                                         widthSample=widthSample,
                                         heightSample=heightSample,
                                         shape=shape)

        verts = geom.genDetectors.get_matrix_detectors(nCols, nRows, sample_width=widthSample, sample_height=heightSample)
        origins, directions = geom.genDetectors.get_line_direction(verts)

        data = [verts, origins, directions, nCols, nRows]

        return data

    # ========= TYPES GRAPH ===========

    def __ViewPlanes(self):

        plane = str(self._plane.currentText())
        nCols = int(self._nCols.value())
        nRows = int(self._nRows.value())
        nplanes = nCols * nRows
        translate = int(self._translate.value())
        distance = self._distance.value()
        dimensions = np.array([self._xdim.value(),self._ydim.value(),self._zdim.value()])
        widthSample = self._widtSample.value()
        heightSample = self._heightSample.value()

        anglesStr = str(self._angles.currentText())

        stepAngle = self._stepAngle.value()
        if anglesStr == 'Rotación completa':
            angles = np.arange(0, 360, stepAngle)
        elif anglesStr == 'Media rotación':
            angles = np.arange(0, 180, stepAngle)

        forma =  str(self._shape.currentText())
        if forma == 'Paralelepipedo':
            shape = 'parallelepiped'
        else:
            shape = 'cylinder'


        geom = GeomGenerator()
        geom.genDetectors.set_parameters(plane = plane,
                                         dimensions = dimensions,
                                         distance = distance,
                                         translate = translate,
                                         angles = angles,
                                         nplanes = nplanes,
                                         widthSample=widthSample,
                                         heightSample=heightSample,
                                         shape=shape)

        verts = geom.genDetectors.get_matrix_detectors(nCols, nRows, sample_width=widthSample, sample_height=heightSample)
        origins, directions = geom.genDetectors.get_line_direction(verts)

        list_bodies = []
        for idx, vertices in enumerate(verts):
            # Agregar cada cilindro como un mesh3d para visualización
            x, y, z = vertices[:, 0], vertices[:, 1], vertices[:, 2]
            list_bodies.append(go.Mesh3d(
                x=x, y=y, z=z,
                alphahull=0,
                color='lightblue',
                opacity=0.5
                # name=f'Cilindro {idx + 1}'
            ))

        if self.__basenameSuffix == 'npy':
            dataPhaseSpace = np.load(self.pathFilePS, allow_pickle=True)[()]

            # DATOS DEL SCATTERING DEL ESPACIO DE FASE
            scattering = dataPhaseSpace['Scattering-PhaseSpace']
            xd, yd, zd = np.array(scattering['u']), np.array(scattering['v']), np.array(scattering['w'])
            xx, yy, zz = np.array(scattering['x']), np.array(scattering['y']), np.array(scattering['z'])
            ee = np.array(scattering['energy'])

            # Puntos del espacio de fase
            list_bodies.append(go.Scatter3d(
                x=xx[::500], y=yy[::500], z=zz[::500],
                mode='markers', marker=dict(size=3, color='orange'), name='PhaseSpace'
            ))

        # Datos para el eje x
        list_bodies.append(go.Scatter3d(x=[0, 6], y=[0, 0], z=[0, 0], mode='lines', name='X Axis', line=dict(color='red', width=5)))

        # Datos para el eje y
        list_bodies.append(go.Scatter3d(x=[0, 0], y=[0, 6], z=[0, 0], mode='lines', name='Y Axis', line=dict(color='green', width=5)))

        # Datos para el eje z
        list_bodies.append(go.Scatter3d(x=[0, 0], y=[0, 0], z=[0, 6], mode='lines', name='Z Axis', line=dict(color='blue', width=5)))


        # layout = go.Layout(scene_xaxis_visible=False, scene_yaxis_visible=False, scene_zaxis_visible=False)
        # layout = go.Layout(scene_xaxis_visible=True, scene_yaxis_visible=True, scene_zaxis_visible=True,
        #                   scene = dict(xaxis=dict(range=[-10,10]),
        #                                yaxis=dict(range=[-10,10]),
        #                                zaxis=dict(range=[-10,10])))

        # df = px.data.tips()
        # fig = px.box(df, x="day", y="total_bill", color="smoker")
        # fig.update_traces(quartilemethod="exclusive") # or "inclusive", or "linear" by default
        #


        layout = go.Layout(scene_xaxis_visible=False, scene_yaxis_visible=False, scene_zaxis_visible=False)
        # layout = go.Layout(scene_xaxis_visible=True, scene_yaxis_visible=True, scene_zaxis_visible=True,
        #                   scene = dict(xaxis=dict(range=[-10,10]),
        #                                yaxis=dict(range=[-10,10]),
        #                                zaxis=dict(range=[-10,10])))

        # df = px.data.tips()
        # fig = px.box(df, x="day", y="total_bill", color="smoker")
        # fig.update_traces(quartilemethod="exclusive") # or "inclusive", or "linear" by default
        #

        fig = go.Figure(data = list_bodies, layout = layout)

        # Configuración del gráfico
        fig.update_layout(
            scene=dict(
                xaxis_title='X',
                yaxis_title='Y',
                zaxis_title='Z',
                aspectmode='data'
            ),
            title='Sistema de Colimadores en 3D'
        )

        # fig.update_layout(scene_camera_eye_z= 0.55)
        fig.layout.scene.camera.projection.type = "orthographic" #commenting this line you get a fig with perspective proj
        self.browser.setHtml(fig.to_html(include_plotlyjs='cdn'))
        # fig.show()

class VentanaPrincipal(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sistemas de Detección")

        # (1) MENU PRINCIPAL
        # (1.1) File
        fileMenu = self.menuBar().addMenu("&File")
        loadAction = QAction("Load...", self, shortcut="Ctrl+L", triggered=self.load_file)
        fileMenu.addAction(loadAction)
        saveAction = QAction("Save...", self, shortcut="Ctrl+S", triggered=self.save_file)
        fileMenu.addAction(saveAction)
        exitAction = QAction("E&xit", self, shortcut="Ctrl+Q", triggered=self.close)
        fileMenu.addAction(exitAction)

        # (1.2) About
        aboutMenu = self.menuBar().addMenu("&About")
        aboutQtAct = QAction("About &Qt", self, triggered=QApplication.instance().aboutQt)
        aboutMenu.addAction(aboutQtAct)

        # (1.3) Barra de herramientas
        toolBar = QToolBar()
        self.addToolBar(toolBar)

        # Barra de botones
        geometryAction = QAction("Geometría Detector", self, triggered=self.__geometryDetector)
        simulateAction = QAction("Simulación", self, triggered=self.__simulatedRayTracing)
        plotsAction = QAction("Plots", self, triggered=self.__plotsTools)

        # Agregamos las acciones
        toolBar.addAction(geometryAction)
        toolBar.addAction(simulateAction)
        toolBar.addAction(plotsAction)

        # (2) VENTANA PRINCIPAL
        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)

        # Instancias de las ventanas
        self.geometry_widget = None
        self.simulation_widget = None
        self.plots_widget = None

    def __geometryDetector(self):
        if self.geometry_widget is None:
            self.geometry_widget = DetSystemGen()
            self.central_widget.addWidget(self.geometry_widget)
        self.central_widget.setCurrentWidget(self.geometry_widget)

    def __simulatedRayTracing(self):
        if self.simulation_widget is None:

            if self.geometry_widget is None:
                self.simulation_widget = SimulateRayTracing(parent=None)
                self.central_widget.addWidget(self.simulation_widget)
            else:
                self.simulation_widget = SimulateRayTracing(parent=self.geometry_widget)
                self.central_widget.addWidget(self.simulation_widget)

        self.central_widget.setCurrentWidget(self.simulation_widget)

    def __plotsTools(self):
        if self.plots_widget is None:
            self.plots_widget = plotsTools()
            self.central_widget.addWidget(self.plots_widget)
        self.central_widget.setCurrentWidget(self.plots_widget)

    def load_file(self):
        opciones = QFileDialog.Options()
        opciones |= QFileDialog.DontUseNativeDialog
        pathfile, _ = QFileDialog.getOpenFileName(
            self, "Seleccionar archivo", "",
            "Archivos de texto (*.dat);;Archivos de texto (*.txt);;Todos los archivos (*)",
            options=opciones
        )

        if pathfile:
            basename = os.path.basename(pathfile)
            if basename.split('.')[-1] != "dat" or basename.split('.')[0][:-1] != "Track":
                msgBox = QMessageBox()
                msgBox.setText("No se puede cargar ese tipo de archivos.")
                msgBox.setStandardButtons(QMessageBox.Cancel)
                msgBox.exec()
            else:
                # Cargamos el archivo seleccionado.
                data_base = LoadData(pathfile)
                data_dict = data_base.GetDataIonizations

                # Cargamos el Plot3DView en la pagina principal
                if self.geometry_widget is None:
                    self.geometry_widget = Plot3DView(data=data_dict)
                    self.central_widget.addWidget(self.geometry_widget)
                else:
                    self.geometry_widget.update_data(data_dict)
                self.central_widget.setCurrentWidget(self.geometry_widget)

    def save_file(self):
        opciones = QFileDialog.Options()
        opciones |= QFileDialog.DontUseNativeDialog
        archivo, _ = QFileDialog.getSaveFileName(
            self, "Guardar archivo", "",
            "Archivos de texto (*.txt);;Todos los archivos (*)",
            options=opciones
        )
        if archivo:
            print(f'Se guardará el archivo en: {archivo}')


# stylesheet = '''
#     QMainWindow {
#         background-image: url(./icon_mc-tcad.png);
#         background-repeat: no-repeat;
#         background-position: center;
#     }
# '''

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # app.setStyleSheet(stylesheet)
    mainWin = VentanaPrincipal()

    availableGeometry = mainWin.screen().availableGeometry()
    mainWin.resize(availableGeometry.width()/2, availableGeometry.height()/2)
    mainWin.show()

    sys.exit(app.exec())
