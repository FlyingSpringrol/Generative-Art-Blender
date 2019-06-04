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
	    scale_face(face, .2)
	    extrude_arcs(bm, o, face)
	bm.to_mesh(me)
	me.update()
	bpy.context.scene.update()

#need to compute distance away from 0:returns magnitude of distance from 0
def orig_dist(mat, face):
	v_sum = Vector()
	for v in face.verts:
		v_sum += mat * v.co #convert to world space
	return v_sum.length

def scale_face(face, factor):
	mat = Matrix.Scale(factor, 4)
	for v in face.verts:
		v.co = mat * v.co

#have it work on a flat plane, with faces facing upwards
def extrude_arcs(bm, ob, face):
	#farther away from origin, the lower the slope
	mat = ob.matrix_world
	extrusions = 4
	angle = 2.0 + random.random() * 1.0/orig_dist(mat, face) #will get closer to zero?
	quat_a = Quaternion((1.0, 0.0, 0.0), math.radians(angle)).to_matrix()
	#size down
	for i in range(extrusions):
		holder = bmesh.ops.extrude_discrete_faces(bm, faces=[face]) #should select?
		face = holder['faces'][0]
		bmesh.ops.translate(bm, vec=face.normal, verts=face.verts)
		for v in face.verts:
			v.co = quat_a * v.co

