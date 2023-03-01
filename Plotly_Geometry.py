import numpy as np
import plotly.graph_objects as go
from GeomView.main import MainWindow

class Plotly_Geometry:

    def __init__(self):
        tuki=0

    def cylinder(r, h, a=0, nt=100, nv =50):
        """
        parametrize the cylinder of radius r, height h, base point a
        """
        theta = np.linspace(0, 2*np.pi, nt)
        v = np.linspace(a, a+h, nv )
        theta, v = np.meshgrid(theta, v)
        x = r*np.cos(theta)
        y = r*np.sin(theta)
        z = v
        return x, y, z

    def boundary_circle(r, h, nt=100):
        """
        r - boundary circle radius
        h - height above xOy-plane where the circle is included
        returns the circle parameterization
        """
        theta = np.linspace(0, 2*np.pi, nt)
        x= r*np.cos(theta)
        y = r*np.sin(theta)
        z = h*np.ones(theta.shape)
        return x, y, z
    #
    # def paralepipede():
    #     go.Mesh3d(
    #     # 8 vertices of a cube
    #     x=[0.608, 0.608, 0.998, 0.998, 0.608, 0.608, 0.998, 0.998],
    #     y=[0.091, 0.963, 0.963, 0.091, 0.091, 0.963, 0.963, 0.091],
    #     z=[0.140, 0.140, 0.140, 0.140, 0.571, 0.571, 0.571, 0.571],
    #
    #     i = [7, 0, 0, 0, 4, 4, 6, 6, 4, 0, 3, 2],
    #     j = [3, 4, 1, 2, 5, 6, 5, 2, 0, 1, 6, 3],
    #     k = [0, 7, 2, 3, 6, 7, 1, 1, 5, 5, 7, 6],
    #     opacity=0.6,
    #     color='#DC143C',
    #     flatshading = True
    #     )
    #     ])


class GetDataBody:
    def __init__(self):

        mainWin = MainWindow()
        self.num_bodies = len(mainWin.BodyList)

        for num_b in range(self.num_bodies):
            data_body = mainWin.BodyList[num_b]
            self.__data_surfaces = data_body['Surfaces']
            self.__GetBodyTypeWithSurfaces()

    def __GetBodyTypeWithSurfaces(self):

        surfaces = []
        num_surfaces = len(self.__data_surfaces)
        for num_s in range(num_surfaces):
            surface = data_surfaces['S{}'.format(num_s)]
            surfaces.append(surface['Type'])

        if surfaces.count('Plane') == 2 and surfaces.count('Cylinder') == 1:
            type_body = 'Cylinder'
        elif surfaces.count('Plane') == 6:
            type_body = 'Parallelepiped'

        return type_body

    def Cylinder():

        num_surfaces = len(self.__data_surfaces)
        for num_s in range(num_surfaces):

            surface = data_surfaces['S{}'.format(num_s)]
            type_surface = surface['Type']

            pos_surface = surface['Position']
            rot_surface = surface['Rotation']
            sca_surface = surface['Scale']


            if type_surface == 'Plane':

            elif type_surface == 'Cylinder':
                r = np.linalg.norm(sca_surface)
                a1 =




r1 = 2


