
import os
import sys
import re
import numpy as np
import plotly.graph_objects as go
import subprocess
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
#
# class LoadVoxGeom():
#
#     class Coordinate():
#
#         def __init__(self, xyz):
#             self.x = xyz[0]
#             self.y = xyz[1]
#             self.z = xyz[2]
#
#     class VoxelData():
#
#         def __init__(self,data):
#         print("Making voxels")
#         self.data = data
#         self.triangles = np.zeros((np.size(np.shape(self.data)),1))
#         self.xyz = self.get_coords()
#         # self.x = self.xyz[0,:]
#         # self.y = self.xyz[1,:]
#         # self.z = self.xyz[2,:]
#         self.x_length = np.size(data,0)
#         self.y_length = np.size(data,1)
#         self.z_length = np.size(data,2)
#         self.vert_count = 0
#         self.vertices = self.make_edge_verts()
#         self.triangles = np.delete(self.triangles, 0,1)
#         #self.make_triangles()
#
#
#         def get_coords(self):
#             indices = np.nonzero(self.data)
#             indices = np.stack((indices[0], indices[1],indices[2]))
#             return indices
#
#         def has_voxel(self,neighbor_coord):
#             return self.data[neighbor_coord[0],neighbor_coord[1],neighbor_coord[2]]
#
#
#         def get_neighbor(self, voxel_coords, direction):
#             x = voxel_coords[0]
#             y = voxel_coords[1]
#             z = voxel_coords[2]
#             offset_to_check = CubeData.offsets[direction]
#             neighbor_coord = [x+ offset_to_check[0], y+offset_to_check[1], z+offset_to_check[2]]
#
#             # return 0 if neighbor out of bounds or nonexistent
#             if (any(np.less(neighbor_coord,0)) | (neighbor_coord[0] >= self.x_length) | (neighbor_coord[1] >= self.y_length) | (neighbor_coord[2] >= self.z_length)):
#                 return 0
#             else:
#                 return self.has_voxel(neighbor_coord)
#
#
#         def remove_redundant_coords(self, cube):
#             i = 0
#             while(i < np.size(cube,1)):
#                 coord = (cube.T)[i]
#                 cu = cube[:, cube[0,:] == coord[0]]
#                 cu = cu[:, cu[1,:] == coord[1]]
#                 cu = cu[:, cu[2,:] == coord[2]]
#                 # if more than one coord of same value, delete
#                 if i >= np.size(cube,1):
#                     break
#                 if np.size(cu, 1) >1:
#                     cube = np.delete(cube, i, 1)
#                     i = i-1
#                 i+=1
#             return cube
#
#
#         def make_face(self, voxel, direction):
#             voxel_coords = self.xyz[:, voxel]
#             explicit_dir = CubeData.direction[direction]
#             vert_order = CubeData.face_triangles[explicit_dir]
#
#             # Use if triangle order gets fixed
#             # next_triangles = np.add(vert_order, voxel)
#             # next_i = [next_triangles[0], next_triangles[0]]
#             # next_j = [next_triangles[1], next_triangles[2]]
#             # next_k = [next_triangles[2], next_triangles[3]]
#
#             next_i = [self.vert_count, self.vert_count]
#             next_j = [self.vert_count+1, self.vert_count+2]
#             next_k = [self.vert_count+2, self.vert_count+3]
#
#             next_tri = np.vstack((next_i, next_j, next_k))
#             self.triangles = np.hstack((self.triangles, next_tri))
#             # self.triangles = np.vstack((self.triangles, next_triangles))
#
#             face_verts = np.zeros((len(voxel_coords),len(vert_order)))
#             for i in range(len(vert_order)):
#                 face_verts[:,i] = voxel_coords + CubeData.cube_verts[vert_order[i]]
#
#             self.vert_count = self.vert_count+4
#             return face_verts
#
#
#         def make_cube_verts(self, voxel):
#             voxel_coords = self.xyz[:, voxel]
#             cube = np.zeros((len(voxel_coords), 1))
#
#             # only make a new face if there's no neighbor in that direction
#             dirs_no_neighbor = []
#             for direction in range(len(CubeData.direction)):
#                 if np.any(self.get_neighbor(voxel_coords, direction)):
#                     continue
#                 else:
#                     dirs_no_neighbor = np.append(dirs_no_neighbor, direction)
#                     face = self.make_face(voxel, direction)
#                     cube = np.append(cube,face, axis=1)
#
#             # remove cube initialization
#             cube = np.delete(cube, 0, 1)
#
#             # remove redundant entries: not doing this cuz it messes up the triangle order
#             # and i'm too lazy to fix that so excess vertices it is
#             # cube = self.remove_redundant_coords(cube)
#             return cube
#
#
#         def make_edge_verts(self):
#             # make only outer vertices
#             edge_verts = np.zeros((np.size(self.xyz, 0),1))
#             num_voxels = np.size(self.xyz, 1)
#             for voxel in range(num_voxels):
#                 cube = self.make_cube_verts(voxel)          # passing voxel num rather than
#                 edge_verts = np.append(edge_verts, cube, axis=1)
#             edge_verts = np.delete(edge_verts, 0,1)
#             return edge_verts
#
#     class CubeData:
#         # all data and knowledge from https://github.com/boardtobits/procedural-mesh-tutorial/blob/master/CubeMeshData.cs
#         # for creating faces correctly by direction
#         face_triangles = {
#     		'North':  [0, 1, 2, 3 ],        # +y
#             'East': [ 5, 0, 3, 6 ],         # +x
#     	    'South': [ 4, 5, 6, 7 ],        # -y
#             'West': [ 1, 4, 7, 2 ],         # -x
#             'Up': [ 5, 4, 1, 0 ],           # +z
#             'Down': [ 3, 2, 7, 6 ]          # -z
#     	}
#
#         cube_verts = [
#             [1,1,1],
#             [0,1,1],
#             [0,1,0],
#             [1,1,0],
#             [0,0,1],
#             [1,0,1],
#             [1,0,0],
#             [0,0,0],
#         ]
#
#         # cool twist
#         # cube_verts = [
#         #     [0,0,0],
#         #     [1,0,0],
#         #     [1,0,1],
#         #     [0,0,1],
#         #     [0,1,1],
#         #     [1,1,1],
#         #     [1,1,0],
#         #     [0,1,0],
#         # ]
#
#         # og
#         # cube_verts = [
#         #     [1,1,1],
#         #     [0,1,1],
#         #     [0,0,1],
#         #     [1,0,1],
#         #     [0,1,0],
#         #     [1,1,0],
#         #     [1,0,0],
#         #     [0,0,0]
#         # ]
#
#         direction = [
#             'North',
#             'East',
#             'South',
#             'West',
#             'Up',
#             'Down'
#         ]
#
#         opposing_directions = [
#             ['North','South'],
#             ['East','West'],
#             ['Up', 'Down']
#         ]
#
#         # xyz direction corresponding to 'Direction'
#         offsets = [
#             [0, 1, 0],
#             [1, 0, 0],
#             [0, -1, 0],
#             [-1, 0, 0],
#             [0, 0, 1],
#             [0, 0, -1],
#         ]
#         # offsets = [
#         #     [0, 0, 1],
#         #     [1, 0, 0],
#         #     [0, 0, -1],
#         #     [-1, 0, 0],
#         #     [0, 1, 0],
#         #     [0, -1, 0]
#         # ]
#
#     # ------------
#     # LOADER DATA
#
#     import os
#     import os.path
#     import numpy as np
#     from toy_volume_gen_class import Toy_Volume
#     from random import randint
#
#
#     EXTENSIONS = ['.npy', '.NPY']
#
#     def is_acceptable(filename):
#         return any(filename.endswith(extension) for extension in EXTENSIONS)
#
#     def load_data(opt):
#         data_paths = []
#         data = []
#
#         # Read in all numpy arrays in curr dir unless 'filename' was specified
#         if not opt.file_name:         # if no filename given
#             assert os.path.isdir(opt.dataroot), '%s is not a valid directory' % opt.dataroot
#
#             for root, dir, fnames in sorted(os.walk(opt.dataroot)):
#                 for fname in fnames:
#                     if is_acceptable(fname):
#                         data_path = os.path.join(root,fname)
#                         data_paths.append(data_path)
#         else:
#             data_paths = opt.file_name
#
#         # Make toy dataset if no files found or opt set
#         if opt.toy_dataset:
#             print('Making toy dataset')
#             d = opt.toy_dataset
#             # data = np.floor(np.random.rand(d,d,d)*2)
#             # data = data > 0
#
#             n_reps, n_classes = 4, 3
#             width, height, depth = d,d,d
#             colour_channels = 3
#
#             td = Toy_Volume(n_classes, width, height, depth, colour_channels)
#
#             for rep in range(n_reps):
#                 for colour_idx in range(n_classes):
#                     #td.set_colour_to_random_xyz(colour_idx)
#                     x, y, z = td.get_random_xyz()
#                     rand_x_len = randint(1, int(td.width/4))
#                     rand_y_len = randint(1, int(td.height/4))
#                     rand_z_len = randint(1, int(td.depth/4))
#                     rnd_i = randint(0, 1)
#                     if rnd_i == 0:
#                         td.set_rect_cuboid_to_xyz(x, y, z,
#                                                 rand_x_len, rand_y_len, rand_z_len,
#                                                 colour_idx)
#                     elif rnd_i == 1:
#                         td.set_ellipsoid_to_xyz(x, y, z,
#                                                 rand_x_len, rand_y_len, rand_z_len,
#                                                 colour_idx)
#
#             data = td.volume
#             data = data[:,:,:,1]
#
#         else:
#             assert data_paths, 'The directory %s does not contain files with valid extensions %s' % (opt.dataroot, EXTENSIONS)
#             print("data_paths", data_paths)
#             data = np.load(data_paths)
#
#
#         return data
#
#     ##########################################################################################################
#     # Joe's toy_volume_gen.py script below so i can use the volume for trial
#     ##########################################################################################################
#
#     import numpy as np
#     from random import randint
#
#
#     class Toy_Volume:
#         def __init__(self, n_classes, width, height, depth, colour_channels=3):
#             self.init_check(n_classes, width, height, depth, colour_channels)
#             self.n_classes = n_classes
#             self.width = width
#             self.height = height
#             self.depth = depth
#             self.colour_channels = colour_channels
#             self.class_colours = Toy_Volume.get_class_colours(n_classes, colour_channels)
#             self.volume = self.get_empty_array()
#             self.one_hot_array = self.get_empty_array(channels=self.n_classes)
#
#         def init_check(self, n_classes, width, height, depth, colour_channels):
#             assert type(n_classes) is int, "n_classes must be of type int"
#             assert n_classes > 0, "Need at least one class"
#             assert width > 0, "Need postive width"
#             assert height > 0, "Need positive height"
#             assert depth > 0, "Need positive depth"
#             assert (colour_channels == 3) or (colour_channels == 1), "Either RGB or grayscale"
#
#         @staticmethod
#         def get_class_colours(n_classes, colour_channels):
#             """ Generates random colours to be visualised with and returns the list """
#             classes = []
#             for class_idx in range(n_classes):
#                 count = 0
#                 valid = False
#                 while( not valid ):
#                     colour = Toy_Volume.get_random_colour(colour_channels)
#                     if colour not in classes:
#                         classes.append(colour)
#                         valid = True
#             return classes
#
#         @staticmethod
#         def get_random_colour(colour_channels):
#             """ Returns a random colour """
#             if colour_channels == 1:
#                 return [randint(0,255)]
#             return [randint(0,255)/255,randint(0,255)/255,randint(0,255)/255]
#
#         def get_empty_array(self, channels=None):
#             """ Empty starting array """
#             if channels is None:
#                 channels = self.colour_channels
#             return np.zeros([self.width, self.height, self.depth, channels], dtype=float)
#
#         def get_random_xyz(self):
#             x = randint(0, self.width-1)
#             y = randint(0, self.height-1)
#             z = randint(0, self.depth-1)
#             return x, y, z
#
#         def set_colour_to_xyz(self, x, y, z, colour_idx):
#             """ Sets the colour for a specific pixel """
#             if self.colour_channels == 1:
#                 self.volume[x][y][z][0] = self.class_colours[colour_idx][0]
#             else:
#                 self.volume[x][y][z][0] = self.class_colours[colour_idx][0]
#                 self.volume[x][y][z][1] = self.class_colours[colour_idx][1]
#                 self.volume[x][y][z][2] = self.class_colours[colour_idx][2]
#             self.one_hot_array[x][y][z][:] = 0
#             self.one_hot_array[x][y][z][colour_idx] = 1
#
#         def set_colour_to_random_xyz(self, colour_idx):
#             self.set_colour_to_xyz(*self.get_random_xyz(), colour_idx)
#
#         def get_volume_cube_range(self, x, y, z, length):
#             assert type(length) is int, "length must be an int, it should be half the width of the object"
#             (x_min, x_max) = self.get_axis_range(x, length, self.width)
#             (y_min, y_max) = self.get_axis_range(y, length, self.height)
#             (z_min, z_max) = self.get_axis_range(z, length, self.depth)
#             return (x_min, x_max), (y_min, y_max), (z_min, z_max)
#
#         def get_axis_range(self, axis_pos, axis_length, frame_length):
#             inputs = (axis_pos, axis_length)
#             (axis_min, axis_max) = (self.get_shape_range_min(*inputs), self.get_shape_range_max(*inputs, frame_length))
#             return (axis_min, axis_max)
#
#         def get_shape_range_min(self, axis_pos, length):
#             assert type(length) is int, "length must be an int"
#             temp_min = axis_pos - length
#             range_min = temp_min if temp_min > 0 else 0
#             return range_min
#
#         def get_shape_range_max(self, axis_pos, length, frame_length):
#             assert type(length) is int, "length must be an int"
#             temp_max = axis_pos + length
#             range_max = temp_max if temp_max < (frame_length - 1) else frame_length
#             return range_max
#
#         def set_rect_cuboid_to_xyz(self, x, y, z,
#                                    x_length, y_length, z_length,
#                                    colour_idx):
#             (x_min, x_max) = self.get_axis_range(x, x_length, self.width)
#             (y_min, y_max) = self.get_axis_range(y, y_length, self.height)
#             (z_min, z_max) = self.get_axis_range(z, z_length, self.depth)
#             for x_ in range(x_min, x_max):
#                 for y_ in range(y_min, y_max):
#                     for z_ in range(z_min, z_max):
#                         self.set_colour_to_xyz(x_, y_, z_, colour_idx)
#
#         def set_cube_to_xyz(self, x, y, z, length, colour_idx):
#             self.set_rect_cuboid_to_xyz(x, y, z, length, length, length, colour_idx)
#
#         def is_in_sphere(self, x, y, z, centre, radius):
#             return self.is_in_ellipsoid(x, y, z, centre, radius, radius, radius)
#
#         def is_in_ellipsoid(self, x, y, z, centre, x_radius, y_radius, z_radius):
#             x_centre, y_centre, z_centre = centre
#             if ((x_centre-x)**2)/x_radius**2 + ((y_centre-y)**2)/y_radius**2 + ((z_centre-z)**2)/z_radius**2 < 1:
#                 return True
#             return False
#
#         def set_sphere_to_xyz(self, x, y, z, radius, colour_idx):
#             self.set_ellipsoid_to_xyz(x, y, z, radius, radius, radius, colour_idx)
#
#         def set_ellipsoid_to_xyz(self, x, y, z, x_radius, y_radius, z_radius, colour_idx):
#             (x_min, x_max) = self.get_axis_range(x, x_radius, self.width)
#             (y_min, y_max) = self.get_axis_range(y, y_radius, self.height)
#             (z_min, z_max) = self.get_axis_range(z, z_radius, self.depth)
#             for x_ in range(x_min, x_max):
#                 for y_ in range(y_min, y_max):
#                     for z_ in range(z_min, z_max):
#                         if self.is_in_ellipsoid(x_, y_, z_, (x, y, z), x_radius, y_radius, z_radius):
#                             self.set_colour_to_xyz(x_, y_, z_, colour_idx)
#
#
#     def get_test_volumes(n_volumes, n_reps, n_classes,
#                          width, height, depth, colour_channels):
#         #volumes, one_hots = [], []
#         volumes, one_hots = None, None
#
#         return volumes, one_hots
#
#     def plot_volume(volume, show=True):
#         voxel = volume[:,:,:,0] > 0
#         import matplotlib.pyplot as plt
#         from mpl_toolkits.mplot3d import Axes3D
#         fig = plt.figure()
#         ax = fig.gca(projection='3d')
#         ax.voxels(voxel, facecolors=volume, linewidth=0.5)
#         if show:
#             plt.show()
#
#
#     def rgb_to_hex(rgb):
#         assert type(rgb) is list
#         assert len(rgb) == 3
#         assert all((0 <= col < 256 and type(col) is int) for col in rgb), "The colours must be an int from 0 to 255"
#         return '#%02x%02x%02x' % tuple(rgb)
#
#     if __name__ == "__main__":
#         n_reps, n_classes = 4, 3
#         width, height, depth = 100, 100, 100
#         colour_channels = 3
#
#         td = Toy_Volume(n_classes, width, height, depth, colour_channels)
#
#         for rep in range(n_reps):
#             for colour_idx in range(n_classes):
#                 #td.set_colour_to_random_xyz(colour_idx)
#                 x, y, z = td.get_random_xyz()
#                 rand_x_len = randint(1, int(td.width/4))
#                 rand_y_len = randint(1, int(td.height/4))
#                 rand_z_len = randint(1, int(td.depth/4))
#                 rnd_i = randint(0, 1)
#                 if rnd_i == 0:
#                     td.set_rect_cuboid_to_xyz(x, y, z,
#                                               rand_x_len, rand_y_len, rand_z_len,
#                                               colour_idx)
#                 elif rnd_i == 1:
#                     td.set_ellipsoid_to_xyz(x, y, z,
#                                             rand_x_len, rand_y_len, rand_z_len,
#                                             colour_idx)
#
#
#
#     ##########################################################################################################
#     # End joe's toy_volume_gen.py (copied as is)
#     ##########################################################################################################
#
#     from options import Options
#     from data_loader import load_data
#     from VoxelData import VoxelData
#     import plotly.graph_objects as go
#     import matplotlib.pyplot as plt
#     import numpy as np
#
#     if __name__ == "__main__":
#
#         opt = Options().parse()
#         data = load_data(opt)
#
#         Voxels = VoxelData(data)
#         # print("Voxels.data\n",Voxels.data)
#         # print("Voxels.vertices\n",Voxels.vertices)
#         # print("Voxels.triangles\n",Voxels.triangles)
#
#         print("Generating figure")
#         fig = go.Figure(data=go.Mesh3d(
#             x=Voxels.vertices[0],
#             y=Voxels.vertices[1],
#             z=Voxels.vertices[2],
#             i=Voxels.triangles[0],
#             j=Voxels.triangles[1],
#             k=Voxels.triangles[2]
#             ))
#         fig.show()
#



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

        if basename.startswith('fln-impdet'):
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
        for n in range(0,nplanes+1):
            print(n)
            alpha=n*angle
            print(alpha)
            Z, verts =  self.PutTogetherPlanes(plane=plane, alpha=alpha , radio=radio, dimensions=dimensions)

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

