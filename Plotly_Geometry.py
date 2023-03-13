import os
import sys
import re
import numpy as np
import plotly.graph_objects as go
from GeomView.main import MainWindow
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


# class Plotly_Geometry:
#
#     def __init__(self):
#         tuki=0
#
#     def cylinder(r, h, a=0, nt=100, nv =50):
#         """
#         parametrize the cylinder of radius r, height h, base point a
#         """
#         theta = np.linspace(0, 2*np.pi, nt)
#         v = np.linspace(a, a+h, nv )
#         theta, v = np.meshgrid(theta, v)
#         x = r*np.cos(theta)
#         y = r*np.sin(theta)
#         z = v
#         return x, y, z
#
#     def boundary_circle(r, h, nt=100):
#         """
#         r - boundary circle radius
#         h - height above xOy-plane where the circle is included
#         returns the circle parameterization
#         """
#         theta = np.linspace(0, 2*np.pi, nt)
#         x= r*np.cos(theta)
#         y = r*np.sin(theta)
#         z = h*np.ones(theta.shape)
#         return x, y, z
#     #
#     # def paralepipede():
#     #     go.Mesh3d(
#     #     # 8 vertices of a cube
#     #     x=[0.608, 0.608, 0.998, 0.998, 0.608, 0.608, 0.998, 0.998],
#     #     y=[0.091, 0.963, 0.963, 0.091, 0.091, 0.963, 0.963, 0.091],
#     #     z=[0.140, 0.140, 0.140, 0.140, 0.571, 0.571, 0.571, 0.571],
#     #
#     #     i = [7, 0, 0, 0, 4, 4, 6, 6, 4, 0, 3, 2],
#     #     j = [3, 4, 1, 2, 5, 6, 5, 2, 0, 1, 6, 3],
#     #     k = [0, 7, 2, 3, 6, 7, 1, 1, 5, 5, 7, 6],
#     #     opacity=0.6,
#     #     color='#DC143C',
#     #     flatshading = True
#     #     )
#     #     ])
#
#
# class GetDataBody:
#     def __init__(self):
#
#         mainWin = MainWindow()
#         self.num_bodies = len(mainWin.BodyList)
#
#         for num_b in range(self.num_bodies):
#             data_body = mainWin.BodyList[num_b]
#             self.__data_surfaces = data_body['Surfaces']
#             self.__GetBodyTypeWithSurfaces()
#
#     def __GetBodyTypeWithSurfaces(self):
#
#         surfaces = []
#         num_surfaces = len(self.__data_surfaces)
#         for num_s in range(num_surfaces):
#             surface = data_surfaces['S{}'.format(num_s)]
#             surfaces.append(surface['Type'])
#
#         if surfaces.count('Plane') == 2 and surfaces.count('Cylinder') == 1:
#             type_body = 'Cylinder'
#         elif surfaces.count('Plane') == 6:
#             type_body = 'Parallelepiped'
#
#         return type_body
#
#     def Cylinder():
#
#         num_surfaces = len(self.__data_surfaces)
#         for num_s in range(num_surfaces):
#
#             surface = data_surfaces['S{}'.format(num_s)]
#             type_surface = surface['Type']
#
#             pos_surface = surface['Position']
#             rot_surface = surface['Rotation']
#             sca_surface = surface['Scale']
#
#
#             if type_surface == 'Plane':
#
#             elif type_surface == 'Cylinder':
#                 r = np.linalg.norm(sca_surface)
#                 a1 =
#
#
#
#
#
# # ==============================================================================
# import itertools
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection
import itertools
from itertools import groupby
from MonteCarlo.Utils.utils import option_list, print_list_columns


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
                    new_string_list.append('IMPDET {} {} {} {} {}         [E-window, no. of bins, IPSF, IDCUT]\n'.format(emin,emax,nbins,'0','0'))
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

