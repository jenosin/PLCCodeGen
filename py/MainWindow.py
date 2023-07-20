import tkinter as tk
from tkinter import ttk
import hardware_main
#import tags_main
#import program_import_tab

def create_main_window():
    root = tk.Tk()
    root.geometry("1100x600")
    root.minsize(1100, 700)
    root.title("Lucid Code Gen")

    tab_control = ttk.Notebook(root)

    hardware_tab = ttk.Frame(tab_control)
    tags_tab = ttk.Frame(tab_control)
    program_import_tab = ttk.Frame(tab_control)

    tab_control.add(hardware_tab, text="硬件组态")
    tab_control.pack(expand=True, fill="both")
    tab_control.add(tags_tab, text="程序结构")
   # tab_control.add(program_import_tab, text="程序导入")

    hardware_main.create_hardware_configuration_tab(hardware_tab)
    #tags_main.create_labels_tab(tags_tab)
    #program_import_tab.create_program_import_tab(program_import_tab)

    tab_control.pack(expand=True, fill=tk.BOTH)

    root.mainloop()

if __name__ == "__main__":
    create_main_window()
