import bpy

##################### Update Sculpt Hide Other Shape Layers #############################
def sculpt_single_shape_layer_changed(self, context):
	sculpt_single_shape_layer = context.scene.sculpt_single_shape_layer

	ob = bpy.context.active_object

	current_frame = bpy.context.active_object.active_shape_key_index
	keys = ob.data.shape_keys.key_blocks.keys()
	for shape in ob.data.shape_keys.key_blocks:
		if shape.name == ob.active_shape_key.name or shape.name == 'Base Shape':
			shape.mute = False
		else:
			shape.mute = sculpt_single_shape_layer


class Sculpt_Shape_Layers_Panel(bpy.types.Panel):
	bl_idname = 'SCULPT_PT_shape_layers_panel'
	bl_category = 'TMG'
	bl_label = 'TMG Shape Layers Panel'
	bl_context = "sculpt_mode"
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'UI'
	COMPAT_ENGINES = {'BLENDER_RENDER', 'BLENDER_EEVEE', 'BLENDER_WORKBENCH'}

	@classmethod
	def poll(cls, context):
		engine = context.engine
		obj = context.object
		return (obj and obj.type in {'MESH', 'LATTICE', 'CURVE', 'SURFACE'} and (engine in cls.COMPAT_ENGINES))

	def draw(self, context):

		preferences = context.preferences
		addon_prefs = preferences.addons['tmg-shape-layers-panel'].preferences
		tmg_prefs = context.preferences.addons['tmg-shape-layers-panel'].preferences

		button_mode = tmg_prefs.Sculpt_Button_Mode
		keyframe_timeline = tmg_prefs.Sculpt_Keyframe_Timeline
		shape_settings_menu = tmg_prefs.shape_settings_menu

		scene = context.scene
		sculpt_single_shape_layer = context.scene.sculpt_single_shape_layer

		layout = self.layout

		ob = bpy.context.active_object
		key = ob.data.shape_keys
		kb = ob.active_shape_key

		all_keys = []

		if ob.data.shape_keys:
			for _i in bpy.context.active_object.data.shape_keys.key_blocks.keys():
				all_keys.append(_i)
		
		keys_total = len(all_keys)

		col = self.layout.column(align=True)

		if button_mode:

			if keys_total > 0:

				layout = self.layout.column(align=True)
				panel = layout.column(align=True)
				lay = panel.row(align=False)
				col_1 = lay.row()
				col_2 = lay.row()
				col_3 = lay.row()

				# Button Group 3
				row = col_1.row(align=True)

				row.operator('mesh.sculpt_ot_shape_key_hide_others',
									text='',
									icon='RESTRICT_RENDER_OFF')

				row.operator('mesh.sculpt_ot_keyframe_shape_keys',
									text='',
									icon='KEYINGSET')

				row.operator('mesh.sculpt_ot_clear_all_keyframes',
									text='',
									icon='KEYFRAME',
									)

				row.operator('mesh.sculpt_ot_merge_shape_keys',
									text='',
									icon='SHAPEKEY_DATA',
									)

				row.operator('mesh.sculpt_ot_apply_shape_keys',
									text='',
									icon='MESH_CUBE',
									)

				lay = panel.row(align=True)

				panel = layout.row(align=True)
				lay = panel.row(align=True)
				row = col_3.row(align=True)

				row.prop(addon_prefs, "Sculpt_Keyframe_Timeline", text="", icon='KEY_HLT')
				row.operator('mesh.sculpt_ot_show_tmg_addon_prefs', text='', icon='TOOL_SETTINGS')

				
			else:

				layout = self.layout.column(align=True)
				panel = layout.column(align=True)
				lay = panel.row(align=False)
				col_1 = lay.row()
				col_2 = lay.row()
				col_3 = lay.row()

				row = col_1.row(align=True)

				lay = panel.row(align=True)

				panel = layout.row(align=True)
				lay = panel.row(align=True)
				row = col_3.row(align=True)

				row.prop(addon_prefs, "Sculpt_Keyframe_Timeline", text="", icon='KEY_HLT')
				row.operator('mesh.sculpt_ot_show_tmg_addon_prefs', text='', icon='TOOL_SETTINGS')


		else:

			layout = self.layout.column(align=True)
			panel = layout.column(align=True)
			lay = panel.row(align=False)
			col_1 = lay.row()
			col_2 = lay.row()
			col_3 = lay.row()

			row = col_3.row(align=True)
			row.prop(addon_prefs, "Sculpt_Keyframe_Timeline", text="Keyframe", icon='KEY_HLT')
			
			row.operator('mesh.sculpt_ot_show_tmg_addon_prefs',
								text='Preferences',
								icon='TOOL_SETTINGS')

			if keys_total > 0:

				layout = self.layout.column(align=True)
				panel = layout.column(align=True)

				row = panel.column(align=True)

				row.operator('mesh.sculpt_ot_shape_key_hide_others',
									text='Toggle Other Layers',
									icon='RESTRICT_RENDER_OFF')

				row.operator('mesh.sculpt_ot_keyframe_shape_keys',
									text='Keyframe Layers',
									icon='KEYINGSET')

				row.operator('mesh.sculpt_ot_clear_all_keyframes',
									text='Clear All Keyframes',
									icon='KEYFRAME',
									)

				row.operator('mesh.sculpt_ot_merge_shape_keys',
									text='Merge Layers',
									icon='SHAPEKEY_DATA',
									)

				row.operator('mesh.sculpt_ot_apply_shape_keys',
									text='Apply Object',
									icon='MESH_CUBE',
									)
								

		layout = self.layout.column(align=True)
		panel = layout.column(align=True)

		enable_edit = ob.mode != 'EDIT'
		enable_edit_value = False

		if ob.show_only_shape_key is False:
			if enable_edit or (ob.type == 'MESH' and ob.use_shape_key_edit_mode):
				enable_edit_value = True

		row = layout.row()

		rows = 3
		if kb:
			rows = 6

		row.template_list("MESH_UL_shape_keys", "", key,
						  "key_blocks", ob, "active_shape_key_index", rows=rows)

		col = row.column(align=True)

		props = col.operator('mesh.sculpt_ot_add_new_shape_layer',
							 text='',
							 icon='ADD')

		col.operator('mesh.sculpt_ot_remove_selected_layer',
							 text='',
							 icon='REMOVE')

		col.separator()


		layout = self.layout.column(align=True)
		panel = layout.column(align=True)
		lay = panel.row(align=False)
		col_1 = lay.row()
		col_2 = lay.row()
		col_3 = lay.row()

		row = col_1.row(align=True)

		if tmg_prefs.shape_settings_menu:
			row.prop(tmg_prefs, "shape_settings_menu", text="", icon='DOWNARROW_HLT')
		else:
			row.prop(tmg_prefs, "shape_settings_menu", text="", icon='RIGHTARROW')

		if button_mode:
			pass
		else:
			row = col_1.row(align=True)

			row.label(text="Layer Settings")

		col.separator()

		col.menu("MESH_MT_shape_key_context_menu",
				icon='DOWNARROW_HLT', text="")

		if kb:
			col.separator()

			sub = col.column(align=True)
			sub.operator("object.shape_key_move",
						icon='TRIA_UP', text="").type = 'UP'
			sub.operator("object.shape_key_move",
						icon='TRIA_DOWN', text="").type = 'DOWN'

			if tmg_prefs.shape_settings_menu:

				layout = self.layout.column(align=True)
				panel = layout.column(align=True)
				lay = panel.row(align=False)
				col_1 = lay.row()
				col_2 = lay.row()
				col_3 = lay.row()

				row = panel.column(align=True)

				boxed_menu = row.box()

				boxed_split = boxed_menu.split(factor=0.4)
				split = boxed_split
				row = split.row()
				row.enabled = enable_edit
				row.prop(key, "use_relative")

				row = split.row()
				row.alignment = 'RIGHT'

				sub = row.row(align=True)
				sub.label()  # XXX, for alignment only
				subsub = sub.row(align=True)
				subsub.active = enable_edit_value
				subsub.prop(ob, "show_only_shape_key", text="")
				sub.prop(ob, "use_shape_key_edit_mode", text="")

				sub = row.row()
				if key.use_relative:
					sub.operator("object.shape_key_clear", icon='X', text="")
				else:
					sub.operator("object.shape_key_retime",
								icon='RECOVER_LAST', text="")

				layout.use_property_split = True
				if key.use_relative:
					if ob.active_shape_key_index != 0:
						row = boxed_menu.row()
						row.active = enable_edit_value
						row.prop(kb, "value")

						col = boxed_menu.column()
						sub.active = enable_edit_value
						sub = col.column(align=True)
						sub.prop(kb, "slider_min", text="Range Min")
						sub.prop(kb, "slider_max", text="Max")

						col.prop_search(kb, "vertex_group", ob,
										"vertex_groups", text="Vertex Group")
						col.prop_search(kb, "relative_key", key,
										"key_blocks", text="Relative To")

				else:
					layout.prop(kb, "interpolation")
					row = layout.column()
					row.active = enable_edit_value
					row.prop(key, "eval_time")


