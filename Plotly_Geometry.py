import os
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

class TransformGeometry():

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
            self.__string_list = self.__loadfile()

            self.__get_data_main()


        elif self.pen == 'pencyl_2018':

            # ---------------------------------------------------
            # Buscamos y elegimos el path del GEOMETRY a cargar
            path_geometry = self.__find_geometry_cyl(pathfolder)
            self.path = path_geometry

            # ---------------------------------------------------
            # Cargamos los datos del GEOMETRY en una lista
            self.__string_list = self.__loadfile()

            self.__get_data_cyl()

        else:
            print('No se encontro el archivo correspondiente a la geometria de la simulacion.')


        # ---------------------------------------------------
        # Separamos en bloques los datos del INPUT
        # self.__num_bloq = self.__data_process()

        # ---------------------------------------------------
        # Recolecta la informacion del INPUT dependiendo el PEN

    def __format_e(self,n):

        a = '%e' % n
        d = a.split('e')[0].rstrip('0').rstrip('.')
        return d[:4] + 'e' + a.split('e')[1][1:]

    def __converttotext(self, c):
        num_str = '{:.7f}'.format(c/10000)
        numtxt = len('0.000000000000000')
        format = 'E+00'
        if len(num_str) != numtxt:
            cantidad = numtxt - len(num_str)
            for i in range(cantidad):
                num_str = num_str + '0'
        num_str = num_str + format
        return num_str

    def circle_detectors(self):

        def __converttotext(c):
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

        pathpen = "D:\Proyectos_Investigacion\Proyectos_de_Doctorado\Proyectos\SimulationXF_Detectors\Code\RUN\penmain_2018"
        geom = LoadDataFileGeometry(pathpen)
        path = geom.path
        string_list = geom.string_list
        clone = True

        if clone:

            # Buscamos el body detector
            data_module = []
            for num in range(geom.numBodys):
                nbody = geom.GetDataBody[num+1]
                if nbody['Type'] == 'MODULE':
                    data_module.append([num+1,nbody['Name']])
            data_module = np.array(data_module)

            respuesta =  option_list(data_module[:,1], input_type='int', question='¿Que MODULE desea repetir?', return_type=False)
            num_module = int(data_module[respuesta,0])

            # list_detect = list(np.arange(1,13,1))
            # num_detect =  option_list(list_detect, input_type='int', question='¿Cuantos desea agregar?', return_type=True)
            num_detect = 12
            # self.__circle_radius(geom, radius, plane, detect, target)

            # Extraemos los datos
            # detector = self.GetDataBody[num_module]
            # target = self.GetDataBody[num_module+1]
            detector = geom.GetDataBody[num_module]
            target = geom.GetDataBody[num_module+1]
            surface_detector = detector['Surfaces'][0]
            surface_target = target['Surfaces'][0]
            data_target = target['Data Surfaces'][surface_target]
            data_detect = detector['Data Surfaces'][surface_detector]

            # Definimos el angulo
            angle = 360/num_detect * np.pi/180
            # angle = 30 * np.pi/180
            vpos_detect = np.array([data_detect['XSH'][0],data_detect['YSH'][0],data_detect['ZSH'][0]])
            vpos_target = np.array([data_target['XSH'][0],data_target['YSH'][0],data_target['ZSH'][0]])
            v_distance =  vpos_detect - vpos_target

            # Radio del circulo
            R = np.linalg.norm(v_distance)

            # --------------------------------------------------
            # Creamos el archivo con los detectores circulares

            num = len(geom.blocks_bodys)

            block = geom.blocks_bodys[-1]
            new_string = string_list[:block[1]+1]

            # ----
            for n in range(1,num_detect):
            # for n in range(1,num+1):
                # n=1
                # Nueva posicion del detector
                xp = R*np.cos(angle*n)
                yp = R*np.sin(angle*n)
                zp = data_target['ZSH'][0]
                vpos_new_detect = np.array([xp,yp,zp])

                X_shift = vpos_target[0] - vpos_new_detect[0]
                Y_shift = vpos_target[1] - vpos_new_detect[1]
                Z_shift = vpos_new_detect[2] - vpos_target[2]

                # Angulos
                omega = 0
                theta = 0
                phi = angle*n*180/np.pi

                nb = num+n+1
                if nb < 10:
                    line_clone = "CLONE   (   {})  Detector {} - Prism".format(num+n+1, n+2)
                else:
                    line_clone = "CLONE   (  {})  Detector {} - Prism".format(num+n+1, n+2)

                block_text = [line_clone,
                              "MODULE  (   {})".format(num_module),
                              "1111111111111111111111111111111111111111111111111111111111111111",
                              "  OMEGA=({},   0)".format(__converttotext(omega)),
                              "  THETA=({},   0)".format(__converttotext(theta)),
                              "    PHI=({},   0)".format(__converttotext(phi)),
                              "X-SHIFT=({},   0)".format(__converttotext(X_shift)),
                              "Y-SHIFT=({},   0)".format(__converttotext(Y_shift)),
                              "Z-SHIFT=({},   0)".format(__converttotext(Z_shift)),
                              "0000000000000000000000000000000000000000000000000000000000000000"]

                for bloque in block_text:
                    new_string.append(bloque+'\n')
            # ----

        else:

            # Buscamos el body detector
            for num in range(geom.numBodys):
                nbody = geom.GetDataBody[num+1]
                print(nbody['Name'])
                if nbody['Name'].startswith('Detector') or nbody['Name'].startswith('detector'):
                    detector = nbody
                if nbody['Name'].startswith('Target') or nbody['Name'].startswith('target'):
                    target = nbody

            # NUMERO DE DETECTORES
            list_detect = list(np.arange(1,13,1))
            num_detect =  option_list(list_detect, input_type='int', question='¿Cuantos desea agregar?', return_type=True)
            # Definimos el angulo
            angle = 360/num_detect * np.pi/180

            # TARGET
            surfaces_target = target['Surfaces'][0]
            data_target = target['Data Surfaces'][surfaces_target]
            # Vector posicion del target
            vpos_target = np.array([data_target['XSH'][0],data_target['YSH'][0],data_target['ZSH'][0]])


            # DETECTOR
            surfaces_detector = detector['Surfaces']
            vpos_detect = np.array([data_detect['XSH'][0],data_detect['YSH'][0],data_detect['ZSH'][0]])
            v_distance =  vpos_detect - vpos_target

            # Radio del circulo
            R = np.linalg.norm(v_distance)

            # --------------------------------------------------
            # Creamos el archivo con los detectores circulares

            num = len(blocks_bodys)

            block = blocks_bodys[-1]
            new_string = string_list[:block[1]+1]

            # ----
            for n in range(1,num_detect):
            # for n in range(1,num+1):
                # n=1
                # Nueva posicion del detector
                xp = R*np.cos(angle*n)
                yp = R*np.sin(angle*n)
                zp = data_target['ZSH'][0]
                vpos_new_detect = np.array([xp,yp,zp])

                print('N={}'.format(n))
                # Vector de translacion
                v_translate = vpos_new_detect - vpos_detect
                print('({})'.format(v_translate))
                X_shift = v_translate[1] + vpos_target[0]
                Y_shift = v_translate[0] + vpos_target[1]
                Z_shift = v_translate[2] + vpos_target[2]

                # x0 = vpos_target[0]
                # y0 = vpos_target[1]
                # z0 = vpos_target[2]
                #
                # # Definir la matriz de transformación de traslación T
                # T = np.array([[1, 0, 0, -x0],
                #               [0, 1, 0, -y0],
                #               [0, 0, 1, -z0],
                #               [0, 0, 0, 1]])
                #
                # # Definir la matriz de rotación R
                # theta = angle
                # R = np.array([[np.cos(theta), 0, np.sin(theta), 0],
                #                 [0, 1, 0, 0],
                #                 [-np.sin(theta), 0, np.cos(theta), 0],
                #                 [0, 0, 0, 1]])
                #
                # # # Definir el vector de traslación
                # # vector_traslacion = np.array([[1, 0, 0, 0],
                # #                               [0, 1, 0, 0],
                # #                               [0, 0, 1, 0],
                # #                               [-5, 0, 0, 1]])
                #
                # # Calcular la matriz de transformación compuesta M
                # M = np.matmul(R, T)
                #
                # # Calcular los coeficientes del plano transformado
                # A_new, B_new, C_new, D_new = np.matmul([1, 0, 0, 0], M)
                # #
                # # # Verificar que el plano resultante esté orientado hacia el centro de la circunferencia
                # normal_vector = np.array([A_new, B_new, C_new])
                # center_vector = np.array([x0, y0, z0])
                # if np.dot(normal_vector, center_vector) > 0:
                #     A_new *= -1
                #     B_new *= -1
                #     C_new *= -1
                #     D_new *= -1


                # Angulos
                omega = angle*n*180/np.pi
                theta = 0
                phi = 0

                # block_text = ["CLONE   (   {})  Detector {} - Prism".format(num+n, n+2),
                #               "MODULE  (   {})".format(num_module),
                #               "1111111111111111111111111111111111111111111111111111111111111111",
                #               "  OMEGA=( {},   0)".format(self.__converttotext(omega)),
                #               "  THETA=( {},   0)".format(self.__converttotext(theta)),
                #               "    PHI=( {},   0)".format(self.__converttotext(phi)),
                #               "X-SHIFT=( {},   0)".format(self.__converttotext(X_shift)),
                #               "Y-SHIFT=( {},   0)".format(self.__converttotext(Y_shift)),
                #               "Z-SHIFT=( {},   0)".format(self.__converttotext(Z_shift)),
                #               "0000000000000000000000000000000000000000000000000000000000000000"]
                nb = num+n+1
                if nb < 10:
                    line_clone = "CLONE   (   {})  Detector {} - Prism".format(num+n+1, n+2)
                else:
                    line_clone = "CLONE   (  {})  Detector {} - Prism".format(num+n+1, n+2)

                block_text = [line_clone,
                              "MODULE  (   {})".format(num_module),
                              "1111111111111111111111111111111111111111111111111111111111111111",
                              "  OMEGA=({},   0)".format(__converttotext(omega)),
                              "  THETA=({},   0)".format(__converttotext(theta)),
                              "    PHI=({},   0)".format(__converttotext(phi)),
                              "X-SHIFT=({},   0)".format(__converttotext(X_shift)),
                              "Y-SHIFT=({},   0)".format(__converttotext(Y_shift)),
                              "Z-SHIFT=({},   0)".format(__converttotext(Z_shift)),
                              "0000000000000000000000000000000000000000000000000000000000000000"]

                for bloque in block_text:
                    new_string.append(bloque+'\n')
            # ----

        new_string.append(string_list[block[1]+1])

        pathfile = os.path.join('D:\\',*path.split('\\')[1:-1], 'detector_original_1.geo')

        my_file = open('{}'.format(pathfile),'w')
        new_file_contents = "".join(new_string)
        my_file.write(new_file_contents)
        my_file.close()

    def modify_ticknness(self, surface, change):

        # Cargamos el texto de GEOMETRY
        string_list = self.__string_list
        path = self.path

        value = surface[0]

        # file=open(path)
        # string_list = file.readlines()
        # file.close()

        for i, string in enumerate(string_list):
            if string.find('SURFACE (   {})  '.format(int(value))) != -1:
                for j, string in enumerate(string_list[i:]):
                    if not string.find('000000000000000000') != -1:
                        if string.find('Z-SHIFT') !=-1:
                            string_list[i+j] = 'Z-SHIFT=( {},   0)\n'.format(change)
                            break
                    else:
                        break


        my_file = open('{}'.format(path),'w')
        new_file_contents = "".join(string_list)
        my_file.write(new_file_contents)
        my_file.close()

    def __circle_radius(self, geom, radius, plane, detect, target):

        string_list = geom.string_list
        for num in range(geom.numBodys):
            nbody = geom.GetDataBody[num+1]
            if nbody['Name'].startswith('Detector'):
                body_detect = nbody
            if nbody['Name'].startswith('Target'):
                body_target = nbody

        if detect:
            print('Detect')
            if plane == 'XZ':
                print('Plane XZ')
                for ds in body_detect['Data Surfaces'].keys():
                    surface_body = body_detect['Data Surfaces'][ds]

                    # Eje Z
                    sb = surface_body['SURFACE'][0]
                    if sb == 1:
                        if surface_body['AZ'] != []:
                            surface_body['A0'] = - 0.25

                            # Modificamos el archivo con el nuevo valor.
                            sblocks = geom.blocks_surfaces_complete[sb-1]
                            if sblocks[0] == sb:
                                blocks = sblocks[1]
                                for l in range(blocks[0],blocks[1]):

                                    if string_list[l].startswith('Z-SHIFT'):
                                        string_list[l] = 'Z-SHIFT=({},   0)\n'.format(__converttotext(surface_body['A0']))
                                        print('Plane 1')

                    if sb == 2:
                        if surface_body['AZ'] != []:
                            surface_body['A0'] = 0.25

                            # Modificamos el archivo con el nuevo valor.
                            sblocks = geom.blocks_surfaces_complete[sb-1]
                            if sblocks[0] == sb:
                                blocks = sblocks[1]
                                for l in range(blocks[0],blocks[1]):

                                    if string_list[l].startswith('Z-SHIFT'):
                                        string_list[l] = 'Z-SHIFT=({},   0)\n'.format(__converttotext(surface_body['A0']))
                                        print('Plane 2')
                    # Eje X
                    if sb == 3:
                        if surface_body['AX'] != []:
                            surface_body['A0'] = -radius + 0.25

                            # Modificamos el archivo con el nuevo valor.
                            sblocks = geom.blocks_surfaces_complete[sb-1]
                            if sblocks[0] == sb:
                                blocks = sblocks[1]
                                for l in range(blocks[0],blocks[1]):

                                    if string_list[l].startswith('     A0='):
                                        string_list[l] = '     A0=({},   0)\n'.format(__converttotext(surface_body['A0']))
                                        print('Plane 3')

                    if sb == 4:
                        if surface_body['AX'] != []:
                            surface_body['A0'] = -radius - 0.25

                            # Modificamos el archivo con el nuevo valor.
                            sblocks = geom.blocks_surfaces_complete[sb-1]
                            if sblocks[0] == sb:
                                blocks = sblocks[1]
                                for l in range(blocks[0],blocks[1]):

                                    if string_list[l].startswith('     A0='):
                                        string_list[l] = '     A0=({},   0)\n'.format(__converttotext(surface_body['A0']))
                                        print('Plane 4')

                    # Eje Y
                    if sb == 5:
                        if surface_body['AY'] != []:
                            surface_body['A0'] = -radius + 0.05

                            # Modificamos el archivo con el nuevo valor.
                            sblocks = geom.blocks_surfaces_complete[sb-1]
                            if sblocks[0] == sb:
                                blocks = sblocks[1]
                                for l in range(blocks[0],blocks[1]):

                                    if string_list[l].startswith('     A0='):
                                        string_list[l] = '     A0=({},   0)\n'.format(__converttotext(surface_body['A0']))
                                        print('Plane 5')

                    if sb == 6:
                        if surface_body['AY'] != []:
                            surface_body['A0'] = -radius - 0.05

                            # Modificamos el archivo con el nuevo valor.
                            sblocks = geom.blocks_surfaces_complete[sb-1]
                            if sblocks[0] == sb:
                                blocks = sblocks[1]
                                for l in range(blocks[0],blocks[1]):
                                    print(l)
                                    if string_list[l].startswith('     A0='):
                                        string_list[l] = '     A0=({},   0)\n'.format(__converttotext(surface_body['A0']))
                                        print('Plane 6')

            if plane == 'YZ':

                for ds in body_detect['Data Surfaces'].keys():
                    surface_body = body_detect['Data Surfaces'][ds]
                    # Eje Z
                    if surface_body['SURFACE'][0] == 1:
                        if surface_body['AZ'] != []:
                            surface_body['A0'] = - 0.25
                    if surface_body['SURFACE'][0] == 2:
                        if surface_body['AZ'] != []:
                            surface_body['A0'] = 0.25
                    # Eje X
                    if surface_body['SURFACE'][0] == 3:
                        if surface_body['AX'] != []:
                            surface_body['A0'] = radius - 0.05
                    if surface_body['SURFACE'][0] == 4:
                        if surface_body['AX'] != []:
                            surface_body['A0'] = radius + 0.05
                    # Eje Y
                    if surface_body['SURFACE'][0] == 5:
                        if surface_body['AY'] != []:
                            surface_body['A0'] = radius - 0.25
                    if surface_body['SURFACE'][0] == 6:
                        if surface_body['AY'] != []:
                            surface_body['A0'] = radius + 0.25

            if plane == 'XY':
                print('Continuara....')

        if target:

            print('Continuara.....')

        pathfile = os.path.join('D:\\', *path.split('\\')[1:-1], 'detector_1.geo')
        my_file = open('{}'.format(pathfile),'w')
        new_file_contents = "".join(string_list)
        my_file.write(new_file_contents)
        my_file.close()

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
pathfolder = "D:\Proyectos_Investigacion\Proyectos_de_Doctorado\Proyectos\SimulationXF_Detectors\Code\RUN\penmain_2018"
cdetectors = CircleDetectors(pathfolder)




