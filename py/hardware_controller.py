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
		self.model.update_module_data()						#写入生成模块数据
		self.view.dropdown_init()																			#初始化下拉选择按钮


	def dropdown_on_select(self,value):
		selected_item = value.strip()
		print("The selected item is:", selected_item)

		if selected_item != "":
			# 构建 Module 文件路径
			md_filename = selected_item + ".txt"
			md_filepath = "Resource/Module/" + md_filename
			self.model.properties = self.model.parse_module_data(md_filepath)
			self.view.show_data(md_filepath, self.model.properties)
			self.view.update_Parent()


	def save_config(self):
		self.model.treeview_data = self.model.save_treeview_data(self.view.treeview)
		with open("generated/treeview_data.json", "w") as file:
			json.dump(self.model.treeview_data, file)
		print("Treeview data saved.") 
			
	
	def load_config(self):
		with open("generated/treeview_data.json", "r") as file:
			self.model.treeview_data = json.load(file)
		self.view.clear_treeview()
		for node_data in self.model.treeview_data:
			self.view.create_node("", node_data)
		print("Treeview data loaded.")


	def on_select_tree(self, event):
		selected_item = self.view.treeview.selection()
		if selected_item != "" and self.model.properties != []:
			self.view.update_Parent()

	def modify_config(self):
		selected_item = self.view.treeview.selection()
		if selected_item:
			self_name = self.view.treeview.item(selected_item,"text")
		md_filename = self_name + ".txt"
		md_filepath = "generated/modules/" + md_filename
		self.model.properties = self.model.parse_module_data(md_filepath)
		self.view.show_data(md_filepath, self.model.properties)

	def delete_config(self):
		selected_item = self.view.treeview.selection()		
		if selected_item:
			self_name = self.view.get_name(selected_item)
			children = self.view.treeview.get_children(selected_item)
			for child in children:
				child_name = self.view.get_name(child)
				md_filename = child_name + ".txt"
				md_filepath = "generated/modules/" + md_filename
				os.remove(md_filepath)
				self.view.delete_tree_item(child)
			self.view.delete_tree_item(selected_item)
			md_filename = self_name + ".txt"
			md_filepath = "generated/modules/" + md_filename
			os.remove(md_filepath)

	def on_import(self):
		sheet = self.model.iplist_open()
		self.view.clear_treeview()
		self.view.ip_to_treeview(sheet)
