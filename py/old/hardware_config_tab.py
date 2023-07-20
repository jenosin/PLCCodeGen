import tkinter as tk
from tkinter import ttk
import os
import json

def create_hardware_configuration_tab(tab):
    global frame
    frame = ttk.Frame(tab, borderwidth=2, relief="groove")
    frame.grid(row=0, column=0,padx=10, pady=10, sticky="nsew")
    empty_h = tk.Frame(frame, width=150)
    empty_h.grid(row=0, column=1)
    empty_v = tk.Frame(frame, height=400,width = 50)
    empty_v.grid(row=0, column=2, rowspan= 15)

    # 设置方框 Frame 的行数为 15
    for i in range(15):
        frame.grid_rowconfigure(i, weight=1)

    for i in range(2):
        frame.grid_columnconfigure(i, weight=1)

    global dropdown
    global selected_item
    selected_item = ""
    dropdown = tk.StringVar()
    dropdown.set("选择模块")
    
    # 获取当前文件的目录路径
    current_directory = os.path.dirname(os.path.abspath(__file__))

    # 构建新的工作目录路径
    global new_directory
    new_directory = current_directory.replace("\\py","")

    # 更改当前工作目录
    os.chdir(new_directory)

    # 从文件中读取每一行的数据
    with open("Resource/Module/ModuleList.txt", "r") as file:
        module_list = file.readlines()

    global labels
    global entries
    labels = []
    entries = []

    def on_select(value):
        selected_item = value.strip()
        print("The selected item is:", selected_item)

        if selected_item != "":
            # 构建 Module 文件路径
            md_filename = selected_item + ".txt"
            md_filepath = "Resource/Module/" + md_filename
            show_data(md_filepath)
            update_Parent()


    # 创建下拉菜单控件
    dropdown_menu = tk.OptionMenu(frame, dropdown, *module_list, command=on_select)
    dropdown_menu.config(width=20,height=1,anchor='center')
    dropdown_menu.grid(row=0, column=0,padx=10, pady=10, sticky="w")
        
    save_button = tk.Button(frame, text="Save Changes", command=save_changes)
    save_button.grid(row=14, column=1, padx=10, pady=10, sticky="se")

    tree_container = ttk.Frame(tab,borderwidth=2, relief="groove")
    tree_container.grid(row=0, column=1, columnspan=1, padx=10, pady=10, sticky="nsew")
    for i in range(15):
        tree_container.grid_rowconfigure(i, weight=1)

    # 创建滚动文本框
    scrollbar = ttk.Scrollbar(tree_container)
    scrollbar.grid(row=0,column=0,rowspan=12,sticky="w")

    # 创建 Treeview 控件
    global treeview
    treeview = ttk.Treeview(tree_container, yscrollcommand=scrollbar.set)
    treeview.grid(row=0,column=1,rowspan=12,sticky="nsew")
    treeview["columns"] = ("Module","IP")

    # 设置列标题
    treeview.heading("#0", text="Name")
    treeview.heading("Module", text="Module")
    treeview.heading("IP", text="IP")
    treeview.bind("<<TreeviewSelect>>", on_select_tree)

    # 配置 Treeview 的滚动条
    scrollbar.config(command=treeview.yview)

    global treeview_data
    treeview_data = []
    save_tree_button = tk.Button(tree_container, text="Save Configuration", command=save_config)
    save_tree_button.grid(row=14, column=1, padx=10, pady=10,sticky="se")

    load_tree_button = tk.Button(tree_container, text="Load Configuration", command=load_config)
    load_tree_button.grid(row=15, column=1, padx=10, pady=10,sticky="se")   

    modify_item_button = tk.Button(tree_container, text="Modify Selection", command=modify_config)
    modify_item_button.grid(row=14, column=1, padx=10, pady=10,sticky="sw")

    delete_item_button = tk.Button(tree_container, text="Delete Selection", command=delete_config)
    delete_item_button.grid(row=15, column=1, padx=10, pady=10,sticky="sw")

    global saved_modules
    saved_modules = []

def save_changes():
    for key, value in entry_fields.items():
        properties[key] = value.get()
    print("Parent: " + properties["Parent"])

    instance_data = update_module_data(properties)

    module_name = properties["MODULE"]
    parent_name = properties["Parent"]
    module_type = properties["CatalogNumber"]

    if module_type in ["1756-L83ES", "1756-L8SP"]:
        ip_add = "No Ip address"        
    else: ip_add = properties["NodeAddress"]

        # 清空下拉菜单的选择
    dropdown.set("选择模块")

    if module_name not in saved_modules:
        if parent_name == "Local":
            parent_node = treeview.insert("", "end", text=module_name, values=(module_type,ip_add))
            saved_modules.append(module_name)
        else:
            # 查找父节点的引用
            parent_node = None
            for node in treeview.get_children():
                if parent_name in treeview.item(node, "text"):
                    parent_node = node
                    break

            # 如果父节点存在，则添加为子节点
            if parent_node:
                treeview.insert(parent_node, "end", text=module_name, values=(module_type,ip_add))
                treeview.item(parent_node, open=True)
                saved_modules.append(module_name)
    

    savefile = 'generated/modules/'+ module_name + '.txt'
    with open(savefile, 'w') as file:
        file.write(instance_data)
    properties.clear()


