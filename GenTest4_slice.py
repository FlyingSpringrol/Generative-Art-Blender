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
	#bpy.ops.mesh.remove_doubles(threshold=.001) #smaller than divisions
	bm.free()

def slice(bm):
	xmin, xmax = measure(bm)
	numslices = 4
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
	offset = .001
	mid_offset = .01
	#first cut group
	target_down1 = i
	target_down2 = target_down1 + offset
	target_down3 = target_down2 + offset
	target_down4 = target_down3 + offset
	#mi
	target_mid = target_down4 + mid_offset
	#second group
	target_up1 = target_mid + mid_offset
	target_up2 = target_up1 + offset
	target_up3 = target_up2 + offset
	target_up4 = target_up3 + offset
	#first three
	result = bmesh.ops.bisect_plane(bm,
		dist=0.0000001, 
		geom=geom,
		plane_co=(0, 0, target_down1),
		plane_no=(0, 0, 1),
	)
	geom = result['geom']
	result = bmesh.ops.bisect_plane(bm,
		dist=0.0000001, 
		geom=geom,
		plane_co=(0, 0, target_down2),
		plane_no=(0, 0, 1),
	)
	geom = result['geom']
	result = bmesh.ops.bisect_plane(bm,
		dist=0.0000001, 
		geom=geom,
		plane_co=(0, 0, target_down3),
		plane_no=(0, 0, 1),
	)
	geom = result['geom']
	result = bmesh.ops.bisect_plane(bm,
		dist=0.0000001, 
		geom=geom,
		plane_co=(0, 0, target_down4),
		plane_no=(0, 0, 1),
	)
	geom = result['geom']
	result = bmesh.ops.bisect_plane(bm,
		dist=0.0000001, 
		geom=geom,
		plane_co=(0, 0, target_mid),
		plane_no=(0, 0, 1),
	)
	geom = result['geom']
	result = bmesh.ops.bisect_plane(bm,
		dist=0.0000001, 
		geom=geom,
		plane_co=(0, 0, target_up1),
		plane_no=(0, 0, 1),
	)
	geom = result['geom']
	result = bmesh.ops.bisect_plane(bm,
		dist=0.0000001, 
		geom=geom,
		plane_co=(0, 0, target_up2),
		plane_no=(0, 0, 1),
	)
	geom = result['geom']
	result = bmesh.ops.bisect_plane(bm,
		dist=0.0000001, 
		geom=geom,
		plane_co=(0, 0, target_up3),
		plane_no=(0, 0, 1),
	)
	geom = result['geom']
	result = bmesh.ops.bisect_plane(bm,
		dist=0.0000001, 
		geom=geom,
		plane_co=(0, 0, target_up4),
		plane_no=(0, 0, 1),
	)
	geom = result['geom']
	#cuts, now deselect
	bm.verts.ensure_lookup_table()
	#remove other cuts
	for v in bm.verts:
		if math.isclose(v.co.z, target_up1, abs_tol=.0000001) or math.isclose(v.co.z, target_up3, abs_tol=.0000001) or math.isclose(v.co.z, target_down2, abs_tol=.0000001) or math.isclose(v.co.z, target_down4, abs_tol=.0000001) or math.isclose(v.co.z, target_mid, abs_tol=.00001):
			bm.verts.remove(v)
	bm.edges.ensure_lookup_table()
	to_fill = []
	for e in bm.edges:
		v1 = e.verts[0]
		v2 = e.verts[1]
		if math.isclose(v1.co.z, target_down3, abs_tol=.00001) and math.isclose(v2.co.z, target_down3, abs_tol=.00001): #if on a high edge
			to_fill.append(e)
			e.select = True
	bmesh.ops.holes_fill(bm, edges=to_fill)
	#bottom part:
	to_fill = []
	for e in bm.edges:
		v1 = e.verts[0]
		v2 = e.verts[1]
		if math.isclose(v1.co.z, target_up2, abs_tol=.00001) and math.isclose(v2.co.z, target_up2, abs_tol=.00001): #if on a high edge
			to_fill.append(e)
			e.select = True
	bmesh.ops.holes_fill(bm, edges=to_fill)
