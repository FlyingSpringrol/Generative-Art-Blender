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

def disp(amount): #am is displacement
	o = bpy.context.active_object
	me = o.data
	bm = bmesh.new()
	bm.from_mesh(me)
	#now slice
	bm.verts.ensure_lookup_table()
	for v in bm.verts:
		fac = amount
		v.co += Vector((fac*(random.random()-.5),fac*(random.random()-.5),fac*(random.random()-.5)))
	#now run updates
	bm.to_mesh(me)
	me.update()
	bpy.context.scene.update()
	#assumes that all the edges have been selected
	#add in the slices on each edge selection, may have to do this one by one
	bpy.ops.object.mode_set(mode = 'EDIT')
	bm.free()