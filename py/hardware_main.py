import tkinter as tk
from tkinter import ttk
import os
import json
import hardware_view
import hardware_model
import hardware_controller

def create_hardware_configuration_tab(tab):
	model = hardware_model.Hardware_model()
	controller = hardware_controller.Hardware_controller(tab, model, None)
	view = hardware_view.Hardware_view(tab, controller)
	controller.view = view
