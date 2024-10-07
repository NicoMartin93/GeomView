
import os
import sys
import ast
import plotly.express as px

from PySide6 import QtWidgets, QtGui
from PySide6.QtCore import QUrl, QPoint, Qt
from PySide6.QtGui import QGuiApplication, QSurfaceFormat, QAction
from PySide6.QtQml import QQmlApplicationEngine


from PySide6.QtAxContainer import QAxSelect, QAxWidget
from PySide6.QtWidgets import *
from PySide6.QtQuick3D import QQuick3D
from PySide6.QtQuick import QQuickView, QQuickWindow, QSGRendererInterface
from PySide6.QtQuickWidgets import QQuickWidget
from PySide6.QtWebEngineWidgets import QWebEngineView

from GeomView.main_geometry import GeometryDefinition
from GeomView.WindowPlotly import WidgetPlotly

import plotly.graph_objects as go
# ----------------------------------------------------------------

def class_name(o):
    return o.metaObject().className()

def init_widget(w, name):
    """Init a widget for the gallery, give it a tooltip showing the
       class name"""
    w.setObjectName(name)
    w.setToolTip(class_name(w))

def style_names(list_name):
    """Return a list of styles, default platform style first"""
    if list_name == 'surface':
        style_list = ['Surface','Surface implicit form', 'Plane', 'Esfera',
                           'Cylinder', 'Hyperbolic cylinder', 'Cone', 'One sheet hyperboloid',
                           'Two sheet hyperboloid', 'Paraboloid', 'Parabolic cylinder',
                           'Hyperbolic paraboloid']
    elif list_name == 'units':
        style_list = ['cm', 'inch']
    elif list_name == 'angle':
        style_list = ['Rad', 'Deg']
    elif list_name == 'body':
        style_list = ['Body', 'Module']
    elif list_name == 'material':
        style_list = ['1', '2', '3', '4', '5', '6', '7', '8', '9']

    result = []
    for style in style_list:
        if style.lower() == style_list:
            result.insert(0, style)
        else:
            result.append(style)
    return result

def surfaces_indices(surface):
    style_list = ['Surface','Surface implicit form', 'Plane', 'Esfera',
                       'Cylinder', 'Hyperbolic cylinder', 'Cone', 'One sheet hyperboloid',
                       'Two sheet hyperboloid', 'Paraboloid', 'Parabolic cylinder',
                       'Hyperbolic paraboloid']

    indices = [(1,1,1,1,1), (0,0,0,0,0), (0,0,0,1,0), (1,1,1,0,-1), (1,1,0,0,-1),
            (1,-1,0,0,-1), (1,1,-1,0,0), (1,1,-1,0,-1), (1,1,-1,0,1), (1,1,0,-1,0),
            (1,0,0,-1,0), (1,-1,0,-1,0)]

    for i, surf_list in enumerate(style_list):
        if surface == surf_list:
            return indices[i]

class PopUp(QDialog):
    def __init__(self, labels):
        QDialog.__init__(self, None, Qt.Popup | Qt.FramelessWindowHint)
        self.itemSelected = ""
        self.setLayout(QVBoxLayout())
        lWidget = QListWidget(self)
        self.layout().addWidget(lWidget)
        lWidget.addItems(labels)
        lWidget.itemClicked.connect(self.onItemClicked)
        self.layout().setContentsMargins(0, 0, 0, 0)

    def onItemClicked(self, item):
        self.itemSelected = item.text()
        self.accept()

    def text(self):
        return self.itemSelected


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.setWindowTitle("GeoView - PENELOPE")

        # (1) MENU PRINCIPAL
        # (1.1) FILE
        fileMenu = self.menuBar().addMenu("&File")  # Dentro de File las opciones de Load... y Exit
        loadAction = QAction("Load...", self, shortcut="Ctrl+L", triggered=self.load)
        fileMenu.addAction(loadAction)
        exitAction = QAction("E&xit", self, shortcut="Ctrl+Q", triggered=self.close)
        fileMenu.addAction(exitAction)
        # (1.2) About
        aboutMenu = self.menuBar().addMenu("&About")
        aboutQtAct = QAction("About &Qt", self, triggered=qApp.aboutQt)
        aboutMenu.addAction(aboutQtAct)
        self.axWidget = QAxWidget()
        self.setCentralWidget(self.axWidget)

        # (2) BARRA DE HERRAMIENTAS
        toolBar = QToolBar()
        self.addToolBar(toolBar)
        # Barra de botones
        loadAction = QAction("Load...", self, shortcut="Ctrl+L", triggered=self.load)
        viewAction = QAction('View', self, shortcut="Ctrl+V", triggered=self.view)
        surfacesAction = QAction('Surfaces', self, shortcut="Ctrl+S", triggered=self.surfaces)
        bodiesAction = QAction('Bodies', self, shortcut="Ctrl+B", triggered=self.bodies)
        # Agregamos las acciones
        toolBar.addAction(loadAction)
        toolBar.addAction(surfacesAction)
        toolBar.addAction(bodiesAction)
        toolBar.addAction(viewAction)

        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)

        # Cargamos las clases y pasamos los datos
        self.surfaces_widget = SurfacesWidget(self)
        self.bodies_widget = BodiesWidget(self)



    def load(self):
        axSelect = QAxSelect(self)
        if axSelect.exec() == QDialog.Accepted:
            clsid = axSelect.clsid()
            if not self.axWidget.setControl(clsid):
                QMessageBox.warning(self, "AxViewer", f"Unable to load {clsid}.")

    def view(self):
        engine = QQmlApplicationEngine()
        QSurfaceFormat.setDefaultFormat(QQuick3D.idealSurfaceFormat(4))
        pathfolder = './GeomView/'
        qml_file = os.path.join(pathfolder, 'main.qml')
        engine.load(QUrl.fromLocalFile(qml_file))
        self.engine = engine

        if not engine.rootObjects():
            sys.exit(-1)

    def surfaces(self):

        self.central_widget.addWidget(self.surfaces_widget)
        self.central_widget.setCurrentWidget(self.surfaces_widget)

    def bodies(self):

        self.central_widget.addWidget(self.bodies_widget)
        self.central_widget.setCurrentWidget(self.bodies_widget)