# # # PRIMERA FORMA
# pathfolder = "D:\Proyectos_Investigacion\Proyectos_de_Doctorado\Proyectos\SimulationXF_Detectors\Code\RUN\penmain_2018"
# cdetectors = CircleDetectors(pathfolder)
# #

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
    if list_name == 'type_plot':
        style_list = ['Espectro antes del detector', 'Espectro despues del detector', 'Espacio de fase', 'Fluencia antes del detector']
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
        self._type_plot = QComboBox()
        init_widget(self._type_plot, "styleComboBox")
        self._type_plot.addItems(style_names(list_name='type_plot'))

        # Detector para visualizar
        self._nbody = QDoubleSpinBox()
        self._nbody.setPrefix("Detector: ")
        self._nbody.setValue(1)
        self._nbody.setRange(1, self.num_bodys)
        init_widget(self._nbody, "xdim")

        # Boton de ejecución para visualizar el plot elegido
        self.button_view = QPushButton("Ver")
        init_widget(self.button_view, "view_label")


        # # Agregamos el layout
        self.llayout = QVBoxLayout()
        self.llayout.setContentsMargins(1, 1, 1, 1)

        self.label1 = QLabel("PLOTS DE DATOS")
        self.label1.setStyleSheet("border: 2px solid gray; position: center;")
        self.llayout.addWidget(self.label1)

        self.llayout.addWidget(QLabel("Datos para visualizar:"))
        self.llayout.addWidget(self._type_plot)



        self.llayout.addWidget(QLabel("Detector:"))
        self.llayout.addWidget(self._nbody)

        self.llayout.addWidget(self.button_view)

        self.llayout.addStretch()

        # # Agregamos las Conexiones
        self.button_view.clicked.connect(self.__ViewPlot)

        # --------------------------------------------------
        # # Panel DERECHO - PLOTS

        self.rlayout = QVBoxLayout()
        self.rlayout.setContentsMargins(1, 1, 1, 1)
        self.fig = Figure(figsize=(2, 2))
        self.can = FigureCanvasQTAgg(self.fig)
        self.rlayout.addWidget(self.can)

    def __sourcePut(self, state):

        if state == Qt.Checked:
            self._xs.setVisible(True)
            self._ys.setVisible(True)
            self._zs.setVisible(True)
            self._activeSource = True
        else:
            self._xs.setVisible(False)
            self._ys.setVisible(False)
            self._zs.setVisible(False)
            self._activeSource = False

    def __func(self,label):
        index = self.__labels.index(label)
        self.__plots[index].set_visible(not self.__plots[index].get_visible())
        self.can.draw()

    def __ViewPlot(self):

        # (1) Extraemos los datos
        ibody = str(self._nbody.value()).split('.')[0]
        if len(ibody) < 2:
            ibody = '0'+ibody
        type_plot = str(self._type_plot.currentText())

        if type_plot == 'Espectro antes del detector':

            # (1) --- SEPARAMOS LOS DATOS
            # Separamos los datos
            column = self.database['spc-impdet'][ibody].GetTitlesColumns
            data = self.database['spc-impdet'][ibody].GetDataColumns
            units = self.database['spc-impdet'][ibody].GetUnits
            title = self.database['spc-impdet'][ibody].GetTitle

            energy = data[column[0]]
            den_prob = data[column[1]]
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

            self.__labels = [column[1],column[3],column[5], column[7]]
            print(column)
            # here you can set up your figure/axis
            self.ax = self.can.figure.add_subplot(111)
            matplotlib.rcParams.update({'font.size': 8})

            plot1, = self.ax.plot(energy, den_prob, 'b-', label=self.__labels[0])
            plot2, = self.ax.plot(energy, dp_electron, 'r-', label=self.__labels[1])
            plot3, = self.ax.plot(energy, dp_fotones, 'g-', label=self.__labels[2])
            plot4, = self.ax.plot(energy, dp_positrons, 'y-', label=self.__labels[3])

            self.__plots = [plot1, plot2, plot3, plot4]

            self.ax.legend(loc="upper left", fontsize=10)
            self.ax.set_xlabel('{}'.format(units[0]))
            self.ax.set_ylabel('{}'.format(units[1]))
            self.ax.set_title('{}'.format(title))

            visibility = [line.get_visible() for line in self.__plots]
            axcolor = 'lightgoldenrodyellow'
            rax = self.can.figure.add_axes([0.8, 0.7, 0.15, 0.15], facecolor=axcolor)

            self.__check = CheckButtons(rax, self.__labels, visibility)
            self.__check.on_clicked(self.__func)

            self.can.draw()

        if type_plot == 'Espectro despues del detector':

            self.can.deleteLater()

            self.fig = Figure(figsize=(2, 2))
            self.can = FigureCanvasQTAgg(self.fig)
            self.rlayout.addWidget(self.can)

            # here you can set up your figure/axis
            self.ax = self.can.figure.add_subplot(111)
            matplotlib.rcParams.update({'font.size': 8})
            print(ibody)
            print(self.database['spc-impdet'])
            # Separamos los datos
            column = self.database['spc-enddet'][ibody].GetTitlesColumns
            data = self.database['spc-enddet'][ibody].GetDataColumns
            units = self.database['spc-enddet'][ibody].GetUnits
            title = self.database['spc-enddet'][ibody].GetTitle

            # Ploteamos los resultados
            self.ax.plot(data[column[0]], data[column[1]])

            self.ax.legend(loc="upper left", fontsize=10)
            self.ax.set_xlabel('{}'.format(units[0]))
            self.ax.set_ylabel('{}'.format(units[1]))
            self.ax.set_title('{}'.format(title))

            self.can.draw()

        if type_plot == 'Fluencia del espacio de fase':

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

        if type_plot == 'Fluencia antes del detector':

            self.can.deleteLater()

            self.fig = Figure(figsize=(2, 2))
            self.can = FigureCanvasQTAgg(self.fig)
            self.rlayout.addWidget(self.can)

            # here you can set up your figure/axis
            self.ax = self.can.figure.add_subplot(111)
            matplotlib.rcParams.update({'font.size': 8})
            print(ibody)
            print(self.database['fln-impdet'])
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
        print(path_geo)
        # -------------------------------------------
        # # INPUT
        # (1) Cargamos el INPUT
        path_input = self.pathFileInput
        print(path_input)

        print(self.pathFileExe)

        # -------------------------------------------
        # # SIMULACION
        # os.system('cls')
        print('-------------------------------------------------------')
        print('INICIO de simulación para un espectro energético: MonoE')
        print('-------------------------------------------------------\n')

        # --------------------------------------------------------
        # # Introducimos el input en el ejecutable.
        path_cwd = os.path.join('D:\\',*self.pathFileExe.split('/')[1:-1])
        print(path_cwd)

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

        print('----------------------------------------------------')
        print('FIN de simulación para un espectro energético: MonoE')
        print('----------------------------------------------------\n')

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

        self.sourcePut = QCheckBox("¿Considerar posición de la fuente?",self)

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

        self.llayout.addWidget(self.sourcePut)
        self.llayout.addWidget(QLabel("Posición de la fuente:"))
        self.horizontalLayou2 = QHBoxLayout()
        self.horizontalLayou2.addWidget(self._xs)
        self.horizontalLayou2.addWidget(self._ys)
        self.horizontalLayou2.addWidget(self._zs)
        self._xs.setVisible(False)
        self._ys.setVisible(False)
        self._zs.setVisible(False)
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
        self.sourcePut.stateChanged.connect(self.__sourcePut)
        # --------------------------------------------------
        # # Panel DERECHO - Definición de configuraciones

        self.cllayout = QVBoxLayout()
        self.cllayout.setContentsMargins(1, 1, 1, 1)
        self.browser = QWebEngineView(self)
        self.cllayout.addWidget(self.browser)

    def __sourcePut(self, state):

        if state == Qt.Checked:
            self._xs.setVisible(True)
            self._ys.setVisible(True)
            self._zs.setVisible(True)
            self._activeSource = True
        else:
            self._xs.setVisible(False)
            self._ys.setVisible(False)
            self._zs.setVisible(False)
            self._activeSource = False


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

        if self._activeSource:
            m=1
        else:
            m=0

        # Definimos unidad angular de partición
        angle = 360/nplanes
        j=0

        for n in range(m,nplanes):
            Z, verts =  self.__PutTogetherPlanes(plane=plane, alpha=n*angle, radio=radio, dimensions=dimensions)

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

        if self._activeSource:
            m=1
        else:
            m=0

        angle = 360/nplanes
        list_bodys = []
        for n in range(m,nplanes):

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
        geometryAction = QAction("Geometría Detector", self, shortcut="Ctrl+L", triggered=self.__geometryDetector)
        circleAction = QAction("Circulo Detectores", self, shortcut="Ctrl+L", triggered=self.__geometryCircle)
        simulateAction = QAction("Simualción", self, shortcut="Ctrl+L", triggered=self.__simulatedPenelope)
        plotsAction = QAction("Plots", self, shortcut="Ctrl+L", triggered=self.__plotsTools)
        # Agregamos las acciones
        toolBar.addAction(geometryAction)
        toolBar.addAction(circleAction)
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

    def __geometryCircle(self):

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
