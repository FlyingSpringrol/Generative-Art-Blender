import math
import random
import bmesh
from bpy import ops, context

def dump(obj, leva=0):
	for attr in dir(obj):
		if hasattr( obj, "attr" ):
			print( "obj.%s = %s" % (attr, getattr(obj, attr)))
		else:
			print( attr )

def run():
	o = bpy.context.active_object
	me = o.data
	bm = bmesh.new()
	bm.from_mesh(me)
	bm.edges.ensure_lookup_table()
	for e in bm.edges:
		v1 = e.verts[0]
		v2 = e.verts[1]
		create_line(v1, v2)
	bm.verts.ensure_lookup_table()
	for v in bm.verts:
		create_node(v)
	bm.to_mesh(me)
	me.update()
	bpy.context.scene.update()

def create_node(v1):
	ops.mesh.primitive_ico_sphere_add(size=.04)
	node = context.active_object
	node.location = v1.co

def create_line(v1, v2):
	diff = v2.co-v1.co
	n_diff = diff.normalized() #normalize difference
	ops.mesh.primitive_cube_add(radius=.01)
	cube = context.active_object
	#grab the end verts before rotating
	cube_me = cube.data
	cube_bm = bmesh.new()
	cube_bm.from_mesh(cube_me)
	top_vs = return_top_cube_verts(cube_bm)
	cube.location = v1.co #not scale invariant for some reason??
	#compute the rotation, special case because cylinder is upright
	cube.rotation_mode = 'QUATERNION'
	cube.rotation_quaternion = n_diff.to_track_quat('Z','Y')
	#now move the top part
	for v in top_vs:
		v.co += Vector((0.0, 0.0, diff.length))
	cube_bm.to_mesh(cube_me)
	cube_me.update()
	bpy.context.scene.update()

def return_top_cube_verts(cube_bm):
	max_z = -math.inf
	sel = []
	cube_bm.verts.ensure_lookup_table()
	for v in cube_bm.verts:
		if v.co.z > max_z:
			max_z = v.co.z
	for v in cube_bm.verts:
		if v.co.z >= max_z:
			sel.append(v)
	return sel