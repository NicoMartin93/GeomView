

__author__ = "Antonio Serrano"
__email__ = "toni.sm91@gmail.com"
__version__ = "0.0.3"
__license__ = "MIT License"

__all__ = ["GeometryDefinition"]

import os
try:
    from GeomView.Blocks import *
except:
    import Blocks

# GEOMETRY-DEFINITION MANAGER

class GeometryDefinition():
    def __init__(self, description="", unit="cm", angle="DEG"):
        self.definition=[]
        self.description=description
        self.unit=unit
        self.angle=angle
        self.void_inner_volume_factor=1

        self._sm_characters=[120, 97, 97, 96]

    # surfaces
    def surface(self, label=None, indices=(1,1,1,1,1), starred=False, comment="", **kwargs):
        kwargs["unit"]=kwargs.get("unit", self.unit)
        kwargs["angle"]=kwargs.get("angle", self.angle)
        if label is None:
            label=self._sm_label()
        self.definition.append(blocks.Surface(label, indices, starred, comment, **kwargs))
        return self.definition[-1]

    def surface_implicit_form(self, label=None, indices=(0,0,0,0,0), starred=False, comment="", **kwargs):
        kwargs["unit"]=kwargs.get("unit", self.unit)
        kwargs["angle"]=kwargs.get("angle", self.angle)
        if label is None:
            label=self._sm_label()
        self.definition.append(blocks.Surface(label, indices, starred, comment, **kwargs))
        return self.definition[-1]

    def surface_plane(self, label=None, indices=(0,0,0,1,0), starred=False, comment="", **kwargs):
        kwargs["unit"]=kwargs.get("unit", self.unit)
        kwargs["angle"]=kwargs.get("angle", self.angle)
        if label is None:
            label=self._sm_label()
        self.definition.append(blocks.Surface(label, indices, starred, comment, **kwargs))
        return self.definition[-1]

    def surface_sphere(self, label=None, indices=(1,1,1,0,-1), starred=False, comment="", **kwargs):
        kwargs["unit"]=kwargs.get("unit", self.unit)
        kwargs["angle"]=kwargs.get("angle", self.angle)
        if label is None:
            label=self._sm_label()
        self.definition.append(blocks.Surface(label, indices, starred, comment, **kwargs))
        return self.definition[-1]

    def surface_cylinder(self, label=None, indices=(1,1,0,0,-1), starred=False, comment="", **kwargs):
        kwargs["unit"]=kwargs.get("unit", self.unit)
        kwargs["angle"]=kwargs.get("angle", self.angle)
        if label is None:
            label=self._sm_label()
        self.definition.append(blocks.Surface(label, indices, starred, comment, **kwargs))
        return self.definition[-1]

    def surface_hyperbolic_cylinder(self, label=None, indices=(1,-1,0,0,-1), starred=False, comment="", **kwargs):
        kwargs["unit"]=kwargs.get("unit", self.unit)
        kwargs["angle"]=kwargs.get("angle", self.angle)
        if label is None:
            label=self._sm_label()
        self.definition.append(blocks.Surface(label, indices, starred, comment, **kwargs))
        return self.definition[-1]

    def surface_cone(self, label=None, indices=(1,1,-1,0,0), starred=False, comment="", **kwargs):
        kwargs["unit"]=kwargs.get("unit", self.unit)
        kwargs["angle"]=kwargs.get("angle", self.angle)
        if label is None:
            label=self._sm_label()
        self.definition.append(blocks.Surface(label, indices, starred, comment, **kwargs))
        return self.definition[-1]

    def surface_one_sheet_hyperboloid(self, label=None, indices=(1,1,-1,0,-1), starred=False, comment="", **kwargs):
        kwargs["unit"]=kwargs.get("unit", self.unit)
        kwargs["angle"]=kwargs.get("angle", self.angle)
        if label is None:
            label=self._sm_label()
        self.definition.append(blocks.Surface(label, indices, starred, comment, **kwargs))
        return self.definition[-1]

    def surface_two_sheet_hyperboloid(self, label=None, indices=(1,1,-1,0,1), starred=False, comment="", **kwargs):
        kwargs["unit"]=kwargs.get("unit", self.unit)
        kwargs["angle"]=kwargs.get("angle", self.angle)
        if label is None:
            label=self._sm_label()
        self.definition.append(blocks.Surface(label, indices, starred, comment, **kwargs))
        return self.definition[-1]

    def surface_paraboloid(self, label=None, indices=(1,1,0,-1,0), starred=False, comment="", **kwargs):
        kwargs["unit"]=kwargs.get("unit", self.unit)
        kwargs["angle"]=kwargs.get("angle", self.angle)
        if label is None:
            label=self._sm_label()
        self.definition.append(blocks.Surface(label, indices, starred, comment, **kwargs))
        return self.definition[-1]

    def surface_parabolic_cylinder(self, label=None, indices=(1,0,0,-1,0), starred=False, comment="", **kwargs):
        kwargs["unit"]=kwargs.get("unit", self.unit)
        kwargs["angle"]=kwargs.get("angle", self.angle)
        if label is None:
            label=self._sm_label()
        self.definition.append(blocks.Surface(label, indices, starred, comment, **kwargs))
        return self.definition[-1]

    def surface_hyperbolic_paraboloid(self, label=None, indices=(1,-1,0,-1,0), starred=False, comment="", **kwargs):
        kwargs["unit"]=kwargs.get("unit", self.unit)
        kwargs["angle"]=kwargs.get("angle", self.angle)
        if label is None:
            label=self._sm_label()
        self.definition.append(blocks.Surface(label, indices, starred, comment, **kwargs))
        return self.definition[-1]

    # body
    def body(self, label=None, material=0, comment="", **kwargs):
        kwargs["unit"]=kwargs.get("unit", self.unit)
        kwargs["angle"]=kwargs.get("angle", self.angle)
        if label is None:
            label=self._sm_label()
        self.definition.append(blocks.Body(label, material, comment, **kwargs))
        return self.definition[-1]

    # module
    def module(self, label=None, material=0, comment="", **kwargs):
        kwargs["unit"]=kwargs.get("unit", self.unit)
        kwargs["angle"]=kwargs.get("angle", self.angle)
        if label is None:
            label=self._sm_label()
        self.definition.append(blocks.Module(label, material, comment, **kwargs))
        return self.definition[-1]

    # clone
    def clone(self, label=None, module="", comment="", **kwargs):
        kwargs["unit"]=kwargs.get("unit", self.unit)
        kwargs["angle"]=kwargs.get("angle", self.angle)
        if label is None:
            label=self._sm_label()
        self.definition.append(blocks.Clone(label, module, comment, **kwargs))
        return self.definition[-1]

    # include
    def include(self, filename, starred=False, comment=""):
        self.definition.append(blocks.Include(filename, starred, comment))
        return self.definition[-1]

    # end
    def end(self):
        self.definition.append(blocks.End())
        return self.definition[-1]

    def export_definition(self, filename):
        with open(file=filename, mode='w') as file_object:
            s=""
            if self.description:
                s="\n"+self.description+"\n"
            for definition in self.definition:
                definition.set_void_inner_volume_factor(self.void_inner_volume_factor)
                s+="\n"+str(definition)
            try:
                if type(self.definition[-1])!=blocks.End:
                    s+="\n"+str(blocks.End())
                s+="\n"
            except IndexError:
                s="EMPTY GEOMETRY-DEFINITION"
            file_object.write(s)

    def show_void_inner_volumes(self, show=True):
        if show:
            self.void_inner_volume_factor=-1
        else:
            self.void_inner_volume_factor=1

    def _sm_label(self):
        # 52728 labels from 'XAAA' to 'ZZZZ'
        self._sm_characters[3]+=1
        if self._sm_characters[3]>122:
            self._sm_characters[3]=97
            self._sm_characters[2]+=1
            if self._sm_characters[2]>122:
                self._sm_characters[2]=97
                self._sm_characters[1]+=1
                if self._sm_characters[1]>122:
                    self._sm_characters[1]=97
                    self._sm_characters[0]+=1
                    if self._sm_characters[0]>122:
                        self._sm_characters[0]=120
        return "".join([chr(c).upper() for c in self._sm_characters])

    def __str__(self):
        s=""
        if self.description:
            s="\n"+self.description+"\n"
        for definition in self.definition:
            definition.set_void_inner_volume_factor(self.void_inner_volume_factor)
            s+="\n"+str(definition)
        try:
            if type(self.definition[-1])!=blocks.End:
                s+="\n"+str(blocks.End())
        except IndexError:
            return ""
        return s
