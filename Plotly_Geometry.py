import os
import numpy as np
import plotly.graph_objects as go
from GeomView.main import MainWindow
#
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
        blocks_surfaces = []
        blocks_bodys = []
        for i, block in enumerate(blocks_limits):
            for line in string_list[block[0]:block[1]]:
                if line.startswith('SURFACE'):
                    blocks_surfaces.append(block)
                    break
                if line.startswith('BODY') or line.startswith('MODULE'):
                    blocks_bodys.append(block)
                    break

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

            list_detect = list(np.arange(1,13,1))
            num_detect =  option_list(list_detect, input_type='int', question='¿Cuantos desea agregar?', return_type=True)

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

                print('N={}'.format(n))
                print('({})'.format(v_translate))
                X_shift = vpos_target[0] - vpos_new_detect[0]
                Y_shift = vpos_target[1] - vpos_new_detect[1]
                Z_shift = vpos_new_detect[2] - vpos_target[2]
                # X_shift = vpos_new_detect[0] + vpos_target[0]
                # Y_shift = vpos_new_detect[1] + vpos_target[0]
                # Z_shift = vpos_new_detect[2]
                #
                # X_shift = 0.0
                # Y_shift = 0.0
                # Z_shift = 0.0
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
                omega = 0
                theta = 0
                phi = angle*n*180/np.pi

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

        pathfile = os.path.join('D:\\',*path.split('\\')[1:-1], 'detector.geo')

        my_file = open('{}'.format(pathfile),'w')
        new_file_contents = "".join(new_string)
        my_file.write(new_file_contents)
        my_file.close()

        # --------------------------------------------------------------------------
        # Preguntamos cual se quiere modificar


        self.__get_data_main()


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



