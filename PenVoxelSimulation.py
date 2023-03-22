


import os
import pydicom
import numpy as np


class LoadVoxGeom():

    class Coordinate():

        def __init__(self, xyz):
            self.x = xyz[0]
            self.y = xyz[1]
            self.z = xyz[2]

    class VoxelData():

        def __init__(self,data):
        print("Making voxels")
        self.data = data
        self.triangles = np.zeros((np.size(np.shape(self.data)),1))
        self.xyz = self.get_coords()
        # self.x = self.xyz[0,:]
        # self.y = self.xyz[1,:]
        # self.z = self.xyz[2,:]
        self.x_length = np.size(data,0)
        self.y_length = np.size(data,1)
        self.z_length = np.size(data,2)
        self.vert_count = 0
        self.vertices = self.make_edge_verts()
        self.triangles = np.delete(self.triangles, 0,1)
        #self.make_triangles()


        def get_coords(self):
            indices = np.nonzero(self.data)
            indices = np.stack((indices[0], indices[1],indices[2]))
            return indices

        def has_voxel(self,neighbor_coord):
            return self.data[neighbor_coord[0],neighbor_coord[1],neighbor_coord[2]]


        def get_neighbor(self, voxel_coords, direction):
            x = voxel_coords[0]
            y = voxel_coords[1]
            z = voxel_coords[2]
            offset_to_check = CubeData.offsets[direction]
            neighbor_coord = [x+ offset_to_check[0], y+offset_to_check[1], z+offset_to_check[2]]

            # return 0 if neighbor out of bounds or nonexistent
            if (any(np.less(neighbor_coord,0)) | (neighbor_coord[0] >= self.x_length) | (neighbor_coord[1] >= self.y_length) | (neighbor_coord[2] >= self.z_length)):
                return 0
            else:
                return self.has_voxel(neighbor_coord)


        def remove_redundant_coords(self, cube):
            i = 0
            while(i < np.size(cube,1)):
                coord = (cube.T)[i]
                cu = cube[:, cube[0,:] == coord[0]]
                cu = cu[:, cu[1,:] == coord[1]]
                cu = cu[:, cu[2,:] == coord[2]]
                # if more than one coord of same value, delete
                if i >= np.size(cube,1):
                    break
                if np.size(cu, 1) >1:
                    cube = np.delete(cube, i, 1)
                    i = i-1
                i+=1
            return cube


        def make_face(self, voxel, direction):
            voxel_coords = self.xyz[:, voxel]
            explicit_dir = CubeData.direction[direction]
            vert_order = CubeData.face_triangles[explicit_dir]

            # Use if triangle order gets fixed
            # next_triangles = np.add(vert_order, voxel)
            # next_i = [next_triangles[0], next_triangles[0]]
            # next_j = [next_triangles[1], next_triangles[2]]
            # next_k = [next_triangles[2], next_triangles[3]]

            next_i = [self.vert_count, self.vert_count]
            next_j = [self.vert_count+1, self.vert_count+2]
            next_k = [self.vert_count+2, self.vert_count+3]

            next_tri = np.vstack((next_i, next_j, next_k))
            self.triangles = np.hstack((self.triangles, next_tri))
            # self.triangles = np.vstack((self.triangles, next_triangles))

            face_verts = np.zeros((len(voxel_coords),len(vert_order)))
            for i in range(len(vert_order)):
                face_verts[:,i] = voxel_coords + CubeData.cube_verts[vert_order[i]]

            self.vert_count = self.vert_count+4
            return face_verts


        def make_cube_verts(self, voxel):
            voxel_coords = self.xyz[:, voxel]
            cube = np.zeros((len(voxel_coords), 1))

            # only make a new face if there's no neighbor in that direction
            dirs_no_neighbor = []
            for direction in range(len(CubeData.direction)):
                if np.any(self.get_neighbor(voxel_coords, direction)):
                    continue
                else:
                    dirs_no_neighbor = np.append(dirs_no_neighbor, direction)
                    face = self.make_face(voxel, direction)
                    cube = np.append(cube,face, axis=1)

            # remove cube initialization
            cube = np.delete(cube, 0, 1)

            # remove redundant entries: not doing this cuz it messes up the triangle order
            # and i'm too lazy to fix that so excess vertices it is
            # cube = self.remove_redundant_coords(cube)
            return cube


        def make_edge_verts(self):
            # make only outer vertices
            edge_verts = np.zeros((np.size(self.xyz, 0),1))
            num_voxels = np.size(self.xyz, 1)
            for voxel in range(num_voxels):
                cube = self.make_cube_verts(voxel)          # passing voxel num rather than
                edge_verts = np.append(edge_verts, cube, axis=1)
            edge_verts = np.delete(edge_verts, 0,1)
            return edge_verts

    class CubeData:
        # all data and knowledge from https://github.com/boardtobits/procedural-mesh-tutorial/blob/master/CubeMeshData.cs
        # for creating faces correctly by direction
        face_triangles = {
    		'North':  [0, 1, 2, 3 ],        # +y
            'East': [ 5, 0, 3, 6 ],         # +x
    	    'South': [ 4, 5, 6, 7 ],        # -y
            'West': [ 1, 4, 7, 2 ],         # -x
            'Up': [ 5, 4, 1, 0 ],           # +z
            'Down': [ 3, 2, 7, 6 ]          # -z
    	}

        cube_verts = [
            [1,1,1],
            [0,1,1],
            [0,1,0],
            [1,1,0],
            [0,0,1],
            [1,0,1],
            [1,0,0],
            [0,0,0],
        ]

        # cool twist
        # cube_verts = [
        #     [0,0,0],
        #     [1,0,0],
        #     [1,0,1],
        #     [0,0,1],
        #     [0,1,1],
        #     [1,1,1],
        #     [1,1,0],
        #     [0,1,0],
        # ]

        # og
        # cube_verts = [
        #     [1,1,1],
        #     [0,1,1],
        #     [0,0,1],
        #     [1,0,1],
        #     [0,1,0],
        #     [1,1,0],
        #     [1,0,0],
        #     [0,0,0]
        # ]

        direction = [
            'North',
            'East',
            'South',
            'West',
            'Up',
            'Down'
        ]

        opposing_directions = [
            ['North','South'],
            ['East','West'],
            ['Up', 'Down']
        ]

        # xyz direction corresponding to 'Direction'
        offsets = [
            [0, 1, 0],
            [1, 0, 0],
            [0, -1, 0],
            [-1, 0, 0],
            [0, 0, 1],
            [0, 0, -1],
        ]
        # offsets = [
        #     [0, 0, 1],
        #     [1, 0, 0],
        #     [0, 0, -1],
        #     [-1, 0, 0],
        #     [0, 1, 0],
        #     [0, -1, 0]
        # ]

    # ------------
    # LOADER DATA

    import os
    import os.path
    import numpy as np
    from toy_volume_gen_class import Toy_Volume
    from random import randint


    EXTENSIONS = ['.npy', '.NPY']

    def is_acceptable(filename):
        return any(filename.endswith(extension) for extension in EXTENSIONS)

    def load_data(opt):
        data_paths = []
        data = []

        # Read in all numpy arrays in curr dir unless 'filename' was specified
        if not opt.file_name:         # if no filename given
            assert os.path.isdir(opt.dataroot), '%s is not a valid directory' % opt.dataroot

            for root, dir, fnames in sorted(os.walk(opt.dataroot)):
                for fname in fnames:
                    if is_acceptable(fname):
                        data_path = os.path.join(root,fname)
                        data_paths.append(data_path)
        else:
            data_paths = opt.file_name

        # Make toy dataset if no files found or opt set
        if opt.toy_dataset:
            print('Making toy dataset')
            d = opt.toy_dataset
            # data = np.floor(np.random.rand(d,d,d)*2)
            # data = data > 0

            n_reps, n_classes = 4, 3
            width, height, depth = d,d,d
            colour_channels = 3

            td = Toy_Volume(n_classes, width, height, depth, colour_channels)

            for rep in range(n_reps):
                for colour_idx in range(n_classes):
                    #td.set_colour_to_random_xyz(colour_idx)
                    x, y, z = td.get_random_xyz()
                    rand_x_len = randint(1, int(td.width/4))
                    rand_y_len = randint(1, int(td.height/4))
                    rand_z_len = randint(1, int(td.depth/4))
                    rnd_i = randint(0, 1)
                    if rnd_i == 0:
                        td.set_rect_cuboid_to_xyz(x, y, z,
                                                rand_x_len, rand_y_len, rand_z_len,
                                                colour_idx)
                    elif rnd_i == 1:
                        td.set_ellipsoid_to_xyz(x, y, z,
                                                rand_x_len, rand_y_len, rand_z_len,
                                                colour_idx)

            data = td.volume
            data = data[:,:,:,1]

        else:
            assert data_paths, 'The directory %s does not contain files with valid extensions %s' % (opt.dataroot, EXTENSIONS)
            print("data_paths", data_paths)
            data = np.load(data_paths)


        return data

    ##########################################################################################################
    # Joe's toy_volume_gen.py script below so i can use the volume for trial
    ##########################################################################################################

    import numpy as np
    from random import randint


    class Toy_Volume:
        def __init__(self, n_classes, width, height, depth, colour_channels=3):
            self.init_check(n_classes, width, height, depth, colour_channels)
            self.n_classes = n_classes
            self.width = width
            self.height = height
            self.depth = depth
            self.colour_channels = colour_channels
            self.class_colours = Toy_Volume.get_class_colours(n_classes, colour_channels)
            self.volume = self.get_empty_array()
            self.one_hot_array = self.get_empty_array(channels=self.n_classes)

        def init_check(self, n_classes, width, height, depth, colour_channels):
            assert type(n_classes) is int, "n_classes must be of type int"
            assert n_classes > 0, "Need at least one class"
            assert width > 0, "Need postive width"
            assert height > 0, "Need positive height"
            assert depth > 0, "Need positive depth"
            assert (colour_channels == 3) or (colour_channels == 1), "Either RGB or grayscale"

        @staticmethod
        def get_class_colours(n_classes, colour_channels):
            """ Generates random colours to be visualised with and returns the list """
            classes = []
            for class_idx in range(n_classes):
                count = 0
                valid = False
                while( not valid ):
                    colour = Toy_Volume.get_random_colour(colour_channels)
                    if colour not in classes:
                        classes.append(colour)
                        valid = True
            return classes

        @staticmethod
        def get_random_colour(colour_channels):
            """ Returns a random colour """
            if colour_channels == 1:
                return [randint(0,255)]
            return [randint(0,255)/255,randint(0,255)/255,randint(0,255)/255]

        def get_empty_array(self, channels=None):
            """ Empty starting array """
            if channels is None:
                channels = self.colour_channels
            return np.zeros([self.width, self.height, self.depth, channels], dtype=float)

        def get_random_xyz(self):
            x = randint(0, self.width-1)
            y = randint(0, self.height-1)
            z = randint(0, self.depth-1)
            return x, y, z

        def set_colour_to_xyz(self, x, y, z, colour_idx):
            """ Sets the colour for a specific pixel """
            if self.colour_channels == 1:
                self.volume[x][y][z][0] = self.class_colours[colour_idx][0]
            else:
                self.volume[x][y][z][0] = self.class_colours[colour_idx][0]
                self.volume[x][y][z][1] = self.class_colours[colour_idx][1]
                self.volume[x][y][z][2] = self.class_colours[colour_idx][2]
            self.one_hot_array[x][y][z][:] = 0
            self.one_hot_array[x][y][z][colour_idx] = 1

        def set_colour_to_random_xyz(self, colour_idx):
            self.set_colour_to_xyz(*self.get_random_xyz(), colour_idx)

        def get_volume_cube_range(self, x, y, z, length):
            assert type(length) is int, "length must be an int, it should be half the width of the object"
            (x_min, x_max) = self.get_axis_range(x, length, self.width)
            (y_min, y_max) = self.get_axis_range(y, length, self.height)
            (z_min, z_max) = self.get_axis_range(z, length, self.depth)
            return (x_min, x_max), (y_min, y_max), (z_min, z_max)

        def get_axis_range(self, axis_pos, axis_length, frame_length):
            inputs = (axis_pos, axis_length)
            (axis_min, axis_max) = (self.get_shape_range_min(*inputs), self.get_shape_range_max(*inputs, frame_length))
            return (axis_min, axis_max)

        def get_shape_range_min(self, axis_pos, length):
            assert type(length) is int, "length must be an int"
            temp_min = axis_pos - length
            range_min = temp_min if temp_min > 0 else 0
            return range_min

        def get_shape_range_max(self, axis_pos, length, frame_length):
            assert type(length) is int, "length must be an int"
            temp_max = axis_pos + length
            range_max = temp_max if temp_max < (frame_length - 1) else frame_length
            return range_max

        def set_rect_cuboid_to_xyz(self, x, y, z,
                                   x_length, y_length, z_length,
                                   colour_idx):
            (x_min, x_max) = self.get_axis_range(x, x_length, self.width)
            (y_min, y_max) = self.get_axis_range(y, y_length, self.height)
            (z_min, z_max) = self.get_axis_range(z, z_length, self.depth)
            for x_ in range(x_min, x_max):
                for y_ in range(y_min, y_max):
                    for z_ in range(z_min, z_max):
                        self.set_colour_to_xyz(x_, y_, z_, colour_idx)

        def set_cube_to_xyz(self, x, y, z, length, colour_idx):
            self.set_rect_cuboid_to_xyz(x, y, z, length, length, length, colour_idx)

        def is_in_sphere(self, x, y, z, centre, radius):
            return self.is_in_ellipsoid(x, y, z, centre, radius, radius, radius)

        def is_in_ellipsoid(self, x, y, z, centre, x_radius, y_radius, z_radius):
            x_centre, y_centre, z_centre = centre
            if ((x_centre-x)**2)/x_radius**2 + ((y_centre-y)**2)/y_radius**2 + ((z_centre-z)**2)/z_radius**2 < 1:
                return True
            return False

        def set_sphere_to_xyz(self, x, y, z, radius, colour_idx):
            self.set_ellipsoid_to_xyz(x, y, z, radius, radius, radius, colour_idx)

        def set_ellipsoid_to_xyz(self, x, y, z, x_radius, y_radius, z_radius, colour_idx):
            (x_min, x_max) = self.get_axis_range(x, x_radius, self.width)
            (y_min, y_max) = self.get_axis_range(y, y_radius, self.height)
            (z_min, z_max) = self.get_axis_range(z, z_radius, self.depth)
            for x_ in range(x_min, x_max):
                for y_ in range(y_min, y_max):
                    for z_ in range(z_min, z_max):
                        if self.is_in_ellipsoid(x_, y_, z_, (x, y, z), x_radius, y_radius, z_radius):
                            self.set_colour_to_xyz(x_, y_, z_, colour_idx)


    def get_test_volumes(n_volumes, n_reps, n_classes,
                         width, height, depth, colour_channels):
        #volumes, one_hots = [], []
        volumes, one_hots = None, None

        return volumes, one_hots

    def plot_volume(volume, show=True):
        voxel = volume[:,:,:,0] > 0
        import matplotlib.pyplot as plt
        from mpl_toolkits.mplot3d import Axes3D
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        ax.voxels(voxel, facecolors=volume, linewidth=0.5)
        if show:
            plt.show()


    def rgb_to_hex(rgb):
        assert type(rgb) is list
        assert len(rgb) == 3
        assert all((0 <= col < 256 and type(col) is int) for col in rgb), "The colours must be an int from 0 to 255"
        return '#%02x%02x%02x' % tuple(rgb)

    if __name__ == "__main__":
        n_reps, n_classes = 4, 3
        width, height, depth = 100, 100, 100
        colour_channels = 3

        td = Toy_Volume(n_classes, width, height, depth, colour_channels)

        for rep in range(n_reps):
            for colour_idx in range(n_classes):
                #td.set_colour_to_random_xyz(colour_idx)
                x, y, z = td.get_random_xyz()
                rand_x_len = randint(1, int(td.width/4))
                rand_y_len = randint(1, int(td.height/4))
                rand_z_len = randint(1, int(td.depth/4))
                rnd_i = randint(0, 1)
                if rnd_i == 0:
                    td.set_rect_cuboid_to_xyz(x, y, z,
                                              rand_x_len, rand_y_len, rand_z_len,
                                              colour_idx)
                elif rnd_i == 1:
                    td.set_ellipsoid_to_xyz(x, y, z,
                                            rand_x_len, rand_y_len, rand_z_len,
                                            colour_idx)



    ##########################################################################################################
    # End joe's toy_volume_gen.py (copied as is)
    ##########################################################################################################

    from options import Options
    from data_loader import load_data
    from VoxelData import VoxelData
    import plotly.graph_objects as go
    import matplotlib.pyplot as plt
    import numpy as np

    if __name__ == "__main__":

        opt = Options().parse()
        data = load_data(opt)

        Voxels = VoxelData(data)
        # print("Voxels.data\n",Voxels.data)
        # print("Voxels.vertices\n",Voxels.vertices)
        # print("Voxels.triangles\n",Voxels.triangles)

        print("Generating figure")
        fig = go.Figure(data=go.Mesh3d(
            x=Voxels.vertices[0],
            y=Voxels.vertices[1],
            z=Voxels.vertices[2],
            i=Voxels.triangles[0],
            j=Voxels.triangles[1],
            k=Voxels.triangles[2]
            ))
        fig.show()



