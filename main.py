
import os
import sys

from PyQt5 import QtCore
from PySide6.QtCore import QUrl, QPoint, Qt
from PySide6.QtGui import QGuiApplication, QSurfaceFormat, QAction
from PySide6.QtQml import QQmlApplicationEngine

from PySide6.QtAxContainer import QAxSelect, QAxWidget
from PySide6.QtWidgets import *
from PySide6.QtQuick3D import QQuick3D
from PySide6.QtQuick import QQuickView, QQuickWindow, QSGRendererInterface
from PySide6.QtQuickWidgets import QQuickWidget

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
    elif list_name == 'angle':
        style_list = ['Rad', 'Deg']
    elif list_name == 'body':
        style_list = ['Body', 'Module']
    elif list_name == 'material':
        style_list = ['Cdte', 'Si']

    result = []
    for style in style_list:
        if style.lower() == style_list:
            result.insert(0, style)
        else:
            result.append(style)
    return result

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

    def __init__(self):
        super().__init__()

        # (1) Barra de herramientas superior
        toolBar = QToolBar()
        self.addToolBar(toolBar)

        # (1.1) Definimos FILE
        fileMenu = self.menuBar().addMenu("&File")
        # Dentro de File las opciones de Load... y Exit

        # Definimos la accion de Load
        loadAction = QAction("Load...", self, shortcut="Ctrl+L", triggered=self.load)
        viewAction = QAction('View', self, shortcut="Ctrl+V", triggered=self.view)
        # Agregamos la accion en la barra de herramienta al apretar Load...
        fileMenu.addAction(loadAction)
        # Agregamos la accion en el menu principal de opciones
        toolBar.addAction(loadAction)
        toolBar.addAction(viewAction)
        exitAction = QAction("E&xit", self, shortcut="Ctrl+Q", triggered=self.close)
        fileMenu.addAction(exitAction)

        # (1.2) Definimos About
        aboutMenu = self.menuBar().addMenu("&About")
        aboutQtAct = QAction("About &Qt", self, triggered=qApp.aboutQt)
        aboutMenu.addAction(aboutQtAct)
        self.axWidget = QAxWidget()
        self.setCentralWidget(self.axWidget)

        # (2) Definimos barra de control y tabla
        self.__SurfaceBodyConfiguration()


    def load(self):
        axSelect = QAxSelect(self)
        if axSelect.exec() == QDialog.Accepted:
            clsid = axSelect.clsid()
            if not self.axWidget.setControl(clsid):
                QMessageBox.warning(self, "AxViewer", f"Unable to load {clsid}.")

    def view(self):
        engine = QQmlApplicationEngine()
        QSurfaceFormat.setDefaultFormat(QQuick3D.idealSurfaceFormat(4))
        pathfolder = 'D:\Proyectos_Investigacion\Proyectos_de_Doctorado\Main_Code\Prueba'
        qml_file = os.path.join(pathfolder, 'main.qml')
        engine.load(QUrl.fromLocalFile(qml_file))
        self.engine = engine

        if not engine.rootObjects():
            sys.exit(-1)

    def input(self):
        print('Continuara...')

    # ============= SURFACE-BODY CONFIGURATION ==============

    def __SurfaceBodyConfiguration(self):

        # Central widget
        self._main = QWidget()
        self.setCentralWidget(self._main)

        # --------------------------------------------------
        # # Panel IZQUIERDO

        # (1) Creamos los widgets

        # Lista de opciones de superficies
        self._style_surfaces = QComboBox()
        init_widget(self._style_surfaces, "styleComboBox")
        self._style_surfaces.addItems(style_names(list_name='surface'))

        style_surface_label = QLabel("Surface:")
        init_widget(style_surface_label, "superficie_label")
        style_surface_label.setBuddy(self._style_surfaces)

        # Posiciones
        self.xpos = QDoubleSpinBox()
        self.ypos = QDoubleSpinBox()
        self.zpos = QDoubleSpinBox()
        self.xpos.setPrefix("xshift: ")
        self.ypos.setPrefix("yshift: ")
        self.zpos.setPrefix("zshift: ")
        self.xpos.setValue(10)
        self.ypos.setValue(10)
        self.zpos.setValue(10)
        init_widget(self.xpos, "x-label")
        init_widget(self.ypos, "y-label")
        init_widget(self.zpos, "z-label")

        # Rotation
        self.xrot = QDoubleSpinBox()
        self.yrot = QDoubleSpinBox()
        self.zrot = QDoubleSpinBox()
        self.xrot.setPrefix("Omega: ")
        self.yrot.setPrefix("Theta: ")
        self.zrot.setPrefix("Phi: ")
        self.xrot.setValue(0)
        self.yrot.setValue(0)
        self.zrot.setValue(0)
        init_widget(self.xrot, "omega-label")
        init_widget(self.yrot, "theta-label")
        init_widget(self.zrot, "phi-label")

        # Lista de opciones de medidas de angulo
        self._style_angle = QComboBox()
        init_widget(self._style_angle, "styleComboBox")
        self._style_angle.addItems(style_names(list_name='angle'))

        style_angle_label = QLabel("Angle type:")
        init_widget(style_angle_label, "angle_label")
        style_angle_label.setBuddy(self._style_angle)

        # Scale
        self.xsca = QDoubleSpinBox()
        self.ysca = QDoubleSpinBox()
        self.zsca = QDoubleSpinBox()
        self.xsca.setPrefix("xscale: ")
        self.ysca.setPrefix("yscale: ")
        self.zsca.setPrefix("zscale: ")
        self.xsca.setValue(1)
        self.ysca.setValue(1)
        self.zsca.setValue(1)
        init_widget(self.xsca, "xscale-label")
        init_widget(self.ysca, "yscale-label")
        init_widget(self.zsca, "zscale-label")

        # Agregar o quitar superficie
        self.button1 = QPushButton("Agregar")
        self.button2 = QPushButton("Quitar")
        init_widget(self.button1, "agregar_label")
        init_widget(self.button2, "quitar_label")

        # Agregamos widgets
        llayout = QVBoxLayout()
        llayout.setContentsMargins(1, 1, 1, 1)
        llayout.addWidget(QLabel("Configuración:"))
        llayout.addWidget(QLabel("Surfaces:"))
        llayout.addWidget(self._style_surfaces)
        llayout.addWidget(QLabel("Position:"))
        llayout.addWidget(self.xpos)
        llayout.addWidget(self.ypos)
        llayout.addWidget(self.zpos)
        llayout.addWidget(QLabel("Rotation:"))
        llayout.addWidget(self._style_angle)
        llayout.addWidget(self.xrot)
        llayout.addWidget(self.yrot)
        llayout.addWidget(self.zrot)
        llayout.addWidget(QLabel("Scale:"))
        llayout.addWidget(self.xsca)
        llayout.addWidget(self.ysca)
        llayout.addWidget(self.zsca)
        llayout.addWidget(self.button1)
        llayout.addWidget(self.button2)

        self.button1.clicked.connect(self.__add_table_surface)
        self.button2.clicked.connect(self.__quit_table_surface)

        # --------------------------------------------------
        # # Panel CENTRAL IZQUIERDO

        # Nombres de columnas
        self.column_names_surface = ["Surface","Traslation", "Rotation", "Scale"]

        self.table_surface = QTableWidget()
        header = self.table_surface.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        self.table_surface.setColumnCount(4)
        self.table_surface.setHorizontalHeaderLabels(self.column_names_surface)

        # Formar body
        self.button3 = QPushButton("Formar Body")
        init_widget(self.button3, "formar_body_label")

        self.button3.clicked.connect(self.__formar_table_body)

        # Layout Derecha
        cllayout = QVBoxLayout()
        cllayout.setContentsMargins(1, 1, 1, 1)
        cllayout.addWidget(QLabel("Tabla de superficies:"))
        cllayout.addWidget(self.table_surface)
        cllayout.addWidget(self.button3)

        # --------------------------------------------------
        # # Panel CENTRAL DERECHO

        # (1) Creamos los widgets

        # Lista de opciones de superficies
        self._style_body = QComboBox()
        init_widget(self._style_body, "styleComboBox")
        self._style_body.addItems(style_names(list_name='body'))

        style_body_label = QLabel("Options:")
        init_widget(style_body_label, "body_label")
        style_body_label.setBuddy(self._style_body)

        # Nombre del body
        self.body_name = QPlainTextEdit()
        self.body_name.setPlainText("Body 0")

        # Lista de Materiales
        self._style_material = QComboBox()
        init_widget(self._style_material, "styleComboBox")
        self._style_material.addItems(style_names(list_name='material'))

        style_material_label = QLabel("Material:")
        init_widget(style_body_label, "material_label")
        style_material_label.setBuddy(self._style_material)

        # Table surface
        self.column_names_surf = ['Surface', 'Side Pointer']
        self.table_surf = QTableWidget()
        header = self.table_surf.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        self.table_surf.setColumnCount(2)
        self.table_surf.setHorizontalHeaderLabels(self.column_names_surf)

        self.table_surf.clicked.connect(self.onClicked)

        # Comentario
        self.body_comment = QPlainTextEdit()
        self.body_comment.setPlainText("Comment")

        # Agregar body
        self.button4 = QPushButton("Agregar")
        self.button5 = QPushButton("Quitar")
        init_widget(self.button4, "agregar_body_label")
        init_widget(self.button5, "quitar_body_label")

        # Agregamos widgets
        crlayout = QVBoxLayout()
        crlayout.setContentsMargins(1, 1, 1, 1)
        crlayout.addWidget(QLabel("Configuración:"))
        crlayout.addWidget(QLabel("Bodys:"))
        crlayout.addWidget(self._style_body)
        crlayout.addWidget(QLabel("Body Name:"))
        crlayout.addWidget(self.body_name)
        crlayout.addWidget(self.table_surf)
        crlayout.addWidget(QLabel("Material:"))
        crlayout.addWidget(self._style_material)
        crlayout.addWidget(QLabel("Comment:"))
        crlayout.addWidget(self.body_comment)
        crlayout.addWidget(self.button4)
        crlayout.addWidget(self.button5)

        self.button4.clicked.connect(self.__add_table_body)
        self.button5.clicked.connect(self.__quit_table_body)

        # --------------------------------------------------
        # # Panel DERECHO

        # Nombres de columnas
        self.column_names_body = ["Body"," Material", "Surfaces", "Comment"]

        self.table_body = QTableWidget()
        header = self.table_body.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        self.table_body.setColumnCount(4)
        self.table_body.setHorizontalHeaderLabels(self.column_names_body)

        # Agregar body
        self.button6 = QPushButton("View")
        init_widget(self.button6, "view_label")
        self.button7 = QPushButton("Armar Input")
        init_widget(self.button7, "armar_input_label")

        # Layout Derecha
        rlayout = QVBoxLayout()
        rlayout.setContentsMargins(1, 1, 1, 1)
        rlayout.addWidget(QLabel("Tabla de cuerpos:"))
        rlayout.addWidget(self.table_body)
        rlayout.addWidget(self.button6)
        rlayout.addWidget(self.button7)

        self.button6.clicked.connect(self.view)
        self.button7.clicked.connect(self.input)


        # --------------------------------------------------
        # # Panel completo

        layout = QHBoxLayout(self._main)
        layout.addLayout(llayout, 16)
        layout.addLayout(cllayout, 33)
        layout.addLayout(crlayout, 16)
        layout.addLayout(rlayout, 33)

    def __add_table_surface(self):

        """ Update the plot with the current input values """
        xpos = self.xpos.value()
        ypos = self.ypos.value()
        zpos = self.zpos.value()

        xrot = self.xrot.value()
        yrot = self.yrot.value()
        zrot = self.zrot.value()

        xsca = self.xsca.value()
        ysca = self.ysca.value()
        zsca = self.zsca.value()

        surface = str(self._style_surfaces.currentText())

        num = self.table_surface.rowCount()

        self.table_surface.setRowCount(num+1)
        self.table_surface.setColumnCount(4)
        self.table_surface.setHorizontalHeaderLabels(self.column_names_surface)

        self.table_surface.setItem(num, 0, QTableWidgetItem(f"{surface}"))
        self.table_surface.setItem(num, 1, QTableWidgetItem(f"({xpos:.2f},{ypos:.2f},{zpos:.2f})"))
        self.table_surface.setItem(num, 2, QTableWidgetItem(f"({xrot:.2f},{yrot:.2f},{zrot:.2f})"))
        self.table_surface.setItem(num, 3, QTableWidgetItem(f"({xsca:.2f},{ysca:.2f},{zsca:.2f})"))

    def __quit_table_surface(self):
        num = self.table_surface.rowCount()
        self.table_surface.removeRow(num+1)
        self.table_surface.setRowCount(num-1)
        self.table_surface.setHorizontalHeaderLabels(self.column_names_surface)

    def __formar_table_body(self):

        """ Update the plot with the current input values """

        # Agregamos las superficies a la subtabla

        num = self.table_surface.rowCount()
        for n in range(num):
            self.table_surf.setRowCount(n+1)
            self.table_surf.setColumnCount(2)
            self.table_surf.setHorizontalHeaderLabels(self.column_names_surf)
            self.table_surf.setItem(n, 0, QTableWidgetItem(f"S{n}"))
            self.table_surf.setItem(n, 1, QTableWidgetItem("1"))

        # Quitamos los datos de la tabla surface
        self.table_surface.setRowCount(0)

    def __add_table_body(self):

        """ Update the plot with the current input values """
        num = self.table_surf.rowCount()

        if num != 0:
            body = str(self._style_body.currentText())
            material = str(self._style_material.currentText())

            num = self.table_surf.rowCount()
            table_values = []
            for n in range(num):
                item = self.table_surf.itemAt(n,1)
                table_values.append(item.text())
            print(table_values)

            comment = self.body_comment.toPlainText()

            num = self.table_body.rowCount()
            self.table_body.setRowCount(num+1)
            self.table_body.setColumnCount(4)
            self.table_body.setHorizontalHeaderLabels(self.column_names_body)

            self.table_body.setItem(num, 0, QTableWidgetItem(f"{body}"))
            self.table_body.setItem(num, 1, QTableWidgetItem(f"{material}"))
            self.table_body.setItem(num, 2, QTableWidgetItem(f"{table_values}"))
            self.table_body.setItem(num, 3, QTableWidgetItem(f"{comment}"))

        elif num == 0:
            errorMSE = QErrorMessage()
            errorMSE.showMessage("No hay ninguna superficie creada.")

        # Quitamos los datos de la tabla surface
        self.table_surf.setRowCount(0)

    def __quit_table_body(self):
        num = self.table_body.rowCount()
        self.table_body.removeRow(num+1)
        self.table_body.setRowCount(num-1)
        self.table_body.setHorizontalHeaderLabels(self.column_names_body)

    def onClicked(self, index):
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

if __name__ == "__main__":
    # app = QGuiApplication(sys.argv)
    app = QApplication(sys.argv)

    # Ventana de ajustes
    mainWin = MainWindow()
    availableGeometry = mainWin.screen().availableGeometry()
    mainWin.resize(availableGeometry.width() / 2, availableGeometry.height() / 2)
    mainWin.show()

    sys.exit(app.exec())
