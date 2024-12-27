
import os
import sys
import re
import numpy as np
import shutil
import plotly.graph_objects as go
import subprocess
# from GeomView.main import MainWindow
#

from PySide6.QtCore import QUrl, QPoint, Qt
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6 import QtWidgets
import plotly.express as px
from PySide6 import QtWidgets, QtGui
from PySide6.QtCore import QUrl, QPoint, Qt
from PySide6.QtGui import QGuiApplication, QSurfaceFormat, QAction, QIcon
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtAxContainer import QAxSelect, QAxWidget
from PySide6.QtWidgets import *
from PySide6.QtQuick3D import QQuick3D
from PySide6.QtQuick import QQuickView, QQuickWindow, QSGRendererInterface
from PySide6.QtQuickWidgets import QQuickWidget
from PySide6.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtGui import QPixmap

import matplotlib.pyplot as plt

import matplotlib
import matplotlib.gridspec as gridspec
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT
from matplotlib.figure import Figure
import matplotlib.image as mpimg
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import matplotlib.ticker as mtick
from matplotlib import cm
from matplotlib.colors import Normalize
import matplotlib.pyplot as mpl
from matplotlib.widgets import Slider, Button, CheckButtons

from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection
import itertools
from itertools import groupby
from MonteCarlo.Utils.utils import option_list, print_list_columns

class LoadDataResults():

    def __init__(self, path,**kwargs):
        # Instance Variable
        self.pathfile = path
        self.TypeDataFile = ''
        # Cargamos la dirección del archivo
        basename_path = self.__basename(path)
        self.__loaddata(basename_path)

    def __basename(self, path):
        basename_path = os.path.basename(path)
        return basename_path

    def __loadfile(self):
        file = open(self.pathfile)
        string_list = file.readlines()
        file.close()
        return string_list

    def __loaddata(self, basename):
        # Cargamos los datos del archivo
        string_list = self.__loadfile()

        # SPC Files

        if basename.startswith('spc-enddet-'):
            self.GetData = self.__LoadData_SPC_EndDet(string_list)
            self.TypeDataFile = 'spc-enddet'
            self.Body = basename.split('-')[-1].split('.')[0]

        if basename.startswith('spc-impdet-'):
            self.GetData = self.__LoadData_SPC_ImpDet(string_list)
            self.TypeDataFile = 'spc-impdet'
            self.Body = basename.split('-')[-1].split('.')[0]

        if basename.startswith('psf-impdet'):
            self.GetData = self.__LoadData_PSF_ImpDet(string_list)
            self.TypeDataFile = 'psf-impdet'
            self.Body = basename.split('-')[-1].split('.')[0]

        if basename.startswith('fln-impdet-'):
            self.GetData = self.__LoadData_FLN_ImpDet(string_list)
            self.TypeDataFile = 'fln-impdet'
            self.Body = basename.split('-')[-1].split('.')[0]


    class __LoadData_SPC_EndDet():

        def __init__(self, string_list,**kwargs):
            # Instance Variable
            self.__data_process(string_list)

        def __data_process(self, string_list):

                # ----------------------------------------------------------------------
                # (1) Separamos el encabezado de los datos.
                encabezado = [f for f in string_list if f.startswith(' #')]
                data = [f[1:].lstrip(' ') for f in string_list if not f.startswith(' #')]

                # ----------------------------------------------------------------------
                # (2) Separamos el encabezado en: titulos y nombre de columnas.

                header = [f for f in encabezado if not (f.startswith(' #  1st') or f.startswith(' #  2nd') or f.startswith(' #  3rd') or f.startswith(' #  4th') or f.startswith(' #  5th') or f.startswith(' #  6th') or f.startswith(' #  7th') or f.startswith(' #  8th') or f.startswith(' #  PDFs') or f.startswith(' #  columns') or f.startswith(' #  PLANE') or f.startswith(' #/') or f.startswith(' #-') or f.startswith(' #\n'))]

                columns = [f for f in encabezado if f.startswith(' #  1st') or f.startswith(' #  2nd') or f.startswith(' #  3rd') or f.startswith(' #  4th') or f.startswith(' #  5th') or f.startswith(' #  6th') or f.startswith(' #  7th') or f.startswith(' #  8th') or f.startswith(' #  columns') or f.startswith(' #/')]

                # ------------------------------------------------------------------
                # (3) Separamos la información que brinda el encabezado.

                # --- Titulo
                row_1 = header[0].rstrip("\n").rstrip('.').lstrip(" #  ").split('.')
                if len(row_1) != 1:
                    self.GetMain = row_1[0].split(' ')[-1]
                    self.GetTitle = row_1[1].lstrip(' ')
                else:
                    self.GetTitle = header[1].rstrip("\n").rstrip('.').lstrip(" #  ")


                # ----------------------------------------------------------------------
                # (4) Separamos los titulos de las columnas, los datos y las unidades.

                # Obtenemos los titulos de las columnas.
                if len(columns) == 1:
                    titles_columns = re.split(r'\s+(?=[^"]*(?:"[^"]*"[^"]*)*$)',columns[0])
                    titles_columns = [f.lstrip('#/') for f in titles_columns if f!='']
                    units = [[' '][0] for f in titles_columns]
                else:

                    units = []
                    titles_columns = []

                    for title in columns:

                        # --- Limpiamos el string.
                        # Quitamos "\n", ".", "#".
                        title = title.rstrip("\n").rstrip(".")
                        title = title.lstrip('#  ')
                        title = title.lstrip(' ').rstrip(' ')

                        title_1, title_2 = title.split(':')

                        title_1 = title_1.rstrip("\n").rstrip(".")
                        title_1 = title_1.lstrip('#  ')
                        title_1 = title_1.lstrip(' ').rstrip(' ')

                        title_2 = title_2.rstrip("\n").rstrip(".")
                        title_2 = title_2.lstrip('#  ')
                        title_2 = title_2.lstrip(' ').rstrip(' ')

                        if title_1.find('to') != -1:
                            num_columns = [int(s) for s in title_1.split() if s.isdigit()]
                            list_numcol = np.arange(np.min(num_columns),np.max(num_columns),1)
                            if title_2.find('X,Y,Z') != -1:
                                titles_columns.append('X')
                                units.append('cm')
                                titles_columns.append('Y')
                                units.append('cm')
                                titles_columns.append('Z')
                                units.append('cm')
                            if title_2.find('IX,IY,IZ') != -1:
                                titles_columns.append('IX')
                                units.append(' ')
                                titles_columns.append('IY')
                                units.append(' ')
                                titles_columns.append('IZ')
                                units.append(' ')
                        else:

                            # --- Limpiamos el string.
                            # Quitamos los espacios, "\n" y "." finales
                            title_2 = title_2.rstrip("\n").rstrip(".")
                            title_2 = title_2.lstrip(' ').rstrip(' ')
                            # Quitamos las comas.
                            if title_2.find(',') != -1:
                                title_2 = title_2.replace(',','')

                            # --- Guardamos y quitamos las unidades.

                            # Si el string tiene unidades entre parentesis
                            if title_2.find('(') != -1:
                                # Guardamos la unidad en la lista unites
                                unit = title_2.split('(', 1)[1].split(')')[0]
                                # Quitamos la unidad del string
                                title_2 = title_2.split('(', 1)[0].rstrip(' ').lstrip(' ')
                            else:
                                other_unite = [f for f in encabezado if f.startswith(' #  PDFs')]
                                if other_unite != []:
                                    other_unite = [f for f in encabezado if f.startswith(' #  PDFs')][0]
                                    other_unite = other_unite.rstrip("\n").rstrip(".")
                                    other_unite = other_unite.lstrip(' ').rstrip(' ')
                                    unit = other_unite.split(' ')[-1]
                                else:
                                    other_unite = [f for f in encabezado if f.startswith(' #  Fluences')][0]
                                    other_unite = other_unite.rstrip("\n").rstrip(".")
                                    other_unite = other_unite.lstrip(' ').rstrip(' ')
                                    unit = other_unite.split(' ')[-1]


                            # --- Guardamos el tipo de particula.
                            # Si el string tiene el for
                            if title_2.find('for') != -1:
                                # Guardamos el tipo de particula
                                particles = title_2.split('for')[1]
                                particles = particles.rstrip(' ').lstrip(' ')
                                # Quitamos el tipo de particula del string
                                title_2 = title_2.split('for')[0]
                            else:
                                particles = ''

                            if title_2.find('and') != -1:
                                title_2 = title_2.lstrip(' ').rstrip(' ')
                                other_titles = title_2.split(' and ')
                                for string in other_titles:
                                    if len(string.split(' ')) !=1:
                                        strings = string
                                        particles = string.split(' ')[0]
                                    elif particles == '':
                                        strings = particles+' '+string
                                    else:
                                        strings = particles+' '+string
                                    titles_columns.append(strings.lstrip(' ').rstrip(' '))
                                    units.append(unit)
                            else:
                                titles_columns.append(title_2)
                                units.append(unit)

                # Reemplazamos espacios por guiones bajos.
                titles_columns = [f.replace(' ','_') for f in titles_columns]

                self.GetTitlesColumns = titles_columns
                self.GetUnits = units

                #-------------------------------------------------------------------
                # (5) Obtenemos los datos de cada columna
                data_dict = {k:[] for k in titles_columns}

                for i,x in enumerate(data):
                    x = x.rstrip("\n")
                    if len(x)>4:
                        x = re.split(r'\s+(?=[^"]*(?:"[^"]*"[^"]*)*$)',x)
                        for j, title in enumerate(titles_columns):
                            data_dict[title].append(float(x[j]))

                self.GetDataColumns = data_dict

    class __LoadData_SPC_ImpDet():

        def __init__(self, string_list,**kwargs):
            # Instance Variable
            self.__data_process(string_list)

        def __data_process(self, string_list):

                # ----------------------------------------------------------------------
                # (1) Separamos el encabezado de los datos.
                encabezado = [f for f in string_list if f.startswith(' #')]
                data = [f[1:].lstrip(' ') for f in string_list if not f.startswith(' #')]

                # ----------------------------------------------------------------------
                # (2) Separamos el encabezado en: titulos y nombre de columnas.

                header = [f for f in encabezado if not (f.startswith(' #  1st') or f.startswith(' #  2nd') or f.startswith(' #  3rd') or f.startswith(' #  4th') or f.startswith(' #  5th') or f.startswith(' #  6th') or f.startswith(' #  7th') or f.startswith(' #  8th') or f.startswith(' #  PDFs') or f.startswith(' #  columns') or f.startswith(' #  PLANE') or f.startswith(' #/') or f.startswith(' #-') or f.startswith(' #\n'))]

                columns = [f for f in encabezado if f.startswith(' #  1st') or f.startswith(' #  2nd') or f.startswith(' #  3rd') or f.startswith(' #  4th') or f.startswith(' #  5th') or f.startswith(' #  6th') or f.startswith(' #  7th') or f.startswith(' #  8th') or f.startswith(' #  columns') or f.startswith(' #/')]

                # ------------------------------------------------------------------
                # (3) Separamos la información que brinda el encabezado.

                # --- Titulo
                titles_list = header[0].rstrip("\n").rstrip('.').lstrip(" #  ").split('.')
                if len(titles_list) != 1:
                    self.GetTitle = titles_list[1].lstrip(' ')
                else:
                    self.GetTitle = header[1].rstrip("\n").rstrip('.').lstrip(" #  ")

                # ----------------------------------------------------------------------
                # (4) Separamos los titulos de las columnas, los datos y las unidades.

                # Obtenemos los titulos de las columnas.
                if len(columns) == 1:
                    titles_columns = re.split(r'\s+(?=[^"]*(?:"[^"]*"[^"]*)*$)',columns[0])
                    titles_columns = [f.lstrip('#/') for f in titles_columns if f!='']
                    units = [[' '][0] for f in titles_columns]
                else:

                    units = []
                    titles_columns = []

                    for title in columns:

                        # --- Limpiamos el string.
                        # Quitamos "\n", ".", "#".
                        title = title.rstrip("\n").rstrip(".")
                        title = title.lstrip('#  ')
                        title = title.lstrip(' ').rstrip(' ')

                        title_1, title_2 = title.split(':')

                        title_1 = title_1.rstrip("\n").rstrip(".")
                        title_1 = title_1.lstrip('#  ')
                        title_1 = title_1.lstrip(' ').rstrip(' ')

                        title_2 = title_2.rstrip("\n").rstrip(".")
                        title_2 = title_2.lstrip('#  ')
                        title_2 = title_2.lstrip(' ').rstrip(' ')

                        if title_1.find('to') != -1:
                            num_columns = [int(s) for s in title_1.split() if s.isdigit()]
                            list_numcol = np.arange(np.min(num_columns),np.max(num_columns),1)
                            if title_2.find('X,Y,Z') != -1:
                                titles_columns.append('X')
                                units.append('cm')
                                titles_columns.append('Y')
                                units.append('cm')
                                titles_columns.append('Z')
                                units.append('cm')
                            if title_2.find('IX,IY,IZ') != -1:
                                titles_columns.append('IX')
                                units.append(' ')
                                titles_columns.append('IY')
                                units.append(' ')
                                titles_columns.append('IZ')
                                units.append(' ')
                        else:

                            # --- Limpiamos el string.
                            # Quitamos los espacios, "\n" y "." finales
                            title_2 = title_2.rstrip("\n").rstrip(".")
                            title_2 = title_2.lstrip(' ').rstrip(' ')
                            # Quitamos las comas.
                            if title_2.find(',') != -1:
                                title_2 = title_2.replace(',','')

                            # --- Guardamos y quitamos las unidades.

                            # Si el string tiene unidades entre parentesis
                            if title_2.find('(') != -1:
                                # Guardamos la unidad en la lista unites
                                unit = title_2.split('(', 1)[1].split(')')[0]
                                # Quitamos la unidad del string
                                title_2 = title_2.split('(', 1)[0].rstrip(' ').lstrip(' ')
                            else:
                                other_unite = [f for f in encabezado if f.startswith(' #  PDFs')]
                                if other_unite != []:
                                    other_unite = [f for f in encabezado if f.startswith(' #  PDFs')][0]
                                    other_unite = other_unite.rstrip("\n").rstrip(".")
                                    other_unite = other_unite.lstrip(' ').rstrip(' ')
                                    unit = other_unite.split(' ')[-1]
                                else:
                                    other_unite = [f for f in encabezado if f.startswith(' #  Fluences')][0]
                                    other_unite = other_unite.rstrip("\n").rstrip(".")
                                    other_unite = other_unite.lstrip(' ').rstrip(' ')
                                    unit = other_unite.split(' ')[-1]


                            # --- Guardamos el tipo de particula.
                            # Si el string tiene el for
                            if title_2.find('for') != -1:
                                # Guardamos el tipo de particula
                                particles = title_2.split('for')[1]
                                particles = particles.rstrip(' ').lstrip(' ')
                                # Quitamos el tipo de particula del string
                                title_2 = title_2.split('for')[0]
                            else:
                                particles = ''

                            if title_2.find('and') != -1:
                                title_2 = title_2.lstrip(' ').rstrip(' ')
                                other_titles = title_2.split(' and ')
                                for string in other_titles:
                                    if len(string.split(' ')) !=1:
                                        strings = string
                                        particles = string.split(' ')[0]
                                    elif particles == '':
                                        strings = particles+' '+string
                                    else:
                                        strings = particles+' '+string
                                    titles_columns.append(strings.lstrip(' ').rstrip(' '))
                                    units.append(unit)
                            else:
                                titles_columns.append(title_2)
                                units.append(unit)

                # Reemplazamos espacios por guiones bajos.
                titles_columns = [f.replace(' ','_') for f in titles_columns]

                self.GetTitlesColumns = titles_columns
                self.GetUnits = units

                #-------------------------------------------------------------------
                # (5) Obtenemos los datos de cada columna
                data_dict = {k:[] for k in titles_columns}

                for i,x in enumerate(data):
                    x = x.rstrip("\n")
                    if len(x)>4:
                        x = re.split(r'\s+(?=[^"]*(?:"[^"]*"[^"]*)*$)',x)
                        for j, title in enumerate(titles_columns):
                            data_dict[title].append(float(x[j]))

                self.GetDataColumns = data_dict

    class __LoadData_PSF_ImpDet():

        def __init__(self, string_list,**kwargs):
            # Instance Variable
            self.__data_process(string_list)

        def __data_process(self, string_list):

                # ----------------------------------------------------------------------
                # (1) Separamos el encabezado de los datos.
                encabezado = [f for f in string_list if f.startswith(' #')]
                data = [f[1:].lstrip(' ') for f in string_list if not f.startswith(' #')]

                # ----------------------------------------------------------------------
                # (2) Separamos el encabezado en: titulos y nombre de columnas.

                header = [f for f in encabezado if not (f.startswith(' #  1st') or f.startswith(' #  2nd') or f.startswith(' #  3rd') or f.startswith(' #  4th') or f.startswith(' #  5th') or f.startswith(' #  6th') or f.startswith(' #  7th') or f.startswith(' #  8th') or f.startswith(' #  PDFs') or f.startswith(' #  columns') or f.startswith(' #  PLANE') or f.startswith(' #/') or f.startswith(' #-') or f.startswith(' #\n'))]

                columns = [f for f in encabezado if f.startswith(' #  1st') or f.startswith(' #  2nd') or f.startswith(' #  3rd') or f.startswith(' #  4th') or f.startswith(' #  5th') or f.startswith(' #  6th') or f.startswith(' #  7th') or f.startswith(' #  8th') or f.startswith(' #  columns') or f.startswith(' #/')]

                # ------------------------------------------------------------------
                # (3) Separamos la información que brinda el encabezado.

                # --- Titulo
                titles_list = header[0].rstrip("\n").rstrip('.').lstrip(" #  ").split('.')
                if len(titles_list) != 1:
                    self.GetPen = titles_list[0].split(' ')[-1]
                    self.GetTitle = titles_list[1].lstrip(' ')
                else:
                    self.GetTitle = header[1].rstrip("\n").rstrip('.').lstrip(" #  ")

                # ----------------------------------------------------------------------
                # (4) Separamos los titulos de las columnas, los datos y las unidades.

                # Obtenemos los titulos de las columnas.
                if len(columns) == 1:
                    titles_columns = re.split(r'\s+(?=[^"]*(?:"[^"]*"[^"]*)*$)',columns[0])
                    titles_columns = [f.lstrip('#/') for f in titles_columns if f!='']
                    units = [[' '][0] for f in titles_columns]
                else:

                    units = []
                    titles_columns = []

                    for title in columns:

                        # --- Limpiamos el string.
                        # Quitamos "\n", ".", "#".
                        title = title.rstrip("\n").rstrip(".")
                        title = title.lstrip('#  ')
                        title = title.lstrip(' ').rstrip(' ')

                        title_1, title_2 = title.split(':')

                        title_1 = title_1.rstrip("\n").rstrip(".")
                        title_1 = title_1.lstrip('#  ')
                        title_1 = title_1.lstrip(' ').rstrip(' ')

                        title_2 = title_2.rstrip("\n").rstrip(".")
                        title_2 = title_2.lstrip('#  ')
                        title_2 = title_2.lstrip(' ').rstrip(' ')

                        if title_1.find('to') != -1:
                            num_columns = [int(s) for s in title_1.split() if s.isdigit()]
                            list_numcol = np.arange(np.min(num_columns),np.max(num_columns),1)
                            if title_2.find('X,Y,Z') != -1:
                                titles_columns.append('X')
                                units.append('cm')
                                titles_columns.append('Y')
                                units.append('cm')
                                titles_columns.append('Z')
                                units.append('cm')
                            if title_2.find('IX,IY,IZ') != -1:
                                titles_columns.append('IX')
                                units.append(' ')
                                titles_columns.append('IY')
                                units.append(' ')
                                titles_columns.append('IZ')
                                units.append(' ')
                        else:

                            # --- Limpiamos el string.
                            # Quitamos los espacios, "\n" y "." finales
                            title_2 = title_2.rstrip("\n").rstrip(".")
                            title_2 = title_2.lstrip(' ').rstrip(' ')
                            # Quitamos las comas.
                            if title_2.find(',') != -1:
                                title_2 = title_2.replace(',','')

                            # --- Guardamos y quitamos las unidades.

                            # Si el string tiene unidades entre parentesis
                            if title_2.find('(') != -1:
                                # Guardamos la unidad en la lista unites
                                unit = title_2.split('(', 1)[1].split(')')[0]
                                # Quitamos la unidad del string
                                title_2 = title_2.split('(', 1)[0].rstrip(' ').lstrip(' ')
                            else:
                                other_unite = [f for f in encabezado if f.startswith(' #  PDFs')]
                                if other_unite != []:
                                    other_unite = [f for f in encabezado if f.startswith(' #  PDFs')][0]
                                    other_unite = other_unite.rstrip("\n").rstrip(".")
                                    other_unite = other_unite.lstrip(' ').rstrip(' ')
                                    unit = other_unite.split(' ')[-1]
                                else:
                                    other_unite = [f for f in encabezado if f.startswith(' #  Fluences')][0]
                                    other_unite = other_unite.rstrip("\n").rstrip(".")
                                    other_unite = other_unite.lstrip(' ').rstrip(' ')
                                    unit = other_unite.split(' ')[-1]


                            # --- Guardamos el tipo de particula.
                            # Si el string tiene el for
                            if title_2.find('for') != -1:
                                # Guardamos el tipo de particula
                                particles = title_2.split('for')[1]
                                particles = particles.rstrip(' ').lstrip(' ')
                                # Quitamos el tipo de particula del string
                                title_2 = title_2.split('for')[0]
                            else:
                                particles = ''

                            if title_2.find('and') != -1:
                                title_2 = title_2.lstrip(' ').rstrip(' ')
                                other_titles = title_2.split(' and ')
                                for string in other_titles:
                                    if len(string.split(' ')) !=1:
                                        strings = string
                                        particles = string.split(' ')[0]
                                    elif particles == '':
                                        strings = particles+' '+string
                                    else:
                                        strings = particles+' '+string
                                    titles_columns.append(strings.lstrip(' ').rstrip(' '))
                                    units.append(unit)
                            else:
                                titles_columns.append(title_2)
                                units.append(unit)

                # Reemplazamos espacios por guiones bajos.
                titles_columns = [f.replace(' ','_') for f in titles_columns]

                self.GetTitlesColumns = titles_columns
                self.GetUnits = units

                #-------------------------------------------------------------------
                # (5) Obtenemos los datos de cada columna
                data_dict = {k:[] for k in titles_columns}

                for i,x in enumerate(data):
                    x = x.rstrip("\n")
                    if len(x)>4:
                        x = re.split(r'\s+(?=[^"]*(?:"[^"]*"[^"]*)*$)',x)
                        for j, title in enumerate(titles_columns):
                            data_dict[title].append(float(x[j]))

                self.GetDataColumns = data_dict

    class __LoadData_FLN_ImpDet():

        def __init__(self, string_list,**kwargs):
            # Instance Variable
            self.__data_process(string_list)

        def __data_process(self, string_list):

                # ----------------------------------------------------------------------
                # (1) Separamos el encabezado de los datos.
                encabezado = [f for f in string_list if f.startswith(' #')]
                data = [f[1:].lstrip(' ') for f in string_list if not f.startswith(' #')]

                # ----------------------------------------------------------------------
                # (2) Separamos el encabezado en: titulos y nombre de columnas.

                header = [f for f in encabezado if not (f.startswith(' #  1st') or f.startswith(' #  2nd') or f.startswith(' #  3rd') or f.startswith(' #  4th') or f.startswith(' #  5th') or f.startswith(' #  6th') or f.startswith(' #  7th') or f.startswith(' #  8th') or f.startswith(' #  PDFs') or f.startswith(' #  columns') or f.startswith(' #  PLANE') or f.startswith(' #/') or f.startswith(' #-') or f.startswith(' #\n'))]

                columns = [f for f in encabezado if f.startswith(' #  1st') or f.startswith(' #  2nd') or f.startswith(' #  3rd') or f.startswith(' #  4th') or f.startswith(' #  5th') or f.startswith(' #  6th') or f.startswith(' #  7th') or f.startswith(' #  8th') or f.startswith(' #  columns') or f.startswith(' #/')]

                # ------------------------------------------------------------------
                # (3) Separamos la información que brinda el encabezado.

                # --- Titulo
                titles_list = header[0].rstrip("\n").rstrip('.').lstrip(" #  ").split('.')
                if len(titles_list) != 1:
                    self.GetTitle = titles_list[1].lstrip(' ')
                else:
                    self.GetTitle = header[1].rstrip("\n").rstrip('.').lstrip(" #  ")

                # ----------------------------------------------------------------------
                # (4) Separamos los titulos de las columnas, los datos y las unidades.

                # Obtenemos los titulos de las columnas.
                if len(columns) == 1:
                    titles_columns = re.split(r'\s+(?=[^"]*(?:"[^"]*"[^"]*)*$)',columns[0])
                    titles_columns = [f.lstrip('#/') for f in titles_columns if f!='']
                    units = [[' '][0] for f in titles_columns]
                else:

                    units = []
                    titles_columns = []

                    for title in columns:

                        # --- Limpiamos el string.
                        # Quitamos "\n", ".", "#".
                        title = title.rstrip("\n").rstrip(".")
                        title = title.lstrip('#  ')
                        title = title.lstrip(' ').rstrip(' ')

                        title_1, title_2 = title.split(':')

                        title_1 = title_1.rstrip("\n").rstrip(".")
                        title_1 = title_1.lstrip('#  ')
                        title_1 = title_1.lstrip(' ').rstrip(' ')

                        title_2 = title_2.rstrip("\n").rstrip(".")
                        title_2 = title_2.lstrip('#  ')
                        title_2 = title_2.lstrip(' ').rstrip(' ')

                        if title_1.find('to') != -1:
                            num_columns = [int(s) for s in title_1.split() if s.isdigit()]
                            list_numcol = np.arange(np.min(num_columns),np.max(num_columns),1)
                            if title_2.find('X,Y,Z') != -1:
                                titles_columns.append('X')
                                units.append('cm')
                                titles_columns.append('Y')
                                units.append('cm')
                                titles_columns.append('Z')
                                units.append('cm')
                            if title_2.find('IX,IY,IZ') != -1:
                                titles_columns.append('IX')
                                units.append(' ')
                                titles_columns.append('IY')
                                units.append(' ')
                                titles_columns.append('IZ')
                                units.append(' ')
                        else:

                            # --- Limpiamos el string.
                            # Quitamos los espacios, "\n" y "." finales
                            title_2 = title_2.rstrip("\n").rstrip(".")
                            title_2 = title_2.lstrip(' ').rstrip(' ')
                            # Quitamos las comas.
                            if title_2.find(',') != -1:
                                title_2 = title_2.replace(',','')

                            # --- Guardamos y quitamos las unidades.

                            # Si el string tiene unidades entre parentesis
                            if title_2.find('(') != -1:
                                # Guardamos la unidad en la lista unites
                                unit = title_2.split('(', 1)[1].split(')')[0]
                                # Quitamos la unidad del string
                                title_2 = title_2.split('(', 1)[0].rstrip(' ').lstrip(' ')
                            else:
                                other_unite = [f for f in encabezado if f.startswith(' #  PDFs')]
                                if other_unite != []:
                                    other_unite = [f for f in encabezado if f.startswith(' #  PDFs')][0]
                                    other_unite = other_unite.rstrip("\n").rstrip(".")
                                    other_unite = other_unite.lstrip(' ').rstrip(' ')
                                    unit = other_unite.split(' ')[-1]
                                else:
                                    other_unite = [f for f in encabezado if f.startswith(' #  Fluences')][0]
                                    other_unite = other_unite.rstrip("\n").rstrip(".")
                                    other_unite = other_unite.lstrip(' ').rstrip(' ')
                                    unit = other_unite.split(' ')[-1]


                            # --- Guardamos el tipo de particula.
                            # Si el string tiene el for
                            if title_2.find('for') != -1:
                                # Guardamos el tipo de particula
                                particles = title_2.split('for')[1]
                                particles = particles.rstrip(' ').lstrip(' ')
                                # Quitamos el tipo de particula del string
                                title_2 = title_2.split('for')[0]
                            else:
                                particles = ''

                            if title_2.find('and') != -1:
                                title_2 = title_2.lstrip(' ').rstrip(' ')
                                other_titles = title_2.split(' and ')
                                for string in other_titles:
                                    if len(string.split(' ')) !=1:
                                        strings = string
                                        particles = string.split(' ')[0]
                                    elif particles == '':
                                        strings = particles+' '+string
                                    else:
                                        strings = particles+' '+string
                                    titles_columns.append(strings.lstrip(' ').rstrip(' '))
                                    units.append(unit)
                            else:
                                titles_columns.append(title_2)
                                units.append(unit)

                # Reemplazamos espacios por guiones bajos.
                titles_columns = [f.replace(' ','_') for f in titles_columns]

                self.GetTitlesColumns = titles_columns
                self.GetUnits = units

                #-------------------------------------------------------------------
                # (5) Obtenemos los datos de cada columna
                data_dict = {k:[] for k in titles_columns}

                for i,x in enumerate(data):
                    x = x.rstrip("\n")
                    if len(x)>4:
                        x = re.split(r'\s+(?=[^"]*(?:"[^"]*"[^"]*)*$)',x)
                        for j, title in enumerate(titles_columns):
                            data_dict[title].append(float(x[j]))

                self.GetDataColumns = data_dict