class Voxelgeom:

    def __init__(self):
        self.xbin = None
        self.ybin = None
        self.zbin = None
        self.xFac = None
        self.yFac = None
        self.zFac = None
        self.ihxFac = None
        self.ihyFac = None
        self.ihzFac = None
        self.sqhWx = None
        self.sqhWy = None
        self.sqhWz = None
        self.hnxBin = None
        self.hnyBin = None
        self.hnzBin = None
        self.IndeFac = None
        self.zBinFac = None
        self.Dicom = None

    def DefineBox(self, Wx0, Wy0, Wz0, nxBin0, nyBin0, nzBin0):
        self.nxBin = nxBin0
        self.nyBin = nyBin0
        self.nzBin = nzBin0

        self.hnxBin = (self.nxBin + 1) // 2
        self.hnyBin = (self.nyBin + 1) // 2
        self.hnzBin = (self.nzBin + 1) // 2

        self.xFac = float(self.nxBin) / Wx0
        self.yFac = float(self.nyBin) / Wy0
        self.zFac = float(self.nzBin) / Wz0

        self.ihxFac = 0.5 / self.xFac  # Wx0 / 254d0
        self.ihyFac = 0.5 / self.yFac  # Wy0 / 254d0
        self.ihzFac = 0.5 / self.zFac  # Wz0 / 254d0

        self.hWx = 0.5 * Wx0
        self.hWy = 0.5 * Wy0
        self.hWz = 0.5 * Wz0

        self.sqhWx = (0.5 * Wx0)**2
        self.sqhWy = (0.5 * Wy0)**2
        self.sqhWz = (0.5 * Wz0)**2

        self.zBinFac = self.nxBin * self.nyBin
        self.IndeFac = self.zBinFac + self.nxBin

    def Geomin(self, ParInp, NPInp, NMat, NBody, IRD, IWR):

        NPInp = int(NPInp)
        ParInp = np.array(ParInp, dtype=float)
        self.nxBin = int(input())
        self.nyBin = int(input())
        self.nzBin = int(input())
        vzx = float(input())
        vzy = float(input())
        vzz = float(input())

        self.DefineBox(float(self.nxBin)*vzx*0.1, float(self.nyBin)*vzy*0.1, float(self.nzBin)*vzz*0.1, self.nxBin, self.nyBin, self.nzBin)

        self.NMat = 0

        for k in range(1, self.nzBin+1):
            for j in range(1, self.nyBin+1):
                for i in range(1, self.nxBin+1):
                    Dicom = int(input())
                    self.Dicom[i-1,j-1,k-1] = Dicom
                    if self.NMat < self.Dicom[i-1,j-1,k-1]:
                        self.NMat = Dicom[i-1,j-1,k-1]

        NBody = self.nxBin*self.nyBin*self.nzBin+1

