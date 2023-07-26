import tkinter as tk
from tkinter import ttk
import os
import json
import openpyxl



class Hardware_controller:

	def __init__(self, root, model, view):
		self.root = root
		self.model = model
		self.view = view
		self.module_list = self.model.module_list

	def save_changes(self):
		for key, value in self.view.entry_fields.items():
				self.model.properties[key] = value.get()
		self.view.treeview_update(self.model.properties,self.model.saved_modules)		#更新树结构
		self.view.dropdown_init()
		self.view.show_info(self.model.properties["MODULE"] + " is added to list.")																		#初始化下拉选择按钮


	def dropdown_on_select(self,value):
		selected_item = value.strip()
		if selected_item != "":
			md_filepath = self.model.modulebase_path(selected_item)
			lines = self.model.module_data_lines(md_filepath)
			self.model.properties = self.model.parse_module_data(lines)
			self.view.show_data(self.model.properties)
			self.view.update_Parent()
			self.view.show_info(selected_item + " selected, please modify its data before adding to list.")


	def save_config(self):
		self.model.treeview_data = self.model.save_treeview_data(self.view.treeview)
		with open("generated/treeview_data.json", "w") as file:
			json.dump(self.model.treeview_data, file)
		self.view.show_info("Treeview data saved.")
			
	
	def load_config(self):
		with open("generated/treeview_data.json", "r") as file:
			self.model.treeview_data = json.load(file)
		self.view.clear_treeview()
		for node_data in self.model.treeview_data:
			self.view.create_node("", node_data)
		self.view.show_info("Treeview data loaded.")


	def on_select_tree(self, event):
		selected_item = self.view.get_selection()
		if selected_item != "" and "Parent" in self.view.entry_fields:
			self.view.update_Parent()
			self.view.show_info("Module parent is changed.")

	def modify_config(self):
		selected_item = self.view.get_selection()
		self_name = self.view.get_name(selected_item)
		md_filepath = self.model.moduleinst_path(self_name)
		if os.path.exists(md_filepath):
			lines = self.model.module_data_lines(md_filepath)
			properties = self.model.parse_module_data(lines)
		else: 
			properties = self.model.parse_tree_item(self.view.treeview)
		self.view.show_data(properties)
		self.view.show_info("module data loaded, you can start modifying.")

	def delete_config(self):
		selected_items = self.view.get_selection()		
		if selected_items:
			for item in selected_items:
				self_name = self.view.get_name(item)
				children = self.view.treeview.get_children(item)
				self.view.delete_tree_item(children)
				for child in children:
					child_name = self.view.get_name(child)
					md_filepath = self.model.moduleinst_path(child_name)
					if os.path.exists(md_filepath):
						os.remove(md_filepath)
				md_filepath = self.model.moduleinst_path(self_name)
				if os.path.exists(md_filepath):
					os.remove(md_filepath)
			self.view.delete_tree_item(selected_items)
		self.view.show_info(self_name + " and its childen deleted!")
								

	def delete_config_pb(self,event):
		self.delete_config()

	def on_import(self):
		sheet = self.model.iplist_open()
		self.view.clear_treeview()
		self.view.ip_to_treeview(sheet)
		self.view.show_info("IP list imported successfully!")

	def hardware_gencode(self, treeview):
		self.model.treeview_to_modules(treeview)
		self.view.show_info("modules generation succeeded!")
