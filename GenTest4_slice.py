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

def deselect_f(bm):
	for face in bm.faces:
		if face.select:
			face.select = False

def deselect_e(bm):
	for e in bm.edges:
		if e.select:
			e.select = False

def deselect_v(bm):
	for v in bm.verts:
		if v.select:
			v.select = False

def measure(bm):
	xmin = math.inf
	xmax = -math.inf
	for vert in bm.verts:
		if vert.co.z >= xmax:
			xmax = vert.co.z
		if vert.co.z <= xmin:
			xmin = vert.co.z
	return (xmin, xmax)

def run():
	o = bpy.context.active_object
	me = o.data
	bm = bmesh.new()
	bm.from_mesh(me)
	#now slice
	slice(bm)
	#now run updates
	bm.to_mesh(me)
	me.update()
	bpy.context.scene.update()
	#assumes that all the edges have been selected
	#add in the slices on each edge selection
	bpy.ops.object.mode_set(mode = 'EDIT')
	bpy.ops.mesh.edge_face_add()

def slice(bm):
	xmin, xmax = measure(bm)
	numslices = 50
	step = (xmax - xmin) / float(numslices)
	for i in range(numslices):
		z = step * i + xmin
		slice_in_edge(bm, z)
		
#slice in three edges, delete the middle
def slice_in_edge(bm, i):
	bm.edges.ensure_lookup_table()
	bm.faces.ensure_lookup_table()
	bm.verts.ensure_lookup_table()
	edges = [e for e in bm.edges]
	faces = [f for f in bm.faces]
	geom = []
	geom.extend(edges)
	geom.extend(faces)
	#save floats where the vertex z locations should be, hardcoded for now
	offset = 1.0/100.0
	target_up = i
	target_del = i + offset
	target_down = i + 2 * offset
	result = bmesh.ops.bisect_plane(bm,
		dist=0.0000001, 
		geom=geom,
		plane_co=(0, 0, target_down),
		plane_no=(0, 0, 1),
	)
	geom = result['geom']
	result = bmesh.ops.bisect_plane(bm,
		dist=0.0000001, 
		geom=geom,
		plane_co=(0, 0, target_del),
		plane_no=(0, 0, 1),
	)
	geom = result['geom']
	result = bmesh.ops.bisect_plane(bm,
		dist=0.0000001, 
		geom=geom,
		plane_co=(0, 0, target_up),
		plane_no=(0, 0, 1),
	)
	geom = result['geom']
	#cuts, now deselect
	bm.verts.ensure_lookup_table()
	for v in bm.verts:
		if math.isclose(v.co.z, target_del, abs_tol=.0000001): #if on a high edge
			bm.verts.remove(v)
	for v in bm.verts:
		if math.isclose(v.co.z, target_up, abs_tol=.0000001): #if on a high edge
			v.select = True
	for v in bm.verts:
		if math.isclose(v.co.z, target_down, abs_tol=.0000001): #if on a high edge
			v.select = True