def DicomReader():

    print('Initializing DicomReader...')

    folder_path = 'D:\Proyectos_Investigacion\Proyectos_de_Doctorado\Proyectos\SimulationXF_Detectors\Rata_SegmetacionOro'
    # folder_path = os.getcwd()
    file_list = os.listdir(folder_path)
    n_files = len(file_list)

    rslices = 0  # número de rebanadas leídas correctamente
    sl2 = np.inf

    for c in range(n_files):

      try:
          if os.path.isdir(file_list[c]) == 0:
              info = pydicom.dcmread(os.path.join(folder_path, file_list[c]))

              if info.SOPClassUID == '1.2.840.10008.5.1.4.1.1.2':
                  if rslices == 0:  # crea el búfer
                      dicombuff = np.zeros((info.Rows, info.Columns, n_files), dtype=np.int16)
                      rslices = 1
                      sl1 = info.ImagePositionPatient[2]
                      in1 = info.InstanceNumber

                  # Transponer la imagen leída por dicomread para que el sistema de
                  # coordenadas sea (filas,columna) = (x,y)
                  dicombuff[:, :, info.InstanceNumber - 1] = np.transpose(info.pixel_array)

                  rslices += 1

                  if info.ImagePositionPatient[2] < sl2:
                      sl2 = info.ImagePositionPatient[2]
                      in2 = info.InstanceNumber
                      ctinfo = info

                  print(' file <', file_list[c], '> readed.')

      except Exception as errinfo:
          print(f' Error reading <{file_list[c]}> : {errinfo}')

    rslices -= 1
    print('Processing data...')
    try:
        if (float(sl1) - float(sl2)) / (float(in1) - float(in2)) <= 0:
            # invertir el eje Z para que coincida con las coordenadas DICOM
            Dicom = np.zeros((dicombuff.shape[0], dicombuff.shape[1], rslices), dtype=np.int16)
            for c in range(rslices):
                Dicom[:, :, c] = dicombuff[:, :, rslices - c - 1]

        else:
            Dicom = dicombuff[:, :, :rslices]

    except Exception as errinfo:
        print(f' Error reading: {errinfo}')

    # flip x axis (no se sabe por qué)
    # Dicom = np.flip(Dicom, axis=1)

    print('Finished.')

    return Dicom, ctinfo

