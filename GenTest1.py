import bmesh
import math
import random

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
	faces = bm.faces[:]
	for face in faces:
	    r = bmesh.ops.extrude_discrete_faces(bm, faces=[face])
	    face = r['faces'][0]
	    extrude_bunch(bm, face, 10)
	bm.to_mesh(me)
	me.update()
	bpy.context.scene.update()

def extrude_bunch(bm, face, n):
	mats = 5
	for i in range(n):
		holder = bmesh.ops.extrude_discrete_faces(bm, faces=[face]) #should select?
		face = holder['faces'][0]
		quat_a = Quaternion((1.0, 0.0, 0.0), math.radians(20.0)).to_matrix()
		quat_b = Quaternion((0.0, 1.0, 0.0), math.radians(20.0)).to_matrix()
		quat_c = quat_a * quat_b
		for v in face.verts:
			v.co = v.co * quat_c
		face.material_index = random.randint(0, mats)
		bmesh.ops.translate(bm, vec=face.normal, verts=face.verts)


