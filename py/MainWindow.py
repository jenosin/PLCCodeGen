import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import hardware_view
import hardware_model
import hardware_controller
import tags_view
import tags_model
import tags_controller
#import program_import_tab


def create_hardware_tab(tab):
	global controller
	model = hardware_model.Hardware_model()
	controller = hardware_controller.Hardware_controller(tab, model, None)
	view = hardware_view.Hardware_view(tab, controller)
	controller.view = view

def create_tags_tab(tab):
	model = tags_model.Tags_model()
	controller = tags_controller.Tags_controller(tab, model, None)
	view = tags_view.Tags_view(tab, controller)
	controller.view = view

def on_close():
	answer = messagebox.askyesnocancel("Confirmation", "Do you want to save the changes?")
	if answer is None:
		return  # Cancel
	elif answer:
		controller.save_config()
	root.destroy()

def create_main_window():
	global root
	root = tk.Tk()
	root.geometry("1250x700")
	root.minsize(1250, 700)
	root.title("Lucid Code Gen")

	tab_control = ttk.Notebook(root)

	hardware_tab = ttk.Frame(tab_control)
	tags_tab = ttk.Frame(tab_control)
	program_import_tab = ttk.Frame(tab_control)

	tab_control.add(hardware_tab, text="硬件组态")
	tab_control.pack(expand=True, fill="both")
	tab_control.add(tags_tab, text="程序结构")
   # tab_control.add(program_import_tab, text="程序导入")

	create_hardware_tab(hardware_tab)
	create_tags_tab(tags_tab)
	#program_import_tab.create_program_import_tab(program_import_tab)

	tab_control.pack(expand=True, fill=tk.BOTH)
	root.protocol("WM_DELETE_WINDOW", on_close)

	root.mainloop()

if __name__ == "__main__":
	create_main_window()