class LoadDataFileInput():

    def __init__(self, pathfolder, input_used=None, list_input=False):
        # # Instance Variable

        if list_input:

            self.path = pathfolder
                # Extraemos el PEN que se utiliza
            self.pen = pathfolder.split('\\')[-3]
            self.__string_list = self.__loadfile()

            # ---------------------------------------------------
            # Cargamos el tipo de energia del INPUT
            self.__load_energy_type()

            # ---------------------------------------------------
            # Separamos en bloques los datos del INPUT
            self.__num_bloq = self.__data_process()

            # ---------------------------------------------------
            # Recolecta la informacion del INPUT dependiendo el PEN
            bloque = np.array(self.__num_bloq)

            if self.pen.find('pencyl') != -1:

                for bloq in bloque[:,1]:

                    if bloq.find('Source') != -1:
                        self.Source = self.__Source_Cyl(self.__string_list, self.__num_bloq)
                    if bloq.find('Input phase-space') != -1:
                        self.PhaseSpace = self.__Input_Phase_Space_Main(self.__string_list, self.__num_bloq)
                    if bloq.find('Material data') != -1:
                        self.Materials = self.__Material_Cyl(self.__string_list, self.__num_bloq)
                    if bloq.find('Interaction forcing') != -1:
                        self.InteractionForcing = self.__Interaction_Forcing_Cyl(self.__string_list, self.__num_bloq)
                    if bloq.find('Local maximum') != -1:
                        self.EmergingParticles = self.__Local_Maximum_Step_Length_Cyl(self.__string_list, self.__num_bloq)
                    if bloq.find('Counter array') != -1:
                        self.ImpactDetectors = self.__Counter_Array_Dimensions_Cyl(self.__string_list, self.__num_bloq)
                    if bloq.find('Energy-deposition') != -1 or bloq.find('Energy deposition') != -1:
                        self.EnergyDeposition = self.__Energy_Deposition_Cyl(self.__string_list, self.__num_bloq)
                    if bloq.find('Dose') != -1:
                        self.DoseDistribution = self.__Dose_Distribution_Cyl(self.__string_list, self.__num_bloq)
                    if bloq.find('Charge') != -1 or bloq.find('charge') != -1:
                        self.ChargeDistribution = self.__Charge_Distribution_Cyl(self.__string_list, self.__num_bloq)
                    if bloq.find('Job') != -1:
                        self.JobProperties = self.__Job_Properties_Cyl(self.__string_list, self.__num_bloq)


            elif self.pen.find('penmain') != -1:

                for bloq in bloque[:,1]:

                    if bloq.find('Source') != -1:
                        self.Source = self.__Source_Main(self.__string_list, self.__num_bloq)
                    if bloq.find('Input phase-space') != -1:
                        self.PhaseSpace = self.__Input_Phase_Space_Main(self.__string_list, self.__num_bloq)
                    if bloq.find('Material data') != -1:
                        self.Materials = self.__Material_Main(self.__string_list, self.__num_bloq)
                    if bloq.find('Geometry definition') != -1:
                        self.Geometry = self.__Geometry_Main(self.__string_list, self.__num_bloq)
                    if bloq.find('Interaction forcing') != -1:
                        self.InteractionForcing = self.__Interaction_Forcing_Main(self.__string_list, self.__num_bloq)
                    if bloq.find('Emerging particles') != -1:
                        self.EmergingParticles = self.__Emerging_Particles_Main(self.__string_list, self.__num_bloq)
                    if bloq.find('Impact detectors') != -1:
                        self.ImpactDetectors = self.__Impact_Detectors_Main(self.__string_list, self.__num_bloq)
                    if bloq.find('Energy deposition') != -1:
                        self.EnergyDeposition = self.__Energy_Deposition_Main(self.__string_list, self.__num_bloq)
                    if bloq.find('Dose distribution') != -1:
                        self.DoseDistribution = self.__Dose_Distribution_Main(self.__string_list, self.__num_bloq)
                    if bloq.find('Charge distribution') != -1:
                        self.ChargeDistribution = self.__Charge_Distribution_Main(self.__string_list, self.__num_bloq)
                    if bloq.find('Job') != -1:
                        self.JobProperties = self.__Job_Properties_Main(self.__string_list, self.__num_bloq)

            else:
                print('No se puede determinar el PEN que se esta utilizando')


        else:
            # ---------------------------------------------------
            # Buscamos y elegimos el path del INPUT a cargar

            path_input = self.__find_input(pathfolder, input_used=input_used)
            self.path = path_input

            # ---------------------------------------------------
            # Extraemos el PEN que se utiliza
            self.pen = pathfolder.split('\\')[-1]

            # ---------------------------------------------------
            # Cargamos los datos del INPUT en una lista
            self.__string_list = self.__loadfile()

            # ---------------------------------------------------
            # Cargamos el tipo de energia del INPUT
            self.__load_energy_type()

            # ---------------------------------------------------
            # Separamos en bloques los datos del INPUT
            self.__num_bloq = self.__data_process()

            # ---------------------------------------------------
            # Recolecta la informacion del INPUT dependiendo el PEN
            bloque = np.array(self.__num_bloq)

            if self.pen.find('pencyl') != -1:

                for bloq in bloque[:,1]:

                    if bloq.find('Source') != -1:
                        self.Source = self.__Source_Cyl(self.__string_list, self.__num_bloq)
                    if bloq.find('Material data') != -1:
                        self.Materials = self.__Material_Cyl(self.__string_list, self.__num_bloq)
                    if bloq.find('Interaction forcing') != -1:
                        self.InteractionForcing = self.__Interaction_Forcing_Cyl(self.__string_list, self.__num_bloq)
                    if bloq.find('Local maximum') != -1:
                        self.EmergingParticles = self.__Local_Maximum_Step_Length_Cyl(self.__string_list, self.__num_bloq)
                    if bloq.find('Counter array') != -1:
                        self.ImpactDetectors = self.__Counter_Array_Dimensions_Cyl(self.__string_list, self.__num_bloq)
                    if bloq.find('Energy-deposition') != -1 or bloq.find('Energy deposition') != -1:
                        self.EnergyDeposition = self.__Energy_Deposition_Cyl(self.__string_list, self.__num_bloq)
                    if bloq.find('Dose') != -1:
                        self.DoseDistribution = self.__Dose_Distribution_Cyl(self.__string_list, self.__num_bloq)
                    if bloq.find('Charge') != -1 or bloq.find('charge') != -1:
                        self.ChargeDistribution = self.__Charge_Distribution_Cyl(self.__string_list, self.__num_bloq)
                    if bloq.find('Job') != -1:
                        self.JobProperties = self.__Job_Properties_Cyl(self.__string_list, self.__num_bloq)


            elif self.pen.find('penmain') != -1:

                for bloq in bloque[:,1]:

                    if bloq.find('Source') != -1:
                        self.Source = self.__Source_Main(self.__string_list, self.__num_bloq)
                    if bloq.find('Material data') != -1:
                        self.Materials = self.__Material_Main(self.__string_list, self.__num_bloq)
                    if bloq.find('Geometry definition') != -1:
                        self.Geometry = self.__Geometry_Main(self.__string_list, self.__num_bloq)
                    if bloq.find('Interaction forcing') != -1:
                        self.InteractionForcing = self.__Interaction_Forcing_Main(self.__string_list, self.__num_bloq)
                    if bloq.find('Emerging particles') != -1:
                        self.EmergingParticles = self.__Emerging_Particles_Main(self.__string_list, self.__num_bloq)
                    if bloq.find('Impact detectors') != -1:
                        self.ImpactDetectors = self.__Impact_Detectors_Main(self.__string_list, self.__num_bloq)
                    if bloq.find('Energy deposition') != -1:
                        self.EnergyDeposition = self.__Energy_Deposition_Main(self.__string_list, self.__num_bloq)
                    if bloq.find('Dose distribution') != -1:
                        self.DoseDistribution = self.__Dose_Distribution_Main(self.__string_list, self.__num_bloq)
                    if bloq.find('Charge distribution') != -1:
                        self.ChargeDistribution = self.__Charge_Distribution_Main(self.__string_list, self.__num_bloq)
                    if bloq.find('Job') != -1:
                        self.JobProperties = self.__Job_Properties_Main(self.__string_list, self.__num_bloq)

            else:
                print('No se puede determinar el PEN que se esta utilizando')

    def __reload_file(self):

        # ---------------------------------------------------
        # Cargamos los datos del INPUT en una lista
        self.__string_list = self.__loadfile()

        # ---------------------------------------------------
        # Separamos en bloques los datos del INPUT
        self.__num_bloq = self.__data_process()

        # ---------------------------------------------------
        # Recolecta la informacion del INPUT dependiendo el PEN
        bloque = np.array(self.__num_bloq)

        if self.pen.find('pencyl') != -1:

            for bloq in bloque[:,1]:

                if bloq.find('Source') != -1:
                    self.Source = self.__Source_Cyl(self.__string_list, self.__num_bloq)
                if bloq.find('Input phase-space') != -1:
                    self.PhaseSpace = self.__Input_Phase_Space_Main(self.__string_list, self.__num_bloq)
                if bloq.find('Material data') != -1:
                    self.Materials = self.__Material_Cyl(self.__string_list, self.__num_bloq)
                if bloq.find('Interaction forcing') != -1:
                    self.InteractionForcing = self.__Interaction_Forcing_Cyl(self.__string_list, self.__num_bloq)
                if bloq.find('Local maximum') != -1:
                    self.EmergingParticles = self.__Local_Maximum_Step_Length_Cyl(self.__string_list, self.__num_bloq)
                if bloq.find('Counter array') != -1:
                    self.ImpactDetectors = self.__Counter_Array_Dimensions_Cyl(self.__string_list, self.__num_bloq)
                if bloq.find('Energy-deposition') != -1 or bloq.find('Energy deposition') != -1:
                    self.EnergyDeposition = self.__Energy_Deposition_Cyl(self.__string_list, self.__num_bloq)
                if bloq.find('Dose') != -1:
                    self.DoseDistribution = self.__Dose_Distribution_Cyl(self.__string_list, self.__num_bloq)
                if bloq.find('Charge') != -1 or bloq.find('charge') != -1:
                    self.ChargeDistribution = self.__Charge_Distribution_Cyl(self.__string_list, self.__num_bloq)
                if bloq.find('Job') != -1:
                    self.JobProperties = self.__Job_Properties_Cyl(self.__string_list, self.__num_bloq)


        elif self.pen.find('penmain') != -1:

            for bloq in bloque[:,1]:

                if bloq.find('Source') != -1:
                    self.Source = self.__Source_Main(self.__string_list, self.__num_bloq)
                if bloq.find('Material data') != -1:
                    self.Materials = self.__Material_Main(self.__string_list, self.__num_bloq)
                if bloq.find('Geometry definition') != -1:
                    self.Geometry = self.__Geometry_Main(self.__string_list, self.__num_bloq)
                if bloq.find('Interaction forcing') != -1:
                    self.InteractionForcing = self.__Interaction_Forcing_Main(self.__string_list, self.__num_bloq)
                if bloq.find('Emerging particles') != -1:
                    self.EmergingParticles = self.__Emerging_Particles_Main(self.__string_list, self.__num_bloq)
                if bloq.find('Impact detectors') != -1:
                    self.ImpactDetectors = self.__Impact_Detectors_Main(self.__string_list, self.__num_bloq)
                if bloq.find('Energy deposition') != -1:
                    self.EnergyDeposition = self.__Energy_Deposition_Main(self.__string_list, self.__num_bloq)
                if bloq.find('Dose distribution') != -1:
                    self.DoseDistribution = self.__Dose_Distribution_Main(self.__string_list, self.__num_bloq)
                if bloq.find('Charge distribution') != -1:
                    self.ChargeDistribution = self.__Charge_Distribution_Main(self.__string_list, self.__num_bloq)
                if bloq.find('Job') != -1:
                    self.JobProperties = self.__Job_Properties_Main(self.__string_list, self.__num_bloq)

        else:
            print('No se puede determinar el PEN que se esta utilizando')

    def __find_input(self, pathfolder, input_used=None):

        print('------')
        print('INPUTS')
        print('------\n')

        path_files = os.path.join(pathfolder, 'input')
        files_input = [os.path.join(path_files, f) for f in os.listdir(path_files)
            if os.path.isfile(os.path.join(path_files, f)) and f.endswith('.in')]

        list_files = [os.path.basename(f) for f in os.listdir(path_files) if os.path.isfile(os.path.join(path_files, f)) and f.endswith('.in')]

        if input_used == None:

            respuesta = option_list(answer_list=list_files, input_type='int', question='Archivos INPUTS encontrados', return_type=False)

            path_input = files_input[respuesta]

        else:
            files_input = [os.path.join(path_files, f) for f in os.listdir(path_files)
                if os.path.isfile(os.path.join(path_files, f)) and f.endswith('.in') and f.startswith(input_used)]

            path_input = files_input[0]

        return path_input

    def __basename(self, path):
        if len(path) != 1:
            basename_path = [os.path.basename(f) for f in path]
        else:
            basename_path = os.path.basename(path)

        return basename_path

    def __loadfile(self):
        file = open(self.path)
        string_list = file.readlines()
        file.close()
        return string_list

    def __load_energy_type(self):

        # Tomamos el texto completo y lo almacenamos en string_list
        string_list = self.__string_list

        # (1) Buscamos la fila que tenga la palabra SENERG or SPECTR
        row_string = [[i,string] for i,string in enumerate(string_list) if string.startswith('SENERG')]
        if len(row_string) != 0:
            self.energy_type = "SENERG"
        else:
            self.energy_type = "SPECTR"

    def __data_process(self):

        num_bloq = []
        # (1) Separamos el texto en bloques.
        for i, row_string in enumerate(self.__string_list):

            row_string = row_string.lstrip('       ').rstrip('.').rstrip('\n')

            if row_string.startswith("TITLE"):
                self.Title = row_string.split('  ')[1]

            if row_string.startswith(">>>"):
                num_bloq.append([i,' '.join(re.split(r'[\s,;,>]+',row_string)).lstrip(' ').rstrip('.')])

            if row_string.startswith('END '):
                num_bloq.append([i,row_string.split(' ')[0]])

        return num_bloq

    def __format_e(self,n):
        a = '%e' % n
        d = a.split('e')[0].rstrip('0').rstrip('.')
        return d[:4] + 'e' + a.split('e')[1][1:]

    def modify_energy(self,value_energy):

        # Convertimos en string el valor de energia ingresado.
        value_energy = float(value_energy)
        value_energy = self.__format_e(value_energy)

        # Para PRUEBAS DE CODIGO
        # path = 'D:\Proyectos_Investigacion\Imaging_XFCT_microCT\Code_Imaging_XFCT_microCT\Detector\RUN\penmain_2018\input\input.in'
        # file = open(path)
        # string_list = file.readlines()
        # file.close()

        # Tomamos el texto completo y lo almacenamos en string_list
        string_list = self.__string_list

        # (1) Buscamos la fila que tenga la palabra SENERG or SPECTR
        row_string = [[i,string] for i,string in enumerate(string_list) if string.startswith('SENERG')]
        row_string = row_string[0]
        len_string = len(row_string[1])

        # (2) Procesamos la fila: Separamos el dato a modificar del comentario
        # Dato
        data = row_string[1].split('[')[0]

        # Comentario
        if len( row_string[1].split('[')) > 1:
            has_comment = True
            comment = row_string[1].split('[')[1]
        else:
            has_comment = False

        # (2.1) Procesamos el dato
        # Quitamos los espacios y caracteres innecesarios.
        data = ' '.join(re.split(r'[\s,;,>,\],\[]+',data))
        data = data.split(' ')
        data = [f for f in data if f]

        new_row_string = data[0]
        size_ind = len(new_row_string)

        if size_ind < 8:
            add_ind = 7 - size_ind
            for f in range(add_ind):
                new_row_string = new_row_string + ' '

        # (3) Modificamos los datos
        values = data[1:]
        if len(values) > 1:

            for j, value in enumerate(value_energy):
                new_row_string = new_row_string + '{} '.format(value)

        else:

            new_row_string = new_row_string + '{} '.format(value_energy)

        # (4) Agregamos comnetario si lo tiene
        if has_comment:

            len_comment = len(comment)+1
            len_space = len_string - len(new_row_string) - len_comment
            for f in range(len_space):
                new_row_string = new_row_string + ' '

            new_row_string = new_row_string + '[' + comment

        else:

            len_space = len_string - len(new_row_string)
            for f in range(len_space):
                new_row_string = new_row_string + ' '

            new_row_string = new_row_string + '\n'

        # (5) Guardamos los datos modificados
        string_list[row_string[0]] = new_row_string
        my_file = open('{}'.format(self.path), "w")
        new_file_contents = "".join(string_list)
        my_file.write(new_file_contents)
        my_file.close()

        # (6) Cargamos el archivo nuevamente
        self.__reload_file()

    def modify_input(self):

        ''' Modificamos los valores de los parametros del INPUT
        '''

        os.system('cls')

        print('------------')
        print('MODIFY INPUT')
        print('------------\n')

        modify_parameters = option_list(input_type='string', question='¿Desea modificar el input?')

        if modify_parameters:

            string_list = self.__string_list
            num_bloq = np.array(self.__num_bloq)
            # self.num_bloq = self.__num_bloq
            # self.string_list = self.__string_list
            #
            # (2) Iniciamos con la modificaciones de los parametros
            temp = True
            while temp:

                respuesta = option_list(answer_list=num_bloq[:-1,1], input_type='int', question='¿Que bloque desea modificar?)',return_type=False)

                rows_strings = num_bloq[respuesta:respuesta+2,0]
                rows_names =  num_bloq[respuesta,1]

                range_rows = np.arange(int(rows_strings[0]),int(rows_strings[1]))
                range_rows = range_rows[1:-1]

                for i in range_rows:

                    row_string = self.__string_list[i]
                    len_string = len(row_string)

                    # Separamos el dato a modificar del comentario
                    data = row_string.split('[')[0]


                    if len( row_string.split('[')) > 1:
                        has_comment = True
                        comment = row_string.split('[')[1]
                    else:
                        has_comment = False

                    # (1) Procesamos el dato
                    # Quitamos los espacios y caracteres innecesarios.
                    data = ' '.join(re.split(r'[\s,;,>,\],\[]+',data))
                    data = data.split(' ')
                    data = [f for f in data if f]

                    new_row_string = data[0]
                    size_ind = len(new_row_string)

                    if size_ind < 8:
                        add_ind = 7 - size_ind
                        for f in range(add_ind):
                            new_row_string = new_row_string + ' '

                    # (2) Modificamos los datos
                    if has_comment:
                        print('\n')
                        print('- Paramentros a modificar: ', comment[:-2],'\n')
                    else:
                        print('\n')
                        print('- Paramentros a modificar: No se encontro referencia \n')

                    values = data[1:]
                    if len(values) > 1:

                        for j, value in enumerate(values):
                            print('Parametro {}:'.format(j+1))

                            valor = input('\t\t'+new_row_string+'({}) : '.format(value))
                            new_row_string = new_row_string + '{} '.format(valor)

                    else:

                        valor = input('\t\t'+new_row_string+'({}): '.format(values[0]))
                        new_row_string = new_row_string + '{} '.format(valor)

                    if has_comment:

                        len_comment = len(comment)+1
                        len_space = len_string - len(new_row_string) - len_comment
                        for f in range(len_space):
                            new_row_string = new_row_string + ' '

                        new_row_string = new_row_string + '[' + comment

                    else:

                        len_space = len_string - len(new_row_string)
                        for f in range(len_space):
                            new_row_string = new_row_string + ' '

                        new_row_string = new_row_string + '\n'

                    # (3) Guardamos los datos modificados
                    string_list[i] = new_row_string
                    my_file = open('{}'.format(self.path), "w")
                    new_file_contents = "".join(string_list)
                    my_file.write(new_file_contents)
                    my_file.close()

                print('\n')
                respuesta = option_list(input_type='string', question='¿Desea modificar otro bloque? (y/n)')

                if respuesta:
                    temp = True
                else:
                    temp = False

                    self.__reload_file()

    def GetDataBeam(self):

        if self.pen.find('pencyl') != -1:
            self.Source = self.__Source_Cyl(self.__string_list, self.__num_bloq)
        elif self.pen.find('penmain') != -1:
            self.Source = self.__Source_Main(self.__string_list, self.__num_bloq)
        else:
            print('NO SE ENCONTRÓ EL BLOQUE "SOURCE" EN EL INPUT...')
        return self.Source.SPOSIT, self.Source.SCONE

    def modify_materials(self, material):

        # Para PRUEBAS DE CODIGO
        # path = 'D:\Proyectos_Investigacion\Proyectos_de_Doctorado\Proyectos\Efficient_Detector_Si\Code\RUN\penmain_2018\input\input.in'
        # file = open(path)
        # string_list = file.readlines()
        # file.close()

        # Tomamos el texto completo y lo almacenamos en string_list
        string_list = self.__string_list

        # (1) Buscamos la fila que tenga la palabra SENERG or SPECTR
        row_string = [[i,string] for i,string in enumerate(string_list) if string.startswith('MFNAME')]

        # (2) Procesamos la fila: Separamos el dato a modificar del comentario

        for row in row_string:
            # Dato
            srow = row[1]
            data = srow.split('[')[0]
            len_string = len(srow)
            # Comentario
            if len(srow.split('[')) > 1:
                has_comment = True
                comment = srow.split('[')[1]
            else:
                has_comment = False

            # (2.1) Procesamos el dato
            # Quitamos los espacios y caracteres innecesarios.
            data = ' '.join(re.split(r'[\s,;,>,\],\[]+',data))
            data = data.split(' ')
            data = [f for f in data if f]

            # Verificamos que sea el material que se quiere modificar
            mat = data[1].split('\\')[-1]
            com_mat = '\\'.join(data[1].split('\\')[:-1]) +'\\'
            if mat != material and mat != 'Si.mat':
                irow = row[0]
                new_row_string = data[0]
                size_ind = len(new_row_string)

                if size_ind < 8:
                    add_ind = 7 - size_ind
                    for f in range(add_ind):
                        new_row_string = new_row_string + ' '

                # (3) Modificamos los datos
                values = data[1:]
                if len(values) > 1:

                    for j, value in enumerate(material):
                        new_row_string = new_row_string + '{}'.format(com_mat) + '{}.mat '.format(value)

                else:

                    new_row_string = new_row_string + '{}'.format(com_mat) + '{}.mat '.format(material)

                # (4) Agregamos comnetario si lo tiene
                if has_comment:

                    len_comment = len(comment)+1
                    len_space = len_string - len(new_row_string) - len_comment
                    for f in range(len_space):
                        new_row_string = new_row_string + ' '

                    new_row_string = new_row_string + '[' + comment

                else:

                    len_space = len_string - len(new_row_string)
                    for f in range(len_space):
                        new_row_string = new_row_string + ' '

                    new_row_string = new_row_string + '\n'

        # (5) Guardamos los datos modificados
        string_list[irow] = new_row_string
        my_file = open('{}'.format(self.path), "w")
        new_file_contents = "".join(string_list)
        my_file.write(new_file_contents)
        my_file.close()

        # (6) Cargamos el archivo nuevamente
        self.__reload_file()

    def modify_detectors(self, ndetectors, emin, emax, nbins):

        # Para PRUEBAS DE CODIGO
        # path = 'D:\Proyectos_Investigacion\Proyectos_de_Doctorado\Proyectos\Efficient_Detector_Si\Code\RUN\penmain_2018\input\input.in'
        # path = 'D:\Proyectos_Investigacion\Proyectos_de_Doctorado\Proyectos\SimulationXF_Detectors\Code\RUN\penmain_2018\input\input_spectr.in'
        # file = open(path)
        # string_list = file.readlines()
        # file.close()

        # Tomamos el texto completo y lo almacenamos en string_list
        string_list = self.__string_list

        # (1) Separamos en bloques

        blocks_limits = []
        for i,line in enumerate(string_list):
            # Si la linea empieza con 0 o C\n.
            if line.startswith('       >>>>>>>>'):
                print(i)
                for j,line1 in enumerate(string_list[i+1:]):
                    if line1.startswith('       >>>>>>>>'):
                        blocks_limits.append([i,i+j+1])
                        break
                    if line1.startswith('END '):
                        blocks_limits.append([i,i+j+1])
                        break
            if line.startswith('END '):
                blocks_limits.append([i,i])

        # Modificamos los bloques de IMPACT y ENERGY DEPOSITION
        for i,block in enumerate(blocks_limits):

            if string_list[block[0]].startswith('       >>>>>>>> Impact detectors'):
                new_string_list = string_list[:block[0]+1]
                for j in range(1,ndetectors+1):
                    new_string_list.append('IMPDET {} {} {} {} {}         [E-window, no. of bins, IPSF, IDCUT]\n'.format(emin,emax,nbins,'1','2'))
                    new_string_list.append('IDBODY {}\n'.format(j))
                new_string_list.append('       .\n')

            if string_list[block[0]].startswith('       >>>>>>>> Energy deposition detectors'):
                new_string_list.append('       >>>>>>>> Energy deposition detectors (up to 25)\n')
                for j in range(1,ndetectors+1):
                    new_string_list.append('ENDETC {} {} {}                  [E-window, no. of bins, IPSF, IDCUT]\n'.format(emin,emax,nbins))
                    new_string_list.append('EDBODY {}\n'.format(j))
                new_string_list.append('       .\n')

            if string_list[block[0]].startswith('       >>>>>>>> Job properties\n'):
                for line in string_list[block[0]:block[1]]:
                    new_string_list.append(line)

            if string_list[ block[0]].startswith('END'):
                new_string_list.append(string_list[block[0]])

        return new_string_list

    # PENMAIN

    class __Source_Main():

        def __init__(self, string_list, num_bloq):
            # Instance Variable
                # Procesamos los datos.
            self.__data_process(string_list, num_bloq)

        def __data_process(self, string_list, num_bloq):

            for i in range(len(num_bloq)-1):

                if num_bloq[i][1].find('Source') != -1:

                    list_param = ['SKPAR', 'SENERG', 'SPECTR', 'SGPOL', 'SPOSIT',
                                  'SBOX', 'SBODY', 'SCONE', 'SPYRAM']

                    spectr_sub = ['Ei','Pi']
                    sgpol_sub = ['SP1','SP2','SP3']
                    sposit_sub = ['SX0', 'SY0','SZ0']
                    sbox_sub = ['SSX','SSY','SSZ']
                    scone_sub = ['THETA', 'PHI', 'ALPHA']
                    spyram_sub = ['THETAL','THETAU','PHIL','PHIU']

                    for i, row_string in enumerate(string_list):
                        for j, param in enumerate(list_param):

                            if row_string.startswith(param):

                                # Quitamos el comentario entre corchetes, si tiene.
                                init = row_string.find('[')
                                string = row_string[:init]

                                # Quitamos los espacios y caracteres innecesarios.
                                string = ' '.join(re.split(r'[\s,;,>,\],\[]+',string)).lstrip(' ')

                                # Separamos los datos en una lista y quitamos los espacios vacios
                                string = [f for f in string.split(' ') if f]

                                # Separamos los datos
                                if string[0].startswith("SKPAR"):
                                    self.SKPAR = [f for f in string[1:]]

                                if string[0].startswith("SENERG"):
                                    self.SENERG = [f for f in string[1:]]

                                if string[0].startswith("SPECTR"):
                                    self.SPECTR = {n:f for (f,n) in zip(string[1:],spectr_sub)}

                                if string[0].startswith("SGPOL"):
                                    self.SGPOL = {n:f for (f,n) in zip(string[1:],sgpol_sub)}

                                if string[0].startswith("SPOSIT"):
                                    self.SPOSIT = {n:f for (f,n) in zip(string[1:],sposit_sub)}

                                if string[0].startswith("SBOX"):
                                    self.SBOX = {n:f for (f,n) in zip(string[1:],sbox_sub)}

                                if string[0].startswith("SBODY"):
                                    self.SBODY = [f for f in string[1:]]

                                if string[0].startswith("SCONE"):
                                    self.SCONE = {n:f for (f,n) in zip(string[1:],scone_sub)}

                                if string[0].startswith("SPYRAM"):
                                    self.SPYRAM = {n:f for (f,n) in zip(string[1:],spyram_sub)}

    class __Input_Phase_Space_Main():

        def __init__(self, string_list, num_bloq):
            # Instance Variable
                # Procesamos los datos.
            self.__data_process(string_list, num_bloq)

        def __data_process(self, string_list, num_bloq):

            for i in range(len(num_bloq)-1):

                if num_bloq[i][1].find('phase-space') != -1:

                    list_param = ['IPSFN', 'IPSPLI', 'WGTWIN', 'EPMAX']

                    wgtwin_sub = ['WGMIN','WGMAX']

                    for i, row_string in enumerate(string_list):
                        for j, param in enumerate(list_param):

                            if row_string.startswith(param):

                                # Quitamos el comentario entre corchetes, si tiene.
                                init = row_string.find('[')
                                string = row_string[:init]

                                # Quitamos los espacios y caracteres innecesarios.
                                string = ' '.join(re.split(r'[\s,;,>,\],\[]+',string)).lstrip(' ')

                                # Separamos los datos en una lista y quitamos los espacios vacios
                                string = [f for f in string.split(' ') if f]

                                # Separamos los datos
                                if string[0].startswith("IPSFN"):
                                    self.IPSFN = [f for f in string[1:]]

                                if string[0].startswith("IPSPLI"):
                                    self.IPSPLI = [f for f in string[1:]]

                                if string[0].startswith("WFTWIN"):
                                    self.WFTWIN = {n:f for (f,n) in zip(string[1:],spectr_sub)}

                                if string[0].startswith("EPMAX"):
                                    self.SBODY = [f for f in string[1:]]

    class __Material_Main():

        def __init__(self, string_list, num_bloq):
            # Instance Variable
                # Procesamos los datos.
            self.__data_process(string_list, num_bloq)

        def __data_process(self, string_list, num_bloq):

            for i in range(len(num_bloq)-1):

                if num_bloq[i][1].find('Material data') != -1:

                    list_param = ['MFNAME', 'MSIMPA']

                    # Separamos los datos
                    parametros = []
                    materiales = []
                    for i, row_string in enumerate(string_list):
                        for j, param in enumerate(list_param):

                            if row_string.startswith(param):

                                # Quitamos el comentario entre corchetes, si tiene.
                                init = row_string.find('[')
                                string = row_string[:init]

                                # Quitamos los espacios y caracteres innecesarios.
                                string = ' '.join(re.split(r'[\s,;,>,\],\[]+',string)).lstrip(' ')

                                # Separamos los datos en una lista y quitamos los espacios vacios
                                string = [f for f in string.split(' ') if f]

                                # Separamos los datos
                                if string[0].startswith("MSIMPA"):
                                    parametros.append([f for f in string[1:]])

                                if string[0].startswith("MFNAME"):
                                    materiales.append(string[1:][0].split('\\')[-1].rstrip('.mat'))

                    parameters = ['EAB1', 'EAB2', 'EAB3', 'C1', 'C2', 'WCC', 'WCR']
                    self.materials = {k:{p:float(v) for p,v in zip(parameters,parametros[i])} for i,k in enumerate(materiales)}

    class __Geometry_Main():

        def __init__(self, string_list, num_bloq):
            # Instance Variable
                # Procesamos los datos.
            self.__data_process(string_list, num_bloq)

        def __data_process(self, string_list, num_bloq):

            for i in range(len(num_bloq)-1):

                if num_bloq[i][1].find('Geometry') != -1:
                    list_param = ['GEOMFN', 'DSMAX', 'EABSB']

                    dsmax_sub = ['KB', 'DSMAX']
                    eabsb_sub = ['KB', 'EABSB']

                    for i, row_string in enumerate(string_list):
                        for j, param in enumerate(list_param):

                            if row_string.startswith(param):

                                # Quitamos el comentario entre corchetes, si tiene.
                                init = row_string.find('[')
                                string = row_string[:init]

                                # Quitamos los espacios y caracteres innecesarios.
                                string = ' '.join(re.split(r'[\s,;,>,\],\[]+',string)).lstrip(' ')

                                # Separamos los datos en una lista y quitamos los espacios vacios
                                string = [f for f in string.split(' ') if f]

                                # Separamos los datos
                                if string[0].startswith("DSMAX"):
                                    self.DSMAX = {n:f for (f,n) in zip(string[1:],dsmax_sub)}

                                if string[0].startswith("EABSB"):
                                    self.EABSB = {n:f for (f,n) in zip(string[1:],eabsb_sub)}

                                if string[0].startswith("GEOMFN"):
                                    self.geometry = string[1:][0].split('\\')[-1].rstrip('.geo')

    class __Interaction_Forcing_Main():

        def __init__(self, string_list, num_bloq):
            # Instance Variable
                # Procesamos los datos.
            self.__data_process(string_list, num_bloq)

        def __data_process(self, string_list, num_bloq):

            for i in range(len(num_bloq)-1):

                if num_bloq[i][1].find('Interaction forcing') != -1:

                    list_param = ['IFORCE']

                    iforce_sub = ['KB','KPAR','ICOL','FORCER','WLOW','WHIG']

                    for i, row_string in enumerate(string_list):
                        for j, param in enumerate(list_param):

                            if row_string.startswith(param):

                                # Quitamos el comentario entre corchetes, si tiene.
                                init = row_string.find('[')
                                string = row_string[:init]

                                # Quitamos los espacios y caracteres innecesarios.
                                string = ' '.join(re.split(r'[\s,;,>,\],\[]+',string)).lstrip(' ')

                                # Separamos los datos en una lista y quitamos los espacios vacios
                                string = [f for f in string.split(' ') if f]

                                # Separamos los datos
                                if string[0].startswith("IFORCE"):
                                    self.IFORCE = {n:f for (f,n) in zip(string[1:],iforce_sub)}

    class __Emerging_Particles_Main():

        def __init__(self, string_list, num_bloq):
            # Instance Variable
                # Procesamos los datos.
            self.__data_process(string_list, num_bloq)

        def __data_process(self, string_list, num_bloq):

            for i in range(len(num_bloq)-1):

                if num_bloq[i][1].find('Emerging particles') != -1:

                    list_param = ['NBE', 'NBANGL']

                    nbe_sub = ['EL','EU','NBE']
                    nbangl_sub = ['NBTH', 'NBPH']

                    for i, row_string in enumerate(string_list):
                        for j, param in enumerate(list_param):

                            if row_string.startswith(param):

                                # Quitamos el comentario entre corchetes, si tiene.
                                init = row_string.find('[')
                                string = row_string[:init]

                                # Quitamos los espacios y caracteres innecesarios.
                                string = ' '.join(re.split(r'[\s,;,>,\],\[]+',string)).lstrip(' ')

                                # Separamos los datos en una lista y quitamos los espacios vacios
                                string = [f for f in string.split(' ') if f]

                                # Separamos los datos
                                if string[0].startswith("NBE"):
                                    self.NBE = {n:f for (f,n) in zip(string[1:],nbe_sub)}

                                if string[0].startswith("NBANGL"):
                                    self.NBANGL = {n:f for (f,n) in zip(string[1:],nbangl_sub)}

    class __Impact_Detectors_Main():

        def __init__(self, string_list, num_bloq):
            # Instance Variable
                # Procesamos los datos.
            self.__data_process(string_list, num_bloq)

        def __data_process(self, string_list, num_bloq):

            for i in range(len(num_bloq)-1):

                if num_bloq[i][1].find('Impact detectors') != -1:

                    list_param = ['IMPDET', 'IDBODY', 'IDKPAR']

                    impdet_sub = ['EL','EU','NBE','IPSF','IDCUT']

                    for i, row_string in enumerate(string_list):
                        for j, param in enumerate(list_param):

                            if row_string.startswith(param):

                                # Quitamos el comentario entre corchetes, si tiene.
                                init = row_string.find('[')
                                string = row_string[:init]

                                # Quitamos los espacios y caracteres innecesarios.
                                string = ' '.join(re.split(r'[\s,;,>,\],\[]+',string)).lstrip(' ')

                                # Separamos los datos en una lista y quitamos los espacios vacios
                                string = [f for f in string.split(' ') if f]

                                # Separamos los datos
                                if string[0].startswith("IMPDET"):
                                    self.IMPDET = {n:f for (f,n) in zip(string[1:],impdet_sub)}

                                if string[0].startswith("IDBODY"):
                                    self.IDBODY = [f for f in string[1:]]

                                if string[0].startswith("IDKPAR"):
                                    self.IDKPAR = [f for f in string[1:]]

    class __Energy_Deposition_Main():

        def __init__(self, string_list, num_bloq):
            # Instance Variable
                # Procesamos los datos.
            self.__data_process(string_list, num_bloq)

        def __data_process(self, string_list, num_bloq):

            for i in range(len(num_bloq)-1):

                if num_bloq[i][1].find('Energy deposition') != -1 or num_bloq[i][1].find('Energy-deposition') != -1:

                    list_param = ['ENDETC', 'EDSPC', 'EDBODY']

                    endetc_sub = ['EL','EU','NBE']

                    for i, row_string in enumerate(string_list):
                        for j, param in enumerate(list_param):

                            if row_string.startswith(param):

                                # Quitamos el comentario entre corchetes, si tiene.
                                init = row_string.find('[')
                                string = row_string[:init]

                                # Quitamos los espacios y caracteres innecesarios.
                                string = ' '.join(re.split(r'[\s,;,>,\],\[]+',string)).lstrip(' ')

                                # Separamos los datos en una lista y quitamos los espacios vacios
                                string = [f for f in string.split(' ') if f]

                                # Separamos los datos
                                if string[0].startswith("ENDETC"):
                                    self.ENDETC = {n:f for (f,n) in zip(string[1:],endetc_sub)}

                                if string[0].startswith("EDSPC"):
                                    self.EDSPC = [f for f in string[1:]]

                                if string[0].startswith("EDBODY"):
                                    self.EDBODY = [f for f in string[1:]]

    class __Dose_Distribution_Main():

        def __init__(self, string_list, num_bloq):
            # Instance Variable
                # Procesamos los datos.
            self.__data_process(string_list, num_bloq)

        def __data_process(self, string_list, num_bloq):

            for i in range(len(num_bloq)-1):

                if num_bloq[i][1].find('Dose distribution') != -1:

                    list_param = ['GRIDX', 'GRIDY', 'GRIDZ', 'GRIDBN']

                    gridx_sub = ['XL','XU']
                    gridy_sub = ['YL','YU']
                    gridz_sub = ['ZL','ZU']
                    gridbn_sub = ['NDBX','NDBY','NDBZ']

                    for i, row_string in enumerate(string_list):
                        for j, param in enumerate(list_param):

                            if row_string.startswith(param):

                                # Quitamos el comentario entre corchetes, si tiene.
                                init = row_string.find('[')
                                string = row_string[:init]

                                # Quitamos los espacios y caracteres innecesarios.
                                string = ' '.join(re.split(r'[\s,;,>,\],\[]+',string)).lstrip(' ')

                                # Separamos los datos en una lista y quitamos los espacios vacios
                                string = [f for f in string.split(' ') if f]

                                # Separamos los datos
                                if string[0].startswith("GRIDX"):
                                    self.GRIDX = {n:f for (f,n) in zip(string[1:],gridx_sub)}

                                if string[0].startswith("GRIDY"):
                                    self.GRIDY = {n:f for (f,n) in zip(string[1:],gridy_sub)}

                                if string[0].startswith("GRIDZ"):
                                    self.GRIDZ = {n:f for (f,n) in zip(string[1:],gridz_sub)}

                                if string[0].startswith("GRIDBN"):
                                    self.GRIDBN = {n:f for (f,n) in zip(string[1:],gridbn_sub)}

    class __Charge_Distribution_Main():

        def __init__(self, string_list, num_bloq):
            # Instance Variable
                # Procesamos los datos.
            self.__data_process(string_list, num_bloq)

        def __data_process(self, string_list, num_bloq):

            for i in range(len(num_bloq)-1):

                if num_bloq[i][1].find('Charge distribution') != -1:
                    list_param = ['GRIDCX', 'GRIDCY', 'GRIDCZ', 'GRIDCBN']

                    gridcx_sub = ['XL','XU']
                    gridcy_sub = ['YL','YU']
                    gridcz_sub = ['ZL','ZU']
                    gridcbn_sub = ['NDBX','NDBY','NDBZ']

                    for i, row_string in enumerate(string_list):
                        for j, param in enumerate(list_param):

                            if row_string.startswith(param):

                                # Quitamos el comentario entre corchetes, si tiene.
                                init = row_string.find('[')
                                string = row_string[:init]

                                # Quitamos los espacios y caracteres innecesarios.
                                string = ' '.join(re.split(r'[\s,;,>,\],\[]+',string)).lstrip(' ')

                                # Separamos los datos en una lista y quitamos los espacios vacios
                                string = [f for f in string.split(' ') if f]

                                # Separamos los datos
                                if string[0].startswith("GRIDCX"):
                                    self.GRIDCX = {n:f for (f,n) in zip(string[1:],gridx_sub)}

                                if string[0].startswith("GRIDCY"):
                                    self.GRIDCY = {n:f for (f,n) in zip(string[1:],gridy_sub)}

                                if string[0].startswith("GRIDCZ"):
                                    self.GRIDCZ = {n:f for (f,n) in zip(string[1:],gridz_sub)}

                                if string[0].startswith("GRIDCBN"):
                                    self.GRIDCBN = {n:f for (f,n) in zip(string[1:],gridbn_sub)}

    class __Job_Properties_Main():

        def __init__(self, string_list, num_bloq):
            # Instance Variable
                # Procesamos los datos.
            self.__data_process(string_list, num_bloq)

        def __data_process(self, string_list, num_bloq):

            for i in range(len(num_bloq)-1):

                if num_bloq[i][1].find('Job properties') != -1:
                    rows_strings = string_list[num_bloq[i][0]:num_bloq[i+1][0]]

                    # Separamos los datos
                    for i, row_string in enumerate(rows_strings):

                        # Quitamos el string entre corchetes, si tiene.
                        init = row_string.find('[')
                        row_string = row_string[:init]

                        # Quitamos los espacios y caracteres innecesarios.
                        row_string = ' '.join(re.split(r'[\s,;,>,\],\[]+',row_string)).lstrip(' ')

                        # Separamos los datos en una lista y quitamos los espacios vacios
                        row_string = [f for f in row_string.split(' ') if f]

                        if row_string[0].startswith("RESUME"):
                            self.RESUME = row_string[1:][0]
                        if row_string[0].startswith("DUMPTO"):
                            self.DUMPTO = row_string[1:][0]
                        if row_string[0].startswith("RSEED"):
                            self.DUMPP = [f for f in row_string[1:]]
                        if row_string[0].startswith("DUMPP"):
                            self.DUMPP = int(row_string[1:][0])
                        if row_string[0].startswith("NSIMSH"):
                            self.NSIMSH = float(row_string[1:][0])
                        if row_string[0].startswith("TIME"):
                            self.TIME = float(row_string[1:][0])

    # PENCYL

    class __Source_Cyl():

        def __init__(self, string_list, num_bloq):
            # Instance Variable
                # Procesamos los datos.
            self.__data_process(string_list, num_bloq)

        def __data_process(self, string_list, num_bloq):

            for i in range(len(num_bloq)-1):

                if num_bloq[i][1].find('Source') != -1:

                    list_param = ['SKPAR', 'SENERG', 'SPECTR', 'SGPOL', 'SEXTND',
                                  'STHICK', 'SRADII', 'SPOSIT', 'SCONE', 'SPYRAM']

                    spectr_sub = ['Ei','Pi']
                    sgpol_sub = ['SP1','SP2','SP3']
                    sposit_sub = ['SX0', 'SY0','SZ0']
                    sextnd_sub = ['KL','KC','RELAC']
                    scone_sub = ['THETA', 'PHI', 'ALPHA']
                    spyram_sub = ['THETAL','THETAU','PHIL','PHIU']
                    sradii = ['SRIN', 'SROUT']

                    for i, row_string in enumerate(string_list):
                        for j, param in enumerate(list_param):

                            if row_string.startswith(param):

                                # Quitamos el comentario entre corchetes, si tiene.
                                init = row_string.find('[')
                                string = row_string[:init]

                                # Quitamos los espacios y caracteres innecesarios.
                                string = ' '.join(re.split(r'[\s,;,>,\],\[]+',string)).lstrip(' ')

                                # Separamos los datos en una lista y quitamos los espacios vacios
                                string = [f for f in string.split(' ') if f]

                                # Separamos los datos
                                if string[0].startswith("SKPAR"):
                                    self.SKPAR = [f for f in string[1:]]

                                if string[0].startswith("SENERG"):
                                    self.SENERG = [f for f in string[1:]]

                                if string[0].startswith("SPECTR"):
                                    self.SPECTR = {n:f for (f,n) in zip(string[1:],spectr_sub)}

                                if string[0].startswith("SGPOL"):
                                    self.SGPOL = {n:f for (f,n) in zip(string[1:],sgpol_sub)}

                                if string[0].startswith("SPOSIT"):
                                    self.SPOSIT = {n:f for (f,n) in zip(string[1:],sposit_sub)}

                                if string[0].startswith("SEXTND"):
                                    self.SEXTND = {n:f for (f,n) in zip(string[1:],sextnd_sub)}

                                if string[0].startswith("STHICK"):
                                    self.STHICK = [f for f in string[1:]]

                                if string[0].startswith("SRADII"):
                                    self.SRADII = {n:f for (f,n) in zip(string[1:],sradii_sub)}

                                if string[0].startswith("SCONE"):
                                    self.SCONE = {n:f for (f,n) in zip(string[1:],scone_sub)}

                                if string[0].startswith("SPYRAM"):
                                    self.SPYRAM = {n:f for (f,n) in zip(string[1:],spyram_sub)}

    class __Material_Cyl():

        def __init__(self, string_list, num_bloq):
            # Instance Variable
                # Procesamos los datos.
            self.__data_process(string_list, num_bloq)

        def __data_process(self, string_list, num_bloq):

            for i in range(len(num_bloq)-1):

                if num_bloq[i][1].find('Material data') != -1:

                    list_param = ['MFNAME', 'MSIMPA']

                    # Separamos los datos
                    parametros = []
                    materiales = []
                    for i, row_string in enumerate(string_list):
                        for j, param in enumerate(list_param):

                            if row_string.startswith(param):

                                # Quitamos el comentario entre corchetes, si tiene.
                                init = row_string.find('[')
                                string = row_string[:init]

                                # Quitamos los espacios y caracteres innecesarios.
                                string = ' '.join(re.split(r'[\s,;,>,\],\[]+',string)).lstrip(' ')

                                # Separamos los datos en una lista y quitamos los espacios vacios
                                string = [f for f in string.split(' ') if f]

                                # Separamos los datos
                                if string[0].startswith("MSIMPA"):
                                    parametros.append([f for f in string[1:]])

                                if string[0].startswith("MFNAME"):
                                    materiales.append(string[1:][0].split('\\')[-1].rstrip('.mat'))

                    parameters = ['EAB1', 'EAB2', 'EAB3', 'C1', 'C2', 'WCC', 'WCR']
                    self.materials = {k:{p:float(v) for p,v in zip(parameters,parametros[i])} for i,k in enumerate(materiales)}

    class __Interaction_Forcing_Cyl():

        def __init__(self, string_list, num_bloq):
            # Instance Variable
                # Procesamos los datos.
            self.__data_process(string_list, num_bloq)

        def __data_process(self, string_list, num_bloq):

            for i in range(len(num_bloq)-1):

                if num_bloq[i][1].find('Interaction forcing') != -1:

                    list_param = ['IFORCE']

                    iforce_sub = ['KL','KC','KPAR','ICOL','FORCER','WLOW','WHIG']

                    for i, row_string in enumerate(string_list):
                        for j, param in enumerate(list_param):

                            if row_string.startswith(param):

                                # Quitamos el comentario entre corchetes, si tiene.
                                init = row_string.find('[')
                                string = row_string[:init]

                                # Quitamos los espacios y caracteres innecesarios.
                                string = ' '.join(re.split(r'[\s,;,>,\],\[]+',string)).lstrip(' ')

                                # Separamos los datos en una lista y quitamos los espacios vacios
                                string = [f for f in string.split(' ') if f]

                                # Separamos los datos
                                if string[0].startswith("IFORCE"):
                                    self.IFORCE = {n:f for (f,n) in zip(string[1:],iforce_sub)}

    class __Local_Maximum_Step_Length_Cyl():

        def __init__(self, string_list, num_bloq):
            # Instance Variable
                # Procesamos los datos.
            self.__data_process(string_list, num_bloq)

        def __data_process(self, string_list, num_bloq):

            for i in range(len(num_bloq)-1):

                if num_bloq[i][1].find('Local maximum') != -1:

                    list_param = ['DSMAX', 'EABSB']

                    dsmax_sub = ['KL','KC','DSMAX']
                    eabsb_sub = ['KL','KC','EABSB']

                    for i, row_string in enumerate(string_list):
                        for j, param in enumerate(list_param):

                            if row_string.startswith(param):

                                # Quitamos el comentario entre corchetes, si tiene.
                                init = row_string.find('[')
                                string = row_string[:init]

                                # Quitamos los espacios y caracteres innecesarios.
                                string = ' '.join(re.split(r'[\s,;,>,\],\[]+',string)).lstrip(' ')

                                # Separamos los datos en una lista y quitamos los espacios vacios
                                string = [f for f in string.split(' ') if f]

                                # Separamos los datos
                                if string[0].startswith("DSMAX"):
                                    self.DSMAX = {n:f for (f,n) in zip(string[1:],nbe_sub)}

                                if string[0].startswith("EABSB"):
                                    self.EABSB = {n:f for (f,n) in zip(string[1:],nbangl_sub)}

    class __Counter_Array_Dimensions_Cyl():

        def __init__(self, string_list, num_bloq):
            # Instance Variable
                # Procesamos los datos.
            self.__data_process(string_list, num_bloq)

        def __data_process(self, string_list, num_bloq):

            for i in range(len(num_bloq)-1):

                if num_bloq[i][1].find('Counter array') != -1:

                    list_param = ['NBE', 'NBANGL', 'NBZ', 'NBR', 'NBTL']

                    nbe_sub = ['EL','EU','NBE']
                    nbangl_sub = ['NBTH', 'NBPH']
                    nbz_sub = ['NBZ']
                    nbr_sub = ['NBR']
                    nbtl_sub = ['TLMIN','TLMAX','NBTL']

                    for i, row_string in enumerate(string_list):
                        for j, param in enumerate(list_param):

                            if row_string.startswith(param):

                                # Quitamos el comentario entre corchetes, si tiene.
                                init = row_string.find('[')
                                string = row_string[:init]

                                # Quitamos los espacios y caracteres innecesarios.
                                string = ' '.join(re.split(r'[\s,;,>,\],\[]+',string)).lstrip(' ')

                                # Separamos los datos en una lista y quitamos los espacios vacios
                                string = [f for f in string.split(' ') if f]

                                # Separamos los datos
                                if string[0].startswith("NBE"):
                                    self.NBE = {n:f for (f,n) in zip(string[1:],nbe_sub)}

                                if string[0].startswith("NBANGL"):
                                    self.NBANGL = {n:f for (f,n) in zip(string[1:],nbangl_sub)}

                                if string[0].startswith("NBZ"):
                                    self.NBZ = {n:f for (f,n) in zip(string[1:],nbz_sub)}

                                if string[0].startswith("NBR"):
                                    self.NBR = {n:f for (f,n) in zip(string[1:],nbr_sub)}

                                if string[0].startswith("NBTL"):
                                    self.NBTL = {n:f for (f,n) in zip(string[1:],nbtl_sub)}

    class __Energy_Deposition_Cyl():

        def __init__(self, string_list, num_bloq):
            # Instance Variable
                # Procesamos los datos.
            self.__data_process(string_list, num_bloq)

        def __data_process(self, string_list, num_bloq):

            for i in range(len(num_bloq)-1):

                if num_bloq[i][1].find('Energy deposition') != -1 or num_bloq[i][1].find('Energy-deposition') != -1:

                    list_param = ['ENDETC', 'EDSPC', 'EDBODY']

                    endetc_sub = ['EL','EU','NBE']
                    edbody_sub = ['KL', 'KC']

                    for i, row_string in enumerate(string_list):
                        for j, param in enumerate(list_param):

                            if row_string.startswith(param):

                                # Quitamos el comentario entre corchetes, si tiene.
                                init = row_string.find('[')
                                string = row_string[:init]

                                # Quitamos los espacios y caracteres innecesarios.
                                string = ' '.join(re.split(r'[\s,;,>,\],\[]+',string)).lstrip(' ')

                                # Separamos los datos en una lista y quitamos los espacios vacios
                                string = [f for f in string.split(' ') if f]

                                # Separamos los datos
                                if string[0].startswith("ENDETC"):
                                    self.ENDETC = {n:f for (f,n) in zip(string[1:],endetc_sub)}

                                if string[0].startswith("EDSPC"):
                                    self.EDSPC = [f for f in string[1:]]

                                if string[0].startswith("EDBODY"):
                                    self.EDBODY = {n:f for (f,n) in zip(string[1:],edbody_sub)}

    class __Dose_Distribution_Cyl():

        def __init__(self, string_list, num_bloq):
            # Instance Variable
                # Procesamos los datos.
            self.__data_process(string_list, num_bloq)

        def __data_process(self, string_list, num_bloq):

            for i in range(len(num_bloq)-1):

                if num_bloq[i][1].find('Dose') != -1:

                    list_param = ['DOSE2D']

                    dose_sub = ['KL','KC','NZ','NR']

                    for i, row_string in enumerate(string_list):
                        for j, param in enumerate(list_param):

                            if row_string.startswith(param):

                                # Quitamos el comentario entre corchetes, si tiene.
                                init = row_string.find('[')
                                string = row_string[:init]

                                # Quitamos los espacios y caracteres innecesarios.
                                string = ' '.join(re.split(r'[\s,;,>,\],\[]+',string)).lstrip(' ')

                                # Separamos los datos en una lista y quitamos los espacios vacios
                                string = [f for f in string.split(' ') if f]

                                # Separamos los datos
                                if string[0].startswith("DOSE2D"):
                                    self.DOSE2D = {n:f for (f,n) in zip(string[1:],dose_sub)}

    class __Charge_Distribution_Cyl():

        def __init__(self, string_list, num_bloq):
            # Instance Variable
                # Procesamos los datos.
            self.__data_process(string_list, num_bloq)

        def __data_process(self, string_list, num_bloq):

            for i in range(len(num_bloq)-1):

                if num_bloq[i][1].find('Charge') != -1 or num_bloq[i][1].find('charge') != -1:
                    list_param = ['DOSE2D']

                    dose_sub = ['KL','KC','NZ','NR']

                    for i, row_string in enumerate(string_list):
                        for j, param in enumerate(list_param):

                            if row_string.startswith(param):

                                # Quitamos el comentario entre corchetes, si tiene.
                                init = row_string.find('[')
                                string = row_string[:init]

                                # Quitamos los espacios y caracteres innecesarios.
                                string = ' '.join(re.split(r'[\s,;,>,\],\[]+',string)).lstrip(' ')

                                # Separamos los datos en una lista y quitamos los espacios vacios
                                string = [f for f in string.split(' ') if f]

                                # Separamos los datos
                                if string[0].startswith("DOSE2D"):
                                    self.CHARGE2D = {n:f for (f,n) in zip(string[1:],dose_sub)}

    class __Job_Properties_Cyl():

        def __init__(self, string_list, num_bloq):
            # Instance Variable
                # Procesamos los datos.
            self.__data_process(string_list, num_bloq)

        def __data_process(self, string_list, num_bloq):

            for i in range(len(num_bloq)-1):

                if num_bloq[i][1].find('Job properties') != -1:
                    rows_strings = string_list[num_bloq[i][0]:num_bloq[i+1][0]]

                    # Separamos los datos
                    for i, row_string in enumerate(rows_strings):

                        # Quitamos el string entre corchetes, si tiene.
                        init = row_string.find('[')
                        row_string = row_string[:init]

                        # Quitamos los espacios y caracteres innecesarios.
                        row_string = ' '.join(re.split(r'[\s,;,>,\],\[]+',row_string)).lstrip(' ')

                        # Separamos los datos en una lista y quitamos los espacios vacios
                        row_string = [f for f in row_string.split(' ') if f]

                        if row_string[0].startswith("RESUME"):
                            self.RESUME = row_string[1:][0]
                        if row_string[0].startswith("DUMPTO"):
                            self.DUMPTO = row_string[1:][0]
                        if row_string[0].startswith("RSEED"):
                            self.DUMPP = [f for f in row_string[1:]]
                        if row_string[0].startswith("DUMPP"):
                            self.DUMPP = int(row_string[1:][0])
                        if row_string[0].startswith("NSIMSH"):
                            self.NSIMSH = float(row_string[1:][0])
                        if row_string[0].startswith("TIME"):
                            self.TIME = float(row_string[1:][0])

