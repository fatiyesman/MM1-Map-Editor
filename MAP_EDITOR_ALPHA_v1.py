def program_introduction(x):
    """
    =====================================================================
    ================= Midtown Madness 1 Map Editor Alpha ================
    
    This Map Editor allows users to create new maps for Midtown Madness 1
                                             Copyright (C) May 2023 Robin

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful, but
    WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU 
    General Public License for more details.

    For more information about GNU see <http://www.gnu.org/licenses/>.
    =====================================================================
    """

import os
import re
import csv
import math
import struct
import shutil
import random
import subprocess
from typing import List, Union, Tuple
import matplotlib.pyplot as plt                 # python -m ensurepip --upgrade
import matplotlib.transforms as mtransforms     # pip install matplotlib


# SETUP I (mandatory)                   Control + F    "city=="  to jump to The City Creation section
city_name = "USER"                      # One word (no spaces)  --- name of the .AR file
race_locale_name = "My First City"      # Can be multiple words --- name of the city in Game Menu

# Change this to match your case
destination_folder = r"C:\Users\robin\Desktop\MM1 BETA-BAIcc" # Path to your MM1 folder
shortcut_or_exe_name = "Open1560.lnk" # or Open1560.exe or Midtown.exe

# SETUP II (optional)
# Do not change the two variables below
morning, noon, evening, night = 0, 1, 2, 3; clear, cloudy, rain, snow = 0, 1, 2, 3
filler_WP = "0.0, 0.0, 0.0, 0.0, 15.0, 0, 0,"; filler_ALL = [filler_WP, filler_WP]

# =============== RACE EDITOR =============== #
# Max is 15 for Blitz & Circuit, and 12 for Checkpoint
blitz_race_names = ["Just in Time", "The Great Escape"]
circuit_race_names = ["Dading's Race"]
checkpoint_race_names = ["filler_race"]

# WAYPOINTS          Tabbing / spacing out the Coordinates is optional, but recommended for readability and editing
# Maximum number of blue checkpoints for Blitzes is 11 (including the start and finish checkpoints)
# Blitz 0 WP         x:      y:      z:     rot:    width:  ,0,0, 
blz_0_WP_start =    "0.0,   0.0,    0.1,    5.0,    15.0    ,0,0,"
blz_0_WP_ch1 =      "0.0,   0.0,    -20,    5.0,    15.0    ,0,0,"
blz_0_WP_ch2 =      "0.0,   0.0,    -40,    5.0,    15.0    ,0,0,"
blz_0_WP_ch3 =      "0.0,   0.0,    -60,    5.0,    15.0    ,0,0,"
blz_0_WP_ch4 =      "0.0,   0.0,    -80,    5.0,    15.0    ,0,0,"
blz_0_WP_finish =   "0.0,   0.0,    -99,    5.0,    15.0    ,0,0,"
blz_0_ALL = [blz_0_WP_start, blz_0_WP_ch1, blz_0_WP_ch2, blz_0_WP_ch3, blz_0_WP_ch4, blz_0_WP_finish]

# Blitz 1 WP        x:       y:      z:      rot:     width:  ,0,0, 
blz_1_WP_start =    "0.1,    0.0,    0.1,    90.0,    10.0    ,0,0,"
blz_1_WP_ch1 =      "20.0,   0.0,    0.1,    90.0,    10.0    ,0,0,"
blz_1_WP_ch2 =      "40.0,   0.0,    0.1,    90.0,    10.0    ,0,0,"
blz_1_WP_ch3 =      "60.0,   0.0,    0.1,    90.0,    10.0    ,0,0,"
blz_1_WP_ch4 =      "80.0,   0.0,    0.1,    90.0,    10.0    ,0,0,"
blz_1_WP_finish =   "99.0,  0.0,    0.1,    90.0,    10.0    ,0,0,"
blz_1_ALL = [blz_1_WP_start, blz_1_WP_ch1, blz_1_WP_ch2, blz_1_WP_ch3, blz_1_WP_ch4, blz_1_WP_finish]

# Circuit 0 WP      x:           y:       z:          rot:       width:  ,0,0,
cir_1_start =       "-101.5,    0.1,    0.01,         -180.0,     8.0     ,0,0,"
cir_1_ch1 =         "0.01,      0.1,    101.5,        90,         8.0     ,0,0,"
cir_1_ch2 =         "101.5,     0.1,    0.01,         0.01,       8.0     ,0,0,"
cir_1_finish =      "0.01,      0.1,    -101.5,       -90,        8.0     ,0,0,"
cir_1_ALL = [cir_1_start, cir_1_ch1, cir_1_ch2, cir_1_finish]

# Blitz WP file, Time of Day, Weather, Time Limit, Number of Laps (5 arguments)
blitz_waypoints = [(blz_0_ALL, morning, clear, 60, len(blz_0_ALL)-1),   
                   (blz_1_ALL, night, snow, 40, len(blz_1_ALL)-1)]

# Circuit WP file, Time of Day, Weather, Laps Amateur, Laps Pro (5 arguments)
circuit_waypoints = [(cir_1_ALL, night, snow, 2, 3)]

# Checkpoint WP file, Time of Day, Weather (3 arguments)
checkpoint_waypoints = [(filler_ALL, noon, cloudy)] # feel free to change

# COPS AND ROBBERS
cnr_waypoints = [                          # set Cops and Robbers Waypoints manually and concisely
    ## 1st set, Name: ... ## 
    (20.0,1.0,80.0),                       # Bank or Blue Team Hideout
    (80.0,1.0,20.0),                       # Gold
    (20.0,1.0,80.0),                       # Robber or Red Team Hideout
    ## 2nd set, Name: ... ## 
    (-90.0,1.0,-90.0),
    (90.0,1.0,90.0),
    (-90.0,1.0,-90.0),
    ## 3rd set, Name: ... ##
    (50.0,1.0,-50.0),
    (-10.0,1.0,10.0),
    (50.0,1.0,-50.0)]

# ANIM
anim_data = {
    'plane': [                  # you can only use "plane" and "eltrain"
        (250, 40.0, -250),      # other objects won't work
        (250, 40.0, 250),       # you can not add multiple planes or trains
        (-250, 40.0, -250),     # you can set any number of coordinates for your path
        (-250, 40.0, 250)], 
    'eltrain': [
        (80, 25.0, -80),
        (80, 25.0, 80), 
        (-80, 25.0, -80),
        (-80, 25.0, 80)]}

# BRIDGES
slim_bridge = "tpdrawbridge04"
broad_bridge = "tpdrawbridge06"
other_object = "vpmustang99" # you can pass any object here instead of a bridge, for example: vpmustang99

# this is originally reserved for the yellow crossgates, logic to align the crossgates to drawbridge is not implemented yet
filler_object_xyz = "tpsone,0,-9999.99,0.0,-9999.99,-9999.99,0.0,-9999.99" 
                                                                           
# IMPORTANT I: only ONE bridge can be present in ONE cull room (otherwise the game will crash)
# IMPORTANT II: Bridges only work in MULTIPLAYER, in SINGLEPLAYER the game will crash if you enable bridges
# as a result, be cautious with changing setting "create_bridges()" to True at the end of the script

# format: (x,y,z, orientation, bridge number, object)
bridges = [
    ((-50.0, 0.0, -150.0), "vertical", 1, slim_bridge), 
    ((-200.0, 0.0, -200.0), "horizontal_east", 2, broad_bridge)]

"Possible orientations:"
"'vertical', 'vertical_flipped', 'horizontal_east', 'horizontal_west', 'north_east', 'north_west', 'south_east', or 'south_west'"

"Dimension of objects: (feel free to add data)"
"slim_bridge"   # x: 30.0 y: 5.9 z: 32.5
"broad_bridge"  # x: 40.0 y: 5.9 z: 32.5

# OTHER
randomize_string_names = ["T_WATER", "T_GRASS", "T_WOOD", "IND_WALL", "EXPLOSION", "OT_BAR_BRICK", "R4", "R6", "T_WALL", "FXLTGLOW"] 
common_textures_1 = []
common_textures_2 = []
common_textures_3 = []