class Sculpt_OT_Show_TMG_Addon_Prefs(bpy.types.Operator):
	"""Shows the TMG addon preferences"""
	bl_idname = 'mesh.sculpt_ot_show_tmg_addon_prefs'
	bl_label = 'Show Preferences'
	bl_description = 'Shows the TMG addon preferences.'
	bl_options = {'REGISTER'}

	def execute(self, context):

		bpy.ops.preferences.addon_show(module="tmg-shape-layers-panel")

		return {'FINISHED'}


class Sculpt_OT_ADD_New_Shape_Layer(bpy.types.Operator):
	"""Sculpt ADD New Shape Layer"""
	bl_idname = 'mesh.sculpt_ot_add_new_shape_layer'
	bl_label = 'New Layer'
	bl_description = 'Add a new shape layer.'
	bl_options = {'REGISTER'}

	@classmethod
	def poll(cls, context):
		return context.area.type == 'VIEW_3D'

	def execute(self, context):

		preferences = context.preferences
		addon_prefs = preferences.addons['tmg-shape-layers-panel'].preferences

		keyframe_timeline = context.preferences.addons['tmg-shape-layers-panel'].preferences.Sculpt_Keyframe_Timeline

		keys = 0
		ob = bpy.context.active_object
		current_frame = bpy.context.active_object.active_shape_key_index

		# Adds Layer with timeline keyframe
		if keyframe_timeline:
			bpy.ops.object.shape_key_add(from_mix=False)
			current_frame = bpy.context.active_object.active_shape_key_index
			keys = ob.data.shape_keys.key_blocks.keys()

			for shape in ob.data.shape_keys.key_blocks:
				if (current_frame == 0):
					shape.name = 'Base Shape'
					shape.keyframe_insert("value", frame=0)
				elif (shape.name == ob.active_shape_key.name):
					shape.name = "Layer " + str(current_frame)
					shape.value = 1.0
					shape.keyframe_insert(
						"value", frame=ob.active_shape_key_index)
					bpy.data.scenes['Scene'].frame_current = ob.active_shape_key_index

		# Adds Layer without timeline keyframe
		else:
			bpy.ops.object.shape_key_add(from_mix=False)
			current_frame = bpy.context.active_object.active_shape_key_index
			keys = ob.data.shape_keys.key_blocks.keys()

			for shape in ob.data.shape_keys.key_blocks:
				if (current_frame == 0):
					shape.name = 'Base Shape'
				elif (shape.name == ob.active_shape_key.name):
					shape.name = "Layer " + str(current_frame)
					shape.value = 1.0

		return {'FINISHED'}