class LoadDataFileGeometry():

    def __init__(self, pathfolder):
        # # Instance Variable

        # ---------------------------------------------------
        # Extraemos el PEN que se utiliza
        self.pen = pathfolder.split('\\')[-1]

        if self.pen == 'penmain_2018':

            # ---------------------------------------------------
            # Buscamos y elegimos el path del GEOMETRY a cargar
            path_geometry = self.__find_geometry_main(pathfolder)
            self.path = path_geometry

            # ---------------------------------------------------
            # Cargamos los datos del GEOMETRY en una lista
            self.string_list = self.__loadfile()

            self.__get_data_main()
            self.__get_data_info()


        elif self.pen == 'pencyl_2018':

            # ---------------------------------------------------
            # Buscamos y elegimos el path del GEOMETRY a cargar
            path_geometry = self.__find_geometry_cyl(pathfolder)
            self.path = path_geometry

            # ---------------------------------------------------
            # Cargamos los datos del GEOMETRY en una lista
            self.string_list = self.__loadfile()

            self.__get_data_cyl()
        else:
            print('No se encontro el archivo correspondiente a la geometria de la simulacion.')

    def __find_geometry_main(self, pathfolder):

        print('--------')
        print('GEOMETRY')
        print('--------\n')

        path_files = os.path.join(pathfolder, 'geo')
        files_geometry = [os.path.join(path_files, f) for f in os.listdir(path_files)
            if os.path.isfile(os.path.join(path_files, f)) and f.endswith('.rep') or f.endswith('.geo')]

        list_files = self.__basename(files_geometry)

        respuesta = option_list(answer_list=list_files, input_type='int', question='Archivos GEOMETRY encontrados', return_type=False)

        path_geometry = files_geometry[respuesta]

        return path_geometry

    def __find_geometry_cyl(self, pathfolder):

        print('--------')
        print('GEOMETRY')
        print('--------\n')

        path_files = os.path.join(pathfolder, 'input')
        files_geometry = [os.path.join(path_files, f) for f in os.listdir(path_files)
            if os.path.isfile(os.path.join(path_files, f)) and f.endswith('.in')]

        list_files = self.__basename(files_geometry)

        respuesta = option_list(answer_list=list_files, input_type='int', question='Archivos GEOMETRY encontrados', return_type=False)

        path_geometry = files_geometry[respuesta]

        return path_geometry

    def __basename(self, path):

        if len(path) != 1:
            basename_path = [os.path.basename(f) for f in path]
        else:
            basename_path = [os.path.basename(path[0])]

        return basename_path

    def __loadfile(self):

        file = open(self.path)
        string_list = file.readlines()
        file.close()
        return string_list

    def __get_data_main(self):

        string_list = self.string_list

        # --------------------------------------------------------------------------
        # (1) Abrimos el archivo y extraemos los datos de interes.

        # (1.1) Buscamos las lineas de texto que tengan las superficies que utiliza
        # el body

        # path = "D:\Proyectos_Investigacion\Proyectos_de_Doctorado\Proyectos\SimulationXF_Detectors\Code\RUN\penmain_2018\geo\geometry.rep"
        # file = open(path)
        # string_list = file.readlines()
        # file.close()

        # --- Identificamos la ubicacion de los bloques SURFACE, BODYS, MODULES y CLONES.
        blocks_limits = []
        for i,line in enumerate(string_list):
            # Si la linea empieza con 0 o C\n.
            if line.startswith('0'):
                for j,line1 in enumerate(string_list[i+1:]):
                    if line1.startswith('0'):
                        blocks_limits.append([i+1,i+j+1])
                        break
            if line.startswith('END'):
                blocks_limits.append([i,i])

        # --- Separamos los bloques de SURFACES de los otros
        blocks_surfaces_complete = []
        blocks_surfaces = []
        blocks_bodys = []
        for i, block in enumerate(blocks_limits):
            for line in string_list[block[0]:block[1]]:
                if line.startswith('SURFACE'):
                    num_surface = int(line.split(')')[0].split('(')[-1])
                    blocks_surfaces.append(block)
                    blocks_surfaces_complete.append([num_surface, block])
                    break
                if line.startswith('BODY') or line.startswith('MODULE'):
                    blocks_bodys.append(block)
                    break

        self.blocks_surfaces_complete = blocks_surfaces_complete
        self.blocks_surfaces = blocks_surfaces
        self.blocks_bodys = blocks_bodys

        # --- Separamos a cada BODYS, MODULES o CLONES en bloques
        data_body = {}
        for block in blocks_bodys:
            surfaces = []
            for line in string_list[block[0]:block[1]]:
                if line.startswith('MODULE') or line.startswith('BODY') and len(line)>=18:
                    name = line.rstrip('\n').split(' - ')[0].split(') ')[-1].lstrip(' ')
                    geometry = line.rstrip('\n').split(' - ')[1].split(' ')[0]
                    num = int(line.rstrip('\n').split(' - ')[0].split('(')[-1].split(')')[0])
                    type = line.rstrip('\n').split(' - ')[0].split('(')[0].split(' ')[0]
                if line.startswith('MATERIAL'):
                    material = int(line.split(')')[0].split('(')[-1])
                if line.startswith('SURFACE'):
                    surfaces.append(int(line.split(')')[0].split('(')[-1]))

            data_dict = {'Name':name, 'Block':block, 'Type':type, 'Geometry':geometry, 'Material':material,'Surfaces':surfaces}
            data_body.update({num:data_dict})

        bodys_names = []
        for block in blocks_bodys:
            for line in string_list[block[0]:block[1]]:
                if line.startswith('MODULE') or line.startswith('BODY') and len(line)>=18:
                    name = line.rstrip('\n').split(' - ')[0].split(') ')[-1].lstrip(' ')
                    bodys_names.append(name)
        self.BodysNames = bodys_names

        # (2.2) Obtenemos los datos de cada superficie.

        data_surface = []
        for i, block in enumerate(blocks_surfaces):
            surface = {k:[] for k in ['SURFACE', 'TYPE','AXX','AXY','AXZ','AYY','AYZ',
                                    'AZZ','AX','AY','AZ','A0','XSH','YSH','ZSH','XSC',
                                    'YSC','ZSC']}

            for j,line in enumerate(string_list[block[0]:block[1]]):
                if not line.startswith('C'):

                    while line.startswith(' '):
                        line = line.lstrip(' ')

                    # caracteristicas de la superficie
                    if line.startswith('SURFACE'):
                        pos1 = line.find('(')
                        pos2 = line.find(')')
                        nline = line[pos1+1:pos2+1]
                        surface['SURFACE'].append(int(nline.lstrip(' ').rstrip(')')))
                        # Tipo de superficie
                        if line.find('Plano') != -1:
                            surface['TYPE'].append('Plane')
                        elif line.find('Cilindro') != -1:
                            surface['TYPE'].append('Cylinder')
                        elif line.find('Esfera') != -1:
                            surface['TYPE'].append('Sphere')

                    # Vector de desplazamiento
                    if line.startswith('X-SHIFT'):
                        x = float(line.split('=(')[1].split(',')[0])
                        surface['XSH'].append(x)
                    if line.startswith('Y-SHIFT'):
                        y = float(line.split('=(')[1].split(',')[0])
                        surface['YSH'].append(y)
                    if line.startswith('Z-SHIFT'):
                        z = float(line.split('=(')[1].split(',')[0])
                        surface['ZSH'].append(z)

                    # Factor de escala
                    if line.startswith('X-SCALE'):
                        xs = float(line.split('=(')[1].split(',')[0])
                        surface['XSC'].append(xs)
                    if line.startswith('Y-SCALE'):
                        ys = float(line.split('=(')[1].split(',')[0])
                        surface['YSC'].append(ys)
                    if line.startswith('Z-SCALE'):
                        zs = float(line.split('=(')[1].split(',')[0])
                        surface['ZSC'].append(zs)

                    # Valores de matriz de transformacion.
                    if line.startswith('AXX='):
                        xxline = string_list[block[0]:block[1]][j].lstrip(' ')
                        axx = float(xxline.split('=(')[1].split(',')[0])
                        surface['AXX'].append(axx)
                    if line.startswith('AX='):
                        xline = string_list[block[0]:block[1]][j].lstrip(' ')
                        ax = float(xline.split('=(')[1].split(',')[0])
                        surface['AX'].append(ax)

                    if line.startswith('AYY='):
                        yyline = string_list[block[0]:block[1]][j].lstrip(' ')
                        ayy = float(yyline.split('=(')[1].split(',')[0])
                        surface['AYY'].append(ayy)
                    if line.startswith('AY='):
                        yline = string_list[block[0]:block[1]][j].lstrip(' ')
                        ay = float(yline.split('=(')[1].split(',')[0])
                        surface['AY'].append(ay)

                    if line.startswith('AZZ='):
                        zzline = string_list[block[0]:block[1]][j].lstrip(' ')
                        azz = float(zzline.split('=(')[1].split(',')[0])
                        surface['AZZ'].append(azz)
                    if line.startswith('AZ='):
                        zline = string_list[block[0]:block[1]][j].lstrip(' ')
                        az = float(zline.split('=(')[1].split(',')[0])
                        surface['AZ'].append(az)

                    if line.startswith('AXY='):
                        xyline = string_list[block[0]:block[1]][j].lstrip(' ')
                        axy = float(xyline.split('=(')[1].split(',')[0])
                        surface['AXY'].append(axy)
                    if line.startswith('AXZ='):
                        xzline = string_list[block[0]:block[1]][j].lstrip(' ')
                        axz = float(xzline.split('=(')[1].split(',')[0])
                        surface['AXZ'].append(axz)
                    if line.startswith('AYZ='):
                        yzline = string_list[block[0]:block[1]][j].lstrip(' ')
                        ayz = float(yzline.split('=(')[1].split(',')[0])
                        surface['AYZ'].append(ayz)

                    if line.startswith('A0'):
                        oline = string_list[block[0]:block[1]][j].lstrip(' ')
                        A0 = -1.0*float(oline.split('=(')[1].split(',')[0])
                        surface['A0'].append(A0)

            data_surface.append(surface)

        ds = {data_surface[j]['SURFACE'][0]:data_surface[j] for j in range(len(data_surface))}

        self.GetDataSurface = ds
        self.GetDataBody = data_body

        for num_body in data_body.keys():
            list_surfaces = data_body[num_body]['Surfaces']
            data_body[num_body]['Data Surfaces'] = {}
            for num_surf in list_surfaces:
                data_body[num_body]['Data Surfaces'].update({num_surf:ds[num_surf]})

        # self.GetDataSurface = ds

    def __get_data_cyl(self):

        string_list = self.__string_list

        # Definimos el bloque de geometria
        bloq_geo = []
        for i, line in enumerate(string_list):
            if line.startswith('GSTART'):
                bloq_geo.append(i+1)
            elif line.startswith('GEND'):
                bloq_geo.append(i)

        rows_strings = string_list[bloq_geo[0]:bloq_geo[1]]

        list_body = ['BODYS']
        list_param = ['LAYER', 'CENTER', 'CYLIND']

        layer_sub = ['ZLOW', 'ZHIG', 'NBODY']
        center_sub = ['XCEN', 'YCEN']
        cylind_sub = ['M','RIN','ROUT']

        bodys = {}
        # Medimos la cantidad de filas que contiene un BODY
        for row in range(len(rows_strings)):

            line = rows_strings[row]
            if line.startswith('LAYER'):
                # Definimos el body.
                init_body = line.find('[')
                body = line[init_body:].rstrip(']')
                body = ' '.join(re.split(r'[\s,;,>,\],\[]+',body)).lstrip(' ')
                # Separamos los datos en una lista y quitamos los espacios vacios
                body = [f for f in body.split(' ') if f][0]


                # Limpiamos el string
                line = line[:init_body]
                # Quitamos los espacios y caracteres innecesarios.
                line = ' '.join(re.split(r'[\s,;,>,\],\[]+',line)).lstrip(' ')
                # Separamos los datos en una lista y quitamos los espacios vacios
                line = [f for f in line.split(' ') if f]

                layer = {n:f for (f,n) in zip(line[1:],layer_sub)}

                line = rows_strings[row+1]
                if line.startswith('CENTER'):
                    # Quitamos los espacios y caracteres innecesarios.
                    line = ' '.join(re.split(r'[\s,;,>,\],\[]+',line)).lstrip(' ')
                    # Separamos los datos en una lista y quitamos los espacios vacios
                    line = [f for f in line.split(' ') if f]

                    center = {n:f for (f,n) in zip(line[1:],center_sub)}

                    line = rows_strings[row+2]
                    if line.startswith('CYLIND'):
                        # Quitamos los espacios y caracteres innecesarios.
                        line = ' '.join(re.split(r'[\s,;,>,\],\[]+',line)).lstrip(' ')
                        # Separamos los datos en una lista y quitamos los espacios vacios
                        line = [f for f in line.split(' ') if f]
                        cylind = {n:f for (f,n) in zip(line[1:],cylind_sub)}

                    bodys[body] = {'LAYER':layer,'CENTER':center,'CYLIND':cylind}

                elif line.startswith('CYLIND'):
                    # Quitamos los espacios y caracteres innecesarios.
                    line = ' '.join(re.split(r'[\s,;,>,\],\[]+',line)).lstrip(' ')
                    # Separamos los datos en una lista y quitamos los espacios vacios
                    line = [f for f in line.split(' ') if f]
                    cylind = {n:f for (f,n) in zip(line[1:],cylind_sub)}

                    bodys[body] = {'LAYER':layer,'CYLIND':cylind}

        self.Bodys = bodys

    def __get_data_info(self):

        # Obtenemos la informacion de los Bodys o Modules
        databody = self.GetDataBody

        # Contamos la cantidad de bodys
        self.numBodys = len(databody.keys())

        # Contamos la cantidad de superficies
        numSurfaces = []
        for num in databody.keys():
            body = databody[num]
            numSurfaces.append(body['Surfaces'])

        numSurfaces_flat = [item for sublist in numSurfaces for item in sublist]
        numSurfaces = list(set(numSurfaces_flat))
        self.numSurfaces = len(numSurfaces)