# ==============================================================================
import itertools
from itertools import groupby
from MonteCarlo.Utils.utils import option_list, print_list_columns
class LoadData_Geometry():

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

    def __find_geometry_main(self, pathfolder):

        print('--------')
        print('GEOMETRY')
        print('--------\n')

        path_files = os.path.join(pathfolder, 'geo')
        files_geometry = [os.path.join(path_files, f) for f in os.listdir(path_files)
            if os.path.isfile(os.path.join(path_files, f)) and f.endswith('.geo')]

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

    def __format_e(self,n):

        a = '%e' % n
        d = a.split('e')[0].rstrip('0').rstrip('.')
        return d[:4] + 'e' + a.split('e')[1][1:]

    def __get_data_main(self):

        string_list = self.__string_list

        # --------------------------------------------------------------------------
        # (1) Abrimos el archivo y extraemos los datos de interes.

        # (1.1) Buscamos las lineas de texto que tengan las superficies que utiliza
        # el body

        # ---
        blocks_limits = []
        for i,line in enumerate(string_list):
            if (line.find('BODY') != -1 or line.find('MODULE') != -1) and (len(line) >15):
                blocks_limits.append((i,line))
            if len(string_list) == i+1:
                blocks_limits.append((i,'END'))

        # ---
        bodys_names = []
        for i, line in enumerate(blocks_limits):
            if not line[1].startswith('END'):
                body = line[1][16:].rstrip('\n').split(' - ')[0]
                bodys_names.append(body)
                self.BodysNames = bodys_names

        # ---
        block_interval = []
        geometry_body = []
        for (i, line) in zip(range(len(blocks_limits)-1),blocks_limits):
            block_interval.append([blocks_limits[i][0],blocks_limits[i+1][0]])
            geometry_body.append(blocks_limits[i][1].rstrip('\n').split(' - ')[1])

        # ---- Cargamos los SURFACE que forman ese/esos body/s.
        list_surfaces = []
        for block in block_interval:
            surfaces = []
            for i, line in enumerate(string_list[block[0]:block[1]]):
                if line.find('SURFACE') != -1 :
                    surfaces.append(int(line.rstrip('\n').split(',')[0][-3:-1]))
            list_surfaces.append(surfaces)

        # (2.2) Obtenemos los datos de cada superficie.

        # ---- Buscamos las medidas de los surfaces cargados.
        for i,line in enumerate(string_list):
            if line.find('BODYS') != -1:
                string_surface_list = string_list[:i]

        markers = []
        for i,line in enumerate(string_surface_list):
            if line.startswith('0'):
                markers.append(i)

        data_surface = []
        for i in range(1,len(markers)):
            string_surface_block = string_surface_list[markers[i-1]+1:markers[i]]
            surface = {k:[] for k in ['SURFACE', 'TYPE','X','Y','Z','XS','YS','ZS']}

            for j, line in enumerate(string_surface_block):
                if not line.startswith('C'):
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
                    if line.startswith('X-SHIFT'):
                        x = float(line.split('=(')[1].split(',')[0])
                        surface['X'].append(x)
                    if line.startswith('Y-SHIFT'):
                        y = float(line.split('=(')[1].split(',')[0])
                        surface['Y'].append(y)
                    if line.startswith('Z-SHIFT'):
                        z = float(line.split('=(')[1].split(',')[0])
                        surface['Z'].append(z)

                    if line.startswith('     AX'):
                        xline = string_surface_block[-1]
                        if xline.startswith('     A0'):
                            x=-1.0*float(xline.split('=(')[1].split(',')[0])
                            surface['X'].append(x)
                    if line.startswith('     AY'):
                        yline = string_surface_block[-1]
                        if yline.startswith('     A0'):
                            y=-1.0*float(yline.split('=(')[1].split(',')[0])
                            surface['Y'].append(y)
                    if line.startswith('     AZ'):
                        zline = string_surface_block[-1]
                        if zline.startswith('     A0'):
                            z=-1.0*float(zline.split('=(')[1].split(',')[0])
                            surface['Z'].append(z)

                    if line.startswith('X-SCALE'):
                        xs = float(line.split('=(')[1].split(',')[0])
                        surface['XS'].append(xs)
                    if line.startswith('Y-SCALE'):
                        ys = float(line.split('=(')[1].split(',')[0])
                        surface['YS'].append(ys)
                    if line.startswith('Z-SCALE'):
                        zs = float(line.split('=(')[1].split(',')[0])
                        surface['ZS'].append(zs)

            data_surface.append(surface)

        ds = {data_surface[j]['SURFACE'][0]:data_surface[j] for j in range(len(data_surface))}

        list_param = ['Geometry','Surfaces']

        db = {k:{list_param[0]:geometry_body[i], list_param[1]:[ds[list_surfaces[i][j]] for j in range(len(list_surfaces[i]))] } for i,k in enumerate(bodys_names)}

        self.GetDataBody = db
        # self.GetDataSurface = ds

    def reset_materials(self):

        # Cargamos el texto de GEOMETRY
        string_list = self.__string_list
        path = self.path

        # ------------------------------------------------
        # (1) Detectamos los BODY y MODULE.

        bodys_detect = [(i,f.split()[2:4]) for i,f in enumerate(string_list) if (f.startswith('BODY') or f.startswith('MODULE')) and len(f)>15]

        bodys_detect = [(f[0],int(f[1][0].rstrip(")")),f[1][1]) for f in bodys_detect]

        bodys_list = list(set([f[2] for f in bodys_detect]))
        bodys_list.sort()

        # Tomamos los materiales de los BODY y MODULE
        material_list = [f[3:].rstrip("\n").rstrip(' ').lstrip(' ').split(' -> ') for f in string_list if (f.startswith('\t-'))]

        data_list = []
        for bd in bodys_detect:
            for ml in material_list:
                if bd[2] == ml[2]:
                    data_list.append((bd[0], bd[1], bd[2], int(ml[0])))


        # -----------------------------------------------------
        # (2) Preguntamos si modificamos o no la presencia de los BODYS

        respuesta = option_list(input_type='string', question='¿Desea modificar la presencia de algun BODY en la simulación?', return_type=False)

        if respuesta:

            # --------------------------------------------------
            # Convertimos en vacio todos los materiales de los BODY y MODULE

            for body in bodys_detect:
                string_list[body[0]+1] = 'MATERIAL(   0)\n'

            my_file = open('{}'.format(path),'w')
            new_file_contents = "".join(string_list)
            my_file.write(new_file_contents)
            my_file.close()

            # --------------------------------------------------------------------------
            # Preguntamos cual se quiere modificar

            print('--- Lista de cuerpos detectados:\n')

            temp = True
            while temp:

                respuesta = option_list(answer_list=bodys_list, input_type='int', question='Ingresar el cuerpo que desea modificar', return_type=False)

                for body in data_list:
                    if body[2] == bodys_list[respuesta]:
                        string_list[body[0]+1] = 'MATERIAL(   {})\n'.format(body[3])

                my_file = open('{}'.format(path),'w')
                new_file_contents = "".join(string_list)
                my_file.write(new_file_contents)
                my_file.close()

                continuar = option_list(input_type='string', question='¿Desea continuar modificando?', return_type=False)

                if continuar:
                    temp = True
                else:
                    temp = False

        else:

            for body in data_list:
                string_list[body[0]+1] = 'MATERIAL(   {})\n'.format(body[3])

            my_file = open('{}'.format(path),'w')
            new_file_contents = "".join(string_list)
            my_file.write(new_file_contents)
            my_file.close()


        self.__get_data_main()

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

        u = np.linspace(0, 2 * np.pi, 100)
        v = np.linspace(0, np.pi, 100)

        x = r*2 * np.outer(np.cos(u), np.sin(v)) + center_x
        y = r*2 * np.outer(np.sin(u), np.sin(v)) + center_y
        z = r*2 * np.outer(np.ones(np.size(u)), np.cos(v)) + center_z

        return x,y,z

    # --------------------------------------------------------------------------
    # (1) Ubicamos el archivo al cual vamos extraer los datos

    dict_pos = {k:[] for k in ['X','Y','Z']}
    dict_rad =  {k:[] for k in ['XS','YS','ZS']}
    for surface in data['Surfaces']:
        if surface['X'] != []:
            dict_pos['X'].append(surface['X'][0])
        if surface['Y'] != []:
            dict_pos['Y'].append(surface['Y'][0])
        if surface['Z'] != []:
            dict_pos['Z'].append(surface['Z'][0])
        if surface['XS'] != []:
            dict_rad['XS'].append(surface['XS'][0])
        if surface['YS'] != []:
            dict_rad['YS'].append(surface['YS'][0])
        if surface['ZS'] != []:
            dict_rad['ZS'].append(surface['ZS'][0])

    type_body = data['Geometry']

    # --- Ordenamos las coordenadas de menor a mayor para la posiciones
    dict_pos['X'].sort()
    dict_pos['Y'].sort()
    dict_pos['Z'].sort()

    data_list = []
    data_list.append(dict_pos['X'])
    data_list.append(dict_pos['Y'])
    data_list.append(dict_pos['Z'])

    if type_body == 'Cylinder':

        rad_list = []
        rad_list.append(dict_rad['XS'])
        rad_list.append(dict_rad['YS'])
        rad_list.append(dict_rad['ZS'])

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
        rad_list.append(dict_rad['XS'])
        rad_list.append(dict_rad['YS'])
        rad_list.append(dict_rad['ZS'])

        if len(rad_list[0]) == 1:
            R = rad_list[0][0]
        if len(rad_list[1]) == 1:
            R = rad_list[1][0]
        if len(rad_list[2]) == 1:
            R = rad_list[2][0]

        data_graph = data_for_sphere(data_list,R)

        return data_graph, type_body