class Sculpt_OT_Shape_Key_Hide_Others(bpy.types.Operator):
	"""Sculpt Shape Key Hide Other Shape Layers"""
	bl_idname = 'mesh.sculpt_ot_shape_key_hide_others'
	bl_label = 'View Selected Layer Only'
	bl_description = 'Only view selected shape layer.'
	bl_options = {'REGISTER'}

	@classmethod
	def poll(cls, context):
		return context.area.type == 'VIEW_3D'

	def execute(self, context):

		ob = bpy.context.active_object
		sculpt_single_shape_layer = context.scene.sculpt_single_shape_layer

		if context.scene.sculpt_single_shape_layer == True:
			sculpt_single_shape_layer = False
			context.scene.sculpt_single_shape_layer = False
		else:
			sculpt_single_shape_layer = True
			context.scene.sculpt_single_shape_layer = True

		return {'FINISHED'}


class Sculpt_OT_Merge_Shape_Keys(bpy.types.Operator):
	"""Sculpt Merge Shape Layers To New Layer"""
	bl_idname = 'mesh.sculpt_ot_merge_shape_keys'
	bl_label = 'Merge Visible'
	bl_description = 'Merge visible shape layers to a new layer.'
	bl_options = {'REGISTER'}

	@ classmethod
	def poll(cls, context):
		return context.area.type == 'VIEW_3D'

	def execute(self, context):

		keys = 0
		ob = bpy.context.active_object
		current_frame = bpy.context.active_object.active_shape_key_index
		keyframe_timeline = context.scene.keyframe_timeline

		for shape in ob.data.shape_keys.key_blocks:
			if keyframe_timeline:
				shape.keyframe_insert(
					"value", frame=bpy.data.scenes['Scene'].frame_current)
				bpy.data.scenes['Scene'].frame_current = bpy.data.scenes['Scene'].frame_current

		bpy.ops.object.shape_key_add(from_mix=True)

		for shape in ob.data.shape_keys.key_blocks:
			if shape.name == ob.active_shape_key.name:
				shape.name = "Applied Shape " + str(current_frame)
				shape.value = 0.0
				if keyframe_timeline:
					shape.keyframe_insert(
						"value", frame=ob.active_shape_key_index)
					bpy.data.scenes['Scene'].frame_current = ob.active_shape_key_index

		return {'FINISHED'}