def extract_geometric_vertices_from_detector(data, several_elements=True):

    def data_for_cylinder(data_list,radius):

        if len(data_list[0]) != 1:
            center_y = data_list[1][0]
            center_z = data_list[2][0]

            x = np.linspace(data_list[0][0], data_list[0][1], 50)
            theta = np.linspace(0, 2*np.pi, 50)
            theta_grid, x_grid=np.meshgrid(theta, x)
            y_grid = radius*np.cos(theta_grid) + center_y
            z_grid = radius*np.sin(theta_grid) + center_z

            # Vector director del eje.
            p0 = np.array([data_list[0][0],data_list[1][0],data_list[2][0]])
            p1 = np.array([data_list[0][1],data_list[1][0],data_list[2][0]])
            v = p1 - p0
            # Calculamos la magnitud del vector.
            mag = np.linalg.norm(v)
            # Vector unitario en la direccion del eje.
            v = v / mag
            # Otro vector con distinta direccion
            not_v = np.array([0, 1, 0])
            # Vector perpendicular a v
            n1 = np.cross(v, not_v)
            # Normalizamos n1
            n1 /= np.linalg.norm(n1)

            # Vector unitario perpendicular a v y n1
            n2 = np.cross(v, n1)

            rsample = np.linspace(0, radius, 2)
            rsample,theta = np.meshgrid(rsample, theta)

            # "Bottom"
            tapa_1 = [p0[i] + rsample[i] * np.sin(theta) * n1[i] + rsample[i] * np.cos(theta) * n2[i] for i in [0, 1, 2]]

            # "Top"
            tapa_2 = [p0[i] + v[i]*mag + rsample[i] * np.sin(theta) * n1[i] + rsample[i] * np.cos(theta) * n2[i] for i in [0, 1, 2]]

        if len(data_list[1]) != 1:
            center_x = data_list[0][0]
            center_z = data_list[2][0]

            y = np.linspace(data_list[1][0], data_list[1][1], 50)
            theta = np.linspace(0, 2*np.pi, 50)
            theta_grid, y_grid=np.meshgrid(theta, y)
            x_grid = radius*np.cos(theta_grid) + center_x
            z_grid = radius*np.sin(theta_grid) + center_z

        if len(data_list[1]) != 1:
            center_x = data_list[0][0]
            center_y = data_list[1][0]

            z = np.linspace(data_list[2][0], data_list[2][1], 50)
            theta = np.linspace(0, 2*np.pi, 50)
            theta_grid, z_grid=np.meshgrid(theta, z)
            x_grid = radius*np.cos(theta_grid) + center_x
            y_grid = radius*np.sin(theta_grid) + center_y

        return x_grid,y_grid,z_grid,tapa_1,tapa_2

    def data_for_prism(data_list):
        vertex_coord = list(itertools.product(*data_list))
        points = np.array(vertex_coord)
        matrix = [[1,0,0],[0,1,0],[0,0,1]]
        Z = np.zeros((8,3))
        for i in range(len(points)):
            Z[i,:] = np.dot(points[i,:],matrix)
        # Lista de las caras del poligono que forma el detector.
        verts = [[Z[0],Z[1],Z[3],Z[2]],
                 [Z[3],Z[2],Z[6],Z[7]],
                 [Z[6],Z[7],Z[5],Z[4]],
                 [Z[5],Z[4],Z[0],Z[1]],
                 [Z[1],Z[3],Z[7],Z[5]],
                 [Z[0],Z[2],Z[6],Z[4]]]
        return Z, verts

    def data_for_sphere(data_list, r):

        # if not data_list:

        center_x = data_list[0][0]
        center_y = data_list[1][0]
        center_z = data_list[2][0]

        resolution = 100
        u, v = np.mgrid[0:2*np.pi:resolution*2j, -np.pi:np.pi:resolution*1j]
        # u = np.linspace(0, 2 * np.pi, 100)
        # v = np.linspace(0, np.pi, 100)

        x = r*3* np.cos(u)* np.sin(v) + center_x
        y = r*3* np.sin(u)* np.sin(v) + center_y
        z = r*3* np.cos(v) + center_z

        return x,y,z

    # --------------------------------------------------------------------------
    # (1) Ubicamos el archivo al cual vamos extraer los datos
    dict_mat = {k:[] for k in ['AXX','AXY','AXZ','AYY','AYZ','AZZ']}
    dict_pos = {k:[] for k in ['AX','AY','AZ']}
    dict_shi =  {k:[] for k in ['XSH','YSH','ZSH']}
    dict_rad = {k:[] for k in ['XSC','YSC','ZSC']}

    surface = data['Data Surfaces']
    for num in surface.keys():
        if surface[num]['AX'] != []:
            if surface[num]['A0'] != []:
                dict_pos['AX'].append(surface[num]['A0'][0])
            else:
                dict_pos['AX'].append(surface[num]['AX'][0])

        if surface[num]['AY'] != []:
            if surface[num]['A0'] != []:
                dict_pos['AY'].append(surface[num]['A0'][0])
            else:
                dict_pos['AY'].append(surface[num]['AY'][0])

        if surface[num]['AZ'] != []:
            if surface[num]['A0'] != []:
                dict_pos['AZ'].append(surface[num]['A0'][0])
            else:
                dict_pos['AZ'].append(surface[num]['AZ'][0])

        if surface[num]['XSC'] != []:
            dict_rad['XSC'].append(surface[num]['XSC'][0])
        if surface[num]['YSC'] != []:
            dict_rad['YSC'].append(surface[num]['YSC'][0])
        if surface[num]['ZSC'] != []:
            dict_rad['ZSC'].append(surface[num]['ZSC'][0])

        if surface[num]['XSH'] != []:
            dict_pos['AX'].append(surface[num]['XSH'][0])
        if surface[num]['YSH'] != []:
            dict_pos['AY'].append(surface[num]['YSH'][0])
        if surface[num]['ZSH'] != []:
            dict_pos['AZ'].append(surface[num]['ZSH'][0])

    type_body = data['Geometry']

    # --- Ordenamos las coordenadas de menor a mayor para la posiciones
    dict_pos['AX'].sort()
    dict_pos['AY'].sort()
    dict_pos['AZ'].sort()

    data_list = []
    data_list.append(dict_pos['AX'])
    data_list.append(dict_pos['AY'])
    data_list.append(dict_pos['AZ'])
    # print(data_list)

    if type_body == 'Cylinder':

        rad_list = []
        rad_list.append(dict_rad['XSC'])
        rad_list.append(dict_rad['YSC'])
        rad_list.append(dict_rad['ZSC'])

        if len(rad_list[0]) == 1:
            R = rad_list[0][0]
        if len(rad_list[1]) == 1:
            R = rad_list[1][0]
        if len(rad_list[2]) == 1:
            R = rad_list[2][0]

        data_graph = data_for_cylinder(data_list,R)

        if len(data_list[0]) != 1:
            vdir = data_list[0]
        if len(data_list[1]) != 1:
            vdir = data_list[1]
        if len(data_list[2]) != 1:
            vdir = data_list[2]

        return data_graph, type_body

    elif type_body == 'Prism':

        data_graph = data_for_prism(data_list)
        return data_graph, type_body

    elif type_body == 'Sphere':

        rad_list = []
        rad_list.append(dict_rad['XSC'])
        rad_list.append(dict_rad['YSC'])
        rad_list.append(dict_rad['ZSC'])

        # print(rad_list)

        if len(rad_list[0]) == 1:
            R = rad_list[0][0]
        if len(rad_list[1]) == 1:
            R = rad_list[1][0]
        if len(rad_list[2]) == 1:
            R = rad_list[2][0]

        # print(R)

        data_graph = data_for_sphere(data_list,R)

        return data_graph, type_body








