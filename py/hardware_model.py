import tkinter as tk
from tkinter import ttk, filedialog
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

	def update_module_data(self):
		module_name = self.properties["MODULE"]
		parent_name = self.properties["Parent"]
		updated_lines = []
		for line in self.module_data.split('\n'):
			if "MODULE " in line:
				updated_line = "    MODULE " + self.module_dict["MODULE"] + " ("
			elif "NodeAddress" in line:
				updated_line = '                         NodeAddress := "' + self.module_dict["NodeAddress"] + '",'
			elif "Slot " in line:
				updated_line = '                         Slot := ' + self.module_dict["Slot"] + ','
			elif "Parent" in line:
				updated_line = '                         Parent := ' + self.module_dict["Parent"] + ','
			else:
				updated_line = line
			updated_lines.append(updated_line)
		updated_module_data = "\n".join(updated_lines)
		savefile = 'generated/modules/'+ module_name + '.txt'
		with open(savefile, 'w') as file:
			file.write(updated_module_data)

	def parse_module_data(self, module_path):
		with open(module_path, "r") as file:
			self.module_data = file.read()
		lines = self.module_data.split('\n')
		for line in lines:
			if "MODULE " in line:
				key = "MODULE"
				value = line.strip().split()[1]
				#value = "更改模块名字"
				self.module_dict[key] = value
			elif ":=" in line:
				key, value = line.strip().split(":=",maxsplit=1)
				key = key.strip()
				value = value.strip()
				value = value.replace(",","")
				value = value.replace('"',"")
				self.module_dict[key] = value
		return self.module_dict

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


	def update_Parent(self,treeview,entry_fields):
		# 获取选中的节点
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