# Do not change
num_blitz = len(blitz_waypoints)
num_circuit = len(circuit_waypoints)
num_checkpoint = len(checkpoint_waypoints)

# Not applicable yet
ambient_density = 0.2
num_opponents = 8 # gen. 8 opponents all race types, and put the created opponent file names in the correct AIMAP_P files
opponent_car = "vppanozgt" 

################################################################################################################               
################################################################################################################     
   
def to_do_list(x):
            """
            TexCoords --> flip "repeated_horizontal" and flip "vertical". Because tested "R2" example is actually at x=0, y=-200 (and not y=200)
            TexCoords --> check "rotating_repeating" (angles)
            TexCoords --> find way to account for Walls (is the opposite for flat surfaces?)
            TEXTURES --> add TEX16A and TEX16O from existing custom cities
            TEXTURES --> enable custom textures or replace existing textures
            TEXTURES --> will other textures also move if they contain "T_WATER..."?
            Corners --> figure out Triangles
            Corners --> figure out Hills    
            WALL --> is there a way to enable collision on both sides of the wall?
            BRIDGE --> cont.                   
            HUDMAP --> fix automate (correct) alignment
            HUDMAP --> color fill some Polygons (e.g. Blue for Water, Green for Grass), need to correctly retrieve/match Bound Number first (hard)
            SCRIPT --> split "distribute_generated_files" into smaller components    
            SCRIPT --> put everything into a PolygonHandler class? (to retain input data in functions)
            SCRIPT --> split City Settings (coordinates) into separate file
            SCRIPT --> "repeating_horizontal_flipped" shorten (?)
            SCRIPT --> add custom texture functionality
            BAI --> retrieve Center from all set Polygons
            BAI --> set / incorporate Street file template
            PTL --> reinvestigate at some point
            BMS --> export "cache_size" variable correctly
            BMS --> add shifting texture (like the airport lights, string_compare = "fxltglow")
            BMS --> walls are invisible, user must +/- 0.01 to make them visible (fix this) (add type: facing direction)
            FCD --> cont. (?)
            BNG --> improve prop functionality (facing)
            BNG --> add prop list (+ description), where is my folder with all Prop Pictures?
            BNG --> create dataset with x,y,z (dimensions) of all props
            CELLS --> implement Cell type
            CELLS --> # Max 256 characters per row --> add Error Handling/warning
            RACES --> investigate why max 15?
            BLENDER --> [...]
            USER --> "gather" a folder with good to use textures from TEX16O / TEX16A
            GITHUB --> add Readme / other useful info
            OPEN1560 --> add (forked) updated Open1560
            """
            
################################################################################################################               
################################################################################################################        

# VECTOR2 CLASS
class Vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"x = {self.x}, y = {self.y})"

# VECTOR3 CLASS
class Vector3:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    @classmethod
    def from_file(cls, file):
        x, y, z = struct.unpack('<3f', file.read(12))
        return cls(x, y, z)
    
    def to_file(self, file):
        data = struct.pack('<3f', self.x, self.y, self.z)
        file.write(data)
        
    def __repr__(self, round_values=True):
        if round_values:
            return '{{{:.2f},{:.2f},{:.2f}}}'.format(round(self.x, 2), round(self.y, 2), round(self.z, 2))
        else:
            return '{{{:f},{:f},{:f}}}'.format(self.x, self.y, self.z)
       
       
# Calculate BND: center, radius, min and max      
def calculate_max(vertices: List[Vector3]):
    max_ = Vector3(vertices[0].x, vertices[0].y, vertices[0].z)
    for vertex in vertices:
        max_.x = max(max_.x, vertex.x)
        max_.y = max(max_.y, vertex.y)
        max_.z = max(max_.z, vertex.z)
    return max_

def calculate_min(vertices: List[Vector3]):
    min_ = Vector3(vertices[0].x, vertices[0].y, vertices[0].z)
    for vertex in vertices:
        min_.x = min(min_.x, vertex.x)
        min_.y = min(min_.y, vertex.y)
        min_.z = min(min_.z, vertex.z)
    return min_

def calculate_center(vertices: List[Vector3]):
    center = Vector3(0, 0, 0)
    for vertex in vertices:
        center.x += vertex.x
        center.y += vertex.y
        center.z += vertex.z
    center.x /= len(vertices)
    center.y /= len(vertices)
    center.z /= len(vertices)
    return center

def calculate_center_tuples(vertices: List[Tuple[float, float, float]]):
    center = [0, 0, 0]
    for vertex in vertices:
        center[0] += vertex[0]
        center[1] += vertex[1]
        center[2] += vertex[2]
    center[0] /= len(vertices)
    center[1] /= len(vertices)
    center[2] /= len(vertices)
    return center

def calculate_radius(vertices: List[Vector3], center: Vector3):
    radius_sqr = 0
    for vertex in vertices:
        diff = Vector3(vertex.x - center.x, vertex.y - center.y, vertex.z - center.z)
        radius_sqr = max(radius_sqr, diff.x ** 2 + diff.y ** 2 + diff.z ** 2)
    return radius_sqr ** 0.5


# POLYGON CLASS {BND}
class Polygon:
    def __init__(self, word0, mtl_index, flags, vert_indices, some_vecs, corners):
        self.word0 = word0
        self.mtl_index = mtl_index  
        self.flags = flags          
        self.vert_indices = vert_indices
        self.some_vecs = some_vecs
        self.corners = corners

    @classmethod
    def from_file(cls, file):
        word0, mtl_index, flags, *vert_indices = struct.unpack('<HBB4H', file.read(12))
        some_vecs = [Vector3.from_file(file) for _ in range(4)]
        corners = list(struct.unpack('<4f', file.read(16)))
        
        return cls(word0, mtl_index, flags, vert_indices, some_vecs, corners)
    
    def to_file(self, file):
        data = struct.pack('<HBB4H', self.word0, self.mtl_index, self.flags, *self.vert_indices)
        file.write(data)
    
        for vec in self.some_vecs: 
            data = struct.pack('<3f', vec.x, vec.y, vec.z)
            file.write(data)
 
        data = struct.pack('<4f', self.corners[0], self.corners[1], self.corners[2], self.corners[3])
        file.write(data)
        
    def __repr__(self, round_values=True):
        vertices_coordinates = []
        for index in self.vert_indices:
            vertices_coordinates.append(bnd.vertices[index])

        if round_values:
            corners_str = '[{}]'.format(', '.join(['{:.2f}'.format(round(corner, 2)) for corner in self.corners]))
        else:
            corners_str = '[{}]'.format(', '.join(['{:f}'.format(corner) for corner in self.corners]))

        return '\n Polygon \n Bound number: {}\n Material Index: {}\n Flags: {}\n Vertices Indices: {}\n Vertices Coordinates: {}\n Directional Coordinates: {}\n Corners: {}\n'.format(self.word0, self.mtl_index, self.flags, self.vert_indices, vertices_coordinates, self.some_vecs, corners_str)
    

