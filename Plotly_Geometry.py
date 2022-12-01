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
a1 = 0
h1 = 5

r2 = 1.35
a2 = 1
h2 = 3

x1, y1, z1 = Plotly_Geometry.cylinder(r1, h1, a=a1)
x2, y2, z2 = Plotly_Geometry.cylinder(r2, h2, a=a2)

colorscale = [[0, 'blue'],
             [1, 'blue']]

cyl1 = go.Surface(x=x1, y=y1, z=z1,
                 colorscale = colorscale,
                 showscale=False,
                 opacity=0.5)
xb_low, yb_low, zb_low =  Plotly_Geometry.boundary_circle(r1, h=a1)
xb_up, yb_up, zb_up =  Plotly_Geometry.boundary_circle(r1, h=a1+h1)

bcircles1 =go.Scatter3d(x = xb_low.tolist()+[None]+xb_up.tolist(),
                        y = yb_low.tolist()+[None]+yb_up.tolist(),
                        z = zb_low.tolist()+[None]+zb_up.tolist(),
                        mode ='lines',
                        line = dict(color='blue', width=2),
                        opacity =0.55, showlegend=False)

cyl2 = go.Surface(x=x2, y=y2, z=z2,
                 colorscale = colorscale,
                 showscale=False,
                 opacity=0.7)

xb_low, yb_low, zb_low =  Plotly_Geometry.boundary_circle(r2, h=a2)
xb_up, yb_up, zb_up =  Plotly_Geometry.boundary_circle(r2, h=a2+h2)

bcircles2 =go.Scatter3d(x = xb_low.tolist()+[None]+xb_up.tolist(),
                        y = yb_low.tolist()+[None]+yb_up.tolist(),
                        z = zb_low.tolist()+[None]+zb_up.tolist(),
                        mode ='lines',
                        line = dict(color='blue', width=2),
                        opacity =0.75, showlegend=False)

layout = go.Layout(scene_xaxis_visible=False, scene_yaxis_visible=False, scene_zaxis_visible=False)
fig =  go.Figure(data=[cyl2, bcircles2, cyl1, bcircles1], layout=layout)

fig.update_layout(scene_camera_eye_z= 0.55)
fig.layout.scene.camera.projection.type = "orthographic" #commenting this line you get a fig with perspective proj

fig.show()