class SurfacesWidget(QWidget):

    def __init__(self, parent=None, data=None):
        super(SurfacesWidget, self).__init__(parent)


        self.__SurfaceLayout_Config()
        self.__SurfaceLayout_TableView()

        layout_surfaces = QHBoxLayout()
        layout_surfaces.addLayout(self.llayout, 49)
        layout_surfaces.addLayout(self.cllayout, 49)
        self.setLayout(layout_surfaces)

    # Utils Function

    def __convert_str_to_tuple(self, var, type):
        s = var.split(",")
        if type == 'int':
            var = tuple([int(i.lstrip('(').rstrip(')')) for i in s])
        elif type == 'str':
            var = tuple([str(i.lstrip('(').rstrip(')')) for i in s])
        elif type == 'float':
            var = tuple([float(i.lstrip('(').rstrip(')')) for i in s])
        return var

    # Surface Configuration

    def __SurfaceLayout_Config(self):

        # --------------------------------------------------
        # # Panel IZQUIERDO - Definición de una superficie

        # (1) Creamos y definimos caracteristicas de los widgets

        self.ConfigGeneral = {}
        self.count_surfaces = 0

        # # Titulo
        self.title_name = QPlainTextEdit()
        self.title_name.setPlainText("Título")

        # # Unidades longiutd
        self._style_unit = QComboBox()
        init_widget(self._style_unit, "styleComboBox")
        self._style_unit.addItems(style_names(list_name='units'))

        style_unit_label = QLabel("Unit:")
        init_widget(style_unit_label, "unit_label")
        style_unit_label.setBuddy(self._style_unit)

        # # Unidades angulares
        self._style_angle = QComboBox()
        init_widget(self._style_angle, "styleComboBox")
        self._style_angle.addItems(style_names(list_name='angle'))

        style_angle_label = QLabel("Angle:")
        init_widget(style_angle_label, "superficie_label")
        style_angle_label.setBuddy(self._style_angle)

        # # Lista de opciones de superficies
        self._style_surfaces = QComboBox()
        init_widget(self._style_surfaces, "styleComboBox")
        self._style_surfaces.addItems(style_names(list_name='surface'))

        style_surface_label = QLabel("Surface:")
        init_widget(style_surface_label, "superficie_label")
        style_surface_label.setBuddy(self._style_surfaces)

        # # Posición de la superficie
        # X
        self._xpos = QDoubleSpinBox()
        self._xpos.setPrefix("xshift: ")
        self._xpos.setValue(0)
        init_widget(self._xpos, "x-label")
        # Y
        self._ypos = QDoubleSpinBox()
        self._ypos.setPrefix("yshift: ")
        self._ypos.setValue(0)
        init_widget(self._ypos, "y-label")
        # Z
        self._zpos = QDoubleSpinBox()
        self._zpos.setPrefix("zshift: ")
        self._zpos.setValue(0)
        init_widget(self._zpos, "z-label")

        # # Rotation
        # Omega
        self._xrot = QDoubleSpinBox()
        self._xrot.setPrefix("Omega: ")
        self._xrot.setValue(0)
        init_widget(self._xrot, "omega-label")
        # Theta
        self._yrot = QDoubleSpinBox()
        self._yrot.setPrefix("Theta: ")
        self._yrot.setValue(0)
        init_widget(self._yrot, "theta-label")
        # Phi
        self._zrot = QDoubleSpinBox()
        self._zrot.setPrefix("Phi: ")
        self._zrot.setValue(0)
        init_widget(self._zrot, "phi-label")

        # # Scale
        # X
        self._xsca = QDoubleSpinBox()
        self._xsca.setPrefix("xscale: ")
        self._xsca.setValue(1)
        init_widget(self._xsca, "xscale-label")
        # Y
        self._ysca = QDoubleSpinBox()
        self._ysca.setPrefix("yscale: ")
        self._ysca.setValue(1)
        init_widget(self._ysca, "yscale-label")
        # Z
        self._zsca = QDoubleSpinBox()
        self._zsca.setPrefix("zscale: ")
        self._zsca.setValue(1)
        init_widget(self._zsca, "zscale-label")

        # # Botones de Agregar o quitar superficie
        self.button1 = QPushButton("Agregar")
        init_widget(self.button1, "agregar_label")
        self.button2 = QPushButton("Quitar")
        init_widget(self.button2, "quitar_label")


        # (2) Agregamos widgets al panel

        self.llayout = QVBoxLayout()
        self.llayout.setContentsMargins(1, 1, 1, 1)
        self.llayout.addWidget(QLabel("Configuración General:"))
        self.llayout.addWidget(self.title_name)
        self.llayout.addWidget(self._style_angle)
        self.llayout.addWidget(self._style_unit)
        self.llayout.addWidget(QLabel("Configuración para Superficies:"))
        self.llayout.addWidget(QLabel("Surfaces:"))
        self.llayout.addWidget(self._style_surfaces)
        self.llayout.addWidget(QLabel("Position:"))
        self.llayout.addWidget(self._xpos)
        self.llayout.addWidget(self._ypos)
        self.llayout.addWidget(self._zpos)
        self.llayout.addWidget(QLabel("Rotation:"))
        self.llayout.addWidget(self._xrot)
        self.llayout.addWidget(self._yrot)
        self.llayout.addWidget(self._zrot)
        self.llayout.addWidget(QLabel("Scale:"))
        self.llayout.addWidget(self._xsca)
        self.llayout.addWidget(self._ysca)
        self.llayout.addWidget(self._zsca)
        self.llayout.addWidget(self.button1)
        self.llayout.addWidget(self.button2)

        # (3) Conectamos los botones a las acciones

        self.button1.clicked.connect(self.__add_table_surface)
        self.button2.clicked.connect(self.__quit_table_surface)

    def __SurfaceLayout_TableView(self):

        # ----------------------------------------------------
        # # Panel CENTRAL IZQUIERDO - View Surfaces definidos

        # (1) Creamos y definimos caracteristicas de los widgets

        # # Tabla con las superficies definidas
        # Nombres de columnas
        self.table_surface = QTableWidget()
        header = self.table_surface.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        self.table_surface.setColumnCount(6)
        self.column_names_surface = ["ID","Surface","Indices","Traslation", "Rotation", "Scale"]
        self.table_surface.setHorizontalHeaderLabels(self.column_names_surface)

        # # Botón de Formar body
        self.button3 = QPushButton("Formar Body")
        init_widget(self.button3, "formar_body_label")

        # (2) Agregamos widgets al panel

        self.cllayout = QVBoxLayout()
        self.cllayout.setContentsMargins(1, 1, 1, 1)
        self.cllayout.addWidget(QLabel("Tabla de superficies:"))
        self.cllayout.addWidget(self.table_surface)
        self.cllayout.addWidget(self.button3)

        # (3) Conectamos los botones a las acciones
        self.button3.clicked.connect(self.formar_body)

    # Surface functions

    def __add_table_surface(self):

        """ Update the plot with the current input values """
        xpos = self._xpos.value()
        ypos = self._ypos.value()
        zpos = self._zpos.value()

        xrot = self._xrot.value()
        yrot = self._yrot.value()
        zrot = self._zrot.value()

        xsca = self._xsca.value()
        ysca = self._ysca.value()
        zsca = self._zsca.value()

        surface = str(self._style_surfaces.currentText())
        indices = surfaces_indices(surface)


        num = self.table_surface.rowCount()

        self.table_surface.setRowCount(num+1)
        self.table_surface.setColumnCount(6)
        self.table_surface.setHorizontalHeaderLabels(self.column_names_surface)

        self.table_surface.setItem(num, 0, QTableWidgetItem(f"S{self.count_surfaces}"))
        self.table_surface.setItem(num, 1, QTableWidgetItem(f"{surface}"))
        self.table_surface.setItem(num, 2, QTableWidgetItem(f"{indices}"))
        self.table_surface.setItem(num, 3, QTableWidgetItem(f"({xpos:.2f},{ypos:.2f},{zpos:.2f})"))
        self.table_surface.setItem(num, 4, QTableWidgetItem(f"({xrot:.2f},{yrot:.2f},{zrot:.2f})"))
        self.table_surface.setItem(num, 5, QTableWidgetItem(f"({xsca:.2f},{ysca:.2f},{zsca:.2f})"))

        # Sumamos una superficie mas!
        self.count_surfaces += 1

    def __quit_table_surface(self):
        num = self.table_surface.rowCount()

        if num != 0:
            self.table_surface.removeRow(num+1)
            self.table_surface.setRowCount(num-1)
            self.table_surface.setHorizontalHeaderLabels(self.column_names_surface)
            self.count_surfaces -= 1

        elif num == 0:
            msgBox = QMessageBox()
            msgBox.setText("No hay superficies para quitar de la tabla.")
            msgBox.setStandardButtons(QMessageBox.Cancel)
            ret = msgBox.exec()

    def formar_body(self):

        """ Update the plot with the current input values """

        if self.table_surface.rowCount() != 0:

            self.surfacesOfBody = {}
            num = self.table_surface.rowCount()
            for n in range(num):

                self.surfaceID = {}
                # Extraemos la información de la superficie
                Id_Surface = self.table_surface.item(n, 0).text()
                Ty_Surface = self.table_surface.item(n, 1).text()
                In_Surface = self.table_surface.item(n, 2).text()
                Ps_Surface = self.table_surface.item(n, 3).text()
                Rt_Surface = self.table_surface.item(n, 4).text()
                Sc_Surface = self.table_surface.item(n, 5).text()

                In_Surface = self.__convert_str_to_tuple(In_Surface, type='int')
                Ps_Surface = self.__convert_str_to_tuple(Ps_Surface, type='float')
                Rt_Surface = self.__convert_str_to_tuple(Rt_Surface, type='float')
                Sc_Surface = self.__convert_str_to_tuple(Sc_Surface, type='float')

                self.surfaceID['Type'] = Ty_Surface
                self.surfaceID['Label'] = Id_Surface
                self.surfaceID['Indices'] = In_Surface
                self.surfaceID['Position'] = Ps_Surface
                self.surfaceID['Rotation'] = Rt_Surface
                self.surfaceID['Scale'] = Sc_Surface

                self.surfacesOfBody['{}'.format(Id_Surface)] = self.surfaceID

            # Quitamos los datos de la tabla surface
            self.table_surface.setRowCount(0)

            return self.surfacesOfBody


        elif self.table_surface.rowCount() == 0:
            msgBox = QMessageBox()
            msgBox.setText("No hay superficies previamente agregadas.")
            msgBox.setStandardButtons(QMessageBox.Cancel)
            ret = msgBox.exec()

            return print("Error")