class WidgetPlotly(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.button = QtWidgets.QPushButton('Plot', self)
        self.browser = QWebEngineView(self)

        vlayout = QtWidgets.QVBoxLayout(self)
        vlayout.addWidget(self.button, alignment=Qt.AlignHCenter)
        vlayout.addWidget(self.browser)

        self.button.clicked.connect(self.show_graph)
        self.resize(1000,800)

    def show_graph(self):
        df = px.data.tips()
        fig = px.box(df, x="day", y="total_bill", color="smoker")
        fig.update_traces(quartilemethod="exclusive") # or "inclusive", or "linear" by default
        self.browser.setHtml(fig.to_html(include_plotlyjs='cdn'))




class Plot3DView(QWidget):

    def __init__(self, parent=None, data=None):
        super(Plot3DView, self).__init__(parent)

        self.data_base = data

        self.__nsegments = None
        self.__nparticle = None
        self.__method_best = None

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
        self._style_plot = QComboBox()
        init_widget(self._style_plot, "styleComboBox")
        self._style_plot.addItems(style_names(list_name='type_plot'))

        # Elige una particula para visualizar
        self._npart = QDoubleSpinBox()
        self._npart.setPrefix("")
        self._npart.setValue(0)
        init_widget(self._npart, "primario")

        # Boton de ejecución para visualizar el plot elegido
        self.button_view1 = QPushButton("View")
        init_widget(self.button_view1, "view_label1")

        # # Opciones para ver datos procesados
        self._style_method = QComboBox()
        init_widget(self._style_method, "styleComboBox")
        self._style_method.addItems(style_names(list_name='type_method'))

        # Elige el numero de segmentos
        self._nseg = QDoubleSpinBox()
        self._nseg.setPrefix("")
        self._nseg.setValue(0)
        init_widget(self._nseg, "segments")

        # Boton de ejecución para visualizar el plot elegido
        self.button_view2 = QPushButton("View")
        init_widget(self.button_view2, "view_label2")

        # # Opciones para ver resultados

        self._style_results = QComboBox()
        init_widget(self._style_results, "styleComboBox")
        self._style_results.addItems(style_names(list_name='type_results'))

        # # Opciones para ver METODOS
        self._method = QComboBox()
        init_widget(self._method, "styleComboBox")
        self._method.addItems(style_names(list_name='methods'))

        # Boton de ejecución para visualizar el plot elegido
        self.button_view3 = QPushButton("View")
        init_widget(self.button_view3, "view_label3")

        # -----------------------------------------------------
        # Boton de ejecución para visualizar el plot elegido
        self.button_view4 = QPushButton("View")
        init_widget(self.button_view4, "view_label4")

        # Boton de ejecución para armar INPUT TCAD
        self.button3 = QPushButton("Assemble TCAD Input")
        init_widget(self.button3, "armar_tcad")

        # (2) Agregamos widgets al panel
        self.llayout = QVBoxLayout()
        self.llayout.setContentsMargins(1, 1, 1, 1)
        self.llayout.addWidget(QLabel(""))
        self.label = QLabel("    MC-TCAD CONFIGURATION")
        self.label.setStyleSheet("border: 2px solid black; position: center;")
        self.llayout.addWidget(self.label)
        self.llayout.addWidget(QLabel(""))
        self.llayout.addWidget(QLabel("Primary:"))
        self.llayout.addWidget(self._npart)

        self.llayout.addWidget(QLabel("------------------------"))

        self.llayout.addWidget(QLabel("Processed data"))
        self.llayout.addWidget(self._style_plot)
        self.llayout.addWidget(self.button_view1)

        self.llayout.addWidget(QLabel("------------------------"))

        self.llayout.addWidget(QLabel("Linear fit techniques"))
        self.llayout.addWidget(QLabel("Techniques"))
        self.llayout.addWidget(self._style_method)
        self.llayout.addWidget(QLabel("Number of segments:"))
        self.llayout.addWidget(self._nseg)
        self.llayout.addWidget(self.button_view2)

        self.llayout.addWidget(QLabel("------------------------"))

        self.llayout.addWidget(QLabel("LET by techniques"))
        self.llayout.addWidget(QLabel("Select method:"))
        self.llayout.addWidget(self._method)
        self.llayout.addWidget(self.button_view3)

        self.llayout.addWidget(QLabel("------------------------"))

        self.llayout.addWidget(QLabel("Automated method"))
        self.llayout.addWidget(self.button_view4)
        self.llayout.addWidget(QLabel(""))
        self.llayout.addWidget(self.button3)


        # (3) Agregamos las conexiones
        self.button_view1.clicked.connect(self.__ViewPlot)
        self.button_view2.clicked.connect(self.__ViewMethod)
        self.button_view3.clicked.connect(self.__ViewLet)
        self.button_view4.clicked.connect(self.__ViewResults)
        self.button3.clicked.connect(self.__CreateInputTCAD)

        # --------------------------------------------------
        # # Panel DERECHO - Definición de configuraciones

        self.cllayout = QVBoxLayout()
        self.cllayout.setContentsMargins(1, 1, 1, 1)
        self.fig = Figure(figsize=(2, 2))
        self.can = FigureCanvasQTAgg(self.fig)
        self.cllayout.addWidget(self.can)

    # # ========= TYPES PLOTS ===========

    def __ViewPlot(self):

        # (1) Extraemos los datos
        self.__nparticle = self._npart.value()
        self.__type_plot = str(self._style_plot.currentText())

        if self.__type_plot == 'Primaries and Dispersions':

            self.can.deleteLater()

            # Procesamos los datos para primarios y secundarios
            data_processed = DataProcessed(self.data_base, npart=self.__nparticle, type_plot=self.__type_plot)

            data_base = []
            data_base.append(data_processed.primarios)
            data_base.append(data_processed.secundarios)

            self.__view_event_type(data_base)

        elif self.__type_plot == 'Ionizations':

            self.can.deleteLater()

            # Procesamos los datos para primarios y secundarios
            data_processed = DataProcessed(self.data_base, npart=self.__nparticle, type_plot=self.__type_plot)

            data_base = []
            data_base.append(data_processed.ionizations)
            data_base.append(data_processed.no_ionizations)

            self.__view_particle_ionizations(data_base)

    def __func(self,label):
        index = self.__labels.index(label)
        self.__lines[index].set_visible(not self.__lines[index].get_visible())
        self.can.draw()

    def __view_event_type(self, data_base):

        self.fig = Figure(figsize=(2, 2))
        self.can = FigureCanvasQTAgg(self.fig)
        # self.toolbar = NavigationToolbar2QT(self.can, self)
        # self.cllayout.addWidget(self.toolbar)
        self.cllayout.addWidget(self.can)

        # here you can set up your figure/axis
        self.ax = self.can.figure.add_subplot(111, projection='3d')
        matplotlib.rcParams.update({'font.size': 8})

        # Separamos en eventos primarios y secundarios
        pri, sec = data_base

        # Ploteamos los resultados

        if len(sec) != 0:
            surf1 = self.ax.scatter3D(pri[:,0], pri[:,1], pri[:,2], c='b', alpha=0.7, label='Primary')
            surf2 = self.ax.scatter3D(sec[:,0], sec[:,1], sec[:,2], c='r', alpha=0.7, label='Dispersions')
            # ----------------------------------------------------------
            # Primarios o secundarios
            self.__lines = [surf1, surf2]
            self.__labels = ['Primary Track', 'Dispersions Track']
        else:
            surf1 = self.ax.scatter3D(pri[:,0], pri[:,1], pri[:,2], c='b', alpha=0.7, label='Primary')
            # ----------------------------------------------------------
            # Primarios
            self.__lines = [surf1]
            self.__labels = ['Primary Track']

        self.ax.legend(loc="upper left", fontsize=10)
        self.ax.set_xlabel('X [cm]')
        self.ax.set_ylabel('Y [cm]')
        self.ax.set_zlabel('Z [cm]')

        # ----------------------------------------------------------
        # Mostrar primarios o secundarios
        visibility = [line.get_visible() for line in self.__lines]
        axcolor = 'lightgoldenrodyellow'
        rax = self.can.figure.add_axes([0.05, 0.7, 0.15, 0.15], facecolor=axcolor)

        self.__check = CheckButtons(rax, self.__labels, visibility)
        self.__check.on_clicked(self.__func)

        # self.can.figure.rcParams.update({'font.size': 8})
        self.can.draw()

    def __view_particle_ionizations(self, data_base):

        self.fig = Figure(figsize=(2, 2))
        self.can = FigureCanvasQTAgg(self.fig)
        # self.toolbar = NavigationToolbar2QT(self.can, self)
        # self.cllayout.addWidget(self.toolbar)
        self.cllayout.addWidget(self.can)

        # here you can set up your figure/axis
        self.ax = self.can.figure.add_subplot(111, projection='3d')
        matplotlib.rcParams.update({'font.size': 8})

        ion, nion = data_base

        # Ploteamos los resultados

        surf1 = self.ax.scatter3D(ion[:,0], ion[:,1], ion[:,2], c='r', label='Ionizations')
        surf2 = self.ax.scatter3D(nion[:,0], nion[:,1], nion[:,2], c='k', alpha=0.2, label='Not ionizations')
        # ----------------------------------------------------------
        # Ionizaciones o no ionizaciones
        self.__lines = [surf1, surf2]
        self.__labels = ['Ionizations', 'Not ionizations']

        self.ax.legend(loc="upper left", fontsize=10)
        self.ax.set_xlabel('X [cm]')
        self.ax.set_ylabel('Y [cm]')
        self.ax.set_zlabel('Z [cm]')

        visibility = [line.get_visible() for line in self.__lines]
        axcolor = 'lightgoldenrodyellow'
        rax = self.can.figure.add_axes([0.05, 0.7, 0.15, 0.15], facecolor=axcolor)

        self.__check = CheckButtons(rax, self.__labels, visibility)
        self.__check.on_clicked(self.__func)

        self.can.draw()

    # # ========= TYPES METHODS ============

    def __ViewMethod(self):

        # (4) Extraemos los datos
        self.__nsegments = self._nseg.value()
        self.__nparticle = self._npart.value()
        self.__type_method = str(self._style_method.currentText())
        # Filtramos los datos para trabajar
        # data_processed = DataProcessed(self.data_base, npart=self.__nparticle, type_plot="Ionizaciones")
        # Procesamos los datos
        self.track = ProcessingTrack(self.data_base, npart=self.__nparticle, nseg=self.__nsegments)

        # ', 'LET', 'LET_Process', "Resultado Final"]
        if self.__type_method == 'Methods of approximation':

            self.can.deleteLater()

            line1 = self.track.dict_data['Linear']['Line']
            line2 = self.track.dict_data['Ang_Linear']['Line']
            line3 = self.track.dict_data['Centerline']['Line']
            line4 = self.track.dict_data['Fit_Line_Seg']['Line']

            self.__labels = ['Linear', 'Ang_Linear', 'Centerline', 'Fit_Line_Seg', 'Ionizations']

            # Ploteamos los resultados
            self.fig = Figure(figsize=(2, 2))
            self.can = FigureCanvasQTAgg(self.fig)
            # self.toolbar = NavigationToolbar2QT(self.can, self)
            # self.cllayout.addWidget(self.toolbar)
            self.cllayout.addWidget(self.can)

            # here you can set up your figure/axis
            self.ax = self.can.figure.add_subplot(111, projection='3d')
            matplotlib.rcParams.update({'font.size': 8})

            surf1, = self.ax.plot3D(line1[:,0], line1[:,1], line1[:,2], 'b-', label=self.__labels[0])
            surf2, = self.ax.plot3D(line2[:,0], line2[:,1], line2[:,2], 'r-', label=self.__labels[1])
            surf3, = self.ax.plot3D(line3[:,0], line3[:,1], line3[:,2], 'g-', label=self.__labels[2])
            surf4, = self.ax.plot3D(line4[:,0], line4[:,1], line4[:,2], 'o-', label=self.__labels[3])
            surf5, = self.ax.plot3D(self.track.dict_data['Linear']['Data'][:,0],
                                    self.track.dict_data['Linear']['Data'][:,1],
                                    self.track.dict_data['Linear']['Data'][:,2],
                                    'ko',alpha=0.3, label=self.__labels[4])

            # ----------------------------------------------------------
            # Metodos visualizacion
            self.__lines = [surf1, surf2, surf3, surf4, surf5]

            self.ax.legend(loc="upper left", fontsize=10)
            self.ax.set_xlabel('X [cm]')
            self.ax.set_ylabel('Y [cm]')
            self.ax.set_zlabel('Z [cm]')

            visibility = [line.get_visible() for line in self.__lines]
            axcolor = 'lightgoldenrodyellow'
            rax = self.can.figure.add_axes([0.05, 0.7, 0.15, 0.15], facecolor=axcolor)

            self.__check = CheckButtons(rax, self.__labels, visibility)
            self.__check.on_clicked(self.__func)

            self.can.draw()

        elif self.__type_method == 'LET':

            # --------------------------------------------------------
            # Extraemos los datos y los trayectos aproximados con cada técnica

            self.can.deleteLater()

            line1 = self.track.dict_data['Linear']['Line']
            line2 = self.track.dict_data['Ang_Linear']['Line']
            line3 = self.track.dict_data['Centerline']['Line']
            line4 = self.track.dict_data['Fit_Line_Seg']['Line']

            data1 = self.track.dict_data['Linear']['Track']
            data2 = self.track.dict_data['Ang_Linear']['Track']
            data3 = self.track.dict_data['Centerline']['Track']
            data4 = self.track.dict_data['Fit_Line_Seg']['Track']

            data = self.track.dict_data['Fit_Line_Seg']['Data']

            self.__labels = ['Linear', 'Ang_Linear', 'Centerline', 'Fit_Line_Seg', 'Interactions']

            # --------------------------------------------------------
            # Creamos las figuras

            # Ploteamos los resultados
            self.fig = Figure(figsize=(2, 2))
            self.can = FigureCanvasQTAgg(self.fig)
            # self.toolbar = NavigationToolbar2QT(self.can, self)
            # self.cllayout.addWidget(self.toolbar)
            self.cllayout.addWidget(self.can)

            self.grid = gridspec.GridSpec(2, 4, wspace=0.4, hspace=0.3)
            self.main_ax = self.can.figure.add_subplot(self.grid[:, :2],projection='3d')
            self.xx_hist = self.can.figure.add_subplot(self.grid[0, 2])
            self.xy_hist = self.can.figure.add_subplot(self.grid[0, 3])
            self.yx_hist = self.can.figure.add_subplot(self.grid[1, 2])
            self.yy_hist = self.can.figure.add_subplot(self.grid[1, 3])
            matplotlib.rcParams.update({'font.size': 8})

            # mpl.rcParams['font.size'] = 7
            #
            # ---------------------------------------------------------
            # Rellenamos las figuras con los datos
            # Main_ax
            surf1, = self.main_ax.plot3D(line1[:,0], line1[:,1], line1[:,2], 'm-', label=self.__labels[0])
            surf2, = self.main_ax.plot3D(line2[:,0], line2[:,1], line2[:,2], 'r-', label=self.__labels[1])
            surf3, = self.main_ax.plot3D(line3[:,0], line3[:,1], line3[:,2], 'g-', label=self.__labels[2])
            surf4, = self.main_ax.plot3D(line4[:,0], line4[:,1], line4[:,2], 'b-', label=self.__labels[3])
            surf5, = self.main_ax.plot3D(data[:,0], data[:,1], data[:,2], 'ko', alpha=0.3, label=self.__labels[4])

            # Note: location, length_seg, direction_seg, wt_hi, let_f, ions_segment
            let1 = np.array(data1["let_seg"])
            let2 = np.array(data2["let_seg"])
            let3 = np.array(data3["let_seg"])
            let4 = np.array(data4["let_seg"])

            # -------------------------------------------------------
            # Armamos los histogramas con los datos de los let

            dat1 = {'S{}'.format(i+1):value for i,value in enumerate(let1)}
            seg = list(dat1.keys())
            values = list(dat1.values())
            hist1 = self.xx_hist.bar(seg, values, width=.4, color='purple')

            dat2 = {'S{}'.format(i+1):value for i,value in enumerate(let2)}
            seg = list(dat2.keys())
            values = list(dat2.values())
            hist2 = self.xy_hist.bar(seg, values, width=.4, color='red')

            dat3 = {'S{}'.format(i+1):value for i,value in enumerate(let3)}
            seg = list(dat3.keys())
            values = list(dat3.values())
            hist3 = self.yx_hist.bar(seg, values, width=.4, color='green')

            dat4 = {'S{}'.format(i+1):value for i,value in enumerate(let4)}
            seg = list(dat4.keys())
            values = list(dat4.values())
            hist4 = self.yy_hist.bar(seg, values, width=.4, color='blue')

            self.xx_hist.set_title('Linear')
            self.xy_hist.set_title('Ang_Linear')
            self.yx_hist.set_title('Centerline')
            self.yy_hist.set_title('Fit_Line_Seg')
            self.xx_hist.set_xlabel('Div. Track')
            self.xx_hist.set_ylabel('keV/um')
            self.xy_hist.set_xlabel('Div. Track')
            self.xy_hist.set_ylabel('keV/um')
            self.yx_hist.set_xlabel('Div. Track')
            self.yx_hist.set_ylabel('keV/um')
            self.yy_hist.set_xlabel('Div. Track')
            self.yy_hist.set_ylabel('keV/um')

            # ----------------------------------------------------------
            # Opciones y configuraciones del PLOT

            self.__lines = [surf1, surf2, surf3, surf4, surf5]

            self.main_ax.legend(loc="upper right", fontsize=9)
            self.main_ax.set_xlabel('X [cm]')
            self.main_ax.set_ylabel('Y [cm]')
            self.main_ax.set_zlabel('Z [cm]')

            visibility = [line.get_visible() for line in self.__lines]
            axcolor = 'lightgoldenrodyellow'
            rax = self.can.figure.add_axes([0.05, 0.7, 0.08, 0.15], facecolor=axcolor)

            self.__check = CheckButtons(rax, self.__labels, visibility)
            self.__check.on_clicked(self.__func)
            self.can.draw()

    # # ========= TYPES LET ============

    def __ViewLet(self):

        # (4) Extraemos los datos
        self.__nsegments = self._nseg.value()
        self.__nparticle = self._npart.value()
        self.__method = str(self._method.currentText())

        # Filtramos los datos para trabajar
        # data_processed = DataProcessed(self.data_base, npart=self.__nparticle, type_plot="Ionizaciones")
        # Procesamos los datos
        self.track = ProcessingTrack(self.data_base, npart=self.__nparticle, nseg=self.__nsegments)

        # ----------------------------------------------------------
        # (2) Extraemos los datos
        # line1, data1 = ProcessingTrackOfParticle(pri, method='Linear', div=div)
        self.can.deleteLater()

        line1 = self.track.dict_data[self.__method]['Line']
        data1 = self.track.dict_data[self.__method]['Track']
        data = self.track.dict_data[self.__method]['Data']

        pri_i = self.track.dict_data[self.__method]['Ionizations']
        pri_n = self.track.dict_data[self.__method]['No_ionizations']

        ene_seg = data1["ene_seg"]
        length_seg = data1["len_seg"]
        inte_total = data1["ion_seg"]
        let = data1["let_seg"]

        # --------------------------------------------------------
        # Creamos las figuras

        # Ploteamos los resultados
        self.fig = Figure(figsize=(2, 2))
        self.can = FigureCanvasQTAgg(self.fig)
        # self.toolbar = NavigationToolbar2QT(self.can, self)
        # self.cllayout.addWidget(self.toolbar)
        self.cllayout.addWidget(self.can)
        # location, length_seg, direction, wt_hi, let_f, ions_segment, inte_total

        # --------------------------------------------------------
        # (3) Creamos las figuras
        fig = plt.figure()
        self.ax_main1 = self.can.figure.add_subplot(121, projection='3d')
        self.ax_main2 = self.can.figure.add_subplot(122)

        matplotlib.rcParams.update({'font.size': 8})
        # ax_main1

        surf1, = self.ax_main1.plot3D(pri_i[:,0], pri_i[:,1], pri_i[:,2], 'bo', alpha=0.3, label='Ionizations')
        surf2, = self.ax_main1.plot3D(pri_n[:,0], pri_n[:,1], pri_n[:,2], 'ko', alpha=0.2, label='No ionizations')
        surf3, = self.ax_main1.plot3D(line1[:,0], line1[:,1], line1[:,2], 'r-', alpha=0.4, label=self.__method)
        surf4, = self.ax_main1.plot3D(line1[:,0], line1[:,1], line1[:,2], 'go', alpha=0.4, label='Seg.Limits')

        data = np.array(inte_total[0])
        lc = Line3DCollection(data, linewidths=0.7, colors='b', alpha=0.5, label='Distance')
        surf5 = self.ax_main1.add_collection(lc)

        self.ax_main1.legend(loc="upper right", fontsize=9)
        self.ax_main1.set_xlabel('Eje X [cm]')
        self.ax_main1.set_ylabel('Eje Y [cm]')
        self.ax_main1.set_zlabel('Eje Z [cm]')
        # ax_main1.set_xticks(fontsize=7)
        # ax_main1.set_yticks(fontsize=7)
        # ax_main1.set_zticks(fontsize=7)

        # ax_main2
        divn = np.arange(1,5)
        dat2 = {'S{}'.format(i+1):value for i,value in enumerate(let)}
        seg_label = list(dat2.keys())
        values = list(dat2.values())
        self.bar = self.ax_main2.bar(seg_label, values, width=.4, color='red')

        for rect,e,le in zip(self.bar, ene_seg, length_seg):
            height = rect.get_height()
            self.ax_main2.text(rect.get_x() + rect.get_width() / 2.0, height, f'{height:.2f}', ha='center', va='bottom')

        self.ax_main2.set_xlabel('Segments')
        self.ax_main2.set_ylabel('LET [keV/um]')

        # ---------------------
        # Barra controladora 1

        self.__lines = [surf1, surf2, surf3, surf4, surf5]
        self.__labels = ['Ionizaciones', 'No ionizaciones', self.__method, 'Seg.Limits', 'Distance']

        visibility = [line.get_visible() for line in self.__lines]
        axcolor = 'lightgoldenrodyellow'
        rax = self.can.figure.add_axes([0.05, 0.7, 0.08, 0.15], facecolor=axcolor)
        self.__check = CheckButtons(rax, self.__labels, visibility)
        self.__check.on_clicked(self.__func)

        # --------------------
        # Barra controladora 2
        self.ax_seg = self.can.figure.add_axes([0.25, 0.01, 0.65, 0.03])
        sseg = Slider(
            self.ax_seg, "Segments", 0, self.__nsegments-2,
            valinit=1, valstep=1,
            initcolor='none'  # Remove the line marking the valinit position.
        )

        def change(val):
            seg = sseg.val

            data = np.array(inte_total[seg])
            # ll = Line3DCollection(data, linewidths=0.5, colors='b')
            lc.set_segments(data)

            self.can.draw_idle()

        sseg.on_changed(change)

        self.can.draw()

    # # ========= TYPE RESULTS ============

    def __ViewResults(self):

        # (4) Extraemos los datos
        self.__nsegments = self._nseg.value()
        self.__nparticle = self._npart.value()
        self.__type_results = str(self._style_results.currentText())

        # Filtramos los datos para trabajar
        # Procesamos los datos
        self.track = ProcessingTrack(self.data_base, npart=self.__nparticle, nseg=self.__nsegments)

        value_error1 = self.track.dict_data["Linear"]['Error']
        value_error2 = self.track.dict_data["Centerline"]['Error']
        value_error3 = self.track.dict_data["Ang_Linear"]['Error']
        value_error4 = self.track.dict_data["Fit_Line_Seg"]['Error']

        list_method = ["Linear", "Centerline", "Ang_Linear", "Fit_Line_Seg"]
        list_values = []
        for v1,v2,v3,v4 in zip(value_error1,value_error2,value_error3,value_error4):

            dv1 = 1-v1
            dv2 = 1-v2
            dv3 = 1-v3
            dv4 = 1-v4

            list_dv = [dv1,dv2,dv3,dv4]
            min_dv = np.argmin(list_dv)
            list_values.append(min_dv)

        num = mode(list_values)
        method_best = list_method[num]

        mean1 = np.mean(value_error1)
        mean2 = np.mean(value_error2)
        mean3 = np.mean(value_error3)
        mean4 = np.mean(value_error4)
        values_error = [mean1, mean2, mean3, mean4]

        self.__method_best = method_best
        self.values_error = values_error


        # ----------------------------------------------------------
        # (2) Extraemos los datos
        # line1, data1 = ProcessingTrackOfParticle(pri, method='Linear', div=div)
        self.can.deleteLater()

        line1 = self.track.dict_data[self.__method_best]['Line']
        data1 = self.track.dict_data[self.__method_best]['Track']
        data = self.track.dict_data[self.__method_best]['Data']

        pri_i = self.track.dict_data[self.__method_best]['Ionizations']
        pri_n = self.track.dict_data[self.__method_best]['No_ionizations']

        # ----------------------------------------------------------
        # (2) Extraemos los datos
        # line1, data1 = ProcessingTrackOfParticle(pri, method='Linear', div=div)

        ene_seg = data1["ene_seg"]
        length_seg = data1["len_seg"]
        inte_total = data1["ion_seg"]
        let = data1["let_seg"]

        # --------------------------------------------------------
        # (3) Creamos las figuras
        # Ploteamos los resultados
        self.fig = Figure(figsize=(2, 2))
        self.can = FigureCanvasQTAgg(self.fig)
        # self.toolbar = NavigationToolbar2QT(self.can, self)
        # self.cllayout.addWidget(self.toolbar)
        self.cllayout.addWidget(self.can)
        # location, length_seg, direction, wt_hi, let_f, ions_segment, inte_total

        # --------------------------------------------------------
        # (3) Creamos las figuras
        fig = plt.figure()
        self.ax_main1 = self.can.figure.add_subplot(121, projection='3d')
        self.ax_main2 = self.can.figure.add_subplot(122)

        matplotlib.rcParams.update({'font.size': 8})

        # ax_main1
        surf1, = self.ax_main1.plot3D(pri_i[:,0], pri_i[:,1], pri_i[:,2], 'bo', alpha=0.3, label='Ionizations')
        surf2, = self.ax_main1.plot3D(pri_n[:,0], pri_n[:,1], pri_n[:,2], 'ko', alpha=0.2, label='Not ionizations')
        surf3, = self.ax_main1.plot3D(line1[:,0], line1[:,1], line1[:,2], 'r-', alpha=0.4, label=self.__method_best)
        surf4, = self.ax_main1.plot3D(line1[:,0], line1[:,1], line1[:,2], 'go', alpha=0.4, label='Seg.Limits')

        data = np.array(inte_total[0])
        lc = Line3DCollection(data, linewidths=0.7, colors='b', alpha=0.5, label='Distance')
        surf5 = self.ax_main1.add_collection(lc)

        self.ax_main1.legend(loc="upper right", fontsize=9)
        self.ax_main1.set_xlabel('X [cm]')
        self.ax_main1.set_ylabel('Y [cm]')
        self.ax_main1.set_zlabel('Z [cm]')

        # ax_main2
        divn = np.arange(1,5)
        dat2 = {'S{}'.format(i+1):value for i,value in enumerate(let)}
        seg_label = list(dat2.keys())
        values = list(dat2.values())
        self.bar = self.ax_main2.bar(seg_label, values, width=.4, color='red')

        for rect,e,le in zip(self.bar, ene_seg, length_seg):
            height = rect.get_height()
            self.ax_main2.text(rect.get_x() + rect.get_width() / 2.0, height, f'{height:.2f}', ha='center', va='bottom')


        self.ax_main2.set_xlabel('Segments')
        self.ax_main2.set_ylabel('LET [keV/um]')

        # ---------------------
        # Barra controladora 1

        self.__lines = [surf1, surf2, surf3, surf4, surf5]
        self.__labels = ['Ionizations', 'Not ionizations', self.__method_best, 'Seg.Limits', 'Distance']

        visibility = [line.get_visible() for line in self.__lines]
        axcolor = 'lightgoldenrodyellow'
        rax = self.can.figure.add_axes([0.05, 0.7, 0.08, 0.15], facecolor=axcolor)
        self.__check = CheckButtons(rax, self.__labels, visibility)
        self.__check.on_clicked(self.__func)

        # --------------------
        # Barra controladora 2
        self.ax_seg = self.can.figure.add_axes([0.25, 0.01, 0.65, 0.03])
        sseg = Slider(
            self.ax_seg, "Segments", 0, self.__nsegments-2,
            valinit=1, valstep=1,
            initcolor='none'  # Remove the line marking the valinit position.
        )

        def change(val):
            seg = sseg.val

            data = np.array(inte_total[seg])
            # ll = Line3DCollection(data, linewidths=0.5, colors='b')
            lc.set_segments(data)

            self.can.draw_idle()

        sseg.on_changed(change)

        self.can.draw()

    def __CreateInputTCAD(self):

        if self.__nsegments is None or  self.__nparticle is None or self.__method_best is None:
            msgBox = QMessageBox()
            msgBox.setText("No se puede crear un INPUT para TCAD. Primero ingresar 'Automated method'.")
            msgBox.setStandardButtons(QMessageBox.Cancel)
            ret = msgBox.exec()
        else:
            # Cargamos el Plot3DView en la pagina principal
            self.inputTCAD = CreateInputTCAD(pathfolder, data=self.track)
            if self.inputTCAD.error:
                msgBox = QMessageBox()
                msgBox.setText("Archivo creado con exito!")
                msgBox.setStandardButtons(QMessageBox.Cancel)
                ret = msgBox.exec()
            else:
                msgBox = QMessageBox()
                msgBox.setText("No se puede crear un INPUT para TCAD.")
                msgBox.setStandardButtons(QMessageBox.Cancel)
                ret = msgBox.exec()

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

        # (2) VENTANA PRINCIPAL
        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)

        self.mpl_can = Plot3DView(data=data_dict)
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