class GeomGenerator():

    def __init__(self):

        print('\n=================================')
        print(' --- INICIANDO GEOMGENERATOR --- ')
        print('=================================')

        # Cargamos la clase CircleDetectors
        self.genDetectors = self.__ShapeGenerator()
        # Cargamos la clase LoadDataFileGeometry
        self.FileGeometry = self.__FileGeometry()

    class __ShapeGenerator:

        def set_parameters(self, plane='XY', dimensions=[0.5, 0.5, 0.1], distance=3, translate=[0, 0, 0], angles=45, nplanes=9, widthSample=4, heightSample=1, shape='parallelepiped'):
            self.plane = plane
            self.dimensions = np.array(dimensions)
            self.distance = distance
            self.translate = np.array(translate)
            self.angles = angles if isinstance(angles, (list, np.ndarray)) else np.linspace(0, 360, angles, endpoint=False)
            self.nplanes = nplanes
            self.widthSample = widthSample
            self.heightSample = heightSample
            self.shape = shape

        def normalize_vertices(self, vertices):
            """Centra los vértices respecto a su propio centroide."""
            mean = np.mean(vertices, axis=0)
            return vertices - mean

        def translate_vertices(self, vertices, distance_vector):
            """Aplica una traslación a los vértices."""
            return vertices + distance_vector

        def get_unit_vectors(self, alpha):
            """
            Genera los vectores normal, transversal y cruzado para un paralelepípedo
            o un cilindro basado en el plano de apoyo seleccionado.
            """
            alpha_rad = np.radians(alpha)

            if self.plane == 'XY':
                vector_plane_norm = np.array([0, 0, 1])
                vector_face_norm = np.array([np.cos(alpha_rad), np.sin(alpha_rad), 0])
            elif self.plane == 'XZ':
                vector_plane_norm = np.array([0, 1, 0])
                vector_face_norm = np.array([np.cos(alpha_rad), 0, np.sin(alpha_rad)])
            elif self.plane == 'YZ':
                vector_plane_norm = np.array([1, 0, 0])
                vector_face_norm = np.array([0, np.cos(alpha_rad), np.sin(alpha_rad)])
            else:
                raise ValueError("Plano no reconocido. Usa 'XY', 'XZ' o 'YZ'.")

            vector_cross = np.cross(vector_plane_norm, vector_face_norm)
            vector_cross_norm = vector_cross / np.linalg.norm(vector_cross)

            return vector_plane_norm, vector_face_norm, vector_cross_norm

        def generate_cylinder(self, radial_vector):
            """
            Genera los vértices de un cilindro cuya orientación es hacia el origen.
            """
            radius, height = self.dimensions[:2]
            n_slices = 32  # Mayor suavidad del cilindro
            angles = np.linspace(0, 2 * np.pi, n_slices, endpoint=True)

            # Crear la base circular en el plano Z
            base_circle = np.array([[radius * np.cos(theta), radius * np.sin(theta), 0] for theta in angles])
            bottom_circle = base_circle
            top_circle = base_circle + np.array([0, 0, height])

            # Combinar las bases en una sola matriz de vértices
            vertices = np.vstack((bottom_circle, top_circle))

            # Normalizar el vector radial para obtener la dirección del eje
            radial_vector = radial_vector / np.linalg.norm(radial_vector)

            # Calcular un vector ortogonal (usaremos Z como referencia inicial)
            reference_vector = np.array([0, 0, 1])
            if np.allclose(radial_vector, reference_vector):
                reference_vector = np.array([1, 0, 0])  # Evitar degeneración si radial_vector es paralelo a Z

            # Vector ortogonal para definir el plano de rotación
            rotation_axis = np.cross(reference_vector, radial_vector)
            rotation_axis /= np.linalg.norm(rotation_axis)

            # Ángulo de rotación entre el eje Z y el vector radial
            angle = np.arccos(np.dot(reference_vector, radial_vector))

            # Matriz de rotación (usando el eje y el ángulo)
            c, s = np.cos(angle), np.sin(angle)
            ux, uy, uz = rotation_axis
            rotation_matrix = np.array([
                [c + ux**2 * (1 - c), ux * uy * (1 - c) - uz * s, ux * uz * (1 - c) + uy * s],
                [uy * ux * (1 - c) + uz * s, c + uy**2 * (1 - c), uy * uz * (1 - c) - ux * s],
                [uz * ux * (1 - c) - uy * s, uz * uy * (1 - c) + ux * s, c + uz**2 * (1 - c)]
            ])

            # Rotar y posicionar los vértices en el espacio 3D
            vertices = vertices @ rotation_matrix.T
            return vertices

        def get_vertices(self, alpha):
            """
            Genera los vértices de la forma seleccionada (paralelepípedo o cilindro).
            """
            vector_plane, vector_face, vector_cross = self.get_unit_vectors(alpha)
            if self.shape == 'parallelepiped':
                xdim, ydim, zdim = self.dimensions

                alpha_rad = np.radians(alpha)
                radial_vector = np.array([
                    np.cos(alpha_rad) * self.distance,
                    np.sin(alpha_rad) * self.distance,
                    0])
                # Calculamos los vértices básicos del paralelepípedo
                vp1 = vector_plane * zdim
                vp2 = vector_face * xdim
                vp3 = vector_cross * ydim

                # Vértices combinados
                vertices = np.array([
                    vp1, vp2, vp3,
                    vp1 + vp2,
                    vp1 + vp3,
                    vp2 + vp3,
                    vp1 + vp2 + vp3,
                    [0, 0, 0]
                ])
            elif self.shape == 'cylinder':
                alpha_rad = np.radians(alpha)
                radial_vector = np.array([
                    np.cos(alpha_rad) * self.distance,
                    np.sin(alpha_rad) * self.distance,
                    0
                ])
                vertices = self.generate_cylinder(radial_vector)
            else:
                raise ValueError("Forma no reconocida. Usa 'parallelepiped' o 'cylinder'.")

            # Normalizamos los vértices al centro
            vertices = self.normalize_vertices(vertices)

            # Traslación al radio especificado
            vertices = self.translate_vertices(vertices, radial_vector)

            # Traslación final definida por el usuario
            vertices = self.translate_vertices(vertices, self.translate)

            return vertices, [vector_plane, vector_face, vector_cross]

        def get_line_detectors(self):
            """
            Genera una línea de detectores basada en los ángulos y posiciones en los planos
            especificados.
            """
            print('\n--> Obteniendo vértices de los detectores\n')
            vertices_detectors = []

            for alpha in self.angles:
                vertices, normals = self.get_vertices(alpha)
                cross_vector = normals[2]

                # Generamos posiciones equiespaciadas a lo largo de la muestra
                positions = np.linspace(-self.lengthSample / 2, self.lengthSample / 2, self.nplanes)
                for pos in positions:
                    vertices_detectors.append(vertices + cross_vector * pos)

            return vertices_detectors

        def get_line_direction(self, vertices_detectors):
            """
            Extrae la dirección y posición (origen) de los detectores para
            paralelepípedos o cilindros.

            - Parámetros:
                .vertices_detectors: lista
                    Lista de conjuntos de vértices para cada detector.

            - Retorno:
                .origin: numpy.array
                    Posiciones centrales de los detectores.
                .direction: numpy.array
                    Direcciones principales de los detectores.
            """
            print(' --> Extrayendo la posición y dirección de los detectores. \n')

            origins = []
            directions = []

            for vertices in vertices_detectors:
                # Si es un cilindro, los puntos extremos son la base y la tapa circular.
                if self.shape == 'cylinder':
                    # Asumimos que los primeros puntos corresponden a la base y los últimos a la tapa
                    n_points = len(vertices) // 2
                    base_circle = vertices[:n_points]
                    top_circle = vertices[n_points:]

                    # El origen será el centro de la base del cilindro
                    center_base = np.mean(base_circle, axis=0)
                    center_top = np.mean(top_circle, axis=0)

                    # La dirección será el vector entre los centros de la base y la tapa
                    direction_vector = center_top - center_base
                    direction_vector /= np.linalg.norm(direction_vector)

                    origins.append(center_top)
                    directions.append(direction_vector)
                else:
                    # Para paralelepípedos, usamos los vértices conocidos para calcular las direcciones.
                    Z = vertices[:, :2]  # Nos limitamos a las coordenadas X-Y

                    # Dirección de los lados paralelos
                    dir1 = [Z[2, 0] - Z[5, 0], Z[2, 1] - Z[5, 1]]
                    dir2 = [Z[7, 0] - Z[3, 0], Z[7, 1] - Z[3, 1]]

                    # Normalizamos las direcciones
                    dir1 /= np.linalg.norm(dir1)
                    dir2 /= np.linalg.norm(dir2)

                    directions.append([dir1, dir2])

                    # Origen: puntos centrales
                    pos1 = [Z[7, 0], Z[7, 1]]
                    pos2 = [Z[2, 0], Z[2, 1]]

                    origins.append([pos1, pos2])

            origins = np.array(origins)
            directions = np.array(directions)

            return origins, directions

        # def get_matrix_detectors(self, rows, cols, sample_width=1.0, sample_height=1.0):
            # """
            # Genera una matriz de detectores dispuestos en filas y columnas en un plano especificado,
            # con espaciado determinado automáticamente por el tamaño de la muestra.
            #
            # Parámetros:
            # - rows (int): Número de filas de detectores.
            # - cols (int): Número de columnas de detectores.
            # - sample_width (float): Ancho de la muestra (dirección X).
            # - sample_height (float): Altura de la muestra (dirección Y).
            #
            # Retorno:
            # - vertices_detectors (list): Lista de matrices de vértices de detectores en disposición de matriz.
            # """
            # print('\n--> Obteniendo matriz de detectores centrada basada en tamaño de muestra\n')
            # vertices_detectors = []
            #
            # # Calcular el espaciado basado en el tamaño de la muestra
            # spacing_y = sample_width / max(cols - 1, 1)  # Espaciado entre filas
            # spacing_x = sample_height / max(rows - 1, 1)  # Espaciado entre columnas
            #
            # # Iterar sobre los ángulos especificados
            # for alpha in self.angles:
            #     alpha_rad = np.radians(alpha)
            #     radial_vector = np.array([
            #         np.cos(alpha_rad) * self.distance,
            #         np.sin(alpha_rad) * self.distance,
            #         0
            #     ])
            #
            #     # Obtener los vértices base del detector
            #     vertices_base, normals = self.get_vertices(alpha)
            #     cross_vector = normals[2]  # Vector transversal para desplazar detectores en filas
            #     normal_vector = normals[0]  # Vector transversal para desplazar detectores en columnas
            #
            #     # Calcular el desplazamiento para centrar la matriz
            #     row_center_offset = cross_vector * (rows - 1) * spacing_x / 2
            #     col_center_offset = normal_vector * (cols - 1) * spacing_y / 2
            #     center_offset = row_center_offset + col_center_offset
            #
            #     # Generar matriz de detectores
            #     for col in range(cols):
            #         for row in range(rows):
            #             # Calcular desplazamiento en fila y columna desde el centro
            #             row_offset = cross_vector * (row * spacing_x)
            #             col_offset = normal_vector * (col * spacing_y)
            #
            #             # Aplicar los desplazamientos al detector base y centrar
            #             detector = vertices_base + row_offset + col_offset - center_offset
            #             vertices_detectors.append(detector)
            #
            # return vertices_detectors

        def get_matrix_detectors(self, rows, cols, sample_width=1.0, sample_height=1.0):
            """
            Genera una matriz de detectores dispuestos en filas y columnas en un plano especificado,
            con espaciado determinado automáticamente por el tamaño de la muestra.

            Parámetros:
            - rows (int): Número de filas de detectores.
            - cols (int): Número de columnas de detectores.
            - sample_width (float): Ancho de la muestra (ahora para filas, dirección X).
            - sample_height (float): Altura de la muestra (ahora para columnas, dirección Y).

            Retorno:
            - vertices_detectors (list): Lista de matrices de vértices de detectores en disposición de matriz.
            """
            print('\n--> Obteniendo matriz de detectores centrada basada en tamaño de muestra\n')
            vertices_detectors = []

            # Calcular el espaciado basado en el tamaño de la muestra
            spacing_x = sample_width / max(rows - 1, 1)  # Espaciado entre filas (dirección X)
            spacing_y = sample_height / max(cols - 1, 1)  # Espaciado entre columnas (dirección Y)

            # Iterar sobre los ángulos especificados
            for alpha in self.angles:
                alpha_rad = np.radians(alpha)
                radial_vector = np.array([
                    np.cos(alpha_rad) * self.distance,
                    np.sin(alpha_rad) * self.distance,
                    0
                ])

                # Obtener los vértices base del detector
                vertices_base, normals = self.get_vertices(alpha)
                cross_vector = normals[2]  # Vector transversal para desplazar detectores en filas
                normal_vector = normals[0]  # Vector transversal para desplazar detectores en columnas

                # Calcular el desplazamiento para centrar la matriz
                row_center_offset = cross_vector * (rows - 1) * spacing_x / 2  # Ahora filas (X)
                col_center_offset = normal_vector * (cols - 1) * spacing_y / 2  # Ahora columnas (Y)
                center_offset = row_center_offset + col_center_offset

                # Generar matriz de detectores
                for col in range(cols):  # Filas (espaciado en X)
                    for row in range(rows):  # Columnas (espaciado en Y)
                        # Calcular desplazamiento en fila y columna desde el centro
                        row_offset = cross_vector * (row * spacing_x)
                        col_offset = normal_vector * (col * spacing_y)

                        # Aplicar los desplazamientos al detector base y centrar
                        detector = vertices_base + row_offset + col_offset - center_offset
                        vertices_detectors.append(detector)

            return vertices_detectors

    class __FileGeometry():

        def __init__(self):

            # Instance Variable
            self.string_list = []
            print('')

        def ReadFile(self, pathFileGeom):

            self.pathFileGeom = pathFileGeom

            file = open(self.pathFileGeom)
            self.string_list = file.readlines()
            file.close()

            self.__GetDataFile()
            self.__GetDataInfo()

        def __GetDataFile(self):

            string_list = self.string_list

            # --------------------------------------------------------------------------
            # (1) Abrimos el archivo y extraemos los datos de interes.

            # (1.1) Buscamos las lineas de texto que tengan las superficies que utiliza
            # el body

            # path = "D:\Proyectos_Investigacion\Proyectos_de_Doctorado\Proyectos\SimulationXF_Detectors\Code\RUN\penmain_2018\geo\geometry.rep"
            # file = open(path)
            # string_list = file.readlines()
            # file.close()

            # --- Identificamos la ubicacion de los bloques SURFACE, BODYS, MODULES y CLONES.
            blocks_limits = []
            for i,line in enumerate(string_list):
                # Si la linea empieza con 0 o C\n.
                if line.startswith('0'):
                    for j,line1 in enumerate(string_list[i+1:]):
                        if line1.startswith('0'):
                            blocks_limits.append([i+1,i+j+1])
                            break
                if line.startswith('END'):
                    blocks_limits.append([i,i])

            # --- Separamos los bloques de SURFACES de los otros
            blocks_surfaces_complete = []
            blocks_surfaces = []
            blocks_bodys = []
            for i, block in enumerate(blocks_limits):
                for line in string_list[block[0]:block[1]]:
                    if line.startswith('SURFACE'):
                        num_surface = int(line.split(')')[0].split('(')[-1])
                        blocks_surfaces.append(block)
                        blocks_surfaces_complete.append([num_surface, block])
                        break
                    if line.startswith('BODY') or line.startswith('MODULE'):
                        blocks_bodys.append(block)
                        break

            self.blocks_surfaces_complete = blocks_surfaces_complete
            self.blocks_surfaces = blocks_surfaces
            self.blocks_bodys = blocks_bodys

            # --- Separamos a cada BODYS, MODULES o CLONES en bloques
            data_body = {}
            for block in blocks_bodys:
                surfaces = []
                for line in string_list[block[0]:block[1]]:
                    if line.startswith('MODULE') or line.startswith('BODY') and len(line)>=18:
                        name = line.rstrip('\n').split(' - ')[0].split(') ')[-1].lstrip(' ')
                        geometry = line.rstrip('\n').split(' - ')[1].split(' ')[0]
                        num = int(line.rstrip('\n').split(' - ')[0].split('(')[-1].split(')')[0])
                        type = line.rstrip('\n').split(' - ')[0].split('(')[0].split(' ')[0]
                    if line.startswith('MATERIAL'):
                        material = int(line.split(')')[0].split('(')[-1])
                    if line.startswith('SURFACE'):
                        surfaces.append(int(line.split(')')[0].split('(')[-1]))

                data_dict = {'Name':name, 'Block':block, 'Type':type, 'Geometry':geometry, 'Material':material,'Surfaces':surfaces}
                data_body.update({num:data_dict})

            bodys_names = []
            for block in blocks_bodys:
                for line in string_list[block[0]:block[1]]:
                    if line.startswith('MODULE') or line.startswith('BODY') and len(line)>=18:
                        name = line.rstrip('\n').split(' - ')[0].split(') ')[-1].lstrip(' ')
                        bodys_names.append(name)
            self.BodysNames = bodys_names

            # (2.2) Obtenemos los datos de cada superficie.

            data_surface = []
            for i, block in enumerate(blocks_surfaces):
                surface = {k:[] for k in ['SURFACE', 'TYPE','AXX','AXY','AXZ','AYY','AYZ',
                                        'AZZ','AX','AY','AZ','A0','XSH','YSH','ZSH','XSC',
                                        'YSC','ZSC']}

                for j,line in enumerate(string_list[block[0]:block[1]]):
                    if not line.startswith('C'):

                        while line.startswith(' '):
                            line = line.lstrip(' ')

                        # caracteristicas de la superficie
                        if line.startswith('SURFACE'):
                            pos1 = line.find('(')
                            pos2 = line.find(')')
                            nline = line[pos1+1:pos2+1]
                            surface['SURFACE'].append(int(nline.lstrip(' ').rstrip(')')))
                            # Tipo de superficie
                            if line.find('Plano') != -1:
                                surface['TYPE'].append('Plane')
                            elif line.find('Cilindro') != -1:
                                surface['TYPE'].append('Cylinder')
                            elif line.find('Esfera') != -1:
                                surface['TYPE'].append('Sphere')

                        # Vector de desplazamiento
                        if line.startswith('X-SHIFT'):
                            x = float(line.split('=(')[1].split(',')[0])
                            surface['XSH'].append(x)
                        if line.startswith('Y-SHIFT'):
                            y = float(line.split('=(')[1].split(',')[0])
                            surface['YSH'].append(y)
                        if line.startswith('Z-SHIFT'):
                            z = float(line.split('=(')[1].split(',')[0])
                            surface['ZSH'].append(z)

                        # Factor de escala
                        if line.startswith('X-SCALE'):
                            xs = float(line.split('=(')[1].split(',')[0])
                            surface['XSC'].append(xs)
                        if line.startswith('Y-SCALE'):
                            ys = float(line.split('=(')[1].split(',')[0])
                            surface['YSC'].append(ys)
                        if line.startswith('Z-SCALE'):
                            zs = float(line.split('=(')[1].split(',')[0])
                            surface['ZSC'].append(zs)

                        # Valores de matriz de transformacion.
                        if line.startswith('AXX='):
                            xxline = string_list[block[0]:block[1]][j].lstrip(' ')
                            axx = float(xxline.split('=(')[1].split(',')[0])
                            surface['AXX'].append(axx)
                        if line.startswith('AX='):
                            xline = string_list[block[0]:block[1]][j].lstrip(' ')
                            ax = float(xline.split('=(')[1].split(',')[0])
                            surface['AX'].append(ax)

                        if line.startswith('AYY='):
                            yyline = string_list[block[0]:block[1]][j].lstrip(' ')
                            ayy = float(yyline.split('=(')[1].split(',')[0])
                            surface['AYY'].append(ayy)
                        if line.startswith('AY='):
                            yline = string_list[block[0]:block[1]][j].lstrip(' ')
                            ay = float(yline.split('=(')[1].split(',')[0])
                            surface['AY'].append(ay)

                        if line.startswith('AZZ='):
                            zzline = string_list[block[0]:block[1]][j].lstrip(' ')
                            azz = float(zzline.split('=(')[1].split(',')[0])
                            surface['AZZ'].append(azz)
                        if line.startswith('AZ='):
                            zline = string_list[block[0]:block[1]][j].lstrip(' ')
                            az = float(zline.split('=(')[1].split(',')[0])
                            surface['AZ'].append(az)

                        if line.startswith('AXY='):
                            xyline = string_list[block[0]:block[1]][j].lstrip(' ')
                            axy = float(xyline.split('=(')[1].split(',')[0])
                            surface['AXY'].append(axy)
                        if line.startswith('AXZ='):
                            xzline = string_list[block[0]:block[1]][j].lstrip(' ')
                            axz = float(xzline.split('=(')[1].split(',')[0])
                            surface['AXZ'].append(axz)
                        if line.startswith('AYZ='):
                            yzline = string_list[block[0]:block[1]][j].lstrip(' ')
                            ayz = float(yzline.split('=(')[1].split(',')[0])
                            surface['AYZ'].append(ayz)

                        if line.startswith('A0'):
                            oline = string_list[block[0]:block[1]][j].lstrip(' ')
                            A0 = -1.0*float(oline.split('=(')[1].split(',')[0])
                            surface['A0'].append(A0)

                data_surface.append(surface)

            ds = {data_surface[j]['SURFACE'][0]:data_surface[j] for j in range(len(data_surface))}

            self.GetDataSurface = ds
            self.GetDataBody = data_body

            for num_body in data_body.keys():
                list_surfaces = data_body[num_body]['Surfaces']
                data_body[num_body]['Data Surfaces'] = {}
                for num_surf in list_surfaces:
                    data_body[num_body]['Data Surfaces'].update({num_surf:ds[num_surf]})

            # self.GetDataSurface = ds

        def __GetDataInfo(self):

            # Obtenemos la informacion de los Bodys o Modules
            databody = self.GetDataBody

            # Contamos la cantidad de bodys
            self.numBodys = len(databody.keys())

            # Contamos la cantidad de superficies
            numSurfaces = []
            for num in databody.keys():
                body = databody[num]
                numSurfaces.append(body['Surfaces'])

            numSurfaces_flat = [item for sublist in numSurfaces for item in sublist]
            numSurfaces = list(set(numSurfaces_flat))
            self.numSurfaces = len(numSurfaces)

        def GetCoefficientMatrix(self, print_screen=False):

            if self.string_list == []:
                print("No hay archivos de geometria cargados.")
                return

            coeff_bodies = []
            listCoeff = ['AXX','AXY','AXZ','AYY','AYZ','AZZ','AX','AY','AZ','A0','XSH','YSH','ZSH','XSC','YSC','ZSC']
            for numBody in list(self.GetDataBody.keys()):
                body = self.GetDataBody[numBody]
                coeff_rect = []
                for numSurf in list(body['Data Surfaces'].keys()):
                    for numCoeff in listCoeff:
                        stringCoeff = body['Data Surfaces'][numSurf][numCoeff]
                        if numCoeff == 'AX':
                            if stringCoeff != []:
                                ax = stringCoeff[0]
                            else:
                                ax = 0.0
                        if numCoeff == 'AY':
                            if stringCoeff != []:
                                ay = stringCoeff[0]
                            else:
                                ay = 0.0
                        if numCoeff == 'AZ':
                            if stringCoeff != []:
                                az = stringCoeff[0]
                            else:
                                az = 0.0
                        if numCoeff == 'A0':
                            if stringCoeff != []:
                                ao = stringCoeff[0]
                            else:
                                ao = 0.0
                    coeff_rect.append([ax,ay,az,ao])
                coeff_bodies.append(coeff_rect)

            coefficients_rects = np.array(coeff_bodies)

            # Definir los 6 planos
            vertices_rect = []
            for planes in coefficients_rects:
                vertices = []
                for i in range(6):
                    for j in range(i+1, 6):
                        for k in range(j+1, 6):
                            A = np.array([planes[i][:3], planes[j][:3], planes[k][:3]])
                            b = np.array([-planes[i][3], -planes[j][3], -planes[k][3]])
                            try:
                                x = np.linalg.solve(A, b)
                                vertices.append(x)
                            except np.linalg.LinAlgError:
                                pass

                vertices_rect.append(vertices)

            verts = []
            for vertices in vertices_rect:
                print('')
                verts_rect = []
                for i, v in enumerate(vertices):
                    print(f"Vértice {i+1}: ({v[0]:.2f}, {v[1]:.2f}, {v[2]:.2f})")
                    if v[0] > 1000 or v[1] > 1000 or v[2] > 1000 or v[0] < -1000 or v[1] < -1000 or v[2] < -1000:
                        continue
                    else:
                        verts_rect.append([v[0],v[1],v[2]])
                verts.append(verts_rect)

            if print_screen:

                # Imprimir los vértices
                for vertices in verts_rect:
                    print('')
                    for i, v in enumerate(vertices):
                        print(f"Vértice {i+1}: ({v[0]:.2f}, {v[1]:.2f}, {v[2]:.2f})")

            return verts

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
        super(plotsTools, self).__init__()

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

