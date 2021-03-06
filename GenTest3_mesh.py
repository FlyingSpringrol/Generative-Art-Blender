import math
import random
import bmesh
from bpy import ops, context
import time


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
	s = time.time()
	#add in profiling
	create_lines(bm)
	#create_nodes(bm)
	bm.to_mesh(me)
	me.update()
	bpy.context.scene.update()
	e = time.time()
	print(e - s)

def create_nodes(bm):
	#why do verts taking longer to iterate through??? there are less of them
	ops.mesh.primitive_ico_sphere_add(size=.03)
	node = context.active_object
	bm.verts.ensure_lookup_table()
	#now run meat of logic
	nodes = []
	for v in bm.verts:
		nodes.append(create_node(node.data, v))
	for node in nodes:
		node.select = True
	bpy.ops.object.join()
	joined = context.active_object
	joined.select = False

def create_node(node_mesh, v1):
	new_m = node_mesh.copy()
	node = bpy.data.objects.new("node", new_m)
	bpy.context.scene.objects.link(node)
	node.location = v1.co
	return node

def create_lines(bm):
	bm.edges.ensure_lookup_table()
	ops.mesh.primitive_cube_add(radius=.01)
	cube = context.active_object
	#grab the end verts before rotating
	cube_me = cube.data
	lines = []
	for e in bm.edges:
		v1 = e.verts[0]
		v2 = e.verts[1]
		lines.append(create_line(cube.data, v1,v2))
	for l in lines:
		l.select = True
	bpy.ops.object.join()


def create_line(cube_me, v1, v2):
	diff = v2.co-v1.co
	n_diff = diff.normalized() #normalize difference
	#make new object
	m = cube_me.copy();
	#now should never use cube_me again
	cube = bpy.data.objects.new("cube", m)
	bpy.context.scene.objects.link(cube) #same mesh???
	cube_bm = bmesh.new()
	cube_bm.from_mesh(cube.data)
	top_vs = return_top_cube_verts(cube_bm)
	cube.location = v1.co #not scale invariant for some reason??
	#compute the rotation, special case because cylinder is upright
	cube.rotation_mode = 'QUATERNION'
	cube.rotation_quaternion = n_diff.to_track_quat('Z','Y')
	#now move the top part
	for v in top_vs:
		v.co += Vector((0.0, 0.0, diff.length))
		a = 2
	cube_bm.to_mesh(m)
	cube_bm.free()
	return cube

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