def save_config():

    def save_treeview_data(treeview, parent="", node_data_list=None):
        if node_data_list is None:
            node_data_list = []

        nodes = treeview.get_children(parent)
        for node in nodes:
            text = treeview.item(node, "text")
            values = treeview.item(node, "values")
            children_data = []
            
            # 递归保存子节点
            save_treeview_data(treeview, parent=node, node_data_list=children_data)
            
            node_data = {"text": text, "values": values, "children": children_data}
            node_data_list.append(node_data)

        return node_data_list

    treeview_data = save_treeview_data(treeview)
    
    with open("generated/treeview_data.json", "w") as file:
        json.dump(treeview_data, file)
    print("Treeview data saved.")

def load_config():
    with open("generated/treeview_data.json", "r") as file:
        self.model.treeview_data = json.load(file)
        self.view.clear_treeview()

    def create_node(parent, node_data):
        text = node_data["text"]
        values = node_data["values"]
        children = node_data["children"]
        node = treeview.insert(parent, "end", text=text, values=values)
        # 递归创建子节点
        for child_data in children:
            create_node(node, child_data)
    
    for node_data in treeview_data:
        create_node("", node_data)

    print("Treeview data loaded.")


def parse_module_data(module_data):
    module_dict = {}
    lines = module_data.split('\n')
    for line in lines:
        if "MODULE " in line:
            key = "MODULE"
            value = line.strip().split()[1]
            #value = "更改模块名字"
            module_dict[key] = value
        elif ":=" in line:
            key, value = line.strip().split(":=",maxsplit=1)
            key = key.strip()
            value = value.strip()
            value = value.replace(",","")
            value = value.replace('"',"")
            module_dict[key] = value
    return module_dict


def update_module_data(module_dict):
    updated_lines = []
    for line in module_data.split('\n'):
        if "MODULE " in line:
            updated_line = "    MODULE " + module_dict["MODULE"] + " ("
        elif "NodeAddress" in line:
            updated_line = '                         NodeAddress := "' + module_dict["NodeAddress"] + '",'
        elif "Slot " in line:
            updated_line = '                         Slot := ' + module_dict["Slot"] + ','
        elif "Parent" in line:
            updated_line = '                         Parent := ' + module_dict["Parent"] + ','
        else:
            updated_line = line
        updated_lines.append(updated_line)
    updated_module_data = "\n".join(updated_lines)
    return updated_module_data


def on_select_tree(event):
    if selected_item != "":
        update_Parent()

def update_Parent():
        # 获取选中的节点
    selected_item = treeview.selection()
    if selected_item:
        # 获取选中节点的父节点名称
        parent_item = treeview.parent(selected_item)
        parent_name = treeview.item(parent_item,"text")
        self_name = treeview.item(selected_item,"text")
        print(parent_name)
        if parent_item:
            entry_fields["Parent"].delete(0, tk.END)
            entry_fields["Parent"].insert(tk.END, parent_name)
        else:
            entry_fields["Parent"].delete(0, tk.END)
            entry_fields["Parent"].insert(tk.END, self_name)


def modify_config():
    selected_item = treeview.selection()
    if selected_item:
        self_name = treeview.item(selected_item,"text")

    md_filename = self_name + ".txt"
    md_filepath = "generated/modules/" + md_filename

    show_data(md_filepath)

def delete_config():
    selected_item = treeview.selection()
    if selected_item:
        self_name = treeview.item(selected_item,"text")
        treeview.delete(selected_item)

        md_filename = self_name + ".txt"
        md_filepath = "generated/modules/" + md_filename
        os.remove(md_filepath)


def show_data(module_path):
    for label in labels:
        label.destroy()
    for entry in entries:
        entry.destroy()
    labels.clear()
    entries.clear()
    with open(module_path, "r") as file:
        global module_data
        module_data = file.read()

    global properties        
    properties = parse_module_data(module_data)
    global entry_fields
    entry_fields = {}


    row = 1
    for key, value  in properties.items():
        if key in ["CatalogNumber", "Major", "Minor"]:
            # 显示的标签
            label = ttk.Label(frame, text=f"{key}:")
            label.grid(row=row, column=0, padx=10, pady=10, sticky="w")
            # 显示的值
            value_label = ttk.Label(frame, text=value)
            value_label.grid(row=row, column=1, padx=10, pady=10, sticky="w")
            labels.append(value_label)
        elif key in ["MODULE","Slot", "NodeAddress","Parent"]:
            # 可编辑的标签
            label = ttk.Label(frame, text=f"{key}:")
            label.grid(row=row, column=0, padx=10, pady=10, sticky="w")
            labels.append(label)
            # 可编辑的输入框
            entry = ttk.Entry(frame)
            entry.insert(tk.END, value)
            entry.grid(row=row, column=1, padx=10, pady=10, sticky="w")
            entry_fields[key] = entry
            entries.append(entry)
        row += 1