# BND CLASS    
class BND:
    def __init__(self, magic, offset, width, row_count, height, center, radius, radius_sqr, min_, max_, num_verts, num_polys, num_hot_verts, num_vertices_unk, edge_count, scaled_dist_x, z_dist, num_indexs, height_scale, unk12, vertices, polys):
        self.magic = magic
        self.offset = offset    
        self.width = width
        self.row_count = row_count
        self.height = height
        self.center = center    
        self.radius = radius
        self.radius_sqr = radius_sqr
        self.min = min_         
        self.max = max_        
        self.num_verts = num_verts
        self.num_polys = num_polys
        self.num_hot_verts = num_hot_verts
        self.num_vertices_unk = num_vertices_unk
        self.edge_count = edge_count
        self.scaled_dist_x = scaled_dist_x
        self.z_dist = z_dist
        self.num_indexs = num_indexs
        self.height_scale = height_scale
        self.unk12 = unk12
        self.vertices = vertices              
        self.polys = polys                      

    @classmethod
    def from_file(cls, file):
        magic = struct.unpack('<4s', file.read(4))[0]
        offset = Vector3.from_file(file)
        width, row_count, height = struct.unpack('<3l', file.read(12)) 
        center = Vector3.from_file(file)
        radius, radius_sqr = struct.unpack('<2f', file.read(8))
        min_ = Vector3.from_file(file)
        max_ = Vector3.from_file(file)
        num_verts, num_polys, num_hot_verts, num_vertices_unk, edge_count = struct.unpack('<5l', file.read(20))
        scaled_dist_x, z_dist, num_indexs, height_scale, unk12 = struct.unpack('<fflfl', file.read(20))
        vertices = [Vector3.from_file(file) for _ in range(num_verts)]
        polys = [Polygon.from_file(file) for _ in range(num_polys + 1)] 

        return cls(magic, offset, width, row_count, height, center, radius, radius_sqr, min_, max_, num_verts, num_polys, num_hot_verts, num_vertices_unk, edge_count, scaled_dist_x, z_dist, num_indexs, height_scale, unk12, vertices, polys)
    
    def to_file(self, file):
        data = struct.pack('<4s', self.magic)
        file.write(data)
        self.offset.to_file(file)         
        data = struct.pack('<3l', self.width, self.row_count, self.height)
        file.write(data)     
        self.center.to_file(file) 
        data = struct.pack('<ff', self.radius, self.radius_sqr)
        file.write(data)
        self.min.to_file(file)
        self.max.to_file(file)
        data = struct.pack('<5l', self.num_verts, self.num_polys, self.num_hot_verts, self.num_vertices_unk, self.edge_count)
        file.write(data)
        data = struct.pack('<fflfl', self.scaled_dist_x, self.z_dist, self.num_indexs, self.height_scale, self.unk12)
        file.write(data)

        for vertex in self.vertices:       
            vertex.to_file(file)            

        for poly in self.polys:           
            poly.to_file(file)              
                
    # Write BND TEXT data
    def write_to_file(self, file_name):
        with open(file_name, 'w') as f:
            f.write(str(self))
                
    def __repr__(self):
        return 'BND\n Magic: {}\n Offset: {}\n Width: {}\n Row_count: {}\n Height: {}\n Center: {}\n Radius: {}\n Radius_sqr: {}\n min: {}\n max: {}\n Num Verts: {}\n Num Polys: {}\n Num Hot Verts: {}\n Num Vertices Unk: {}\n Edge count: {}\n Scaled Dist. X: {}\n Z Dist.: {}\n Num Indexs: {}\n Height Scale: {}\n Unk12: {}\n Vertices: {}\n\n Polys: {}\n\n'.format(
            self.magic, self.offset, self.width, self.row_count, self.height, self.center, self.radius, self.radius_sqr, self.min, self.max, self.num_verts, self.num_polys, self.num_hot_verts, self.num_vertices_unk, self.edge_count, self.scaled_dist_x, self.z_dist, self.num_indexs, self.height_scale, self.unk12, self.vertices, self.polys)


# BMS CLASS  
class BMS:
    def __init__(self, Magic, VertexCount, AdjunctCount, SurfaceCount, IndicesCount, Radius, Radiussq, BoundingBoxRadius, TextureCount, Flags, StringName, Coordinates, TextureDarkness, TexCoords, enclosed_shape, SurfaceSides, IndicesSides):
        self.Magic = Magic
        self.VertexCount = VertexCount
        self.AdjunctCount = AdjunctCount
        self.SurfaceCount = SurfaceCount
        self.IndicesCount = IndicesCount
        self.Radius = Radius
        self.Radiussq = Radiussq
        self.BoundingBoxRadius = BoundingBoxRadius
        self.TextureCount = TextureCount
        self.Flags = Flags
        self.StringName = StringName
        self.Coordinates = Coordinates
        self.TextureDarkness = TextureDarkness
        self.TexCoords = TexCoords  
        self.enclosed_shape = enclosed_shape  
        self.SurfaceSides = SurfaceSides
        self.IndicesSides = IndicesSides
        
    def to_file(self, file_name: str) -> None:
        with open(file_name, 'wb') as file:
            file.write(struct.pack('<16s', self.Magic.encode('utf-8').ljust(16, b'\x00')))
            file.write(struct.pack('<IIII', self.VertexCount, self.AdjunctCount, self.SurfaceCount, self.IndicesCount))
            file.write(struct.pack('<fff', self.Radius, self.Radiussq, self.BoundingBoxRadius))
            file.write(struct.pack('<bb', self.TextureCount, self.Flags))

            file.write(b'\x00' * 2)
            file.write(b'\x00' * 4)

            for StringName in self.StringName:
                file.write(struct.pack('<32s', StringName.encode('utf-8').ljust(32, b'\x00')))
                file.write(b'\x00' * (4 * 4))

            for coordinate in self.Coordinates:
                file.write(struct.pack('<3f', coordinate.x, coordinate.y, coordinate.z))

            file.write(struct.pack('<' + str(self.AdjunctCount) + 'b', *self.TextureDarkness))
            file.write(struct.pack('<' + str(self.AdjunctCount + self.AdjunctCount) + 'f', *self.TexCoords))            
            file.write(struct.pack('<' + str(self.AdjunctCount) + 'H', *self.enclosed_shape))
            file.write(struct.pack('<' + str(self.SurfaceCount) + 'b', *self.SurfaceSides))

            for indices_side in self.IndicesSides:
                file.write(struct.pack('<' + str(len(indices_side)) + 'H', *indices_side))
      
################################################################################################################               
################################################################################################################       
   
# Do not change
bnd_hit_id = f"{city_name}_HITID.BND"
bnd_hit_id_text = f"{city_name}_HITID.txt"
poly_filler = Polygon(0, 0, 0, [0, 0, 0, 0], [Vector3(0, 0, 0) for _ in range(4)], [0.0, 0.0, 0.0, 0.0])
vertices = []
polys = [poly_filler]
all_polygons_picture = []

# Handle Texture Mapping for BMS files
def generate_tex_coords(mode="horizontal", repeat_x=1, repeat_y=1, tilt=0, angle_degrees=(45, 45), custom=None):
    
    def tex_coords_rotating_repeating(repeat_x, repeat_y, angle_degrees):
        angle_radians = [math.radians(angle) for angle in angle_degrees]

        def rotate(x, y, angle_idx):
            new_x = x * math.cos(angle_radians[angle_idx]) - y * math.sin(angle_radians[angle_idx])
            new_y = x * math.sin(angle_radians[angle_idx]) + y * math.cos(angle_radians[angle_idx])
            return new_x, new_y

        coords = [
            (0, 0),
            (repeat_x, 0),
            (repeat_x, repeat_y),
            (0, repeat_y)]

        rotated_coords = [rotate(x, y, 0) if i < 2 else rotate(x, y, 1) for i, (x, y) in enumerate(coords)]
        return [coord for point in rotated_coords for coord in point]

    # Continue checking / polishin
    # Horizontal
    if mode == "horizontal":
        return [0, 0, 0, 1, 1, 1, 1, 0]
    elif mode == "horizontal_flipped":
        return [0, 1, 0, 0, 1, 0, 1, 1]
   # Vertical 
    elif mode == "vertical":
        return [0, 0, 1, 0, 1, 1, 0, 1]    
    elif mode == "vertical_flipped":
        return [1, 0, 0, 0, 0, 1, 1, 1]
    # Horizontal Repeated
    elif mode == "repeating_horizontal":
        return [0, 0, 0, repeat_y, repeat_x, repeat_y, repeat_x, 0]
    elif mode == "repeating_horizontal_flipped":
        return [0, repeat_y, 0, 0, repeat_x, 0, repeat_x, repeat_y]
    # Vertical Repeated
    elif mode == "repeating_vertical":
        return [0, 0, repeat_y, 0, repeat_y, repeat_x, 0, repeat_x]
    elif mode == "repeating_vertical_flipped":
        return [repeat_y, 0, 0, 0, 0, repeat_x, repeat_y, repeat_x]

    # Check
    elif mode == "rotating_repeating":
        return tex_coords_rotating_repeating(repeat_x, repeat_y, angle_degrees)
    elif mode == "custom":
        if custom is None:
            raise ValueError("Custom TexCoords must be provided for mode 'custom'")
        return custom
    elif mode == "combined":
        return [0, 0, 1, 0, 1, 1 + tilt, 0, 2]
    else:
        raise ValueError(f"Invalid mode '{mode}'. Allowed values are 'horizontal', 'vertical', 'horizontal_flipped', 'vertical_flipped', 'repeating_horizontal', 'repeating_vertical', 'repeating_horizontal_flipped', 'repeating_vertical_flipped', 'rotating_repeating', 'custom', and 'combined'")

