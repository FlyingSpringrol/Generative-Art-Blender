import math
import random
import bmesh
from bpy import ops, context

#questions:
#how does the bisection algorithm work
#how does the face fill algorithm work

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
	deselect_e(bm)
	deselect_v(bm)
	deselect_f(bm)
	slice(bm)
	#now run updates
	bm.to_mesh(me)
	me.update()
	bpy.context.scene.update()
	#assumes that all the edges have been selected
	#add in the slices on each edge selection, may have to do this one by one
	bpy.ops.object.mode_set(mode = 'EDIT')
	bm.free()

def slice(bm):
	xmin, xmax = measure(bm)
	z = .24 # cut at a reasonably small place
	slice_in_edge(bm, z)
		
#slice in three edges, delete the middle
def slice_in_edge(bm, z):
	bm.edges.ensure_lookup_table()
	bm.faces.ensure_lookup_table()
	bm.verts.ensure_lookup_table()
	edges = [e for e in bm.edges]
	faces = [f for f in bm.faces]
	geom = []
	geom.extend(edges)
	geom.extend(faces)
	#first cut group
	offset = .001
	target_slice = z
	target_slice_up = z + offset
	#mi
	result = bmesh.ops.bisect_plane(bm,
		dist=0.0000001, 
		geom=geom,
		plane_co=(0, 0, target_slice),
		plane_no=(0, 0, 1),
	)
	geom = result['geom']
	result = bmesh.ops.bisect_plane(bm,
		dist=0.0000001, 
		geom=geom,
		plane_co=(0, 0, target_slice_up),
		plane_no=(0, 0, 1),
	)
	geom = result['geom']
	#cuts, now deselect
	bm.verts.ensure_lookup_table()
	#remove other cuts
	for v in bm.verts:
		if math.isclose(v.co.z, target_slice, abs_tol=.0000001) or v.co.z < target_slice:
			bm.verts.remove(v)
	bm.edges.ensure_lookup_table()
	#top part
	to_fill = []
	for e in bm.edges:
		v1 = e.verts[0]
		v2 = e.verts[1]
		if math.isclose(v1.co.z, target_slice_up, abs_tol=.0000001) and math.isclose(v2.co.z, target_slice_up, abs_tol=.0000001): #if on a high edge
			to_fill.append(e)
			e.select = True
	bmesh.ops.holes_fill(bm, edges=to_fill)