class BodiesWidget(QWidget):

    def __init__(self, parent=None, data=None):
        super(BodiesWidget, self).__init__(parent)

        self.__BodyLayout_Config()
        self.__BodyLayout_TableView()

        layout_bodies = QHBoxLayout()
        layout_bodies.addLayout(self.crlayout, 49)
        layout_bodies.addLayout(self.rlayout, 49)
        self.setLayout(layout_bodies)

    # ============= BODIES CONFIGURATION ==============

    def __BodyLayout_Config(self):

        # ---------------------------------------------------------
        # # Panel CENTRAL DERECHO - Definimos los cuerpos o modulos

        # (1) Creamos los widgets

        self.count_body = 0
        self.BodyList = []

        # # Lista de opciones de superficies
        self._style_body = QComboBox()
        init_widget(self._style_body, "styleComboBox")
        self._style_body.addItems(style_names(list_name='body'))

        style_body_label = QLabel("Options:")
        init_widget(style_body_label, "body_label")
        style_body_label.setBuddy(self._style_body)

        # # Nombre del body
        self.body_name = QPlainTextEdit()
        self.body_name.setPlainText("Body 0")

        # # Lista de Materiales
        self._style_material = QComboBox()
        init_widget(self._style_material, "styleComboBox")
        self._style_material.addItems(style_names(list_name='material'))

        style_material_label = QLabel("Material:")
        init_widget(style_body_label, "material_label")
        style_material_label.setBuddy(self._style_material)

        # # Table surperficies definidas
        self.column_names_surf = ['Surface', 'Side Pointer']
        self.table_surf = QTableWidget()
        header = self.table_surf.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        self.table_surf.setColumnCount(2)
        self.table_surf.setHorizontalHeaderLabels(self.column_names_surf)

        # # Comentario
        self.body_comment = QPlainTextEdit()
        self.body_comment.setPlainText("Comentario")

        # # Agregar body
        self.button_mat = QPushButton("Agregar material")
        self.button4 = QPushButton("Agregar")
        self.button5 = QPushButton("Quitar")
        init_widget(self.button4, "agregar_body_label")
        init_widget(self.button5, "quitar_body_label")

        # (2) Agregamos widgets al panel

        self.crlayout = QVBoxLayout()
        self.crlayout.setContentsMargins(1, 1, 1, 1)
        self.crlayout.addWidget(QLabel("Configuración para Cuerpos:"))
        self.crlayout.addWidget(QLabel("Body o Module:"))
        self.crlayout.addWidget(self._style_body)
        self.crlayout.addWidget(QLabel("ID - Body o Module:"))
        self.crlayout.addWidget(self.body_name)
        self.crlayout.addWidget(self.table_surf)
        self.crlayout.addWidget(QLabel("Material:"))
        self.crlayout.addWidget(self._style_material)
        self.crlayout.addWidget(self.button_mat)
        self.crlayout.addWidget(QLabel("Comentario:"))
        self.crlayout.addWidget(self.body_comment)
        self.crlayout.addWidget(self.button4)
        self.crlayout.addWidget(self.button5)

        # (3) Conectamos los botones a las acciones

        self.table_surf.clicked.connect(self.__onClicked_TableSurf)
        self.button_mat.clicked.connect(self.__add_material)
        self.button4.clicked.connect(self.__add_table_body)
        self.button5.clicked.connect(self.__quit_table_body)

    def __BodyLayout_TableView(self):

        # ---------------------------------------------------------
        # # Panel CENTRAL DERECHO - View Surfaces definidos

        # (1) Creamos y definimos caracteristicas de los widgets

        # # Tabla de bodys o modulos
        self.table_body = QTableWidget()
        header = self.table_body.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        self.table_body.setColumnCount(6)
        self.column_names_body = ["ID","Body", "Material", "Surfaces", "Side Point", "Comentario"]
        self.table_body.setHorizontalHeaderLabels(self.column_names_body)

        # # Tabla de grupos de bodys o module
        self.table_group = QTableWidget()
        header = self.table_group.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        self.table_group.setColumnCount(2)
        self.column_names_group = ["Externo", "Internos"]
        self.table_group.setHorizontalHeaderLabels(self.column_names_group)

        # # Botones para agregar y quitar bodys
        self.button6 = QPushButton("Crear grupo")
        init_widget(self.button6, "crear_grupo_label")
        self.button7 = QPushButton("Quitar grupo")
        init_widget(self.button7, "quitar_grupo_label")
        self.button8 = QPushButton('Plotly')
        init_widget(self.button8, "view_plotly")
        self.button9 = QPushButton("View")
        init_widget(self.button9, "view_label")
        self.button10 = QPushButton("Armar Geometría")
        init_widget(self.button10, "armar_geometry_label")

        # (2) Agregamos widgets al panel

        self.rlayout = QVBoxLayout()
        self.rlayout.setContentsMargins(1, 1, 1, 1)
        self.rlayout.addWidget(QLabel("Tabla de cuerpos:"))
        self.rlayout.addWidget(self.table_body)
        self.rlayout.addWidget(QLabel("Grupos de cuerpos:"))
        self.rlayout.addWidget(self.button6)
        self.rlayout.addWidget(self.table_group)
        self.rlayout.addWidget(self.button7)
        self.rlayout.addWidget(QLabel("Visualizar Geometría:"))
        self.rlayout.addWidget(self.button8)
        self.rlayout.addWidget(self.button9)
        self.rlayout.addWidget(QLabel("Script Geometry - PENELOPE:"))
        self.rlayout.addWidget(self.button10)

        # (3) Conectamos los botones a las acciones

        self.table_body.itemClicked.connect(self.__OnlyCellChecked)
        self.table_group.clicked.connect(self.__onClicked_TableGroup)
        self.button6.clicked.connect(self.__add_table_group)
        self.button7.clicked.connect(self.__quit_table_group)
        self.button8.clicked.connect(self.view_plotly)
        # self.button9.clicked.connect(self.view)
        self.button10.clicked.connect(self.__GetGeometryInput)

    # Bodys functions

    def __convert_str_to_tuple(self, var, type):
        s = var.split(",")
        if type == 'int':
            var = tuple([int(i.lstrip('(').rstrip(')')) for i in s])
        elif type == 'str':
            var = tuple([str(i.lstrip('(').rstrip(')')) for i in s])
        elif type == 'float':
            var = tuple([float(i.lstrip('(').rstrip(')')) for i in s])
        return var

    def _formar_table_body(self, data_surface):

        """ Update the plot with the current input values """

        if self.table_surface.rowCount() != 0:

            self.SurfacesOfBody = {}
            num = self.table_surface.rowCount()
            for n in range(num):

                self.SurfaceID = {}
                # Extraemos la información de la superficie
                Id_Surface = self.table_surface.item(n, 0).text()
                Ty_Surface = self.table_surface.item(n, 1).text()
                In_Surface = self.table_surface.item(n, 2).text()
                Ps_Surface = self.table_surface.item(n, 3).text()
                Rt_Surface = self.table_surface.item(n, 4).text()
                Sc_Surface = self.table_surface.item(n, 5).text()

                In_Surface = self.__convert_str_to_tuple(In_Surface, type='int')
                Ps_Surface = self.__convert_str_to_tuple(Ps_Surface, type='float')
                Rt_Surface = self.__convert_str_to_tuple(Rt_Surface, type='float')
                Sc_Surface = self.__convert_str_to_tuple(Sc_Surface, type='float')

                self.SurfaceID['Type'] = Ty_Surface
                self.SurfaceID['Label'] = Id_Surface
                self.SurfaceID['Indices'] = In_Surface
                self.SurfaceID['Position'] = Ps_Surface
                self.SurfaceID['Rotation'] = Rt_Surface
                self.SurfaceID['Scale'] = Sc_Surface

                self.SurfacesOfBody['{}'.format(Id_Surface)] = self.SurfaceID

                # Agregamos las superficies a la subtabla
                self.table_surf.setRowCount(n+1)
                self.table_surf.setColumnCount(2)
                self.table_surf.setHorizontalHeaderLabels(self.column_names_surf)
                self.table_surf.setItem(n, 0, QTableWidgetItem(f"{Id_Surface}"))
                self.table_surf.setItem(n, 1, QTableWidgetItem("1"))

        elif self.table_surface.rowCount() == 0:
            msgBox = QMessageBox()
            msgBox.setText("No hay superficies previamente agregadas.")
            msgBox.setStandardButtons(QMessageBox.Cancel)
            ret = msgBox.exec()

        # Quitamos los datos de la tabla surface
        self.table_surface.setRowCount(0)

    def __add_material(self):
        print("Continuara...")

    def __add_table_body(self):

        """ Update the plot with the current input values """
        num = self.table_surf.rowCount()

        if num != 0:

            self.Body = {}

            # Extraemos la información del Body
            self.__Id_Body = f"B{self.count_body}"
            self.__Ty_Body = str(self._style_body.currentText())
            self.__Mt_Body = str(self._style_material.currentText())
            self.__Cm_Body = self.body_comment.toPlainText()

            num = self.table_surf.rowCount()
            self.__Tb_Body = []
            self.__Sf_Body = []
            self.__Sp_Body = []
            for n in range(num):
                surf = self.table_surf.item(n,0).text()
                item = self.table_surf.item(n,1).text()
                self.__Sf_Body.append(surf)
                self.__Tb_Body.append(item)
                self.__Sp_Body.append((surf,item))

            # Lo agregamos a la tabla de Bodys
            num = self.table_body.rowCount()
            self.table_body.setRowCount(num+1)
            self.table_body.setColumnCount(6)
            self.table_body.setHorizontalHeaderLabels(self.column_names_body)

            self.__chkBoxID = QTableWidgetItem(f"{self.__Id_Body}")
            self.__chkBoxID.setText(f"{self.__Id_Body}")
            self.__chkBoxID.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            self.__chkBoxID.setCheckState(Qt.Unchecked)

            self.table_body.setItem(num, 0, self.__chkBoxID)
            self.table_body.setItem(num, 1, QTableWidgetItem(f"{self.__Ty_Body}"))
            self.table_body.setItem(num, 2, QTableWidgetItem(f"{self.__Mt_Body}"))
            self.table_body.setItem(num, 3, QTableWidgetItem(f"{self.__Sf_Body}"))
            self.table_body.setItem(num, 4, QTableWidgetItem(f"{self.__Tb_Body}"))
            self.table_body.setItem(num, 5, QTableWidgetItem(f"{self.__Cm_Body}"))


            # Guardamos la información en una lista
            self.Body['Surfaces'] = self.SurfacesOfBody
            self.Body['ID'] = self.__Id_Body
            self.Body['Type'] = self.__Ty_Body
            self.Body['Material'] = self.__Mt_Body
            self.Body['SidePoint'] = self.__Sp_Body
            self.Body['Comment'] = self.__Cm_Body

            self.BodyList.append(self.Body)

            # Sumamos un body mas
            self.count_body += 1

        elif num == 0:

            msgBox = QMessageBox()
            msgBox.setText("No hay superficies previamente agregadas.")
            msgBox.setStandardButtons(QMessageBox.Cancel)
            ret = msgBox.exec()

        # Quitamos los datos de la tabla surface
        self.table_surf.setRowCount(0)

    def __quit_table_body(self):
        # Quitamos el ultimo Body agregado a la tabla.
        num = self.table_body.rowCount()
        if num != 0:
            self.table_body.removeRow(num+1)
            self.table_body.setRowCount(num-1)
            self.table_body.setHorizontalHeaderLabels(self.column_names_body)

            # Quitamos un elemento del conteo de bodys
            self.count_body -= 1
            self.count_surfaces -= len(self.__Sf_Body)
            # Quitamos el ultimo elemento de la lista.
            self.BodyList = self.BodyList[:-1]
        elif num == 0:
            msgBox = QMessageBox()
            msgBox.setText("No hay bodys para quitar de la tabla.")
            msgBox.setStandardButtons(QMessageBox.Cancel)
            ret = msgBox.exec()

    def __onClicked_TableSurf(self, index):
        row = index.row()
        column = index.column()
        x = self.table_surf.columnViewportPosition(column)
        y = self.table_surf.rowViewportPosition(row) + self.table_surf.rowHeight(row)
        pos = self.table_surf.viewport().mapToGlobal(QPoint(x, y))
        p = PopUp(["-1", "1"])
        p.move(pos)
        if p.exec() == QDialog.Accepted:
            t_item = QTableWidgetItem(p.text())
            self.table_surf.setItem(row, 1, t_item)

    # Group functions

    def __add_table_group(self):

        """ Update the plot with the current input values """
        self.RowBodysList = []

        # # Tomamos el ID del Body checked.
        for i in range(self.table_body.rowCount()):
            if self.table_body.item(i, 0).checkState() == Qt.Checked:
                checked_body = self.table_body.item(i, 0).text()
                checked = 'Checked'
                break
            else:
                checked = 'Unchecked'

        if checked == 'Checked':

            # Lo agregamos a la tabla de Grupos de Bodys.
            num = self.table_group.rowCount()
            self.table_group.setRowCount(num+1)
            self.table_group.setColumnCount(2)
            self.table_group.setHorizontalHeaderLabels(self.column_names_group)

            self.table_group.setItem(num, 0, QTableWidgetItem(checked_body))
            self.table_group.setItem(num, 1, QTableWidgetItem(f"Vacio"))

            # # Creamos una lista con los Bodys creados y quitamos el checked
            self.__List_Bodys = []
            num_body = self.table_body.rowCount()
            for n in range(num_body):
                bodyID = self.table_body.item(n,0).text()
                self.__List_Bodys.append(bodyID)

            self.__List_Bodys.remove(checked_body)
            # # Unchecked de la tabla de Bodys.
            self.__chkBoxID.setCheckState(Qt.Unchecked)

        elif checked == 'Unchecked':
            msgBox = QMessageBox()
            msgBox.setText("No hay un Body marcado para crear un grupo.")
            msgBox.setStandardButtons(QMessageBox.Cancel)
            ret = msgBox.exec()

    def __quit_table_group(self):
        # Quitamos el ultimo Body agregado a la tabla.
        num = self.table_group.rowCount()
        if num != 0:
            self.table_group.removeRow(num+1)
            self.table_group.setRowCount(num-1)
            self.table_group.setHorizontalHeaderLabels(self.column_names_group)

        elif num == 0:
            msgBox = QMessageBox()
            msgBox.setText("No hay grupos para quitar de la tabla.")
            msgBox.setStandardButtons(QMessageBox.Cancel)
            ret = msgBox.exec()

    def __onClicked_TableGroup(self, index):

        row = index.row()
        column = index.column()
        x = self.table_group.columnViewportPosition(column)
        y = self.table_group.rowViewportPosition(row) + self.table_group.rowHeight(row)
        pos = self.table_group.viewport().mapToGlobal(QPoint(x, y))
        p = PopUp(self.__List_Bodys)
        p.move(pos)
        if p.exec() == QDialog.Accepted:
            # t_item = QTableWidgetItem(p.text())
            # self.table_group.setItem(row, 1, t_item)
            self.RowBodysList.append(p.text())

            self.table_group.setItem(row, 1, QTableWidgetItem(str(self.RowBodysList)))

            self.__List_Bodys.remove(p.text())

    def __OnlyCellChecked(self):
        list_checked = []
        for i in range(self.table_body.rowCount()):
            if self.table_body.item(i, 0).checkState() == Qt.Checked:
                list_checked.append(self.table_body.item(i, 0).text())

        if len(list_checked) > 1:
            for i in range(self.table_body.rowCount()):
                if self.table_body.item(i, 0).checkState() == Qt.Checked:
                    self.table_body.item(i,0).setCheckState(Qt.Unchecked)


    # ========= GET DATA INPUT ==========


    def __TypeSurface(self, body, type_surface, surface_label):

        # Definimos parametros del surface
        surface = body['Surfaces'][surface_label]
        label = '{}'.format(surface['Label'])
        indices = surface['Indices']
        scale = surface['Scale']
        rotation = surface['Rotation']
        translation = surface['Position']
        angle = '{}'.format(self.__Angle)

        if type_surface == 'Surface':
            self.g.surface(label=label, indices=indices, scale=scale, rotation=rotation, translation=translation, angle=angle)

        elif type_surface == 'Surface implicit form':
            self.g.surface_implicit_form(label=label, indices=indices, scale=scale, rotation=rotation, translation=translation, angle=angle)

        elif type_surface == 'Plane':
            self.g.surface_plane(label=label, indices=indices, scale=scale, rotation=rotation, translation=translation, angle=angle)

        elif type_surface == 'Esfera':
            self.g.surface_sphere(label=label, indices=indices, scale=scale, rotation=rotation, translation=translation, angle=angle)

        elif type_surface == 'Cylinder':
            self.g.surface_implicit_form(label=label, indices=indices, scale=scale, rotation=rotation, translation=translation, angle=angle)

        elif type_surface == 'Hyperbolic cylinder':
            self.g.surface_hyperbolic_cylinder(label=label, indices=indices, scale=scale, rotation=rotation, translation=translation, angle=angle)

        elif type_surface == 'Cone':
            self.g.surface_cone(label=label, indices=indices, scale=scale, rotation=rotation, translation=translation, angle=angle)

        elif type_surface == 'One sheet hyperboloid':
            self.g.surface_one_sheet_hyperboloid(label=label, indices=indices, scale=scale, rotation=rotation, translation=translation, angle=angle)

        elif type_surface == 'Two sheet hyperboloid':
            self.g.surface_two_sheet_hyperboloid(label=label, indices=indices, scale=scale, rotation=rotation, translation=translation, angle=angle)

        elif type_surface == 'Paraboloid':
            self.g.surface_paraboloid(label=label, indices=indices, scale=scale, rotation=rotation, translation=translation, angle=angle)

        elif type_surface == 'Parabolic cylinder':
            self.g.surface_parabolic_cylinder(label=label, indices=indices, scale=scale, rotation=rotation, translation=translation, angle=angle)

        elif type_surface == 'Hyperbolic paraboloid':
            selg.g.surface_hyperbolic_paraboloid(label=label, indices=indices, scale=scale, rotation=rotation, translation=translation, angle=angle)

        else:
            msgBox = QMessageBox()
            msgBox.setText("No se identifico el tipo de superficie.")
            msgBox.setStandardButtons(QMessageBox.Cancel)
            ret = msgBox.exec()

    def __GetGeometryInput(self):

        # General
        self.__Title = self.title_name.toPlainText()
        self.__Unit = str(self._style_unit.currentText())
        self.__Angle = str(self._style_angle.currentText())

        # BodyGroup
        self.BodyGroup = {}
        num_group = self.table_group.rowCount()
        if num_group != 0:
            for n in range(num_group):
                 surf_ext = self.table_group.item(n,0).text()
                 surf_int = self.table_group.item(n,1).text()
                 surf_int = ast.literal_eval(surf_int)
                 self.BodyGroup[surf_ext] = surf_int


        # # Iniciamos
        self.g=GeometryDefinition("{}".format(self.__Title), unit="{}".format(self.__Unit), angle="{}".format(self.__Angle))

        for i, body in enumerate(self.BodyList):

            # (1) Definimos las superficies
            surfaces = list(body['Surfaces'].keys())

            for j,surf in enumerate(surfaces):

                type_surface = body['Surfaces'][surf]['Type']
                self.__TypeSurface(body, type_surface, surface_label=surf)

            if body['Type'] == 'Body':

                label = body['ID']
                material = int(body['Material'])
                surf_list = [(tup[0],int(tup[1])) for tup in body['SidePoint']]
                comment = body['Comment']

                if num_group != 0 :
                    body_group = list(self.BodyGroup.keys())
                    if label in body_group and label.startswith('B'):
                        bodies = self.BodyGroup[label]
                        self.g.body(label=label, material=material, surfaces=surf_list, bodies=bodies, comment=comment)
                    else:
                        self.g.body(label=label, material=material, surfaces=surf_list, comment=comment)
                else:
                    self.g.body(label=label, material=material, surfaces=surf_list, comment=comment)

            elif body['Type'] == 'Module':

                label = body['ID']
                material = int(body['Material'])
                surf_list = [(tup[0],int(tup[1])) for tup in body['SidePoint']]
                comment = body['Comment']

                if num_goup != 0:
                    body_group = list(self.BodyGroup.keys())
                    if label in body_group and label.startswith('M'):
                        bodies = self.BodyGroup[label]
                        self.g.module(label=label, material=material, surfaces=surf_list, bodies=bodies, comment=comment)
                    else:
                        self.g.module(label=label, material=material, surfaces=surf_list, comment=comment)
                else:
                    self.g.module(label=label, material=material, surfaces=surf_list, comment=comment)

        e=self.g.end()
        self.g.show_void_inner_volumes(False)
        print(self.g)
        self.g.export_definition("test")

        # s1=g.surface(starred=True)
        # s2=g.surface(indices=(1,0,1,0,1), scale=(2,3,4), rotation=(5,6,7), translation=(8,9,1))
        # s3=g.surface(indices=(1,0,1,0,1), xscale=20, yscale=30, zscale=40, omega=50, theta=60, phi=70, xshift=80, yshift=90, zshift=100, angle="deg")
        #
        # b1=g.body("B1", material=-100, comment="body number 1")
        # b2=g.body("B2", material=-200, surfaces=[(s1, 1), (s2, -1)], bodies=[b1], comment="body number 2")
        #
        # m1=g.module(material=3, surfaces=[(s1, 1), (s2, -1), (s3, 1)], bodies=["B2"], modules=["M2"], scale=(2,3,4), rotation=(5,6,7), translation=(8,9,1), angle="deg", comment="module number 1")
        # m2=g.module("M2", material=4, surfaces=[(s1, 1), (s2, -1), (s3, 1)], bodies=[b2], modules=[m1], xscale=20, yscale=30, zscale=40, omega=50, theta=60, phi=70, xshift=80, yshift=90, zshift=100, comment="module number 2")
        # m3=g.module("M3", material=5, comment="module number 3")
        #
        # c1=g.clone("C1", m1, comment="clone number 1")
        # c2=g.clone("C2", m2, scale=(2,3,4), rotation=(5,6,7), translation=(8,9,1), comment="clone number 2")
        # c3=g.clone("C3", "M3", xscale=20, yscale=30, zscale=40, omega=50, theta=60, phi=70, xshift=80, yshift=90, zshift=100, unit="cm", angle="rad", comment="clone number 3")
        #
        # f1=g.include("filename1.test", comment="non starred file")
        # f2=g.include("filename2.test", starred=True, comment="starred file")
        #
        # e=g.end()
        #
        # g.show_void_inner_volumes(False)
        #

    # ============ VIEW GEOMETRY =============

    def Load_QML(self):

        pathfile = 'D:\Proyectos_Investigacion\Proyectos_de_Doctorado\Main_Code\GeomView\main.qml'
        # pathfile = self.pathfile_qml
        file = open(pathfile)
        string_list = file.readlines()
        file.close()

        num_line = [i for i,line in enumerate(string_list) if line.find('//! [objects]') != -1]

        model = ['Model {',
                'position: Qt.vector3d({})'.format(),
                'source: "#{}"'.format(),
                'scale: Qt.vector3d({})'.format(),
                'materials: [ DefaultMaterial {',
                'diffuseColor: "{}"'.format(),
                '}',
                ']',
                '}']

        # ----------------------------------------------------------------------
        # (1) Separamos los datos obtenidos según su encabezado


        #             View3D {
        #                 id: view
        #                 width: parent.width - x
        #                 height: parent.height - y
        #
        #                 //! [environment]
        #                 environment: SceneEnvironment {
        #                     clearColor: "skyblue"
        #                     backgroundMode: SceneEnvironment.Color
        #                 }
        #                 //! [environment]
        #
        #                 //! [camera]
        #                 PerspectiveCamera {
        #                     position: Qt.vector3d(0, 200, 300)
        #                     eulerRotation.x: -30
        #                 }
        #                 //! [camera]
        #
        #                 //! [light]
        #                 DirectionalLight {
        #                     eulerRotation.x: -30
        #                     eulerRotation.y: -70
        #                 }
        #                 //! [light]
        #
        #                 //! [objects]
        #                 Model {
        #                     position: Qt.vector3d(0, -200, 0)
        #                     source: "#Cylinder"
        #                     scale: Qt.vector3d(2, 0.2, 1)
        #                     materials: [ DefaultMaterial {
        #                             diffuseColor: "red"
        #                         }
        #                     ]
        #                 }
        #
        #                 Model {
        #                     position: Qt.vector3d(0, 150, 0)
        #                     source: "#Sphere"
        #
        #                     materials: [ DefaultMaterial {
        #                             diffuseColor: "blue"
        #                         }
        #                     ]
        #                 }
        #                 //! [objects]
        #             }
        #           }
        #         }
        #         Popup {
        #           id: normalPopup
        #           ColumnLayout {
        #             anchors.fill: parent
        #             Label { text: 'Normal Popup' }
        #             CheckBox { text: 'E-mail' }
        #             CheckBox { text: 'Calendar' }
        #             CheckBox { text: 'Contacts' }
        #           }
        #         }
        #         Popup {
        #           id: modalPopup
        #           modal: true
        #           ColumnLayout {
        #             anchors.fill: parent
        #             Label { text: 'Modal Popup' }
        #             CheckBox { text: 'E-mail' }
        #             CheckBox { text: 'Calendar' }
        #             CheckBox { text: 'Contacts' }
        #           }
        #         }
        #         Dialog {
        #           id: dialog
        #           title: 'Dialog'
        #           Label { text: 'The standard dialog.' }
        #           footer: DialogButtonBox {
        #             standardButtons: DialogButtonBox.Ok | DialogButtonBox.Cancel
        #           }
        #         }
        #       }
        #     }
        #
        #
        # }

    def view_plotly(self):
        self._window_plotly = WidgetPlotly()
        self._window_plotly.show()

    def Get3DView(self):
        print(' ')





if __name__ == "__main__":
    # app = QGuiApplication(sys.argv)
    app = QApplication(sys.argv)

    # Ventana de ajustes
    mainWin = MainWindow()
    availableGeometry = mainWin.screen().availableGeometry()
    mainWin.resize(availableGeometry.width() / 2, availableGeometry.height() / 2)
    mainWin.show()

    sys.exit(app.exec())