# HELPER BMS
def generate_and_save_bms_file(
    string_names, texture_indices=[1], vertices=vertices, polys=polys, texture_darkness=None, TexCoords=None, randomized_string_name=False, exclude=False, tex_coord_mode=None, tex_coord_params=None):
    
    poly = polys[-1]  # Get the last polygon added
    bound_number = poly.word0
    
    # Randomize Strings
    if randomized_string_name and not exclude:
        string_names = [random.choice(randomize_string_names)]
    
    # Create correct Water BMS
    if "T_WATER" in string_names:
        bms_filename = "CULL{:02d}_A2.bms".format(bound_number)
    else:
        bms_filename = "CULL{:02d}_H.bms".format(bound_number)
        
    if tex_coord_mode is not None:
        if tex_coord_params is None:
            tex_coord_params = {}
        TexCoords = generate_tex_coords(tex_coord_mode, **tex_coord_params)
        
    single_poly = [poly_filler, poly]
    bms = generate_bms(vertices, single_poly, texture_indices, string_names, texture_darkness, TexCoords)
    bms.to_file(bms_filename)
    # print(f"Successfully created BMS file: {bms_filename}")
             
# GENERATE BMS         
def generate_bms(vertices, polys, texture_indices, string_names: List[str], texture_darkness=None, TexCoords=None):
    shapes = []
    for poly in polys[1:]:  # Skip the first filler polygon
        vertex_coordinates = [vertices[idx] for idx in poly.vert_indices]
        shapes.append(vertex_coordinates)
    
    # DEFAULT BMS VALUES, do not change!
    magic, flags, radius, radiussq, bounding_box_radius = "3HSM", 3, 0.0, 0.0, 0.0  
    texture_count = len(string_names)
    coordinates = [coord for shape in shapes for coord in shape]
    vertex_count = len(coordinates)
    adjunct_count = len(coordinates)
    surface_count = len(texture_indices)            
    indices_count = surface_count * 4
    enclosed_shape = list(range(adjunct_count))

    # Texture Darkness and TexCoords        
    if texture_darkness is None:
        texture_darkness = [2] * adjunct_count
    if TexCoords is None:
        TexCoords = [0.0 for _ in range(adjunct_count * 2)]

    # Create list of indices_sides, one for each shape
    indices_sides = []
    index_start = 0
    for shape in shapes:
        shape_indices = list(range(index_start, index_start + len(shape)))
        indices_sides.append(shape_indices)
        index_start += len(shape)
        
    return BMS(magic, vertex_count, adjunct_count, surface_count, indices_count, radius, radiussq, bounding_box_radius, texture_count, flags, string_names, coordinates, texture_darkness, TexCoords, enclosed_shape, texture_indices, indices_sides)

################################################################################################################               
################################################################################################################  

# Initialize BND   
def initialize_bnd(vertices, polys):
    magic, width, row_count, height = b'2DNB\0', 0, 0, 0
    num_hot_verts, num_vertices_unk, edge_count, scaled_dist_x, z_dist = 0, 0, 0, 0.0, 0.0
    num_indexs, height_scale, unk12, edge_count = 0, 0.0, 0, 0
    offset = Vector3(0.0, 0.0, 0.0)
    center = calculate_center(vertices)
    min_ = calculate_min(vertices)
    max_ = calculate_max(vertices)
    radius = calculate_radius(vertices, center)
    radius_sqr = radius ** 2

    return BND(magic, offset, width, row_count, height, center, radius, radius_sqr, min_, max_, len(vertices), len(polys) - 1, num_hot_verts, num_vertices_unk, edge_count, scaled_dist_x, z_dist, num_indexs, height_scale, unk12, vertices, polys)
    
# Sort BND Vertices Coordinates
def sort_coordinates(vertex_coordinates):
    max_x_coord = max(vertex_coordinates, key=lambda coord: coord[0])
    min_x_coord = min(vertex_coordinates, key=lambda coord: coord[0])
    max_z_for_max_x = max([coord for coord in vertex_coordinates if coord[0] == max_x_coord[0]], key=lambda coord: coord[2])
    min_z_for_max_x = min([coord for coord in vertex_coordinates if coord[0] == max_x_coord[0]], key=lambda coord: coord[2])
    max_z_for_min_x = max([coord for coord in vertex_coordinates if coord[0] == min_x_coord[0]], key=lambda coord: coord[2])
    min_z_for_min_x = min([coord for coord in vertex_coordinates if coord[0] == min_x_coord[0]], key=lambda coord: coord[2])

    return [max_z_for_max_x, min_z_for_max_x, min_z_for_min_x, max_z_for_min_x]

# Sort BND Directional Coordinates
def calculate_directional_coordinates(vertex_coordinates):
    dir_coord_1 = (-1, 0, -vertex_coordinates[0][0])
    dir_coord_2 = (0, 1, vertex_coordinates[1][2])
    dir_coord_3 = (1, 0, vertex_coordinates[2][0])
    dir_coord_4 = (0, -1, -vertex_coordinates[3][2])

    return [dir_coord_1, dir_coord_2, dir_coord_3, dir_coord_4]

# Create Polygon       
def create_polygon(bound_number, material_index, flags, vert_indices, some_vecs, corners):
    return Polygon(bound_number, material_index, flags, vert_indices, some_vecs, corners)
     
# Create and Append Polygon
def create_and_append_polygon(
    bound_number, material_index, vertex_coordinates, corners=None, base_vertex_index=None, flags=None, 
    vertices=vertices, polys=polys, wall_side="outside"):
        
    if base_vertex_index is None:
        base_vertex_index = len(vertices)

    # Handle CORNERS                
    # case 1: FLAT Surface
    if all(vertex[1] == vertex_coordinates[0][1] for vertex in vertex_coordinates):
        corners = [0.0, 1.0, 0.0, -vertex_coordinates[0][1]]
    
    # case 2: WALL with varying X and Y coordinates
    elif (max(coord[0] for coord in vertex_coordinates) - min(coord[0] for coord in vertex_coordinates) > 0.1 and
          max(coord[1] for coord in vertex_coordinates) - min(coord[1] for coord in vertex_coordinates) > 0.1 and
          abs(max(coord[2] for coord in vertex_coordinates) - min(coord[2] for coord in vertex_coordinates)) <= 0.15):
        
        if wall_side == "outside":
            corners = [0, 0, -1, max(coord[2] for coord in vertex_coordinates)]
        elif wall_side == "inside":
            corners = [0, 0, 1, -max(coord[2] for coord in vertex_coordinates)]
    
    # case 3: WALL with varying Z and Y coordinates                               
    elif (abs(max(coord[0] for coord in vertex_coordinates) - min(coord[0] for coord in vertex_coordinates)) <= 0.15 and
          max(coord[1] for coord in vertex_coordinates) - min(coord[1] for coord in vertex_coordinates) > 0.1 and
          max(coord[2] for coord in vertex_coordinates) - min(coord[2] for coord in vertex_coordinates) > 0.1):
                
        if wall_side == "outside":
            corners = [-1, 0, 0, min(coord[0] for coord in vertex_coordinates)]
        elif wall_side == "inside":
            corners = [1, 0, 0, -min(coord[0] for coord in vertex_coordinates)]
            
    # Hills (TO DO)
    # case 4: HILL with varying X, Y and Z coordinates      (1e 3e regels moet kloppen)
    # elif (max(coord[0] for coord in vertex_coordinates) - min(coord[0] for coord in vertex_coordinates) > 0.1 and
          # max(coord[1] for coord in vertex_coordinates) - min(coord[1] for coord in vertex_coordinates) > 0.1 and
          # max(coord[2] for coord in vertex_coordinates) - min(coord[2] for coord in vertex_coordinates) > 0.1):

        # corners = [0, 0, -1, max(coord[2] for coord in vertex_coordinates)]
    
    # TO DO: 
    # case 5: triangles
    elif corners is None:
        raise ValueError("Corners method not implemented yet, please specify Corners manually")
    
    # Handle FLAGS    
    num_vertex_coordinates = len(vertex_coordinates)
    if flags is None:
        if num_vertex_coordinates == 4:
            flags = 6           # flag 4 and 5 should also work for rectangles
        elif num_vertex_coordinates == 3:
            flags = 3           # flag 0, 1, 2, 8, 9, 10 should also work for triangles
            print("WARNING: Triangles are not supported yet")
        else:
            raise ValueError("Unsupported number of coordinates in 'vertex_coordinates'")
    
    sorted_vertex_coordinates = sort_coordinates(vertex_coordinates)
    new_vertices = [Vector3(*coord) for coord in sorted_vertex_coordinates]
    vertices.extend(new_vertices)
    vert_indices = [base_vertex_index + i for i in range(len(new_vertices))]

    directional_vectors = calculate_directional_coordinates(sorted_vertex_coordinates)
    some_vecs = [Vector3(*vec) for vec in directional_vectors]

    poly = create_polygon(bound_number, material_index, flags, vert_indices, some_vecs, corners)
    polys.append(poly)
    
    # Create picture of all shapes
    all_polygons_picture.append(vertex_coordinates)
        