pathfolder = "D:\Proyectos_Investigacion\Proyectos_de_Doctorado\Proyectos\SimulationXF_Detectors\Code\RUN\penmain_2018"

# pathfolder = "D:\Proyectos_Investigacion\Proyectos_de_Doctorado\Proyectos\Imaging_XFCT_microCT\Code\RUN\penmain_2018"
# pathfolder = "D:\Proyectos_Investigacion\Proyectos_de_Doctorado\Proyectos\SimulationXF_Detectors\Code\RUN\penmain_2018"
geom = LoadData_Geometry(pathfolder)

bodysName = [geom.BodysNames]
num_bodys = 1

print_list_columns(geom.BodysNames, cols=2)
print('\n')

list_num = geom.GetDataBody.keys()



list_bodys = []
for i in list(list_num):

        # respuesta = option_list(answer_list=geom.BodysNames, input_type='int', question='¿Que objeto desea agregar?', return_type=True, print_list=False)
        dbody = geom.GetDataBody[i]

        data_graph, type_body = extract_geometric_vertices_from_detector(dbody)

        if type_body == 'Prism':
            Z, verts = data_graph
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


        if type_body == 'Cylinder':

            # Extraemos los datos del cilindro
            Xc,Yc,Zc,tapa_1,tapa_2 = data_graph
            X1,Y1,Z1 = tapa_1
            X2,Y2,Z2 = tapa_2

            colorscale = [[0, 'blue'],
                        [1, 'blue']]

            # Superficie del cilindro
            list_bodys.append(go.Surface(x=Xc, y=Yc, z=Zc,
                             colorscale = colorscale,
                             showscale=False,
                             opacity=0.5))

            # Superficie circulares
            list_bodys.append(go.Surface(x=X1, y=Y1, z=Z1,
                             colorscale = colorscale,
                             showscale=False,
                             opacity=0.5))

            list_bodys.append(go.Surface(x=X2, y=Y2, z=Z2,
                             colorscale = colorscale,
                             showscale=False,
                             opacity=0.5))

            # # Superficie circulares
            # list_bodys.append(go.Scatter3d(x = X1.tolist()+[None]+X2.tolist(),
            #                         y = Y1.tolist()+[None]+Y2.tolist(),
            #                         z = Z1.tolist()+[None]+Z2.tolist(),
            #                         # mode ='lines',
            #                         line = dict(color='blue', width=2),
            #                         opacity =0.55, showlegend=True))


        if type_body == 'Sphere':
            x,y,z = data_graph
            colorscale = [[0, 'blue'],
                          [1, 'blue']]
            list_bodys.append(go.Surface(x=x, y=y, z=z,
                             colorscale = colorscale,
                             showscale=False,
                             opacity=0.5))




layout = go.Layout(scene_xaxis_visible=False, scene_yaxis_visible=False, scene_zaxis_visible=False)
# layout = go.Layout(scene_xaxis_visible=True, scene_yaxis_visible=True, scene_zaxis_visible=True,
#                   scene = dict(xaxis=dict(range=[-10,10]),
#                                yaxis=dict(range=[-10,10]),
#                                zaxis=dict(range=[-10,10])))

fig = go.Figure(data = list_bodys, layout = layout)
# fig.update_layout(scene_camera_eye_z= 0.55)
fig.layout.scene.camera.projection.type = "orthographic" #commenting this line you get a fig with perspective proj

fig.show()