pathfolder = "D:\Proyectos_Investigacion\Proyectos_de_Doctorado\Proyectos\Imaging_XFCT_microCT\Code\RUN\penmain_2018"
# pathfolder = "D:\Proyectos_Investigacion\Proyectos_de_Doctorado\Proyectos\SimulationXF_Detectors\Code\RUN\penmain_2018"
geom = LoadData_Geometry(pathfolder)

bodysName = geom.BodysNames
num_bodys = 10

print_list_columns(geom.BodysNames, cols=2)
print('\n')

list_bodys = []
for i in range(num_bodys):

    respuesta = option_list(answer_list=geom.BodysNames, input_type='int', question='¿Que objeto desea agregar?', return_type=True, print_list=False)
    dbody = geom.GetDataBody[respuesta]

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

        list_bodys.append(go.Surface(x=x, y=y, z=z,
                         colorscale = colorscale,
                         showscale=False,
                         opacity=0.5))

layout = go.Layout(scene_xaxis_visible=False, scene_yaxis_visible=False, scene_zaxis_visible=False)
fig =  go.Figure(data=list_bodys, layout=layout)

fig.update_layout(scene_camera_eye_z= 0.55)
fig.layout.scene.camera.projection.type = "orthographic" #commenting this line you get a fig with perspective proj

fig.show()
