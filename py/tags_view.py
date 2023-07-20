import tkinter as tk
from tkinter import ttk
import os
import json

class Tags_view:

	def __init__(self, tab, controller):
		self.controller = controller

		#创建tab中的分区
		self.module_grid = ttk.Frame(tab, borderwidth=2, relief="groove")
		self.module_grid.grid(row=0, column=0,padx=10, pady=10, sticky="nsew")
		self.tree_grid = ttk.Frame(tab,borderwidth=2, relief="groove")
		self.tree_grid.grid(row=0, column=1, columnspan=2,padx=10, pady=10, sticky="nsew")
		self.info_grid = ttk.Frame(tab,borderwidth=2, relief="solid")
		self.info_grid.grid(row=1,column=0,columnspan=2, padx=10, pady=10,sticky="nsew")
		self.clear_button = tk.Button(tab, text="Clear Errors", command=self.clear_info)
		self.clear_button.grid(row=1,column=2,padx=10, pady=10,sticky="sw")

		#创建模块区域框架和内容
		self.dropdown = tk.StringVar()
		self.dropdown.set("选择类型")
		self.dropdown_menu = tk.OptionMenu(self.module_grid, self.dropdown, *self.controller.module_list, command=self.controller.dropdown_on_select)
		self.dropdown_menu.config(width=20,height=1)
		self.dropdown_menu.pack(side="top",anchor="nw",padx=10,pady=5)
		self.module_frame = ttk.Frame(self.module_grid, width=350, height=400, borderwidth=0, relief="groove")
		self.module_frame.pack(side="top", fill="both", expand=True,padx=10,pady=5)
		self.module_frame.grid_columnconfigure(0, weight=1)
		self.module_frame.grid_columnconfigure(1, weight=1)	
		self.save_button = tk.Button(self.module_grid, text="Save Changes", command=self.controller.save_changes)
		self.save_button.pack(side="bottom",anchor="se",padx=10,pady=5)

		# 创建树状区域框架和内容
		self.tree_frame = ttk.Frame(self.tree_grid, width=350, height=400,borderwidth=1, relief="groove")
		self.tree_frame.pack(side="left", fill="both", expand=True)
		self.scrollbar = ttk.Scrollbar(self.tree_frame)
		self.scrollbar.grid(row=0,column=0,sticky="w")
		self.treeview = ttk.Treeview(self.tree_frame, yscrollcommand=self.scrollbar.set)
		self.treeview.grid(row=0,column=1,sticky="nsew")
		self.treeview["columns"] = ("Module","IP")
		self.treeview.heading("#0", text="Name")
		self.treeview.heading("Module", text="Module")
		self.treeview.heading("IP", text="IP")
		self.treeview.bind("<<TreeviewSelect>>", self.controller.on_select_tree)
		self.scrollbar.config(command=self.treeview.yview)
		self.save_tree_button = tk.Button(self.tree_frame, text="Save Configuration", command=self.controller.save_config)
		self.save_tree_button.grid(row=1, column=1, padx=10, pady=5,sticky="se")
		self.load_tree_button = tk.Button(self.tree_frame, text="Load Configuration", command=self.controller.load_config)
		self.load_tree_button.grid(row=2, column=1, padx=10, pady=5,sticky="se")   
		self.modify_item_button = tk.Button(self.tree_frame, text="Modify Selection", command=self.controller.modify_config)
		self.modify_item_button.grid(row=1, column=1, padx=10, pady=5,sticky="sw")
		self.delete_item_button = tk.Button(self.tree_frame, text="Delete Selection", command=self.controller.delete_config)
		self.delete_item_button.grid(row=2, column=1, padx=10, pady=5,sticky="sw")


		# 创建信息显示区域框架和内容
		self.info_frame = ttk.Frame(self.info_grid, width=900, height=100,borderwidth=1, relief="groove")
		self.info_frame.pack(side="left", fill="both", expand=True)

		self.labels = []
		self.entries = []
		self.entry_fields = {}
		self.info_messages = []


	def dropdown_init(self):
		self.dropdown.set("选择模块")

	def treeview_update(self,properties,saved_modules):
		module_name = properties["MODULE"]
		parent_name = properties["Parent"]
		module_type = properties["CatalogNumber"]

		if module_type in ["1756-L83ES", "1756-L8SP"]:
			ip_add = "No Ip address"        
		else: ip_add = properties["NodeAddress"]

		delete_item = self.Module_Exist(properties)

		if delete_item != None:
			item_name = self.delete_tree_item(delete_item)
			saved_modules.remove(item_name)

		if module_name not in saved_modules:
			if parent_name == "Local":
				parent_node = self.treeview.insert("", "end", text=module_name, values=(module_type,ip_add))
				saved_modules.append(module_name)
			else:
				# 查找父节点的引用
				parent_node = None
				for node in self.treeview.get_children():
					if parent_name in self.treeview.item(node, "text"):
						parent_node = node
						break

				# 如果父节点存在，则添加为子节点
				if parent_node:
					self.treeview.insert(parent_node, "end", text=module_name, values=(module_type,ip_add))
					self.treeview.item(parent_node, open=True)
					saved_modules.append(module_name)	

	def update_Parent(self):
			# 获取选中的节点
		selected_item = self.treeview.selection()
		if selected_item:
			# 获取选中节点的父节点名称
			parent_item = self.treeview.parent(selected_item)
			parent_name = self.treeview.item(parent_item,"text")
			self_name = self.treeview.item(selected_item,"text")
			if parent_item:
				self.entry_fields["Parent"].delete(0, tk.END)
				self.entry_fields["Parent"].insert(tk.END, parent_name)
			else:
				self.entry_fields["Parent"].delete(0, tk.END)
				self.entry_fields["Parent"].insert(tk.END, self_name)	


	def show_data(self, module_path, properties):

		for label in self.labels:
			label.destroy()
		for entry in self.entries:
			entry.destroy()
		self.labels.clear()
		self.entries.clear()

		row = 1
		for key, value  in properties.items():
			if key in ["CatalogNumber", "Major", "Minor"]:
				# 显示的标签
				label = ttk.Label(self.module_frame, text=f"{key}:")
				label.grid(row=row, column=0, padx=10, pady=10, sticky="w")
				# 显示的值
				value_label = ttk.Label(self.module_frame, text=value)
				value_label.grid(row=row, column=1, padx=10, pady=10, sticky="w")
				self.labels.append(value_label)
			elif key in ["MODULE","Slot", "NodeAddress","Parent"]:
				# 可编辑的标签
				label = ttk.Label(self.module_frame, text=f"{key}:")
				label.grid(row=row, column=0, padx=10, pady=10, sticky="w")
				self.labels.append(label)
				# 可编辑的输入框
				entry = ttk.Entry(self.module_frame)
				entry.insert(tk.END, value)
				entry.grid(row=row, column=1, padx=10, pady=10, sticky="w")
				self.entry_fields[key] = entry
				self.entries.append(entry)
			row += 1

	def show_info(self, message):
		self.info_messages.insert(0, message)
		self.update_info()

	def update_info(self):
		for widget in self.info_banner.winfo_children():
			widget.destroy()
		
		for message in self.info_messages:
			label = tk.Label(self.info_banner, text=message, wraplength=400)
			label.pack(anchor="w", padx=10, pady=5)

	def clear_info(self):
		self.info_messages = []
		self.update_info()

	def create_node(self,parent, node_data):
		text = node_data["text"]
		values = node_data["values"]
		children = node_data["children"]
		node = self.treeview.insert(parent, "end", text=text, values=values)
		# 递归创建子节点
		for child_data in children:
			self.create_node(node, child_data)
			self.treeview.item(node, open=True)


	def delete_tree_item(self, target_item):		
		self.treeview.delete(target_item)
		

	def get_name(self, target_item):
		self_name = self.treeview.item(target_item,"text")
		return self_name

	def Module_Exist(self, properties, parent=""):
		module_name = properties["MODULE"]
		nodes = self.treeview.get_children(parent)
		item = None
		for node in nodes:
			text = self.treeview.item(node, "text")
			if text == module_name:
				item = node
				break
			item = self.Module_Exist(properties,parent=node)

		return item

	def clear_treeview(self):
		self.treeview.delete(*self.treeview.get_children())