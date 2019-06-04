import math
import random
from bpy import context, data, ops


def dump(obj, leva=0):
	for attr in dir(obj):
		if hasattr( obj, "attr" ):
			print( "obj.%s = %s" % (attr, getattr(obj, attr)))
		else:
			print( attr )

def create_rings():
	for i in range(20):
		# Create a bezier circle and enter edit mode.
		ops.curve.primitive_bezier_circle_add(radius=1.0,location=(0.0, 0.0, 0.0),enter_editmode=True)
		ops.transform.resize(value=(1.0, i*2.0, 1.0))
		ops.object.mode_set(mode='OBJECT')
		obj_data = context.active_object.data
		# Which parts of the curve to extrude ['HALF', 'FRONT', 'BACK', 'FULL'].
		obj_data.fill_mode = 'FULL'
		# Breadth of extrusion.
		obj_data.extrude = 0.0125
		# Depth of extrusion.
		obj_data.bevel_depth = 0.0125
		# Smoothness of the segments on the curve.
		obj_data.resolution_u = 20
		obj_data.render_resolution_u = 32

def run():
	# Create a bezier circle and enter edit mode.
	ops.curve.primitive_bezier_curve_add(radius=1.0,location=(0.0, 0.0, 0.0),enter_editmode=True)
	curve = context.active_object
	points = curve.data.splines[0].bezier_points
	# Subdivide the curve by a number of cuts, giving the
	# random vertex function more points to work with.
	bpy.ops.curve.handle_type_set(type='FREE_ALIGN') #need this to move them freely without recomputation 
	ops.curve.subdivide(number_cuts=3)
	for i,p in enumerate(points):
		shift = Vector((1.0, 1.0, 0.0))
		#p.handle_left = p.co
		#p.handle_right = p.co
		p.co += shift
		p.handle_left += shift
		p.handle_right += shift #can set them but can't shift them?
		#p.co += shift