def VoxelgeomSaver(filename=None, buff=None, ctinfo=None):
    # ====================================================

    # filename = 'Rata_prueba.voxelgeom'
    # buff = Dicom
    # pixelsize[0] = tensor.spacedirections_matrix[0,0]
    # pixelsize[1] = tensor.spacedirections_matrix[1,1]
    # pixelsize[2] = tensor.spacedirections_matrix[2,2]

    pixelsize = [ctinfo.PixelSpacing[0], ctinfo.PixelSpacing[1], ctinfo.SliceThickness]

    # ====================================================

    with open(filename, 'w') as nfile:
        iF, jF, kF = buff.shape

        # If even, then subtract 1 to convert to odd
        iF -= abs(iF % 2 - 1)
        jF -= abs(jF % 2 - 1)
        kF -= abs(kF % 2 - 1)

        nfile.write(f'{iF}\n{jF}\n{kF}\n')

        nfile.write(f'{pixelsize[0]:.4f}\n{pixelsize[1]:.4f}\n{pixelsize[2]:.4f}\n')

        for k in range(kF):
            print(f'Guardando slice {k}')

            for j in range(jF):
                for i in range(iF):
                    nfile.write(f'{buff[i, j, k]}\n')

    print('Proceso terminado.')


# (1) Cargamos y leemos las DICOM
Dicom, ctinfo = DicomReader()
# (2) Generamos un voxelizado y lo guardamos
VoxelgeomSaver(filename='prueba.voxelgeom', buff=Dicom, ctinfo=ctinfo)