class CircleDetectors():

    def __init__(self, pathfolder):
        # # Instance Variable
        geom = LoadDataFileGeometry(pathfolder)

        materials = np.array([[1,'Cdte']])
        path = geom.path

        # Generamos la visualizacion
        plane = input('Ingrese el plano (XY,XZ,YZ):')
        nplanes = int(input('Ingrese número de detectores: '))
        radio = int(input('Ingrese el radio del cinturon: '))
        xdim= float(input('Ingrese las dimensiones "X" del detector: '))
        ydim= float(input('Ingrese las dimensiones "Y" del detector: '))
        zdim= float(input('Ingrese las dimensiones "Z" del detector: '))
        dimensions = [xdim,ydim,zdim]
        self.ViewPlanes(nplanes, plane, radio, dimensions)

        # Generamos el INPUT
        self.ConstructInput(nplanes, plane, materials, radio, dimensions, path)

    def PutTogetherPlanes(self, plane, alpha, radio, dimensions):

        xdim, ydim, zdim = dimensions

        # Definimos el plano
        if plane == 'XY':

            vplane = np.array([0,0,1])

            # Definir el angulo
            angle = alpha * np.pi/180
            # Definimos el vector normal al plano del paralepipedo
            vnorm_x = np.cos(angle)
            vnorm_y = np.sin(angle)
            vnorm_z = 0
            vp1 = np.array([vnorm_x, vnorm_y, vnorm_z])
            # vp1 = vp1/np.linalg.norm(vp1)

            # Definimos un vector perpendicular al plano y al plano del paralepipedo
            vp2 = np.cross(vplane,vp1)
            vp2 = vp2/np.linalg.norm(vp2)

            # Definimos otro vector perpendicular
            vp3 = np.cross(vp1,vp2)
            vp3 = vp3/np.linalg.norm(vp3)

            # Multiplicamos los vectores para que tengan las dimensiones del detectors
            vp1 = vp1 * zdim    # (cm)
            vp2 = vp2 * xdim    # (cm)
            vp3 = vp3 * ydim    # (cm)
            vp4 = vp1 + vp2
            vp5 = vp1 + vp3
            vp6 = vp2 + vp3
            vp7 = vp1 + vp2 + vp3
            vp8 = np.array([0.0,0.0,0.0])

            vp = np.array([vp1,vp2,vp3,vp4,vp5,vp6,vp7,vp8])
            # Traslada los vértices al centro de coordenadas
            vp_mean = np.mean(vp, axis=0)
            vp = vp - vp_mean

            vp = vp + vp1/np.linalg.norm(vp1) * radio
            # vp = vp - np.array([radio,radio,0])
            Z = vp

            # Los dos primeros --> X
            # Los dos segundos --> Y
            # Los dos ultimos --> Z

            # verts = [[Z[5],Z[1],Z[7],Z[2]], --> MIN X
            #          [Z[0],Z[3],Z[6],Z[4]], --> MAX X
            #          [Z[0],Z[7],Z[2],Z[4]], --> MAX Y
            #          [Z[3],Z[1],Z[5],Z[6]], --> MIN Y
            #          [Z[7],Z[1],Z[3],Z[0]], --> MAX Z
            #          [Z[5],Z[6],Z[4],Z[2]], --> MIN Z

            verts = [[Z[5],Z[1],Z[7],Z[2]],
                     [Z[6],Z[3],Z[0],Z[4]],
                     [Z[3],Z[1],Z[5],Z[6]],
                     [Z[0],Z[7],Z[2],Z[4]],
                     [Z[2],Z[4],Z[6],Z[5]],
                     [Z[7],Z[0],Z[3],Z[1]]]

            # fig = plt.figure()
            # ax = fig.add_subplot(111, projection='3d')
            #
            # ax.scatter3D(Z[0, 0], Z[0, 1], Z[0, 2], c='k')
            # ax.text(Z[0, 0], Z[0, 1], Z[0, 2], s='1')
            # ax.scatter3D(Z[1, 0], Z[1, 1], Z[1, 2], c='k')
            # ax.text(Z[1, 0], Z[1, 1], Z[1, 2], s='2')
            # ax.scatter3D(Z[2, 0], Z[2, 1], Z[2, 2], c='k')
            # ax.text(Z[2, 0], Z[2, 1], Z[2, 2], s='3')
            # ax.scatter3D(Z[3, 0], Z[3, 1], Z[3, 2], c='k')
            # ax.text(Z[3, 0], Z[3, 1], Z[3, 2], s='4')
            # ax.scatter3D(Z[4, 0], Z[4, 1], Z[4, 2], c='k')
            # ax.text(Z[4, 0], Z[4, 1], Z[4, 2], s='5')
            # ax.scatter3D(Z[5, 0], Z[5, 1], Z[5, 2], c='k')
            # ax.text(Z[5, 0], Z[5, 1], Z[5, 2], s='6')
            # ax.scatter3D(Z[6, 0], Z[6, 1], Z[6, 2], c='k')
            # ax.text(Z[6, 0], Z[6, 1], Z[6, 2], s='7')
            # ax.scatter3D(Z[7, 0], Z[7, 1], Z[7, 2], c='k')
            # ax.text(Z[7, 0], Z[7, 1], Z[7, 2], s='8')
            #
            # bbox = Poly3DCollection(verts,
            # facecolors='red', linewidths=1, edgecolors='k', alpha=.1)
            # bbox._facecolors2d= bbox._facecolor3d
            # bbox._edgecolors2d = bbox._edgecolor3d
            # ax.add_collection3d(bbox)
            #
            # ax.set_xlabel('Eje X [cm]')
            # ax.set_ylabel('Eje Y [cm]')
            # ax.set_zlabel('Eje Z [cm]')
            #
            # plt.show()

            return Z, verts

        if plane == 'XZ':

            vplane = np.array([0,1,0])

            # Definir el angulo
            angle = alpha * np.pi/180
            # Definimos el vector normal al plano del paralepipedo
            vnorm_x = np.cos(angle)
            vnorm_y = 0
            vnorm_z = np.sin(angle)
            vp1 = np.array([vnorm_x, vnorm_y, vnorm_z])
            # vp1 = vp1/np.linalg.norm(vp1)

            # Definimos un vector perpendicular al plano y al plano del paralepipedo
            vp2 = np.cross(vplane,vp1)
            vp2 = vp2/np.linalg.norm(vp2)

            # Definimos otro vector perpendicular
            vp3 = np.cross(vp1,vp2)
            vp3 = vp3/np.linalg.norm(vp3)

            # Multiplicamos los vectores para que tengan las dimensiones del detectors
            vp1 = vp1 * ydim    # (cm)
            vp2 = vp2 * xdim    # (cm)
            vp3 = vp3 * zdim    # (cm)
            vp4 = vp1 + vp2
            vp5 = vp1 + vp3
            vp6 = vp2 + vp3
            vp7 = vp1 + vp2 + vp3
            vp8 = np.array([0.0,0.0,0.0])

            vp = np.array([vp1,vp2,vp3,vp4,vp5,vp6,vp7,vp8])
            # Traslada los vértices al centro de coordenadas
            vp_mean = np.mean(vp, axis=0)
            vp = vp - vp_mean

            vp = vp + vp1/np.linalg.norm(vp1) * radio
            # vp = vp - np.array([radio,radio,0])
            Z = vp

            # Los dos primeros --> X
            # Los dos segundos --> Y
            # Los dos ultimos --> Z

            # verts = [[Z[5],Z[1],Z[7],Z[2]], --> MIN X
            #          [Z[0],Z[3],Z[6],Z[4]], --> MAX X
            #          [Z[0],Z[7],Z[2],Z[4]], --> MAX Y
            #          [Z[3],Z[1],Z[5],Z[6]], --> MIN Y
            #          [Z[7],Z[1],Z[3],Z[0]], --> MAX Z
            #          [Z[5],Z[6],Z[4],Z[2]], --> MIN Z

            verts = [[Z[5],Z[1],Z[7],Z[2]],
                     [Z[6],Z[3],Z[0],Z[4]],
                     [Z[3],Z[1],Z[5],Z[6]],
                     [Z[0],Z[7],Z[2],Z[4]],
                     [Z[2],Z[4],Z[6],Z[5]],
                     [Z[7],Z[0],Z[3],Z[1]]]

            # fig = plt.figure()
            # ax = fig.add_subplot(111, projection='3d')
            #
            # ax.scatter3D(Z[0, 0], Z[0, 1], Z[0, 2], c='k')
            # ax.text(Z[0, 0], Z[0, 1], Z[0, 2], s='1')
            # ax.scatter3D(Z[1, 0], Z[1, 1], Z[1, 2], c='k')
            # ax.text(Z[1, 0], Z[1, 1], Z[1, 2], s='2')
            # ax.scatter3D(Z[2, 0], Z[2, 1], Z[2, 2], c='k')
            # ax.text(Z[2, 0], Z[2, 1], Z[2, 2], s='3')
            # ax.scatter3D(Z[3, 0], Z[3, 1], Z[3, 2], c='k')
            # ax.text(Z[3, 0], Z[3, 1], Z[3, 2], s='4')
            # ax.scatter3D(Z[4, 0], Z[4, 1], Z[4, 2], c='k')
            # ax.text(Z[4, 0], Z[4, 1], Z[4, 2], s='5')
            # ax.scatter3D(Z[5, 0], Z[5, 1], Z[5, 2], c='k')
            # ax.text(Z[5, 0], Z[5, 1], Z[5, 2], s='6')
            # ax.scatter3D(Z[6, 0], Z[6, 1], Z[6, 2], c='k')
            # ax.text(Z[6, 0], Z[6, 1], Z[6, 2], s='7')
            # ax.scatter3D(Z[7, 0], Z[7, 1], Z[7, 2], c='k')
            # ax.text(Z[7, 0], Z[7, 1], Z[7, 2], s='8')
            #
            # bbox = Poly3DCollection(verts,
            # facecolors='red', linewidths=1, edgecolors='k', alpha=.1)
            # bbox._facecolors2d= bbox._facecolor3d
            # bbox._edgecolors2d = bbox._edgecolor3d
            # ax.add_collection3d(bbox)
            #
            # ax.set_xlabel('Eje X [cm]')
            # ax.set_ylabel('Eje Y [cm]')
            # ax.set_zlabel('Eje Z [cm]')
            #
            # plt.show()

            return Z, verts

        if plane == 'YZ':

            vplane = np.array([1,0,0])

            # Definir el angulo
            angle = alpha * np.pi/180
            # Definimos el vector normal al plano del paralepipedo
            vnorm_x = 0
            vnorm_y = np.cos(angle)
            vnorm_z = np.sin(angle)
            vp1 = np.array([vnorm_x, vnorm_y, vnorm_z])
            # vp1 = vp1/np.linalg.norm(vp1)

            # Definimos un vector perpendicular al plano y al plano del paralepipedo
            vp2 = np.cross(vplane,vp1)
            vp2 = vp2/np.linalg.norm(vp2)

            # Definimos otro vector perpendicular
            vp3 = np.cross(vp1,vp2)
            vp3 = vp3/np.linalg.norm(vp3)

            # Multiplicamos los vectores para que tengan las dimensiones del detectors
            vp1 = vp1 * ydim    # (cm)
            vp2 = vp2 * xdim    # (cm)
            vp3 = vp3 * zdim    # (cm)
            vp4 = vp1 + vp2
            vp5 = vp1 + vp3
            vp6 = vp2 + vp3
            vp7 = vp1 + vp2 + vp3
            vp8 = np.array([0.0,0.0,0.0])

            vp = np.array([vp1,vp2,vp3,vp4,vp5,vp6,vp7,vp8])
            # Traslada los vértices al centro de coordenadas
            vp_mean = np.mean(vp, axis=0)
            vp = vp - vp_mean

            vp = vp + vp1/np.linalg.norm(vp1) * radio
            # vp = vp - np.array([radio,radio,0])
            Z = vp

            # Los dos primeros --> X
            # Los dos segundos --> Y
            # Los dos ultimos --> Z

            # verts = [[Z[5],Z[1],Z[7],Z[2]], --> MIN X
            #          [Z[0],Z[3],Z[6],Z[4]], --> MAX X
            #          [Z[0],Z[7],Z[2],Z[4]], --> MAX Y
            #          [Z[3],Z[1],Z[5],Z[6]], --> MIN Y
            #          [Z[7],Z[1],Z[3],Z[0]], --> MAX Z
            #          [Z[5],Z[6],Z[4],Z[2]], --> MIN Z

            verts = [[Z[5],Z[1],Z[7],Z[2]],
                     [Z[6],Z[3],Z[0],Z[4]],
                     [Z[3],Z[1],Z[5],Z[6]],
                     [Z[0],Z[7],Z[2],Z[4]],
                     [Z[2],Z[4],Z[6],Z[5]],
                     [Z[7],Z[0],Z[3],Z[1]]]

            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')

            ax.scatter3D(Z[0, 0], Z[0, 1], Z[0, 2], c='k')
            ax.text(Z[0, 0], Z[0, 1], Z[0, 2], s='1')
            ax.scatter3D(Z[1, 0], Z[1, 1], Z[1, 2], c='k')
            ax.text(Z[1, 0], Z[1, 1], Z[1, 2], s='2')
            ax.scatter3D(Z[2, 0], Z[2, 1], Z[2, 2], c='k')
            ax.text(Z[2, 0], Z[2, 1], Z[2, 2], s='3')
            ax.scatter3D(Z[3, 0], Z[3, 1], Z[3, 2], c='k')
            ax.text(Z[3, 0], Z[3, 1], Z[3, 2], s='4')
            ax.scatter3D(Z[4, 0], Z[4, 1], Z[4, 2], c='k')
            ax.text(Z[4, 0], Z[4, 1], Z[4, 2], s='5')
            ax.scatter3D(Z[5, 0], Z[5, 1], Z[5, 2], c='k')
            ax.text(Z[5, 0], Z[5, 1], Z[5, 2], s='6')
            ax.scatter3D(Z[6, 0], Z[6, 1], Z[6, 2], c='k')
            ax.text(Z[6, 0], Z[6, 1], Z[6, 2], s='7')
            ax.scatter3D(Z[7, 0], Z[7, 1], Z[7, 2], c='k')
            ax.text(Z[7, 0], Z[7, 1], Z[7, 2], s='8')

            bbox = Poly3DCollection(verts,
            facecolors='red', linewidths=1, edgecolors='k', alpha=.1)
            bbox._facecolors2d= bbox._facecolor3d
            bbox._edgecolors2d = bbox._edgecolor3d
            ax.add_collection3d(bbox)

            ax.set_xlabel('Eje X [cm]')
            ax.set_ylabel('Eje Y [cm]')
            ax.set_zlabel('Eje Z [cm]')

            plt.show()

            return Z, verts

    def ViewPlanes(self, nplanes, plane, radio, dimensions):

        angle = 360/nplanes
        list_bodys = []
        for n in range(1,nplanes):

            Z, verts =  self.PutTogetherPlanes(plane = plane, alpha = angle*n, radio=radio, dimensions=dimensions)

            x = Z[:,0]
            y = Z[:,1]
            z = Z[:,2]
            i= [7, 0, 0, 0, 4, 4, 6, 1, 4, 0, 3, 6]
            j= [3, 4, 1, 2, 5, 6, 5, 2, 0, 1, 6, 3]
            k= [0, 7, 2, 3, 6, 7, 1, 6, 5, 5, 7, 2]


            list_bodys.append(go.Mesh3d(x=x, y=y, z=z, alphahull = 0,
                                        # i=i, j=j, k=k,
                                        opacity=0.5,
                                        color='blue'))

        # Datos para el eje x
        list_bodys.append(go.Scatter3d(x=[0, 6], y=[0, 0], z=[0, 0], mode='lines', name='X Axis', line=dict(color='red', width=5)))

        # Datos para el eje y
        list_bodys.append(go.Scatter3d(x=[0, 0], y=[0, 6], z=[0, 0], mode='lines', name='Y Axis', line=dict(color='green', width=5)))

        # Datos para el eje z
        list_bodys.append(go.Scatter3d(x=[0, 0], y=[0, 0], z=[0, 6], mode='lines', name='Z Axis', line=dict(color='blue', width=5)))


        layout = go.Layout(scene_xaxis_visible=False, scene_yaxis_visible=False, scene_zaxis_visible=False)
        # layout = go.Layout(scene_xaxis_visible=True, scene_yaxis_visible=True, scene_zaxis_visible=True,
        #                   scene = dict(xaxis=dict(range=[-10,10]),
        #                                yaxis=dict(range=[-10,10]),
        #                                zaxis=dict(range=[-10,10])))

        fig = go.Figure(data = list_bodys, layout = layout)
        # fig.update_layout(scene_camera_eye_z= 0.55)
        fig.layout.scene.camera.projection.type = "orthographic" #commenting this line you get a fig with perspective proj

        fig.show()

    # Crear INPUT con el cinturon de detectores
    def converttotext(self, c):
        if c > 0:
            num_str = '{:.7f}'.format(c)
            numtxt = len('0.000000000000000')
            format = 'E+00'
            if len(num_str) != numtxt:
                cantidad = numtxt - len(num_str)
                for i in range(cantidad):
                    num_str = num_str + '0'
            num_str = '+' + num_str + format
            return num_str
        elif c < 0:
            num_str = '{:.7f}'.format(c)
            numtxt = len('0.000000000000000')
            format = 'E+00'
            if len(num_str) != numtxt:
                cantidad = numtxt - len(num_str)
                for i in range(cantidad+1):
                    num_str = num_str + '0'
            num_str = num_str + format
            return num_str
        else:
            num_str = '{:.7f}'.format(c)
            numtxt = len('0.000000000000000')
            format = 'E+00'
            if len(num_str) != numtxt:
                cantidad = numtxt - len(num_str)
                for i in range(cantidad):
                    num_str = num_str + '0'
            num_str = '+' + num_str + format
            return num_str

    def GetPlaneCoefficient(self,p1,p2,p3,p4):

        # Encontramos dos vectores del plano.
        v1 = p1 - p2
        v2 = p3 - p2
        v3 = p4 - p2
        # Calculamos el vector normal del plano
        normal = np.cross(v2,v3)
        normal /= np.linalg.norm(normal)

        # Calcular la distancia del plano al origen
        d = -np.dot(normal,p1)

        a = normal[0]
        b = normal[1]
        c = normal[2]

        return a,b,c,d

    def ConstructInput(self, nplanes, plane, materials, radio, dimensions, path):

        # # Creamos una lista que contenga el script de INPUT
        string_list = []

        # (1) Agregamos el titulo al INPUT -----------------------------------------

        title = ["XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX\n",
                 "Detector XR --> Definimos las superficies limitantes.\n",
                 "Materiales:\n",
        	     "  - 0 -> Vacio -> Hueco\n",
                 "  - 1 -> {} -> Detector\n".format(materials[0,1]),
                 "\n",
                 "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX\n",
                 "0000000000000000000000000000000000000000000000000000000000000000\n"]

        for line in title:
            string_list.append(line)

        # (2) Creamos las superficies y los bodys para los detectores---------------

        # Definimos unidad angular de partición
        angle = 360/nplanes
        j=0
        for n in range(1,nplanes):

            Z, verts =  self.PutTogetherPlanes(plane=plane, alpha = n*angle, radio=radio, dimensions=dimensions)

            i_detector = ["C\n",
                          "C  **** Detector {}\n".format(n),
                          "C\n",
                          ]

            for line in i_detector:
                string_list.append(line)

            for i,vert in enumerate(verts):
                p1,p2,p3,p4 = vert
                a,b,c,d = self.GetPlaneCoefficient(p1,p2,p3,p4)
                print(a,b,c,d)
                # Corregimos un error de escritura
                if a==-0.0:
                    a=0.0
                if b==-0.0:
                    b=0.0
                if c==-0.0:
                    c=0.0
                if d==-0.0:
                    d=0.0

                # Agregamos el titulo de surface
                if n+i+j < 10:
                    string_list.append("SURFACE (   {})   Plano limitante \n".format(n+i+j))
                if n+i+j < 100 and n+i+j >= 10:
                    string_list.append("SURFACE (  {})   Plano limitante \n".format(n+i+j))
                if n+i+j >= 100:
                    string_list.append("SURFACE ( {})   Plano limitante \n".format(n+i+j))

                if a == 0.0 and b != 0.0 and c != 0.0:
                    string_list.append("INDICES=( 0, 0, 0, 0, 0)\n")
                    string_list.append("     AY=({},   0)\n".format(self.converttotext(b)))
                    string_list.append("     AZ=({},   0)\n".format(self.converttotext(c)))
                    string_list.append("     A0=({},   0)\n".format(self.converttotext(d)))
                elif a != 0.0 and b == 0.0 and c != 0.0:
                    string_list.append("INDICES=( 0, 0, 0, 0, 0)\n")
                    string_list.append("     AX=({},   0)\n".format(self.converttotext(a)))
                    string_list.append("     AZ=({},   0)\n".format(self.converttotext(c)))
                    string_list.append("     A0=({},   0)\n".format(self.converttotext(d)))
                elif a != 0.0 and b != 0.0 and c == 0.0:
                    string_list.append("INDICES=( 0, 0, 0, 0, 0)\n")
                    string_list.append("     AX=({},   0)\n".format(self.converttotext(a)))
                    string_list.append("     AY=({},   0)\n".format(self.converttotext(b)))
                    string_list.append("     A0=({},   0)\n".format(self.converttotext(d)))
                elif a == 0.0 and b == 0.0 and c != 0.0:
                    string_list.append("INDICES=( 0, 0, 0, 0, 0)\n")
                    string_list.append("     AZ=({},   0)\n".format(self.converttotext(c)))
                    string_list.append("     A0=({},   0)\n".format(self.converttotext(d)))
                elif a != 0.0 and b == 0.0 and c == 0.0:
                    string_list.append("INDICES=( 0, 0, 0, 0, 0)\n")
                    string_list.append("     AX=({},   0)\n".format(self.converttotext(a)))
                    string_list.append("     A0=({},   0)\n".format(self.converttotext(d)))
                elif a == 0.0 and b != 0.0 and c == 0.0:
                    string_list.append("INDICES=( 0, 0, 0, 0, 0)\n")
                    string_list.append("     AY=({},   0)\n".format(self.converttotext(b)))
                    string_list.append("     A0=({},   0)\n".format(self.converttotext(d)))

                string_list.append("0000000000000000000000000000000000000000000000000000000000000000\n")


            if n < 10:
                string_list.append("BODY    (   {})  Detector {} - Prism\n".format(n,n))
            elif n>=10 and n<100:
                string_list.append("BODY    (  {})  Detector {} - Prism\n".format(n,n))
            elif n>=100:
                string_list.append("BODY    ( {})  Detector {} - Prism\n".format(n,n))

            string_list.append("MATERIAL(   {})\n".format(materials[0,0]))

            if n+0+j < 10:
                string_list.append("SURFACE (   {}), SIDE POINTER=(-1)\n".format(n+0+j))
            elif n+0+j>=10 and n+0+j<100:
                string_list.append("SURFACE (  {}), SIDE POINTER=(-1)\n".format(n+0+j))
            elif n+0+j>=100:
                string_list.append("SURFACE ( {}), SIDE POINTER=(-1)\n".format(n+0+j))

            if n+1+j < 10:
                string_list.append("SURFACE (   {}), SIDE POINTER=(+1)\n".format(n+1+j))
            elif n+1+j>=10 and n+1+j<100:
                string_list.append("SURFACE (  {}), SIDE POINTER=(+1)\n".format(n+1+j))
            elif n+1+j>=100:
                string_list.append("SURFACE ( {}), SIDE POINTER=(+1)\n".format(n+1+j))

            if n+2+j < 10:
                string_list.append("SURFACE (   {}), SIDE POINTER=(-1)\n".format(n+2+j))
            elif n+2+j>=10 and n+2+j<100:
                string_list.append("SURFACE (  {}), SIDE POINTER=(-1)\n".format(n+2+j))
            elif n+2+j>=100:
                string_list.append("SURFACE ( {}), SIDE POINTER=(-1)\n".format(n+2+j))

            if n+3+j < 10:
                string_list.append("SURFACE (   {}), SIDE POINTER=(+1)\n".format(n+3+j))
            elif n+3+j>=10 and n+3+j<100:
                string_list.append("SURFACE (  {}), SIDE POINTER=(+1)\n".format(n+3+j))
            elif n+3+j>=100:
                string_list.append("SURFACE ( {}), SIDE POINTER=(+1)\n".format(n+3+j))

            if n+4+j < 10:
                string_list.append("SURFACE (   {}), SIDE POINTER=(-1)\n".format(n+4+j))
            elif n+4+j>=10 and n+4+j<100:
                string_list.append("SURFACE (  {}), SIDE POINTER=(-1)\n".format(n+4+j))
            elif n+4+j>=100:
                string_list.append("SURFACE ( {}), SIDE POINTER=(-1)\n".format(n+4+j))

            if n+5+j < 10:
                string_list.append("SURFACE (   {}), SIDE POINTER=(+1)\n".format(n+5+j))
            elif n+5+j>=10 and n+5+j<100:
                string_list.append("SURFACE (  {}), SIDE POINTER=(+1)\n".format(n+5+j))
            elif n+5+j>=100:
                string_list.append("SURFACE ( {}), SIDE POINTER=(+1)\n".format(n+5+j))

            string_list.append("0000000000000000000000000000000000000000000000000000000000000000\n")
            j += 5

        string_list.append("END      0000000000000000000000000000000000000000000000000000000")

        self.geometryFile = string_list

        pathfile = os.path.join('D:\\',*path.split('\\')[1:-1], 'detector_simulated.geo')

        my_file = open('{}'.format(pathfile),'w')
        new_file_contents = "".join(string_list)
        my_file.write(new_file_contents)
        my_file.close()
    # ----