class Sculpt_OT_Keyframe_Shape_Keys(bpy.types.Operator):
	"""Set all shape layer's value on current frame"""
	bl_idname = 'mesh.sculpt_ot_keyframe_shape_keys'
	bl_label = 'Keyframe Layers'
	bl_description = 'Set all shape layers value to current keyframe.'
	bl_options = {'REGISTER'}

	@ classmethod
	def poll(cls, context):
		return context.area.type == 'VIEW_3D'

	def execute(self, context):

		shape_list = []
		keys = 0
		ob = bpy.context.active_object
		current_frame = bpy.context.active_object.active_shape_key_index
		keys = ob.data.shape_keys.key_blocks.keys()

		for shape in ob.data.shape_keys.key_blocks:
			shape.keyframe_insert(
				"value", frame=bpy.data.scenes['Scene'].frame_current)
			bpy.data.scenes['Scene'].frame_current = bpy.data.scenes['Scene'].frame_current

		return {'FINISHED'}



class Sculpt_OT_Remove_Selected_Layer(bpy.types.Operator):
	"""Removes the selected shape layer"""
	bl_idname = 'mesh.sculpt_ot_remove_selected_layer'
	bl_label = 'Remove Selected layer'
	bl_description = 'Remove selected layer and clears keyframe from timeline.'
	bl_options = {'REGISTER'}

	@ classmethod
	def poll(cls, context):
		return context.area.type == 'VIEW_3D'

	def execute(self, context):

		ob = bpy.context.active_object
		key = ob.data.shape_keys
		kb = ob.active_shape_key

		all_keys = []

		current_frame = bpy.context.active_object.active_shape_key_index

		s = bpy.data.scenes['Scene']

		if ob.data.shape_keys:
			for shape in ob.data.shape_keys.key_blocks:
				try:
					shape.keyframe_delete("value", index=-1, frame=current_frame, group="")

				except RuntimeError:
					break
			bpy.ops.object.shape_key_remove(all=False)


		frames_id = []

		for action in bpy.data.actions:
			for fcurve in action.fcurves:
				for point in fcurve.keyframe_points:
					frames_id.append(point)

			for fr in range(current_frame, len(frames_id)):
				frames_id[fr].co.x -= 1

		return {'FINISHED'}