################################################################################################################               
################################################################################################################ 

# ==================CREATING YOUR CITY================== #

def user_notes(x):
    """ 
    NOTES:
    Please find some example Polygons and BMS below this text.
    You can already run this the script with these Polygons and BMS to see how it works.
    
    If you're creating a Flat Surface, you should at the pass this structure to "vertex_coordinates:"
        max_x,max_z 
        min_x,max_z 
        max_x,min_z 
        min_x,min_z 
        
    Please note that the order of the coordinates is NOT important, as they will be sorted automatically by the script (CHECK)
    
    Material Index: 0 = Road, 87 = Grass, 91 (Water, {Sleep with the Fishes})

    Usage examples of TexCoods:
    TexCoords=generate_tex_coords(mode="vertical")
    TexCoords=generate_tex_coords(mode="repeating_vertical", repeat_x=4, repeat_y=2))
    TexCoords=generate_tex_coords(mode="rotating_repeating", repeat_x=3, repeat_y=3, angle_degrees=(45, 45))) {unfinished}
    
    Usage example of Randomize String Names
    In the function DEFINITION (roughly line 364), i.e. "def generate_and_save_bms_file()" you can:
    Set "randomized_string_name=False" to disable
    Set "randomized_string_name=True" to enable (for all Strings)

    See below to Exclude random string name for specified Polygon, while randomizing the rest
    generate_and_save_bms_file(
           string_names=["T_WALL"], exclude=True))
    """
           
# Polygon 1 | Grass Start
create_and_append_polygon(
    bound_number = 1,
    material_index = 87,
    vertex_coordinates=[
        (-200, 0.0, -200),
        (-200, 0.0, 200),	
        (200, 0.0, 200),
        (200, 0.0, -200)])

# Polygon 1 | Texture
generate_and_save_bms_file(
    string_names = ["24_GRASS"], TexCoords=generate_tex_coords(mode="repeating_horizontal", repeat_x=20, repeat_y=20))

# Polygon 2 |
create_and_append_polygon(
    bound_number = 2,
    material_index = 98,        # custom material
    vertex_coordinates=[
        (-200, 0.0, -200),
        (-200, 0.0, 200),	
        (-300, 0.0, 200),
        (-300, 0.0, -200)])

# Polygon 2 | Texture
generate_and_save_bms_file(
    string_names = ["SNOW"], TexCoords=generate_tex_coords(mode="repeating_horizontal", repeat_x=20, repeat_y=20))

################################################################################################################               
################################################################################################################ 

# Initialize and write BND file
bnd = initialize_bnd(vertices, polys)

with open(bnd_hit_id, "wb") as f:
    bnd.to_file(f)
    # print(bnd)
    # bnd.write_to_file(bnd_hit_id_text)

# Create SHOP and FOLDER structure   
def create_folder_structure(city_name):
    os.makedirs("build", exist_ok=True)
    os.makedirs(os.path.join("SHOP", "BMP16"), exist_ok=True)
    os.makedirs(os.path.join("SHOP", "TUNE"), exist_ok=True)
    os.makedirs(os.path.join("SHOP", "BMS", f"{city_name}CITY"), exist_ok=True)
    os.makedirs(os.path.join("SHOP", "BMS", f"{city_name}LM"), exist_ok=True)
    os.makedirs(os.path.join("SHOP", "BND", f"{city_name}CITY"), exist_ok=True)
    os.makedirs(os.path.join("SHOP", "BND", f"{city_name}LM"), exist_ok=True)
    os.makedirs(os.path.join("SHOP", "CITY", f"{city_name}"), exist_ok=True)
    os.makedirs(os.path.join("SHOP", "RACE", f"{city_name}"), exist_ok=True)

    with open(os.path.join("SHOP", "CITY", f"{city_name}.PTL"), "w") as f:
        pass

    with open(os.path.join("SHOP", "TUNE", f"{city_name}.CINFO"), "w") as f:
        localized_name = race_locale_name
        map_name = city_name.lower()
        race_dir = city_name.lower()        
        f.write(f"LocalizedName={localized_name}\n")
        f.write(f"MapName={map_name}\n")
        f.write(f"RaceDir={race_dir}\n")
        f.write(f"BlitzCount={num_blitz}\n")
        f.write(f"CircuitCount={num_circuit}\n")
        f.write(f"CheckpointCount={num_checkpoint}\n")
        blitz_race_names_str = '|'.join(blitz_race_names)
        circuit_race_names_str = '|'.join(circuit_race_names)
        checkpoint_race_names_str = '|'.join(checkpoint_race_names)
        f.write(f"BlitzNames={blitz_race_names_str}\n")
        f.write(f"CircuitNames={circuit_race_names_str}\n")
        f.write(f"CheckpointNames={checkpoint_race_names_str}\n")
        
