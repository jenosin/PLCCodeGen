import tkinter as tk
from tkinter import ttk
import os
import json
import tags_view
import tags_model
import tags_controller

def create_tags_tab(tab):
	model = tags_model.Tags_model()
	controller = tags_controller.Tags_controller(tab, model, None)
	view = tags_view.Tags_view(tab, controller)
	controller.view = view
