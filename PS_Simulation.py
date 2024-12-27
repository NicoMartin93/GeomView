
import os
import sys
import re
import numpy as np
import shutil
import plotly.graph_objects as go
import subprocess
from itertools import groupby

class GeomGenerator():

    def __init__(self):

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
