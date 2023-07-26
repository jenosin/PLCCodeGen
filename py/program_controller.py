import tkinter as tk
from tkinter import ttk
import shutil
from tkinter import filedialog
import os
import json
import openpyxl

class Program_controller:

	def __init__(self, root, model, view):
		self.root = root
		self.model = model
		self.view = view
		self.module_list = self.model.module_list

	def ZoneSafety(self, zonelist, AllStations, AllGates, AllRobots, AllDrives, AllCNVs, AllNextZones):
		program = []
		Rblist = []
		for zone in zonelist:
			Stationlist = AllStations[zone]
			Gatelist = AllGates[zone]
			for station, robots in AllRobots[zone].items():
				Rblist += robots
			for station, drives in AllDrives[zone].items():
				Drivelist += drives	
			for station, CVN in AllCNVs[zone].items():
				CNVlist += CVN							
			Next_Zone = AllNextZones[zone]
			program += self.model.safety_ZoneMain(zone)
			program += self.model.safety_ZoneCommon(zone, index)
			program += self.model.Gate(Gatelist, zone)
			program += self.model.ZoneSftyIn(Stationlist, Gatelist, Rblist, Drivelist, CNVlist, zone, Next_Zone)
			program += self.model.safety_ZoneSummary(zone)
			program += self.model.ZoneSftyOut(zone, index)
			program += self.model.endprogram()
			index += 1
		return program

	def StationSafety(self, AllStations, AllRobots, AllTools, AllSIOs, AllEstops, AllLCs, AllAccLCs, AllOPs, AllSPDs, AllICSDs, AllDrives, zonelist):
		program = []
		for zone in zonelist:
			for station in AllStations[zone].items():
				Rblist = AllRobots[zone][station]
				SIOlist = AllSIOs[zone][station]
				NumEstop = AllEstops[zone][station]
				NumLC = AllLCs[zone][station]
				NumAccLC = AllAccLCs[zone][station]
				NumOP = AllOPs[zone][station]
				NumSPD = AllSPDs[zone][station]
				hasICSD = AllICSDs[zone][station]
				Toollist = AllTools[zone][station]
				Drivelist = AllDrives[zone][station]	
				program += self.model.safety_StationHead(station)
				program += self.model.safety_StationTags(Rblist)
				program += self.model.safety_StationMain(Rblist)
				program += self.model.safety_Mods(station, SIOlist)
				program += self.model.Estop(NumEstop, station, zone)
				program += self.model.LC(NumLC, station, zone)
				program += self.model.AccLC(NumAccLC, station, zone)
				program += self.model.operator(NumOP, station, zone)
				program += self.model.SPD(NumSPD, station, zone)
				program += self.model.ICSD(hasICSD, station)
				program += self.model.safetyRobot(Rblist, station, zone)
				program += self.model.safetyTooling(Toollist, station, zone)
				program += self.model.safetyDrive(Drivelist, station, zone)
				program += self.model.safety_StationSummary(station, zone)
				program += self.model.endprogram()
				st += 1
			zn += 1
		return program

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
		self.view.show_info("Design Matrix imported successfully!")

	def hardware_gencode(self, treeview):
		self.model.treeview_to_modules(treeview)
		self.view.show_info("modules generation succeeded!")