class SimulatePENELOPE(QWidget):

    def __init__(self):
        super(SimulatePENELOPE, self).__init__()

        self.__Layaout_Principal()

        layout_Simulate = QHBoxLayout()
        layout_Simulate.addLayout(self.llayout, 30)
        layout_Simulate.addLayout(self.rlayout, 70)
        self.setLayout(layout_Simulate)

    def __Layaout_Principal(self):

        # --------------------------------------------------
        # (1) LLAYOUT

        # Boton para cargar input
        self.button_input = QPushButton("Load Input")
        init_widget(self.button_input, "load_input")
        self.textbox_input = QLineEdit()

        # Boton para cargar geometria
        self.button_geom = QPushButton("Load Geometry")
        init_widget(self.button_geom, "load_geometry")
        self.textbox_geom = QLineEdit()

        # Boton para cargar ejecutable
        self.button_exe = QPushButton("Load Exe")
        init_widget(self.button_exe, "load_exe")
        self.textbox_exe = QLineEdit()

        # Conexiones con los botones
        self.button_input.clicked.connect(self.loadFileInput)
        self.button_geom.clicked.connect(self.loadFileGeo)
        self.button_exe.clicked.connect(self.loadFileExe)

        # ---- llayout
        self.llayout = QVBoxLayout()
        self.llayout.setContentsMargins(1, 1, 1, 1)

        self.label1 = QLabel("CARGAR ARCHIVOS PARA SIMULACIÓN")
        self.label1.setStyleSheet("border: 2px solid gray; position: center;")
        self.llayout.addWidget(self.label1)

        self.llayout.addWidget(QLabel("Archivo Input:"))
        self.horizontalLayou1 = QHBoxLayout()
        self.horizontalLayou1.addWidget(self.button_input)
        self.horizontalLayou1.addWidget(self.textbox_input)
        self.llayout.addLayout(self.horizontalLayou1)

        self.llayout.addWidget(QLabel("Archivo Geometría:"))
        self.horizontalLayou2 = QHBoxLayout()
        self.horizontalLayou2.addWidget(self.button_geom)
        self.horizontalLayou2.addWidget(self.textbox_geom)
        self.llayout.addLayout(self.horizontalLayou2)

        self.llayout.addWidget(QLabel("Archivo Ejecutable:"))
        self.horizontalLayou3 = QHBoxLayout()
        self.horizontalLayou3.addWidget(self.button_exe)
        self.horizontalLayou3.addWidget(self.textbox_exe)
        self.llayout.addLayout(self.horizontalLayou3)

        self.llayout.addStretch()
        # ----

        # Creamos un QTextEdit y lo hacemos editable
        self.text_edit = QTextEdit(self)
        self.text_edit.setReadOnly(True)

        # Creamos un botón para ejecutar el comando
        self.btn_run = QPushButton('Ejecutar Simulación', self)
        self.btn_run.clicked.connect(self.start_simulation)

        # Creamos un layout vertical y añadimos los widgets
        self.rlayout = QVBoxLayout()
        self.rlayout.setContentsMargins(1, 1, 1, 1)

        self.rlayout.addWidget(self.text_edit)
        self.rlayout.addWidget(self.btn_run)
        # self.setLayout(rlayout)

    def loadFileExe(self):

        # Creamos la ventana emergente para que se pueda seleccionar el archivo.
        opciones = QFileDialog.Options()
        opciones |= QFileDialog.DontUseNativeDialog
        pathfile, _ = QFileDialog.getOpenFileName(self, "Seleccionar archivo Ejecutable", "",
                                                  "Archivos ejecutable (*.exe);;Archivos de texto (*.txt);;Todos los archivos (*)",
                                                  options=opciones)
        basename = os.path.basename(pathfile)
        if basename.split('.')[-1] != "exe":
            msgBox = QMessageBox()
            msgBox.setText("No se puede cargar ese tipo de archivos.")
            msgBox.setStandardButtons(QMessageBox.Cancel)
            ret = msgBox.exec()
        else:
            # Cargamos el archivo seleccionado.
            self.pathFileExe = pathfile
            self.textbox_exe.setText(os.path.basename(self.pathFileExe))

    def loadFileGeo(self):

        # Creamos la ventana emergente para que se pueda seleccionar el archivo.
        opciones = QFileDialog.Options()
        opciones |= QFileDialog.DontUseNativeDialog
        pathfile, _ = QFileDialog.getOpenFileName(self, "Seleccionar archivo de geometría", "",
                                                  "Archivos de geometría (*.geo);;Archivos de texto (*.txt);;Todos los archivos (*)",
                                                  options=opciones)
        basename = os.path.basename(pathfile)
        if basename.split('.')[-1] != "geo":
            msgBox = QMessageBox()
            msgBox.setText("No se puede cargar ese tipo de archivos.")
            msgBox.setStandardButtons(QMessageBox.Cancel)
            ret = msgBox.exec()
        else:
            # Cargamos el archivo seleccionado.
            self.pathFileGeom = pathfile
            self.textbox_geom.setText(os.path.basename(self.pathFileGeom))

    def loadFileInput(self):

        # Creamos la ventana emergente para que se pueda seleccionar el archivo.
        opciones = QFileDialog.Options()
        opciones |= QFileDialog.DontUseNativeDialog
        pathfile, _ = QFileDialog.getOpenFileName(self, "Seleccionar archivo Input", "",
                                                  "Archivos de entrada (*.in);;Archivos de texto (*.txt);;Todos los archivos (*)",
                                                  options=opciones)
        basename = os.path.basename(pathfile)
        if basename.split('.')[-1] != "in":
            msgBox = QMessageBox()
            msgBox.setText("No se puede cargar ese tipo de archivos.")
            msgBox.setStandardButtons(QMessageBox.Cancel)
            ret = msgBox.exec()
        else:
            # Cargamos el archivo seleccionado.
            self.pathFileInput = pathfile
            self.textbox_input.setText(os.path.basename(self.pathFileInput))

    def start_simulation(self):

        pathPen = os.path.join('D:\\', *self.pathFileExe.split('/')[1:-1])

        # ------------------------------------------
        # Removemos los datos que quedaron en RUN.
        path_data = [os.path.join(pathPen, f) for f in os.listdir(pathPen)
            if os.path.isfile(os.path.join(pathPen, f)) and
            (f.endswith('.dat') or f.endswith('.rep')) and not f.startswith('PhaseSpace')]
        if len(path_data) > 0:
            for pathfile in path_data:
                os.remove(pathfile)

        # -------------------------------------------
        # # GEOMETRIA
        # (1) Cargamos la GEOMETRIA
        path_geo = self.pathFileGeom
        # -------------------------------------------
        # # INPUT
        # (1) Cargamos el INPUT
        path_input = self.pathFileInput

        # -------------------------------------------
        # # SIMULACION
        # --------------------------------------------------------
        # # Introducimos el input en el ejecutable.
        path_cwd = os.path.join('D:\\',*self.pathFileExe.split('/')[1:-1])

        process = subprocess.Popen([self.pathFileExe, '<', path_input], shell=True, cwd=path_cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        process.wait()

        # Leemos la salida del proceso y la mostramos en el QTextEdit
        while True:
            output = process.stdout.readline().decode()
            if output == '' and process.poll() is not None:
                break
            if output:
                self.text_edit.append(output.strip())
                QApplication.processEvents()

        # Mostramos los errores del proceso en caso de haberlos
        error = process.stderr.read().decode()
        if error:
            self.text_edit.append(error.strip())


        # --------------------------------------------------------
        # # Movemos los resultados a la carpeta RESULTS

        pathResult = os.path.join('D:\\', *self.pathFileExe.split('/')[1:-3], 'RESULTS')

        path_data = [os.path.join(pathPen, f) for f in os.listdir(pathPen)
            if os.path.isfile(os.path.join(pathPen, f)) and
            (f.endswith('.dat') or f.endswith('.rep')) and not f.startswith('PhaseSpace')]

        pathDirResults = [nameDir for nameDir in os.listdir(pathResult) if nameDir.startswith('Ensayo_') ]
        if len(pathDirResults) != 0:
            e = len(pathDirResults) + 1
        else:
            e = 1

        dest_folder = os.path.join(pathResult, 'Ensayo_{}'.format(e))
        if not os.path.lexists(dest_folder):
            os.makedirs(dest_folder)

        for j in path_data:
            shutil.move(j, dest_folder)

class Plot3DView(QWidget):
    def __init__(self):
        super().__init__()

        # Inicializamos parámetros
        self._activeSource = False

        # Configuramos la pantalla principal
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
        self.add_widgets_to_layout(self.llayout, [
            ("Cargar archivo", self.button_phaseSpace),
        ])

        self.llayout.addStretch()
        # Configuración visual
        self.add_section_label("CONFIGURACIÓN VISUAL DE ANILLOS DETECTORES", self.llayout)
        self.add_widgets_to_layout(self.llayout, [
            ("Plano:", self._plane),
            ("Detectores por fila: ", self._nCols),
            ("Detectores por columna: ", self._nRows),
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

        # self.setWindowIcon(QtGui.QIcon('logo_mc-tcad.png'))
        self.setWindowTitle("Sistemas de Detección")

        # self.image_background = QLabel(self)
        # self.image_background.setStyleSheet(stylesheet)

        # (1) MENU PRINCIPAL
        # (1.1) File
        fileMenu = self.menuBar().addMenu("&File")  # Dentro de File las opciones de Load... y Exit
        loadAction = QAction("Load...", self, shortcut="Ctrl+L", triggered=self.load_file)
        fileMenu.addAction(loadAction)
        saveAction = QAction("Save...", self, shortcut="Ctrl+S", triggered=self.save_file)
        fileMenu.addAction(saveAction)
        exitAction = QAction("E&xit", self, shortcut="Ctrl+Q", triggered=self.close)
        fileMenu.addAction(exitAction)
        # (1.2) About
        aboutMenu = self.menuBar().addMenu("&About")
        aboutQtAct = QAction("About &Qt", self, triggered=qApp.aboutQt)
        aboutMenu.addAction(aboutQtAct)

        # (1.3) Barra de herramientas
        toolBar = QToolBar()
        self.addToolBar(toolBar)
        # Barra de botones
        geometryAction = QAction("Geometría Detector", self, shortcut="Ctrl+L", triggered=self.__geometryDetector)
        simulateAction = QAction("Simualción", self, shortcut="Ctrl+L", triggered=self.__simulatedPenelope)
        plotsAction = QAction("Plots", self, shortcut="Ctrl+L", triggered=self.__plotsTools)
        # Agregamos las acciones
        toolBar.addAction(geometryAction)
        toolBar.addAction(simulateAction)
        toolBar.addAction(plotsAction)

        # (2) VENTANA PRINCIPAL
        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)

    def __geometryDetector(self):

        self.mpl_can = Plot3DView()
        # la agregamos a la ventana principal
        self.central_widget.addWidget(self.mpl_can)
        self.central_widget.setCurrentWidget(self.mpl_can)

    def __simulatedPenelope(self):

        self.__sPen = SimulatePENELOPE()
        # la agregamos a la ventana principal
        self.central_widget.addWidget(self.__sPen)
        self.central_widget.setCurrentWidget(self.__sPen)

    def __plotsTools(self):

        self.plotsTools = plotsTools()
        # la agregamos a la ventana principal
        self.central_widget.addWidget(self.plotsTools)
        self.central_widget.setCurrentWidget(self.plotsTools)

    def load_file(self):

        # Creamos la ventana emergente para que se pueda seleccionar el archivo.
        opciones = QFileDialog.Options()
        opciones |= QFileDialog.DontUseNativeDialog
        pathfile, _ = QFileDialog.getOpenFileName(self, "Seleccionar archivo", "",
                                                  "Archivos de texto (*.dat);;Archivos de texto (*.txt);;Todos los archivos (*)",
                                                  options=opciones)
        basename = os.path.basename(pathfile)
        if basename.split('.')[-1] != "dat" or basename.split('.')[0][:-1] != "Track":
            msgBox = QMessageBox()
            msgBox.setText("No se puede cargar ese tipo de archivos.")
            msgBox.setStandardButtons(QMessageBox.Cancel)
            ret = msgBox.exec()
        else:
            # Cargamos el archivo seleccionado.
            data_base = LoadData(pathfile)
            data_dict = data_base.GetDataIonizations

            # Cargamos el Plot3DView en la pagina principal
            self.mpl_can = Plot3DView(data=data_dict)
            # la agregamos a la ventana principal
            self.central_widget.addWidget(self.mpl_can)
            self.central_widget.setCurrentWidget(self.mpl_can)

    def save_file(self):
        opciones = QFileDialog.Options()
        opciones |= QFileDialog.DontUseNativeDialog
        archivo, _ = QFileDialog.getSaveFileName(self, "Guardar archivo", "",
                                                  "Archivos de texto (*.txt);;Todos los archivos (*)",
                                                  options=opciones)
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