class Sculpt_OT_Clear_All_Keyframes(bpy.types.Operator):
	"""Clears all keyframes from timeline"""
	bl_idname = 'mesh.sculpt_ot_clear_all_keyframes'
	bl_label = 'Clear All Keyframes'
	bl_description = 'Clears all keyframes from timeline.'
	bl_options = {'REGISTER'}

	@ classmethod
	def poll(cls, context):
		return context.area.type == 'VIEW_3D'

	def execute(self, context):

		ob = bpy.context.active_object
		keys = ob.data.shape_keys.key_blocks.keys()

		s = bpy.data.scenes['Scene']

		for fr in range(0, len(keys)):
			s.frame_current = fr
			for shape in ob.data.shape_keys.key_blocks:
				if bpy.data.actions:
					try:
						shape.keyframe_delete(
							"value", index=-1, frame=fr, group="")
					except RuntimeError:
						break

		bpy.data.scenes['Scene'].frame_current = 0

		return {'FINISHED'}


class Sculpt_OT_Apply_Shape_Keys(bpy.types.Operator):
	"""Sculpt Apply Layers"""
	bl_idname = 'mesh.sculpt_ot_apply_shape_keys'
	bl_label = 'Apply Layers'
	bl_description = 'Merges all layers then removes all shape keys from the selected object.'
	bl_options = {'REGISTER'}

	@ classmethod
	def poll(cls, context):
		return context.area.type == 'VIEW_3D'

	def execute(self, context):

		shape_list = []
		keys = 0
		ob = bpy.context.active_object
		current_frame = bpy.context.active_object.active_shape_key_index
		keys = ob.data.shape_keys.key_blocks.keys()

		# Apply all layers to shape
		for shape in ob.data.shape_keys.key_blocks:
			shape.keyframe_insert(
				"value", frame=bpy.data.scenes['Scene'].frame_current)
			bpy.data.scenes['Scene'].frame_current = bpy.data.scenes['Scene'].frame_current

		bpy.ops.object.shape_key_add(from_mix=True)

		for shape in ob.data.shape_keys.key_blocks:
			if shape.name == ob.active_shape_key.name:
				shape.name = "Applied Shape"
				shape.value = 1.0
				shape.keyframe_insert("value", frame=ob.active_shape_key_index)
				bpy.data.scenes['Scene'].frame_current = ob.active_shape_key_index
			else:
				shape_list.append(shape)

		for i in (shape_list):
			# setting the active shapekey
			iIndex = ob.data.shape_keys.key_blocks.keys().index(i.name)
			ob.active_shape_key_index = iIndex

			# delete it
			bpy.ops.object.shape_key_remove()

		bpy.ops.object.shape_key_remove()
		bpy.data.scenes['Scene'].frame_current = 0

		# Edit Mode
		bpy.ops.object.editmode_toggle()

		# Object Mode
		bpy.ops.sculpt.sculptmode_toggle()

		return {'FINISHED'}