# # PRIMERA FORMA
# pathfolder = "D:\Proyectos_Investigacion\Proyectos_de_Doctorado\Proyectos\SimulationXF_Detectors\Code\RUN\penmain_2018"
# cdetectors = CircleDetectors(pathfolder)
#

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

    result = []
    for style in style_list:
        if style.lower() == style_list:
            result.insert(0, style)
        else:
            result.append(style)
    return result

class Plot3DView(QWidget):

    def __init__(self):
        super(Plot3DView, self).__init__()

        self.__Layaout_Principal()

        layout_DataPlot = QHBoxLayout()
        layout_DataPlot.addLayout(self.llayout, 14)
        layout_DataPlot.addLayout(self.cllayout, 84)
        self.setLayout(layout_DataPlot)

    # ========= LAYAUOT PRINCIPAL =========

    def __Layaout_Principal(self):

        # --------------------------------------------------
        # # Panel IZQUIERDO - Definición de configuraciones

        # (1) Creamos y definimos caracteristicas de los widgets

        # # Opciones para ver datos procesados
        self._plane = QComboBox()
        init_widget(self._plane, "styleComboBox")
        self._plane.addItems(style_names(list_name='plane'))

        # # Opciones para ver datos procesados
        self._materials = QComboBox()
        init_widget(self._materials, "styleComboBox")
        self._materials.addItems(style_names(list_name='materials'))

        # Elige una particula para visualizar
        self._nplane = QDoubleSpinBox()
        self._nplane.setPrefix("")
        self._nplane.setValue(0)
        init_widget(self._nplane, "ndetect")

        # Elige una particula para visualizar
        self._radio = QDoubleSpinBox()
        self._radio.setPrefix("")
        self._radio.setValue(0)
        init_widget(self._radio, "radio")

        self._translate = QDoubleSpinBox()
        self._translate.setPrefix("")
        self._translate.setValue(0)
        self._translate.setRange(-100, 100)
        init_widget(self._translate, "translate")

        self._xdim = QDoubleSpinBox()
        self._xdim.setPrefix("X: ")
        self._xdim.setValue(0)
        self._xdim.setRange(-100, 100)
        init_widget(self._xdim, "xdim")

        self._ydim = QDoubleSpinBox()
        self._ydim.setPrefix("Y: ")
        self._ydim.setValue(0)
        self._ydim.setRange(-100, 100)
        init_widget(self._ydim, "ydim")

        self._zdim = QDoubleSpinBox()
        self._zdim.setPrefix("Z: ")
        self._zdim.setValue(0)
        self._zdim.setRange(-100, 100)
        init_widget(self._zdim, "zdim")

        self._xs = QDoubleSpinBox()
        self._xs.setPrefix("X: ")
        self._xs.setValue(0)
        self._xs.setRange(-100, 100)
        init_widget(self._xs, "xs")

        self._ys = QDoubleSpinBox()
        self._ys.setPrefix("Y: ")
        self._ys.setValue(0)
        self._ys.setRange(-100, 100)
        init_widget(self._ys, "ys")

        self._zs = QDoubleSpinBox()
        self._zs.setPrefix("Z: ")
        self._zs.setValue(0)
        self._zs.setRange(-100, 100)
        init_widget(self._zs, "zs")

        # Boton de ejecución para visualizar el plot elegido
        self.button_view = QPushButton("View")
        init_widget(self.button_view, "view_label")

        self.button_text = QPushButton("Generar Geometría")
        init_widget(self.button_text, "generar_label")

        # -----
        self._emin = QDoubleSpinBox()
        self._emin.setPrefix("Energía mínima: ")
        self._emin.setValue(0)
        self._emin.setRange(1000, 1000000000)
        init_widget(self._emin, "emin")

        self._emax = QDoubleSpinBox()
        self._emax.setPrefix("Energía máxima: ")
        self._emax.setValue(0)
        self._emax.setRange(1000, 1000000000)
        init_widget(self._emax, "emax")

        self._nbins = QDoubleSpinBox()
        self._nbins.setPrefix("Num Bins: ")
        self._nbins.setValue(1)
        self._nbins.setRange(1, 800)
        init_widget(self._nbins, "nbins")

        self._nprim = QDoubleSpinBox()
        self._nprim.setPrefix("Primarios: ")
        self._nprim.setValue(0)
        self._nprim.setRange(1, 1000000000)
        init_widget(self._nprim, "nprimarios")

        self.button_input = QPushButton("Generar Input")
        init_widget(self.button_input, "input_label")

        # -----

        # (2) Agregamos widgets al panel
        self.llayout = QVBoxLayout()
        self.llayout.setContentsMargins(1, 1, 1, 1)

        self.label1 = QLabel("CONFIGURACIÓN VISUAL DE ANILLOS DETECTORES")
        self.label1.setStyleSheet("border: 2px solid gray; position: center;")
        self.llayout.addWidget(self.label1)

        self.llayout.addWidget(QLabel("Plano:"))
        self.llayout.addWidget(self._plane)

        self.llayout.addWidget(QLabel("Número de detectores:"))
        self.llayout.addWidget(self._nplane)

        self.llayout.addWidget(QLabel("Material:"))
        self.llayout.addWidget(self._materials)

        self.llayout.addWidget(QLabel("Radio del cinturon:"))
        self.llayout.addWidget(self._radio)

        self.llayout.addWidget(QLabel("Dimensiones de los detectores:"))
        self.horizontalLayou1 = QHBoxLayout()
        self.horizontalLayou1.addWidget(self._xdim)
        self.horizontalLayou1.addWidget(self._ydim)
        self.horizontalLayou1.addWidget(self._zdim)
        self.llayout.addLayout(self.horizontalLayou1)

        self.llayout.addWidget(QLabel("Trasladar detectores:"))
        self.llayout.addWidget(self._translate)

        self.llayout.addWidget(QLabel("Posición de la fuente:"))
        self.horizontalLayou2 = QHBoxLayout()
        self.horizontalLayou2.addWidget(self._xs)
        self.horizontalLayou2.addWidget(self._ys)
        self.horizontalLayou2.addWidget(self._zs)
        self.llayout.addLayout(self.horizontalLayou2)

        self.llayout.addWidget(QLabel("Visualizar geometría"))
        self.llayout.addWidget(self.button_view)
        # self.llayout.addWidget(QLabel(""))

        # ---
        self.label2 = QLabel("             ARCHIVO DE GEOMETRIA-PENELOPE")
        self.label2.setStyleSheet("border: 2px solid gray; position: center;")
        self.llayout.addWidget(self.label2)
        self.llayout.addWidget(self.button_text)
        # self.llayout.addWidget(QLabel(""))

        # ---
        self.label3 = QLabel("               ARCHIVO DE INPUT-PENELOPE")
        self.label3.setStyleSheet("border: 2px solid gray; position: center;")
        self.llayout.addWidget(self.label3)
        self.llayout.addWidget(self._emin)
        self.llayout.addWidget(self._emax)
        self.llayout.addWidget(self._nbins)
        self.llayout.addWidget(self._nprim)
        self.llayout.addWidget(self.button_input)

        self.llayout.addStretch()


        # (3) Agregamos las conexiones
        self.button_view.clicked.connect(self.__ViewPlanes)
        self.button_text.clicked.connect(self.__ConstructGeometry)
        self.button_input.clicked.connect(self.__ConstructInput)

        # --------------------------------------------------
        # # Panel DERECHO - Definición de configuraciones

        self.cllayout = QVBoxLayout()
        self.cllayout.setContentsMargins(1, 1, 1, 1)
        self.browser = QWebEngineView(self)
        self.cllayout.addWidget(self.browser)

    # ========= FUNCIONES DE CALCULO ==========

    def __PutTogetherPlanes(self, plane, alpha, radio, dimensions):

        pos_source = np.array([float(self._xs.value()), float(self._ys.value()), float(self._zs.value())])
        translate = int(self._translate.value())
        xdim, ydim, zdim = dimensions

        # Definimos el plano
        if plane == 'XY':

            vplane = np.array([0,0,1])

            # Definir el angulo
            angle_source = np.arctan2(pos_source[1],pos_source[0])
            # angle_source = np.degrees(angle_source) % 360.0
            if pos_source[2] == 0.0:
                angle = alpha * np.pi/180 + angle_source
            else:
                angle = alpha * np.pi/180
            # Definimos el vector normal al plano del paralepipedo
            vnorm_x = np.cos(angle)
            vnorm_y = np.sin(angle)
            vnorm_z = 0
            vp1 = np.array([vnorm_x, vnorm_y, vnorm_z])
            # vp1 = vp1/np.linalg.norm(vp1)

            # Definimos un vector perpendicular al plano y al plano del paralepipedo
            vp2 = np.cross(vplane,vp1)
            vp2 = vp2/np.linalg.norm(vp2)

            # Definimos otro vector perpendicular
            vp3 = np.cross(vp1,vp2)
            vp3 = vp3/np.linalg.norm(vp3)

            # Multiplicamos los vectores para que tengan las dimensiones del detectors
            vp1 = vp1 * zdim    # (cm)
            vp2 = vp2 * xdim    # (cm)
            vp3 = vp3 * ydim    # (cm)
            vp4 = vp1 + vp2
            vp5 = vp1 + vp3
            vp6 = vp2 + vp3
            vp7 = vp1 + vp2 + vp3
            vp8 = np.array([0.0,0.0,0.0])

            vp = np.array([vp1,vp2,vp3,vp4,vp5,vp6,vp7,vp8])
            # Traslada los vértices al centro de coordenadas
            vp_mean = np.mean(vp, axis=0)
            vp = vp - vp_mean

            # Corremos los detectores al valor del radio
            vp = vp + vp1/np.linalg.norm(vp1) * radio

            # Trasladamos en la dirección Z
            vp = vp + np.array([0,0,translate])
            # vp = vp - np.array([radio,radio,0])
            Z = vp

            # Los dos primeros --> X
            # Los dos segundos --> Y
            # Los dos ultimos --> Z

            # verts = [[Z[5],Z[1],Z[7],Z[2]], --> MIN X
            #          [Z[0],Z[3],Z[6],Z[4]], --> MAX X
            #          [Z[0],Z[7],Z[2],Z[4]], --> MAX Y
            #          [Z[3],Z[1],Z[5],Z[6]], --> MIN Y
            #          [Z[7],Z[1],Z[3],Z[0]], --> MAX Z
            #          [Z[5],Z[6],Z[4],Z[2]], --> MIN Z

            verts = [[Z[5],Z[1],Z[7],Z[2]],
                     [Z[6],Z[3],Z[0],Z[4]],
                     [Z[3],Z[1],Z[5],Z[6]],
                     [Z[0],Z[7],Z[2],Z[4]],
                     [Z[2],Z[4],Z[6],Z[5]],
                     [Z[7],Z[0],Z[3],Z[1]]]

            # fig = plt.figure()
            # ax = fig.add_subplot(111, projection='3d')
            #
            # ax.scatter3D(Z[0, 0], Z[0, 1], Z[0, 2], c='k')
            # ax.text(Z[0, 0], Z[0, 1], Z[0, 2], s='1')
            # ax.scatter3D(Z[1, 0], Z[1, 1], Z[1, 2], c='k')
            # ax.text(Z[1, 0], Z[1, 1], Z[1, 2], s='2')
            # ax.scatter3D(Z[2, 0], Z[2, 1], Z[2, 2], c='k')
            # ax.text(Z[2, 0], Z[2, 1], Z[2, 2], s='3')
            # ax.scatter3D(Z[3, 0], Z[3, 1], Z[3, 2], c='k')
            # ax.text(Z[3, 0], Z[3, 1], Z[3, 2], s='4')
            # ax.scatter3D(Z[4, 0], Z[4, 1], Z[4, 2], c='k')
            # ax.text(Z[4, 0], Z[4, 1], Z[4, 2], s='5')
            # ax.scatter3D(Z[5, 0], Z[5, 1], Z[5, 2], c='k')
            # ax.text(Z[5, 0], Z[5, 1], Z[5, 2], s='6')
            # ax.scatter3D(Z[6, 0], Z[6, 1], Z[6, 2], c='k')
            # ax.text(Z[6, 0], Z[6, 1], Z[6, 2], s='7')
            # ax.scatter3D(Z[7, 0], Z[7, 1], Z[7, 2], c='k')
            # ax.text(Z[7, 0], Z[7, 1], Z[7, 2], s='8')
            #
            # bbox = Poly3DCollection(verts,
            # facecolors='red', linewidths=1, edgecolors='k', alpha=.1)
            # bbox._facecolors2d= bbox._facecolor3d
            # bbox._edgecolors2d = bbox._edgecolor3d
            # ax.add_collection3d(bbox)
            #
            # ax.set_xlabel('Eje X [cm]')
            # ax.set_ylabel('Eje Y [cm]')
            # ax.set_zlabel('Eje Z [cm]')
            #
            # plt.show()

            return Z, verts

        if plane == 'XZ':

            vplane = np.array([0,1,0])

            # Definir el angulo
            angle = alpha * np.pi/180
            # Definimos el vector normal al plano del paralepipedo
            vnorm_x = np.cos(angle)
            vnorm_y = 0
            vnorm_z = np.sin(angle)
            vp1 = np.array([vnorm_x, vnorm_y, vnorm_z])
            # vp1 = vp1/np.linalg.norm(vp1)

            # Definimos un vector perpendicular al plano y al plano del paralepipedo
            vp2 = np.cross(vplane,vp1)
            vp2 = vp2/np.linalg.norm(vp2)

            # Definimos otro vector perpendicular
            vp3 = np.cross(vp1,vp2)
            vp3 = vp3/np.linalg.norm(vp3)

            # Multiplicamos los vectores para que tengan las dimensiones del detectors
            vp1 = vp1 * ydim    # (cm)
            vp2 = vp2 * xdim    # (cm)
            vp3 = vp3 * zdim    # (cm)
            vp4 = vp1 + vp2
            vp5 = vp1 + vp3
            vp6 = vp2 + vp3
            vp7 = vp1 + vp2 + vp3
            vp8 = np.array([0.0,0.0,0.0])

            vp = np.array([vp1,vp2,vp3,vp4,vp5,vp6,vp7,vp8])
            # Traslada los vértices al centro de coordenadas
            vp_mean = np.mean(vp, axis=0)
            vp = vp - vp_mean

            vp = vp + vp1/np.linalg.norm(vp1) * radio
            # vp = vp - np.array([radio,radio,0])
            Z = vp

            # Los dos primeros --> X
            # Los dos segundos --> Y
            # Los dos ultimos --> Z

            # verts = [[Z[5],Z[1],Z[7],Z[2]], --> MIN X
            #          [Z[0],Z[3],Z[6],Z[4]], --> MAX X
            #          [Z[0],Z[7],Z[2],Z[4]], --> MAX Y
            #          [Z[3],Z[1],Z[5],Z[6]], --> MIN Y
            #          [Z[7],Z[1],Z[3],Z[0]], --> MAX Z
            #          [Z[5],Z[6],Z[4],Z[2]], --> MIN Z

            verts = [[Z[5],Z[1],Z[7],Z[2]],
                     [Z[6],Z[3],Z[0],Z[4]],
                     [Z[3],Z[1],Z[5],Z[6]],
                     [Z[0],Z[7],Z[2],Z[4]],
                     [Z[2],Z[4],Z[6],Z[5]],
                     [Z[7],Z[0],Z[3],Z[1]]]

            # fig = plt.figure()
            # ax = fig.add_subplot(111, projection='3d')
            #
            # ax.scatter3D(Z[0, 0], Z[0, 1], Z[0, 2], c='k')
            # ax.text(Z[0, 0], Z[0, 1], Z[0, 2], s='1')
            # ax.scatter3D(Z[1, 0], Z[1, 1], Z[1, 2], c='k')
            # ax.text(Z[1, 0], Z[1, 1], Z[1, 2], s='2')
            # ax.scatter3D(Z[2, 0], Z[2, 1], Z[2, 2], c='k')
            # ax.text(Z[2, 0], Z[2, 1], Z[2, 2], s='3')
            # ax.scatter3D(Z[3, 0], Z[3, 1], Z[3, 2], c='k')
            # ax.text(Z[3, 0], Z[3, 1], Z[3, 2], s='4')
            # ax.scatter3D(Z[4, 0], Z[4, 1], Z[4, 2], c='k')
            # ax.text(Z[4, 0], Z[4, 1], Z[4, 2], s='5')
            # ax.scatter3D(Z[5, 0], Z[5, 1], Z[5, 2], c='k')
            # ax.text(Z[5, 0], Z[5, 1], Z[5, 2], s='6')
            # ax.scatter3D(Z[6, 0], Z[6, 1], Z[6, 2], c='k')
            # ax.text(Z[6, 0], Z[6, 1], Z[6, 2], s='7')
            # ax.scatter3D(Z[7, 0], Z[7, 1], Z[7, 2], c='k')
            # ax.text(Z[7, 0], Z[7, 1], Z[7, 2], s='8')
            #
            # bbox = Poly3DCollection(verts,
            # facecolors='red', linewidths=1, edgecolors='k', alpha=.1)
            # bbox._facecolors2d= bbox._facecolor3d
            # bbox._edgecolors2d = bbox._edgecolor3d
            # ax.add_collection3d(bbox)
            #
            # ax.set_xlabel('Eje X [cm]')
            # ax.set_ylabel('Eje Y [cm]')
            # ax.set_zlabel('Eje Z [cm]')
            #
            # plt.show()

            return Z, verts

        if plane == 'YZ':

            vplane = np.array([1,0,0])

            # Definir el angulo
            angle = alpha * np.pi/180
            # Definimos el vector normal al plano del paralepipedo
            vnorm_x = 0
            vnorm_y = np.cos(angle)
            vnorm_z = np.sin(angle)
            vp1 = np.array([vnorm_x, vnorm_y, vnorm_z])
            # vp1 = vp1/np.linalg.norm(vp1)

            # Definimos un vector perpendicular al plano y al plano del paralepipedo
            vp2 = np.cross(vplane,vp1)
            vp2 = vp2/np.linalg.norm(vp2)

            # Definimos otro vector perpendicular
            vp3 = np.cross(vp1,vp2)
            vp3 = vp3/np.linalg.norm(vp3)

            # Multiplicamos los vectores para que tengan las dimensiones del detectors
            vp1 = vp1 * ydim    # (cm)
            vp2 = vp2 * xdim    # (cm)
            vp3 = vp3 * zdim    # (cm)
            vp4 = vp1 + vp2
            vp5 = vp1 + vp3
            vp6 = vp2 + vp3
            vp7 = vp1 + vp2 + vp3
            vp8 = np.array([0.0,0.0,0.0])

            vp = np.array([vp1,vp2,vp3,vp4,vp5,vp6,vp7,vp8])
            # Traslada los vértices al centro de coordenadas
            vp_mean = np.mean(vp, axis=0)
            vp = vp - vp_mean

            vp = vp + vp1/np.linalg.norm(vp1) * radio
            # vp = vp - np.array([radio,radio,0])
            Z = vp

            # Los dos primeros --> X
            # Los dos segundos --> Y
            # Los dos ultimos --> Z

            # verts = [[Z[5],Z[1],Z[7],Z[2]], --> MIN X
            #          [Z[0],Z[3],Z[6],Z[4]], --> MAX X
            #          [Z[0],Z[7],Z[2],Z[4]], --> MAX Y
            #          [Z[3],Z[1],Z[5],Z[6]], --> MIN Y
            #          [Z[7],Z[1],Z[3],Z[0]], --> MAX Z
            #          [Z[5],Z[6],Z[4],Z[2]], --> MIN Z

            verts = [[Z[5],Z[1],Z[7],Z[2]],
                     [Z[6],Z[3],Z[0],Z[4]],
                     [Z[3],Z[1],Z[5],Z[6]],
                     [Z[0],Z[7],Z[2],Z[4]],
                     [Z[2],Z[4],Z[6],Z[5]],
                     [Z[7],Z[0],Z[3],Z[1]]]

            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')

            ax.scatter3D(Z[0, 0], Z[0, 1], Z[0, 2], c='k')
            ax.text(Z[0, 0], Z[0, 1], Z[0, 2], s='1')
            ax.scatter3D(Z[1, 0], Z[1, 1], Z[1, 2], c='k')
            ax.text(Z[1, 0], Z[1, 1], Z[1, 2], s='2')
            ax.scatter3D(Z[2, 0], Z[2, 1], Z[2, 2], c='k')
            ax.text(Z[2, 0], Z[2, 1], Z[2, 2], s='3')
            ax.scatter3D(Z[3, 0], Z[3, 1], Z[3, 2], c='k')
            ax.text(Z[3, 0], Z[3, 1], Z[3, 2], s='4')
            ax.scatter3D(Z[4, 0], Z[4, 1], Z[4, 2], c='k')
            ax.text(Z[4, 0], Z[4, 1], Z[4, 2], s='5')
            ax.scatter3D(Z[5, 0], Z[5, 1], Z[5, 2], c='k')
            ax.text(Z[5, 0], Z[5, 1], Z[5, 2], s='6')
            ax.scatter3D(Z[6, 0], Z[6, 1], Z[6, 2], c='k')
            ax.text(Z[6, 0], Z[6, 1], Z[6, 2], s='7')
            ax.scatter3D(Z[7, 0], Z[7, 1], Z[7, 2], c='k')
            ax.text(Z[7, 0], Z[7, 1], Z[7, 2], s='8')

            bbox = Poly3DCollection(verts,
            facecolors='red', linewidths=1, edgecolors='k', alpha=.1)
            bbox._facecolors2d= bbox._facecolor3d
            bbox._edgecolors2d = bbox._edgecolor3d
            ax.add_collection3d(bbox)

            ax.set_xlabel('Eje X [cm]')
            ax.set_ylabel('Eje Y [cm]')
            ax.set_zlabel('Eje Z [cm]')

            plt.show()

            return Z, verts

    # ======== GENERADOR DE GEOMETRIA =========

    def __converttotext(self, c):
        if c > 0:
            num_str = '{:.7f}'.format(c)
            numtxt = len('0.000000000000000')
            format = 'E+00'
            if len(num_str) != numtxt:
                cantidad = numtxt - len(num_str)
                for i in range(cantidad):
                    num_str = num_str + '0'
            num_str = '+' + num_str + format
            return num_str
        elif c < 0:
            num_str = '{:.7f}'.format(c)
            numtxt = len('0.000000000000000')
            format = 'E+00'
            if len(num_str) != numtxt:
                cantidad = numtxt - len(num_str)
                for i in range(cantidad+1):
                    num_str = num_str + '0'
            num_str = num_str + format
            return num_str
        else:
            num_str = '{:.7f}'.format(c)
            numtxt = len('0.000000000000000')
            format = 'E+00'
            if len(num_str) != numtxt:
                cantidad = numtxt - len(num_str)
                for i in range(cantidad):
                    num_str = num_str + '0'
            num_str = '+' + num_str + format
            return num_str

    def __GetPlaneCoefficient(self,p1,p2,p3,p4):

        # Encontramos dos vectores del plano.
        v1 = p1 - p2
        v2 = p3 - p2
        v3 = p4 - p2
        # Calculamos el vector normal del plano
        normal = np.cross(v2,v3)
        normal /= np.linalg.norm(normal)

        # Calcular la distancia del plano al origen
        d = -np.dot(normal,p1)

        a = normal[0]
        b = normal[1]
        c = normal[2]

        return a,b,c,d

    def __ConstructGeometry(self):

        nplanes = int(self._nplane.value())
        plane = str(self._plane.currentText())
        material = str(self._materials.currentText())
        materials = np.array([[1,material]])

        radio = self._radio.value()
        dimensions = np.array([self._xdim.value(),self._ydim.value(),self._zdim.value()])

        # # Creamos una lista que contenga el script de INPUT
        string_list = []

        # (1) Agregamos el titulo al INPUT -----------------------------------------

        title = ["XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX\n",
                 "Detector XR --> Definimos las superficies limitantes.\n",
                 "Materiales:\n",
        	     "  - 0 -> Vacio -> Hueco\n",
                 "  - 1 -> {} -> Detector\n".format(materials[0,1]),
                 "\n",
                 "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX\n",
                 "0000000000000000000000000000000000000000000000000000000000000000\n"]

        for line in title:
            string_list.append(line)

        # (2) Creamos las superficies y los bodys para los detectores---------------

        # Definimos unidad angular de partición
        angle = 360/nplanes
        j=0
        for n in range(1,nplanes+1):

            Z, verts =  self.__PutTogetherPlanes(plane=plane, alpha = n*angle, radio=radio, dimensions=dimensions)

            i_detector = ["C\n",
                          "C  **** Detector {}\n".format(n),
                          "C\n",
                          ]

            for line in i_detector:
                string_list.append(line)

            for i,vert in enumerate(verts):
                p1,p2,p3,p4 = vert
                a,b,c,d = self.__GetPlaneCoefficient(p1,p2,p3,p4)
                # print(a,b,c,d)
                # Corregimos un error de escritura
                if a==-0.0:
                    a=0.0
                if b==-0.0:
                    b=0.0
                if c==-0.0:
                    c=0.0
                if d==-0.0:
                    d=0.0

                # Agregamos el titulo de surface
                if n+i+j < 10:
                    string_list.append("SURFACE (   {})   Plano limitante \n".format(n+i+j))
                if n+i+j < 100 and n+i+j >= 10:
                    string_list.append("SURFACE (  {})   Plano limitante \n".format(n+i+j))
                if n+i+j >= 100:
                    string_list.append("SURFACE ( {})   Plano limitante \n".format(n+i+j))

                if a == 0.0 and b != 0.0 and c != 0.0:
                    string_list.append("INDICES=( 0, 0, 0, 0, 0)\n")
                    string_list.append("     AY=({},   0)\n".format(self.__converttotext(b)))
                    string_list.append("     AZ=({},   0)\n".format(self.__converttotext(c)))
                    string_list.append("     A0=({},   0)\n".format(self.__converttotext(d)))
                elif a != 0.0 and b == 0.0 and c != 0.0:
                    string_list.append("INDICES=( 0, 0, 0, 0, 0)\n")
                    string_list.append("     AX=({},   0)\n".format(self.__converttotext(a)))
                    string_list.append("     AZ=({},   0)\n".format(self.__converttotext(c)))
                    string_list.append("     A0=({},   0)\n".format(self.__converttotext(d)))
                elif a != 0.0 and b != 0.0 and c == 0.0:
                    string_list.append("INDICES=( 0, 0, 0, 0, 0)\n")
                    string_list.append("     AX=({},   0)\n".format(self.__converttotext(a)))
                    string_list.append("     AY=({},   0)\n".format(self.__converttotext(b)))
                    string_list.append("     A0=({},   0)\n".format(self.__converttotext(d)))
                elif a == 0.0 and b == 0.0 and c != 0.0:
                    string_list.append("INDICES=( 0, 0, 0, 0, 0)\n")
                    string_list.append("     AZ=({},   0)\n".format(self.__converttotext(c)))
                    string_list.append("     A0=({},   0)\n".format(self.__converttotext(d)))
                elif a != 0.0 and b == 0.0 and c == 0.0:
                    string_list.append("INDICES=( 0, 0, 0, 0, 0)\n")
                    string_list.append("     AX=({},   0)\n".format(self.__converttotext(a)))
                    string_list.append("     A0=({},   0)\n".format(self.__converttotext(d)))
                elif a == 0.0 and b != 0.0 and c == 0.0:
                    string_list.append("INDICES=( 0, 0, 0, 0, 0)\n")
                    string_list.append("     AY=({},   0)\n".format(self.__converttotext(b)))
                    string_list.append("     A0=({},   0)\n".format(self.__converttotext(d)))

                string_list.append("0000000000000000000000000000000000000000000000000000000000000000\n")


            if n < 10:
                string_list.append("BODY    (   {})  Detector {} - Prism\n".format(n,n))
            elif n>=10 and n<100:
                string_list.append("BODY    (  {})  Detector {} - Prism\n".format(n,n))
            elif n>=100:
                string_list.append("BODY    ( {})  Detector {} - Prism\n".format(n,n))

            string_list.append("MATERIAL(   {})\n".format(materials[0,0]))

            if n+0+j < 10:
                string_list.append("SURFACE (   {}), SIDE POINTER=(-1)\n".format(n+0+j))
            elif n+0+j>=10 and n+0+j<100:
                string_list.append("SURFACE (  {}), SIDE POINTER=(-1)\n".format(n+0+j))
            elif n+0+j>=100:
                string_list.append("SURFACE ( {}), SIDE POINTER=(-1)\n".format(n+0+j))

            if n+1+j < 10:
                string_list.append("SURFACE (   {}), SIDE POINTER=(+1)\n".format(n+1+j))
            elif n+1+j>=10 and n+1+j<100:
                string_list.append("SURFACE (  {}), SIDE POINTER=(+1)\n".format(n+1+j))
            elif n+1+j>=100:
                string_list.append("SURFACE ( {}), SIDE POINTER=(+1)\n".format(n+1+j))

            if n+2+j < 10:
                string_list.append("SURFACE (   {}), SIDE POINTER=(-1)\n".format(n+2+j))
            elif n+2+j>=10 and n+2+j<100:
                string_list.append("SURFACE (  {}), SIDE POINTER=(-1)\n".format(n+2+j))
            elif n+2+j>=100:
                string_list.append("SURFACE ( {}), SIDE POINTER=(-1)\n".format(n+2+j))

            if n+3+j < 10:
                string_list.append("SURFACE (   {}), SIDE POINTER=(+1)\n".format(n+3+j))
            elif n+3+j>=10 and n+3+j<100:
                string_list.append("SURFACE (  {}), SIDE POINTER=(+1)\n".format(n+3+j))
            elif n+3+j>=100:
                string_list.append("SURFACE ( {}), SIDE POINTER=(+1)\n".format(n+3+j))

            if n+4+j < 10:
                string_list.append("SURFACE (   {}), SIDE POINTER=(-1)\n".format(n+4+j))
            elif n+4+j>=10 and n+4+j<100:
                string_list.append("SURFACE (  {}), SIDE POINTER=(-1)\n".format(n+4+j))
            elif n+4+j>=100:
                string_list.append("SURFACE ( {}), SIDE POINTER=(-1)\n".format(n+4+j))

            if n+5+j < 10:
                string_list.append("SURFACE (   {}), SIDE POINTER=(+1)\n".format(n+5+j))
            elif n+5+j>=10 and n+5+j<100:
                string_list.append("SURFACE (  {}), SIDE POINTER=(+1)\n".format(n+5+j))
            elif n+5+j>=100:
                string_list.append("SURFACE ( {}), SIDE POINTER=(+1)\n".format(n+5+j))

            string_list.append("0000000000000000000000000000000000000000000000000000000000000000\n")
            j += 5

        string_list.append("END      0000000000000000000000000000000000000000000000000000000")

        self.geometryFile = string_list
        self.__save_file_geometry(string_list)

    def __save_file_geometry(self, string_list):

        opciones = QFileDialog.Options()
        opciones |= QFileDialog.DontUseNativeDialog
        pathfile, _ = QFileDialog.getSaveFileName(self, "Guardar archivo", "",
                                                  "Archivos de texto (*.geo);;Todos los archivos (*)",
                                                  options=opciones)

        basename = os.path.basename(pathfile)
        if basename.split('.')[-1] != "geo":
            msgBox = QMessageBox()
            msgBox.setText("No se puede cargar este formato de archivos.")
            msgBox.setStandardButtons(QMessageBox.Cancel)
            ret = msgBox.exec()
        else:
            # pathfile = os.path.join('D:\\',*path.split('\\')[1:-1], 'detector_simulated.geo')
            self.pathfile_geometry = pathfile
            my_file = open('{}'.format(pathfile),'w')
            new_file_contents = "".join(string_list)
            my_file.write(new_file_contents)
            my_file.close()

    # ======== GENERADOR DE INPUT PENELOPE ========

    def __save_file_input(self, string_list):

        opciones = QFileDialog.Options()
        opciones |= QFileDialog.DontUseNativeDialog
        pathfile, _ = QFileDialog.getSaveFileName(self, "Guardar archivo", "",
                                                  "Archivos de texto (*.in);;Todos los archivos (*)",
                                                  options=opciones)

        basename = os.path.basename(pathfile)
        if basename.split('.')[-1] != "in":
            msgBox = QMessageBox()
            msgBox.setText("No se puede cargar este formato de archivos.")
            msgBox.setStandardButtons(QMessageBox.Cancel)
            ret = msgBox.exec()
        else:

            my_file = open('{}'.format(pathfile),'w')
            new_file_contents = "".join(string_list)
            my_file.write(new_file_contents)
            my_file.close()

    def __ConstructInput(self):

        emin = self._emin.value()
        emin = '%.1e' % emin

        emax = self._emax.value()
        emax = '%.1e' % emax

        nbins = int(self._nbins.value())

        nprimarios = self._nprim.value()
        nprimarios = '%.1e' % nprimarios

        ndetectors = int(self._nplane.value())+1

        material = str(self._materials.currentText())


        # # Creamos una lista que contenga el script de INPUT
        string_list = []

        # (1) Agregamos el titulo al INPUT -----------------------------------------
        title = ['TITLE  Response of a CdTe detector.\n',
                '       .\n',
                '       >>>>>>>> Input phase-space file (psf).\n'
                'IPSFN  PhaseSpace.dat          [Input psf name, up to 20 characters]\n',
                '       .\n',
                '       >>>>>>>> Material data and simulation parameters.\n',
                'MFNAME .\mat\{}.mat                 [Material file, up to 20 chars]\n'.format(material),
                'MSIMPA 1.0e3 1.0e3 1.0e3 0.1 0.1 2e3 2e3    [EABS(1:3),C1,C2,WCC,WCR]\n',
                '       .\n',
                '       >>>>>>>> Geometry definition file.\n',
                'GEOMFN .\geo\detector.geo             [Geometry file, up to 20 chars]\n',
                '       .\n']

        for line in title:
            string_list.append(line)

        # Modificamos los bloques de IMPACT y ENERGY DEPOSITION

        # Impact
        string_list.append('       >>>>>>>> Impact detectors (up to 25 different detectors).\n')
        for j in range(1,ndetectors+1):
            string_list.append('IMPDET {} {} {} {} {}         [E-window, no. of bins, IPSF, IDCUT]\n'.format(emin,emax,nbins,'0','0'))
            string_list.append('IDBODY {}\n'.format(j))
        string_list.append('       .\n')

        # Energy detectors
        string_list.append('       >>>>>>>> Energy deposition detectors (up to 25)\n')
        for j in range(1,ndetectors+1):
            string_list.append('ENDETC {} {} {}                  [E-window, no. of bins, IPSF, IDCUT]\n'.format(emin,emax,nbins))
            string_list.append('EDBODY {}\n'.format(j))
        string_list.append('       .\n')

        # Agregamos el job
        job = ['       >>>>>>>> Job properties\n',
               'RESUME dump.dat                [Resume from this dump file, 20 chars]\n',
               'DUMPTO dump.dat                   [Generate this dump file, 20 chars]\n',
               'DUMPP  60\n',
               '       .\n',
               'NSIMSH {}                      [Desired number of simulated showers]\n'.format(nprimarios),
               'TIME   2e9                         [Allotted simulation time, in sec]\n',
               'END                                  [Ends the reading of input data]\n']

        for line in job:
            string_list.append(line)

        self.inputFile = string_list
        self.__save_file_input(string_list)

    # ========= TYPES GRAPH ===========

    def __ViewPlanes(self):

        nplanes = int(self._nplane.value())+1
        plane = str(self._plane.currentText())
        radio = self._radio.value()
        dimensions = np.array([self._xdim.value(),self._ydim.value(),self._zdim.value()])

        angle = 360/nplanes
        list_bodys = []
        for n in range(1,nplanes):

            Z, verts =  self.__PutTogetherPlanes(plane=plane, alpha=angle*n, radio=radio, dimensions=dimensions)

            x = Z[:,0]
            y = Z[:,1]
            z = Z[:,2]
            i= [7, 0, 0, 0, 4, 4, 6, 1, 4, 0, 3, 6]
            j= [3, 4, 1, 2, 5, 6, 5, 2, 0, 1, 6, 3]
            k= [0, 7, 2, 3, 6, 7, 1, 6, 5, 5, 7, 2]


            list_bodys.append(go.Mesh3d(x=x, y=y, z=z, alphahull = 0,
                                        # i=i, j=j, k=k,
                                        opacity=0.5,
                                        color='blue'))

        # Datos para el eje x
        list_bodys.append(go.Scatter3d(x=[0, 6], y=[0, 0], z=[0, 0], mode='lines', name='X Axis', line=dict(color='red', width=5)))

        # Datos para el eje y
        list_bodys.append(go.Scatter3d(x=[0, 0], y=[0, 6], z=[0, 0], mode='lines', name='Y Axis', line=dict(color='green', width=5)))

        # Datos para el eje z
        list_bodys.append(go.Scatter3d(x=[0, 0], y=[0, 0], z=[0, 6], mode='lines', name='Z Axis', line=dict(color='blue', width=5)))


        layout = go.Layout(scene_xaxis_visible=False, scene_yaxis_visible=False, scene_zaxis_visible=False)
        # layout = go.Layout(scene_xaxis_visible=True, scene_yaxis_visible=True, scene_zaxis_visible=True,
        #                   scene = dict(xaxis=dict(range=[-10,10]),
        #                                yaxis=dict(range=[-10,10]),
        #                                zaxis=dict(range=[-10,10])))

        # df = px.data.tips()
        # fig = px.box(df, x="day", y="total_bill", color="smoker")
        # fig.update_traces(quartilemethod="exclusive") # or "inclusive", or "linear" by default
        #

        fig = go.Figure(data = list_bodys, layout = layout)
        # fig.update_layout(scene_camera_eye_z= 0.55)
        fig.layout.scene.camera.projection.type = "orthographic" #commenting this line you get a fig with perspective proj
        self.browser.setHtml(fig.to_html(include_plotlyjs='cdn'))
        # fig.show()

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()

        # self.setWindowIcon(QtGui.QIcon('logo_mc-tcad.png'))
        self.setWindowTitle("Generador de anillos detectores")

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
        geometryAction = QAction("Geometría", self, shortcut="Ctrl+L", triggered=self.geometry)

        # Agregamos las acciones
        toolBar.addAction(geometryAction)

        # (2) VENTANA PRINCIPAL
        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)

    def geometry(self):

        self.mpl_can = Plot3DView()
        # la agregamos a la ventana principal
        self.central_widget.addWidget(self.mpl_can)
        self.central_widget.setCurrentWidget(self.mpl_can)

    def input(self):

        self.mpl_can = Plot3DView()
        # la agregamos a la ventana principal
        self.central_widget.addWidget(self.mpl_can)
        self.central_widget.setCurrentWidget(self.mpl_can)


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
