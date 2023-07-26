import tkinter as tk
from tkinter import ttk, filedialog
import shutil
import os
import json
import openpyxl


class Hardware_model:

	def __init__(self):

		# 获取当前文件的目录路径
		self.current_directory = os.path.dirname(os.path.abspath(__file__))

		self.new_directory = self.current_directory.replace("\\py","")

		os.chdir(self.new_directory)	

		self.saved_modules = []	
		self.properties = {}
		self.module_data = ""
		self.module_dict = {}
		self.treeview_data = ""

		# 从文件中读取每一行的数据
		with open("Resource/Module/ModuleList.txt", "r") as file:
			self.module_list = file.readlines()		

	def update_module_data(self, properties, module_base_lines):
		module_name = properties["MODULE"]
		parent_name = properties["Parent"]
		node_address = properties["NodeAddress"]
		slot = properties["Slot"]
		parent_name = properties["Parent"]
		updated_lines = []
		for line in module_base_lines:
			if "MODULE " in line:
				updated_line = "    MODULE " + module_name + " ("
			elif "NodeAddress" in line:
				updated_line = '                         NodeAddress := "' + node_address + '",'
			elif "Slot " in line:
				updated_line = '                         Slot := ' + Slot + ','
			elif "Parent" in line:
				updated_line = '                         Parent := ' + parent_name + ','
			else:
				updated_line = line
			updated_lines.append(updated_line)
		updated_module_data = "\n".join(updated_lines)
		savefile = 'generated/modules/'+ module_name + '.txt'
		with open(savefile, 'w') as file:
			file.write(updated_module_data)

	def module_data_lines(self, module_path):
		with open(module_path, "r") as file:
			module_data = file.read()
		return module_data.split('\n')

	def parse_module_data(self, module_data_lines):
		properties = {}
		for line in module_data_lines:
			if "MODULE " in line:
				key = "MODULE"
				value = line.strip().split()[1]
				properties[key] = value
			elif ":=" in line:
				key, value = line.strip().split(":=",maxsplit=1)
				key = key.strip()
				value = value.strip()
				value = value.replace(",","")
				value = value.replace('"',"")
				properties[key] = value
		return properties

	def parse_tree_item(self, treeview):
		selected_item = treeview.selection()
		properties = {}
		properties["MODULE"] = treeview.item(selected_item, "text")
		values = treeview.item(selected_item, "values")
		properties["CatalogNumber"] = values[0]
		properties["NodeAddress"] = values[1]
		properties["Parent"] = values[2]
		return properties

	def save_treeview_data(self, treeview, parent="", node_data_list=None):
		if node_data_list is None:
			node_data_list = []

		nodes = treeview.get_children(parent)
		for node in nodes:
			text = treeview.item(node, "text")
			values = treeview.item(node, "values")
			children_data = []
			
			# 递归保存子节点
			self.save_treeview_data(treeview, parent=node, node_data_list=children_data)
			
			node_data = {"text": text, "values": values, "children": children_data}
			node_data_list.append(node_data)

		return node_data_list	  

	def update_entry_Parent(self,treeview,entry_fields):
		selected_item = treeview.selection()
		if selected_item:
			# 获取选中节点的父节点名称
			parent_item = treeview.parent(selected_item)
			parent_name = treeview.item(parent_item,"text")
			self_name = treeview.item(selected_item,"text")

			if parent_item:
				entry_fields["Parent"].delete(0, tk.END)
				entry_fields["Parent"].insert(tk.END, parent_name)
			else:
				entry_fields["Parent"].delete(0, tk.END)
				entry_fields["Parent"].insert(tk.END, self_name)        

	def iplist_open(self):
		file_path = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx")])
		if not file_path:
			return
		wb = openpyxl.load_workbook(file_path, data_only=True)
		# 获取指定子表
		sheet = wb['Local IP']
		return sheet

	def modulebase_path(self, module_type):
		md_filename = module_type + ".txt"
		return "Resource/Module/" + md_filename
	
	def moduleinst_path(self,module_name):	
		md_filename = module_name + ".txt"
		return "generated/modules/" + md_filename

	def treeview_to_modules(self, treeview, parent=""):
		nodes = treeview.get_children(parent)
		properties = {}
		for node in nodes:
			properties["MODULE"] = treeview.item(node, "text")
			values = treeview.item(node, "values")
			properties["CatalogNumber"] = values[0]
			properties["NodeAddress"] = values[1]
			properties["Parent"] = values[2]
			properties["Slot"] = 2
			base_path = self.modulebase_path(values[0])
			base_lines = self.module_data_lines(base_path)
			self.update_module_data(properties, base_lines)
			
			# 递归保存子节点
			self.treeview_to_modules(treeview, parent=node)