# # # SEGUNDA FORMA
# def extract_geometric_vertices_from_detector(data, several_elements=True):
#
#     def data_for_cylinder(data_list,radius):
#
#         if len(data_list[0]) != 1:
#             center_y = data_list[1][0]
#             center_z = data_list[2][0]
#
#             x = np.linspace(data_list[0][0], data_list[0][1], 50)
#             theta = np.linspace(0, 2*np.pi, 50)
#             theta_grid, x_grid=np.meshgrid(theta, x)
#             y_grid = radius*np.cos(theta_grid) + center_y
#             z_grid = radius*np.sin(theta_grid) + center_z
#
#             # Vector director del eje.
#             p0 = np.array([data_list[0][0],data_list[1][0],data_list[2][0]])
#             p1 = np.array([data_list[0][1],data_list[1][0],data_list[2][0]])
#             v = p1 - p0
#             # Calculamos la magnitud del vector.
#             mag = np.linalg.norm(v)
#             # Vector unitario en la direccion del eje.
#             v = v / mag
#             # Otro vector con distinta direccion
#             not_v = np.array([0, 1, 0])
#             # Vector perpendicular a v
#             n1 = np.cross(v, not_v)
#             # Normalizamos n1
#             n1 /= np.linalg.norm(n1)
#
#             # Vector unitario perpendicular a v y n1
#             n2 = np.cross(v, n1)
#
#             rsample = np.linspace(0, radius, 2)
#             rsample,theta = np.meshgrid(rsample, theta)
#
#             # "Bottom"
#             tapa_1 = [p0[i] + rsample[i] * np.sin(theta) * n1[i] + rsample[i] * np.cos(theta) * n2[i] for i in [0, 1, 2]]
#
#             # "Top"
#             tapa_2 = [p0[i] + v[i]*mag + rsample[i] * np.sin(theta) * n1[i] + rsample[i] * np.cos(theta) * n2[i] for i in [0, 1, 2]]
#
#         if len(data_list[1]) != 1:
#             center_x = data_list[0][0]
#             center_z = data_list[2][0]
#
#             y = np.linspace(data_list[1][0], data_list[1][1], 50)
#             theta = np.linspace(0, 2*np.pi, 50)
#             theta_grid, y_grid=np.meshgrid(theta, y)
#             x_grid = radius*np.cos(theta_grid) + center_x
#             z_grid = radius*np.sin(theta_grid) + center_z
#
#         if len(data_list[1]) != 1:
#             center_x = data_list[0][0]
#             center_y = data_list[1][0]
#
#             z = np.linspace(data_list[2][0], data_list[2][1], 50)
#             theta = np.linspace(0, 2*np.pi, 50)
#             theta_grid, z_grid=np.meshgrid(theta, z)
#             x_grid = radius*np.cos(theta_grid) + center_x
#             y_grid = radius*np.sin(theta_grid) + center_y
#
#         return x_grid,y_grid,z_grid,tapa_1,tapa_2
#
#     def data_for_prism(data_list):
#         vertex_coord = list(itertools.product(*data_list))
#         points = np.array(vertex_coord)
#         matrix = [[1,0,0],[0,1,0],[0,0,1]]
#         Z = np.zeros((8,3))
#         for i in range(len(points)):
#             Z[i,:] = np.dot(points[i,:],matrix)
#         # Lista de las caras del poligono que forma el detector.
#         verts = [[Z[0],Z[1],Z[3],Z[2]],
#                  [Z[3],Z[2],Z[6],Z[7]],
#                  [Z[6],Z[7],Z[5],Z[4]],
#                  [Z[5],Z[4],Z[0],Z[1]],
#                  [Z[1],Z[3],Z[7],Z[5]],
#                  [Z[0],Z[2],Z[6],Z[4]]]
#         return Z, verts
#
#     def data_for_sphere(data_list, r):
#
#         # if not data_list:
#
#         center_x = data_list[0][0]
#         center_y = data_list[1][0]
#         center_z = data_list[2][0]
#
#         resolution = 100
#         u, v = np.mgrid[0:2*np.pi:resolution*2j, -np.pi:np.pi:resolution*1j]
#         # u = np.linspace(0, 2 * np.pi, 100)
#         # v = np.linspace(0, np.pi, 100)
#
#         x = r*3* np.cos(u)* np.sin(v) + center_x
#         y = r*3* np.sin(u)* np.sin(v) + center_y
#         z = r*3* np.cos(v) + center_z
#
#         return x,y,z
#
#     # --------------------------------------------------------------------------
#     # (1) Ubicamos el archivo al cual vamos extraer los datos
#     dict_mat = {k:[] for k in ['AXX','AXY','AXZ','AYY','AYZ','AZZ']}
#     dict_pos = {k:[] for k in ['AX','AY','AZ']}
#     dict_shi =  {k:[] for k in ['XSH','YSH','ZSH']}
#     dict_rad = {k:[] for k in ['XSC','YSC','ZSC']}
#
#
#     surface = data['Data Surfaces']
#     for num in surface.keys():
#         if surface[num]['AX'] != []:
#             if surface[num]['A0'] != []:
#                 dict_pos['AX'].append(surface[num]['A0'][0])
#             else:
#                 dict_pos['AX'].append(surface[num]['AX'][0])
#
#         if surface[num]['AY'] != []:
#             if surface[num]['A0'] != []:
#                 dict_pos['AY'].append(surface[num]['A0'][0])
#             else:
#                 dict_pos['AY'].append(surface[num]['AY'][0])
#
#         if surface[num]['AZ'] != []:
#             if surface[num]['A0'] != []:
#                 dict_pos['AZ'].append(surface[num]['A0'][0])
#             else:
#                 dict_pos['AZ'].append(surface[num]['AZ'][0])
#
#         if surface[num]['XSC'] != []:
#             dict_rad['XSC'].append(surface[num]['XSC'][0])
#         if surface[num]['YSC'] != []:
#             dict_rad['YSC'].append(surface[num]['YSC'][0])
#         if surface[num]['ZSC'] != []:
#             dict_rad['ZSC'].append(surface[num]['ZSC'][0])
#
#         if surface[num]['XSH'] != []:
#             dict_pos['AX'].append(surface[num]['XSH'][0])
#         if surface[num]['YSH'] != []:
#             dict_pos['AY'].append(surface[num]['YSH'][0])
#         if surface[num]['ZSH'] != []:
#             dict_pos['AZ'].append(surface[num]['ZSH'][0])
#
#     type_body = data['Geometry']
#
#     # --- Ordenamos las coordenadas de menor a mayor para la posiciones
#     dict_pos['AX'].sort()
#     dict_pos['AY'].sort()
#     dict_pos['AZ'].sort()
#
#
#     data_list = []
#     data_list.append(dict_pos['AX'])
#     data_list.append(dict_pos['AY'])
#     data_list.append(dict_pos['AZ'])
#     # print(data_list)
#
#     if type_body == 'Cylinder':
#
#         rad_list = []
#         rad_list.append(dict_rad['XSC'])
#         rad_list.append(dict_rad['YSC'])
#         rad_list.append(dict_rad['ZSC'])
#
#         if len(rad_list[0]) == 1:
#             R = rad_list[0][0]
#         if len(rad_list[1]) == 1:
#             R = rad_list[1][0]
#         if len(rad_list[2]) == 1:
#             R = rad_list[2][0]
#
#         data_graph = data_for_cylinder(data_list,R)
#
#         if len(data_list[0]) != 1:
#             vdir = data_list[0]
#         if len(data_list[1]) != 1:
#             vdir = data_list[1]
#         if len(data_list[2]) != 1:
#             vdir = data_list[2]
#
#         return data_graph, type_body
#
#     elif type_body == 'Prism':
#
#         data_graph = data_for_prism(data_list)
#
#         normals = []
#         d=[]
#         surface = data['Data Surfaces']
#         for num in surface.keys():
#             dict_pos = {k:[] for k in ['AX','AY','AZ']}
#
#             if surface[num]['AX'] != []:
#                 AX = surface[num]['AX'][0]
#             else:
#                 AX = 0.0
#             if surface[num]['AY'] != []:
#                 AY = surface[num]['AY'][0]
#             else:
#                 AY = 0.0
#             if surface[num]['AZ'] != []:
#                 AZ = surface[num]['AZ'][0]
#             else:
#                 AZ = 0.0
#             if surface[num]['A0'] != []:
#                 A0 = surface[num]['A0'][0]
#             else:
#                 A0 = 0.0
#
#             if surface[num]['XSH'] != []:
#                 AX = surface[num]['XSH'][0]
#                 A0 = 1.0
#             if surface[num]['YSH'] != []:
#                 AY = surface[num]['YSH'][0]
#                 A0 = 1.0
#             if surface[num]['ZSH'] != []:
#                 A0 = 1.0
#                 AZ = surface[num]['ZSH'][0]
#
#
#         matrix = [[1,0,0],[0,1,0],[0,0,1]]
#         Z = np.zeros((8,3))
#         for i in range(len(points)):
#             Z[i,:] = np.dot(points[i,:],matrix)
#         # Lista de las caras del poligono que forma el detector.
#         verts = [[Z[0],Z[1],Z[3],Z[2]],
#                  [Z[3],Z[2],Z[6],Z[7]],
#                  [Z[6],Z[7],Z[5],Z[4]],
#                  [Z[5],Z[4],Z[0],Z[1]],
#                  [Z[1],Z[3],Z[7],Z[5]],
#                  [Z[0],Z[2],Z[6],Z[4]]]
#
#         data_graph = Z, verts
#
#
#         return data_graph, type_body
#     elif type_body == 'Sphere':
#
#         rad_list = []
#         rad_list.append(dict_rad['XSC'])
#         rad_list.append(dict_rad['YSC'])
#         rad_list.append(dict_rad['ZSC'])
#
#         # print(rad_list)
#
#         if len(rad_list[0]) == 1:
#             R = rad_list[0][0]
#         if len(rad_list[1]) == 1:
#             R = rad_list[1][0]
#         if len(rad_list[2]) == 1:
#             R = rad_list[2][0]
#
#         # print(R)
#
#         data_graph = data_for_sphere(data_list,R)
#
#         return data_graph, type_body
#
# pathfolder = "D:\Proyectos_Investigacion\Proyectos_de_Doctorado\Proyectos\SimulationXF_Detectors\Code\RUN\penmain_2018"
#
# # pathfolder = "D:\Proyectos_Investigacion\Proyectos_de_Doctorado\Proyectos\Imaging_XFCT_microCT\Code\RUN\penmain_2018"
# # pathfolder = "D:\Proyectos_Investigacion\Proyectos_de_Doctorado\Proyectos\SimulationXF_Detectors\Code\RUN\penmain_2018"
# geom = LoadDataFileGeometry(pathfolder)
#
# bodysName = [geom.BodysNames]
# num_bodys = 1
#
# print_list_columns(geom.BodysNames, cols=2)
# print('\n')
#
# list_num = geom.GetDataBody.keys()
#
# list_bodys = []
# for i in list(list_num):
#
#     # respuesta = option_list(answer_list=geom.BodysNames, input_type='int', question='¿Que objeto desea agregar?', return_type=True, print_list=False)
#     dbody = geom.GetDataBody[i]
#     if dbody['Type'] != 'MODULE':
#         data_graph, type_body = extract_geometric_vertices_from_detector(dbody)
#
#         if type_body == 'Prism':
#             Z, verts = data_graph
#             x = Z[:,0]
#             y = Z[:,1]
#             z = Z[:,2]
#             i= [7, 0, 0, 0, 4, 4, 6, 1, 4, 0, 3, 6]
#             j= [3, 4, 1, 2, 5, 6, 5, 2, 0, 1, 6, 3]
#             k= [0, 7, 2, 3, 6, 7, 1, 6, 5, 5, 7, 2]
#
#
#             list_bodys.append(go.Mesh3d(x=x, y=y, z=z, alphahull = 0,
#                                         # i=i, j=j, k=k,
#                                         opacity=0.5,
#                                         color='blue'))
#
#
#         if type_body == 'Cylinder':
#
#             # Extraemos los datos del cilindro
#             Xc,Yc,Zc,tapa_1,tapa_2 = data_graph
#             X1,Y1,Z1 = tapa_1
#             X2,Y2,Z2 = tapa_2
#
#             colorscale = [[0, 'blue'],
#                         [1, 'blue']]
#
#             # Superficie del cilindro
#             list_bodys.append(go.Surface(x=Xc, y=Yc, z=Zc,
#                              colorscale = colorscale,
#                              showscale=False,
#                              opacity=0.5))
#
#             # Superficie circulares
#             list_bodys.append(go.Surface(x=X1, y=Y1, z=Z1,
#                              colorscale = colorscale,
#                              showscale=False,
#                              opacity=0.5))
#
#             list_bodys.append(go.Surface(x=X2, y=Y2, z=Z2,
#                              colorscale = colorscale,
#                              showscale=False,
#                              opacity=0.5))
#
#             # # Superficie circulares
#             # list_bodys.append(go.Scatter3d(x = X1.tolist()+[None]+X2.tolist(),
#             #                         y = Y1.tolist()+[None]+Y2.tolist(),
#             #                         z = Z1.tolist()+[None]+Z2.tolist(),
#             #                         # mode ='lines',
#             #                         line = dict(color='blue', width=2),
#             #                         opacity =0.55, showlegend=True))
#
#
#         if type_body == 'Sphere':
#             x,y,z = data_graph
#             colorscale = [[0, 'blue'],
#                           [1, 'blue']]
#             list_bodys.append(go.Surface(x=x, y=y, z=z,
#                              colorscale = colorscale,
#                              showscale=False,
#                              opacity=0.5))
#
#
# # Datos para el eje x
# list_bodys.append(go.Scatter3d(x=[0, 6], y=[0, 0], z=[0, 0], mode='lines', name='X Axis', line=dict(color='red', width=5)))
#
# # Datos para el eje y
# list_bodys.append(go.Scatter3d(x=[0, 0], y=[0, 6], z=[0, 0], mode='lines', name='Y Axis', line=dict(color='green', width=5)))
#
# # Datos para el eje z
# list_bodys.append(go.Scatter3d(x=[0, 0], y=[0, 0], z=[0, 6], mode='lines', name='Z Axis', line=dict(color='blue', width=5)))
#
#
# layout = go.Layout(scene_xaxis_visible=False, scene_yaxis_visible=False, scene_zaxis_visible=False)
# # layout = go.Layout(scene_xaxis_visible=True, scene_yaxis_visible=True, scene_zaxis_visible=True,
# #                   scene = dict(xaxis=dict(range=[-10,10]),
# #                                yaxis=dict(range=[-10,10]),
# #                                zaxis=dict(range=[-10,10])))
#
# fig = go.Figure(data = list_bodys, layout = layout)
# # fig.update_layout(scene_camera_eye_z= 0.55)
# fig.layout.scene.camera.projection.type = "orthographic" #commenting this line you get a fig with perspective proj
#
# fig.show()