def distribute_generated_files(city_name, bnd_hit_id, num_blitz, blitz_waypoints, num_circuit, 
                               circuit_waypoints, num_checkpoint, checkpoint_waypoints, all_races_files=True):

    bms_files = []
    bms_a2_files = set()
    for file in os.listdir():
        if file.endswith(".bms"):
            bound_number = int(re.findall(r'\d+', file)[0])
            bms_files.append(bound_number)
            if file.endswith("_A2.bms"):
                bms_a2_files.add(bound_number)
            if bound_number < 200:
                shutil.move(file, os.path.join("SHOP", "BMS", f"{city_name}LM", file))
            else:
                shutil.move(file, os.path.join("SHOP", "BMS", f"{city_name}CITY", file))
        
    for file in os.listdir():
        if file.endswith(".bnd"):
            shutil.move(file, os.path.join("SHOP", "BND", file))
    shutil.move(bnd_hit_id, os.path.join("SHOP", "BND", bnd_hit_id))       
        
    # Create WAYPOINTS files
    race_prefixes = ["ASP1", "ASP2", "ASP3", "ASU1", "ASU2", "ASU3", "AFA1", "AFA2", "AFA3", "AWI1", "AWI2", "AWI3"]
    if num_checkpoint > len(race_prefixes):
        raise ValueError("Number of Checkpoint races cannot be more than 12")
    
    for race_type, race_description, prefix, num_files, race_waypoints in [("BLITZ", "Blitz", "ABL", num_blitz, blitz_waypoints), 
                                                                           ("CIRCUIT", "Circuit", "CIR", num_circuit, circuit_waypoints), 
                                                                           ("RACE", "Checkpoint", "RACE", num_checkpoint, checkpoint_waypoints)]:
        
        for i in range(num_files):
            file_name = f"{race_type}{i}WAYPOINTS.CSV"
            
            with open(file_name, "w") as f:
                ordinal = lambda n: "%d%s" % (n, "tsnrhtdd"[((n//10%10!=1)*(n%10<4)*n%10)::4])
                f.write(f"# This is your {ordinal(i)} {race_description} race Waypoint file\n")
                
                for waypoint in race_waypoints[i][0]:
                    f.write(waypoint + "\n")
            shutil.move(file_name, os.path.join("SHOP", "RACE", f"{city_name}", file_name))
            
        # Set MMDATA.CSV values           
        car_type, difficulty, opponent, num_laps_checkpoint = 0, 1, 8, 99
        cops_x = 0.0 # will be customizable later
        ambient_x = 0.0 # will be customizable later
        peds_x = 0.0 # will be customizable later
                
        # Create MMDATA.CSV files
        mm_file_name = f"MM{race_type}DATA.CSV"
        with open(mm_file_name, "w") as f:
            
            f.write("Description, CarType, TimeofDay, Weather, Opponents, Cops, Ambient, Peds, NumLaps, TimeLimit, Difficulty, CarType, TimeofDay, Weather, Opponents, Cops, Ambient, Peds, NumLaps, TimeLimit, Difficulty\n")
            
            for i in range(num_files):
                if race_type == "BLITZ":
                    
                    blitz_waypoints, timeofday, weather, timelimit, num_laps_blitz = race_waypoints[i]  
                    
                    race_data = car_type, timeofday, weather, opponent, cops_x, ambient_x, peds_x, num_laps_blitz, timelimit, difficulty, car_type, timeofday, weather, opponent, cops_x, ambient_x, peds_x, num_laps_blitz, timelimit, difficulty

                elif race_type == "CIRCUIT":
                    
                    circuit_waypoints, timeofday, weather, num_laps_a, num_laps_p = race_waypoints[i]  
                    
                    race_data = car_type, timeofday, weather, opponent, cops_x, ambient_x, peds_x, num_laps_a, timelimit, difficulty, car_type, timeofday, weather, opponent, cops_x, ambient_x, peds_x, num_laps_p, timelimit, difficulty
                    
                elif race_type == "RACE":
                    
                    checkpoint_waypoints, timeofday, weather = race_waypoints[i] 
                    
                    race_data = car_type, timeofday, weather, opponent, cops_x, ambient_x, peds_x, num_laps_checkpoint, timelimit, difficulty, car_type, timeofday, weather, opponent, cops_x, ambient_x, peds_x, num_laps_checkpoint, timelimit, difficulty
                    
                # Race prefixes    
                if race_type == "RACE":
                    race_data_str = ', '.join(map(str, race_data))
                    f.write(f"{race_prefixes[i]}, {race_data_str}\n") 
                else:
                    race_data_str = ', '.join(map(str, race_data))
                    f.write(f"{prefix}{i}, {race_data_str}\n") 
                                    
        destination_path = os.path.join("SHOP", "RACE", city_name, mm_file_name)
        shutil.move(mm_file_name, destination_path)
        
    # Create COPSWAYPOINTS.CSV file
    cnr_csv_file = "COPSWAYPOINTS.CSV"
    with open(cnr_csv_file, "w") as f:
        f.write("This is your Cops & Robbers file, note the structure (per 3): Bank/Blue Team Hideout, Gold, Robber/Red Team Hideout\n")
        for i in range(0, len(cnr_waypoints), 3):
            f.write(", ".join(map(str, cnr_waypoints[i])) + ",0,0,0,0,0,\n") 
            f.write(", ".join(map(str, cnr_waypoints[i+1])) + ",0,0,0,0,0,\n")
            f.write(", ".join(map(str, cnr_waypoints[i+2])) + ",0,0,0,0,0,\n")
        
    shutil.move(cnr_csv_file, os.path.join("SHOP", "RACE", f"{city_name}", cnr_csv_file))

    # Create OPPONENT files
    if all_races_files:
        for race_type, prefix, num_files in [("BLITZ", "B", num_blitz), ("CIRCUIT", "C", num_circuit), ("RACE", "R", num_checkpoint)]:
            for race_index in range(num_files):
                for opp_index in range(1, num_opponents + 1):
                    opp_file_name = f"OPP{opp_index}{race_type}{race_index}.{prefix}{race_index}"
                    with open(opp_file_name, "w") as f:
                        f.write("# This your Opponent file for opponent number #..., in race ...")
                    shutil.move(opp_file_name, os.path.join("SHOP", "RACE", f"{city_name}", opp_file_name)) 
                    
               # Create AIMAP_P files
                aimap_file_name = f"{race_type}{race_index}.AIMAP_P"
                with open(aimap_file_name, "w") as f:
                    f.write("# Ambient Traffic Density \n[Density] \n" + str(ambient_density) + "\n\n")
                    f.write("# Default Road Speed Limit \n[Speed Limit] \n45 \n\n")
                    f.write("# Ambient Traffic Exceptions\n# Rd Id, Density, Speed Limit \n[Exceptions] \n0 \n\n")
                    f.write("# Police Init \n# Geo File, StartLink, Start Dist, Start Mode, Start Lane, Patrol Route \n")
                    f.write("[Police] \n0 \n# vpcop 50.0 0.0 30.0 -90.0 0 4 \n\n")
                    
                    f.write("# Opponent Init, Geo File, WavePoint File \n[Opponent] \n") 
                    f.write(str(num_opponents) + "\n")
                    
                    for opp_index in range(1, num_opponents + 1):
                        f.write(f"{opponent_car} OPP{opp_index}{race_type}{race_index}.{prefix}{opp_index}\n")
                        
                shutil.move(aimap_file_name, os.path.join("SHOP", "RACE", f"{city_name}", aimap_file_name))
    
    # Create CELLS file
    cells_file_path = os.path.join("SHOP", "CITY", f"{city_name}.CELLS")
    with open(cells_file_path, "w") as cells_file:
        set_max_cell = 1000
        bms_count = len(bms_files)
        cells_file.write(f"{bms_count}\n")
        cells_file.write(str(set_max_cell) + "\n")

        sorted_bms_files = sorted(bms_files)
        for bound_number in sorted_bms_files:
            remaining_bound_numbers = [num for num in sorted_bms_files if num != bound_number]
            count_past_4th = len(remaining_bound_numbers)
            
            # Implement Cell type here
            if bound_number in bms_a2_files:
                row = f"{bound_number},32,4,{count_past_4th}"
            else:
                row = f"{bound_number},8,0,{count_past_4th}"
                
            '''
            1 = tunnel          Is Tunnel (Echo, No Lighting, No Reflections, No Ptx) 
            3 = tunnel v2?
            2 = indoors
            4 = water_move if _A2, buffer 32 and texture "T_WATER"
            20 = Zenable            (?)
            80 = FogValue = 0.25    (?)
            200 = No Skids
            '''
            
            for num in remaining_bound_numbers:
                row += f",{num}"
            row += "\n"
            
            # Max 256 characters per row
            row = row[:256]
            cells_file.write(row)
            
    # Copy CMD.exe, RUN.bat, and SHIP.bat to SHOP folder
    for file in os.listdir("angel"):
        if file in ["CMD.EXE", "RUN.BAT", "SHIP.BAT"]:
            shutil.copy(os.path.join("angel", file), os.path.join("SHOP", file))
                
# Create ANIM
def create_anim(city_name, anim_data, set_anim=False):
    if set_anim:
        output_folder_anim = os.path.join("SHOP", "CITY", f"{city_name}")
        main_anim_file = os.path.join(output_folder_anim, "ANIM.CSV")

        # Create ANIM.CSV file and write anim names
        with open(main_anim_file, 'w', newline='') as file:
            writer = csv.writer(file)
            for obj in anim_data.keys():
                writer.writerow([f"anim_{obj}"])

        # Create Individual ANIM files and write Coordinates
        for obj, coordinates in anim_data.items():
            file_name = os.path.join(output_folder_anim, f"ANIM_{obj.upper()}.CSV")
            with open(file_name, 'w', newline='') as file:
                writer = csv.writer(file)
                if coordinates:
                    for coordinate in coordinates:
                        writer.writerow(coordinate)
              
# Create AR file and delete folders
def create_ar_file(city_name, destination_folder, create_plus_move_ar=False, delete_shop=False):
    if create_plus_move_ar:
        os.chdir("SHOP")
        command = f"CMD.EXE /C run !!!!!{city_name}_City"
        subprocess.run(command, shell=True)
        os.chdir("..")

        for file in os.listdir("build"):
            if file.endswith(".ar") and file.startswith(f"!!!!!{city_name}_City"):
                shutil.move(os.path.join("build", file), os.path.join(destination_folder, file))
                
    try:
        shutil.rmtree("build")
    except Exception as e:
        print(f"Failed to delete the build directory. Reason: {e}")
    
    if delete_shop:
        try:
            shutil.rmtree("SHOP")
        except Exception as e:
            print(f"Failed to delete the SHOP directory. Reason: {e}")
    
    
# Create JPG Picture of Shapes (correct sorting)
def plot_polygons(show_label=False, plot_picture=False, export_jpg=False, 
                  x_offset=0, y_offset=0, line_width=1, background_color='black', debug=False):
    
    # Setup
    output_folder_city = os.path.join("SHOP", "BMP16")
    output_folder_cwd = os.getcwd() 
    
    hudmap_picture640 = city_name + "640.JPG"
    hudmap_picture320 = city_name + "320.JPG"
    hudmap_debug = city_name + "_DEBUG.JPG"
    
    # Declare all_polygons_picture as global
    global all_polygons_picture
    
    def draw_polygon(ax, polygon, color, label=None, add_label=False):
        xs, ys = zip(*[(point[0], point[2]) for point in polygon])
        xs, ys = xs + (xs[0],), ys + (ys[0],)
        ax.plot(xs, ys, color=color, linewidth=line_width)
        
        if add_label: # control label addition
            center = calculate_center_tuples(polygon)
            ax.text(center[0], center[2], label, color='white', ha='center', va='center', fontsize=4.0)

    if plot_picture or export_jpg:
        fig, ax = plt.subplots()
        ax.set_facecolor(background_color)

        # Sort the vertex_coordinates in all_polygons_picture
        all_polygons_picture = [sort_coordinates(polygon) for polygon in all_polygons_picture]

        # Enumeration should be based on the bound_number
        for i, polygon in enumerate(all_polygons_picture):
            draw_polygon(ax, polygon, color=f'C{i}', label=f'{i+1}' if show_label else None, add_label=False) # note: do not remove "C" from "C{i}"

        ax.set_aspect('equal', 'box')
        
        if show_label:
            plt.legend()
        
        if export_jpg:
            ax.axis('off')
            trans = mtransforms.Affine2D().translate(x_offset, y_offset) + ax.transData
            for line in ax.lines:
                line.set_transform(trans)
            plt.savefig(os.path.join(output_folder_city, hudmap_picture640), dpi=1000, bbox_inches='tight', pad_inches=0.01, facecolor=background_color)
            plt.savefig(os.path.join(output_folder_city, hudmap_picture320), dpi=1000, bbox_inches='tight', pad_inches=0.01, facecolor=background_color)

            if debug:
                ax.cla()
                ax.set_facecolor(background_color)
                for i, polygon in enumerate(all_polygons_picture):
                    draw_polygon(ax, polygon, color=f'C{i}', label=f'{i+1}' if show_label else None, add_label=True)
                plt.savefig(os.path.join(output_folder_cwd, hudmap_debug), dpi=1000, bbox_inches='tight', pad_inches=0.01, facecolor='white')
                    
        if plot_picture:
            plt.show()

# Create {city_name}.EXT file            
def create_ext_file(city_name, polygonz):
    min_x = min(point[0] for polygon in polygonz for point in polygon)
    max_x = max(point[0] for polygon in polygonz for point in polygon)
    min_z = min(point[2] for polygon in polygonz for point in polygon)
    max_z = max(point[2] for polygon in polygonz for point in polygon)

    output_folder_ext = os.path.join("SHOP", "CITY")       

    ext_file = city_name + ".EXT"
    ext_file_path = os.path.join(output_folder_ext, ext_file)
    os.makedirs(output_folder_ext, exist_ok=True)

    with open(ext_file_path, 'w') as f:
        f.write(f"{min_x} {min_z} {max_x} {max_z}")
       
# Create Bridges       
def create_bridges(all_bridges, create_bridges=False):
    for bridge in all_bridges:
        drawbridge_offset, bridge_orientation, bridge_number, bridge_object = bridge
        # Vertical
        if bridge_orientation == "vertical":
            drawbridge_facing = [drawbridge_offset[0] - 10, drawbridge_offset[1], drawbridge_offset[2]]
        elif bridge_orientation == "vertical_flipped":
            drawbridge_facing = [drawbridge_offset[0] + 10, drawbridge_offset[1], drawbridge_offset[2]]
        # Horizontal
        elif bridge_orientation == "horizontal_east":
            drawbridge_facing = [drawbridge_offset[0], drawbridge_offset[1], drawbridge_offset[2] + 10]
        elif bridge_orientation == "horizontal_west":
            drawbridge_facing = [drawbridge_offset[0], drawbridge_offset[1], drawbridge_offset[2] - 10]
        # Diagonal North    
        elif bridge_orientation == "north_east":
            drawbridge_facing = [drawbridge_offset[0] + 10, drawbridge_offset[1], drawbridge_offset[2] + 10]
        elif bridge_orientation == "north_west":
            drawbridge_facing = [drawbridge_offset[0] + 10, drawbridge_offset[1], drawbridge_offset[2] - 10]
        # Diagonal South   
        elif bridge_orientation == "south_east":
            drawbridge_facing = [drawbridge_offset[0] - 10, drawbridge_offset[1], drawbridge_offset[2] + 10]
        elif bridge_orientation == "south_west":
            drawbridge_facing = [drawbridge_offset[0] - 10, drawbridge_offset[1], drawbridge_offset[2] - 10]
        else:
            print("Invalid Bridge Orientation. Please choose from 'vertical', 'vertical flipped', 'horizontal_east', 'horizontal_west', 'north_east', 'north_west', 'south_east', or 'south_west'.")
            return

        drawbridge_values = (bridge_object, 0) + drawbridge_offset + tuple(drawbridge_facing)
        bridge_data = f"DrawBridge{bridge_number}\n" + '\t' + ','.join(map(str,drawbridge_values)) + '\n' + ('\t'+ filler_object_xyz + '\n') * 5 + f"DrawBridge{bridge_number}\n"
                
        if create_bridges:
            bridge_file_path = os.path.join("SHOP", "CITY", f"{city_name}.GIZMO")
            with open(bridge_file_path, "a") as f:
                if bridge_data is not None:
                    f.write(bridge_data)
                else:
                    pass
                
                  
class BinaryBanger:
    def __init__(self, start: Vector3, end: Vector3, name: str):
        self.room = 4
        self.flags = 0x800
        self.start = start
        self.end = end
        self.name = name

    def __repr__(self):
        return 'BinaryBanger\n Room: {}\n Flags: {}\n Start: {}\n End: {}\n Name: {}\n\n'.format(
            self.Room, self.Flags, self.Start, self.End, self.Name)
        
class BNGFileWriter:
    def __init__(self, filename: str):
        self.filename = filename
        self.objects = []       
        
    def write_props(self, set_props: bool = False):
        if set_props:
            """Write object data to a file."""
            with open(self.filename, mode="wb") as f:
                f.write(struct.pack('<I', len(self.objects)))
            
                for obj in self.objects:
                    f.write(struct.pack('<HH3f3f', obj.room, obj.flags, obj.start.x, obj.start.y, obj.start.z, obj.end.x, obj.end.y, obj.end.z))

                    for char in obj.name: 
                        f.write(struct.pack('<s', bytes(char, encoding='utf8'))) 
                    
    def add_props(self, new_objects: List[Tuple[Union[int, float], ...]]):
        """Add props to the object datalist.
        Args:
            new_objects: list of objects containing [start_x, start_y, start_z, end_x, end_y, end_z, name]
        """
        for obj in new_objects:
            start_x, start_y, start_z, end_x, end_y, end_z, name = obj
            start = Vector3(start_x, start_y, start_z)
            end = Vector3(end_x, end_y, end_z)
            self.objects.append(BinaryBanger(start, end, name + "\x00"))
   
bng_file_path = os.path.join("SHOP", "CITY", f"{city_name}.BNG")  
writer = BNGFileWriter(bng_file_path)

#################################################################################
#################################################################################

physics_folder = os.path.join("SHOP", "MTL")
os.makedirs(physics_folder, exist_ok=True)

input_physics_file = "input_PHYSICS.DB" # cwd
output_physics_file = "physics.db"


class MaterialEditor:
    def __init__(self, name, friction, elasticity, drag, bump_height, bump_width, bump_depth, sink_depth, type, sound, velocity, ptx_color):
        self.name = name
        self.friction = friction
        self.elasticity = elasticity
        self.drag = drag
        self.bump_height = bump_height
        self.bump_width = bump_width
        self.bump_depth = bump_depth
        self.sink_depth = sink_depth
        self.type = type
        self.sound = sound
        self.velocity = velocity
        self.ptx_color = ptx_color 

    @staticmethod
    def read_physics_db(file_name):
        with open(file_name, 'rb') as file:
            count_data = file.read(4)
            count = struct.unpack(">I", count_data)[0]

            agi_phys_parameters = []

            for _ in range(count):
                name_data = file.read(32)
                name = name_data.decode("latin-1").rstrip('\x00')

                params_data = file.read(36)
                params = struct.unpack(">7f2I", params_data)

                velocity_data = file.read(8)
                velocity = Vector2(*struct.unpack(">2f", velocity_data))

                ptx_color_data = file.read(12)
                ptx_color = Vector3(*struct.unpack(">3f", ptx_color_data))

                agi_phys_param = MaterialEditor(name, *params, velocity, ptx_color)
                agi_phys_parameters.append(agi_phys_param)

        return agi_phys_parameters

    @classmethod
    def read_binary(cls, file_name):
        return cls.read_physics_db(file_name)

    @staticmethod
    def write_physics_db(file_name, agi_phys_parameters):
        with open(file_name, 'wb') as file:
            count = len(agi_phys_parameters)
            count_data = struct.pack(">I", count)
            file.write(count_data)

            for param in agi_phys_parameters:
                name_data = param.name.encode("latin-1").ljust(32, b'\x00')
                file.write(name_data)

                params_data = struct.pack(">7f2I", param.friction, param.elasticity, param.drag, param.bump_height, param.bump_width, param.bump_depth, param.sink_depth, param.type, param.sound)
                file.write(params_data)

                velocity_data = struct.pack(">2f", param.velocity.x, param.velocity.y)
                file.write(velocity_data)

                ptx_color_data = struct.pack(">3f", param.ptx_color.x, param.ptx_color.y, param.ptx_color.z)
                file.write(ptx_color_data)

    @classmethod
    def change_physics_db(cls, input_file_name, output_file_name, properties, index=None):
        agi_phys_parameters = cls.read_binary(input_file_name)

        if index is not None:
            for prop, value in properties.items():
                setattr(agi_phys_parameters[index], prop, value)
        else:
            for param in agi_phys_parameters:
                for prop, value in properties.items():
                    setattr(param, prop, value)

        cls.write_physics_db(output_file_name, agi_phys_parameters)

    @staticmethod
    def create_from_scratch(output_file_name, agi_phys_parameters):
        MaterialEditor.write_physics_db(output_file_name, agi_phys_parameters)
        
    def __repr__(self):
        cleaned_name = self.name.rstrip()
        return (f"AgiPhysParameters(\n"
                f"  name        = '{cleaned_name}',\n"
                f"  friction    = {self.friction:.2f},\n"
                f"  elasticity  = {self.elasticity:.2f},\n"
                f"  drag        = {self.drag:.2f},\n"
                f"  bump_height = {self.bump_height:.2f},\n"
                f"  bump_width  = {self.bump_width:.2f},\n"
                f"  bump_depth  = {self.bump_depth:.2f},\n"
                f"  sink_depth  = {self.sink_depth:.2f},\n"
                f"  type        = {self.type},\n"
                f"  sound       = {self.sound},\n"
                f"  velocity    = {self.velocity},\n"
                f"  ptx_color   = {self.ptx_color}\n\n")

     
# Start GAME
def start_game(destination_folder, play_game=False):
    game_path = os.path.join(destination_folder, shortcut_or_exe_name)
    if play_game:
        subprocess.run(game_path, cwd=destination_folder, shell=True)


################################################################################################################               
################################################################################################################

# SET PROPS
# x,y,z (offset), x,y,z (facing), name
writer.add_props([
    [-10, 0.1, -10, -10, 0.1, -10000, "tp_trailer"],
    [10, 0.1, -10, 10, 0.1, -10000, "tp_trailer"]])

# Set multiple props at once with a separator value
for i in range(50):
    writer.add_props([[-50 + (i*4), -30, 0, 0, 0, 0, "TP_BARRICADE"]])

################################################################################################################     

# SET MATERIALS
# material ID you want to change. You can then use this number in 'material_index' in create_and_append_polygon()
index = 98 
# indices that you can use / are "free": 94, 95, 96, 97, 98
# for more info, see: https://github.com/0x1F9F1/Open1560/commit/a8fea1ebb00bbe24bd501264cfe7596c9df0bfaf

# other properties you can change: bump_height, bump_width, bump_depth, sink_depth, type, sound, velocity, ptx_color  
# (for more info see: "PHYSICS_DB_extracted.txt") --- velocity is likely not used by the game, the other variables have not been tested yet
properties = {"friction": 0.01, 
              "elasticity": 0.01, 
              "drag": 0.01}

################################################################################################################   

# Call FUNCTIONS
print("\n===============================================")
print("\nGenerating " + f"{race_locale_name}... \n")
print("===============================================\n")

# Material related
materials = MaterialEditor.read_binary(input_physics_file) 
index = index - 1
MaterialEditor.change_physics_db(input_physics_file, output_physics_file, properties, index)

new_physics_path = os.path.join(physics_folder, output_physics_file)
shutil.move(output_physics_file, new_physics_path)

# The rest
create_folder_structure(city_name)
distribute_generated_files(city_name, bnd_hit_id, num_blitz, blitz_waypoints, num_circuit, circuit_waypoints, num_checkpoint, checkpoint_waypoints, all_races_files=True)

create_ext_file(city_name, all_polygons_picture) 
create_anim(city_name, anim_data, set_anim=False)   # change to "True" if you want ANIM
create_bridges(bridges, create_bridges=False)       # change to "True" if you want BRIDGES (be cautious)
writer.write_props(set_props=False)                 # change to "True" if you want PROPS

# Offset for Moronville is approximately, x_offset=-22.4, y_offset=-40.7
# Automated HUD alignment is not implemented yet
plot_polygons(show_label=False, plot_picture=False, export_jpg=True, 
              x_offset=-0.0, y_offset=-0.0, 
              line_width=0.7, background_color='black', debug=False)


create_ar_file(city_name, destination_folder, create_plus_move_ar=True, delete_shop=True)

print("\n===============================================")
print("\nSuccesfully created " + f"{race_locale_name}!\n")
print("===============================================\n")

start_game(destination_folder, play_game=False)