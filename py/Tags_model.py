import tkinter as tk
from tkinter import ttk
import os
import json


class Tags_model:

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
			save_treeview_data(treeview, parent=node, node_data_list=children_data)
			
			node_data = {"text": text, "values": values, "children": children_data}
			node_data_list.append(node_data)

		return node_data_list	  

	def find_index(self, string, findstring, index):
		start_index = -1
		for i in range(index):
			start_index = string.find(findstring, start_index + 1)
			if start_index == -1:
				return -1
		return start_index

	def join_XIC(self, mode, line, Replace_string, itemlist, fullstring = "", index = 1):
		if mode == 1:
			conn = ""
		if mode == 2:
			conn = ","
		if fullstring == "":
			start_index = find_index(line, "XIC", index)
			end_index = find_index(line, ")", index) + 1
			str_XIC = line[start_index:end_index]
		else: 
			str_XIC = fullstring
		if Replace_string in line and str_XIC in line:
			new_XIC = conn.join(str_XIC.replace(Replace_string, item) for item in itemlist)
			new_line = line.replace(str_XIC, new_XIC)
		else: new_line = line
		return new_line

	def join_OTE_Branch(self, line, Replace_string, itemlist):
		start_index = line.find("[") + 1
		end_index = line.find("]") 
		str_OTE = line[start_index:end_index]
		new_OTE = ",".join(str_OTE.replace(Replace_string, item) for item in itemlist)
		return line.replace(str_OTE, new_OTE)

	def safety_StationHead(self, Station_name):
		with open("Resource/Program/SafetyTask/StationHead.txt", 'r') as file:
			lines = file.readlines()
		new_lines = [line.replace("Station_Name", Station_name) for line in lines]
		return new_lines		

	def safety_StationTags(self,Rblist):
		with open("Resource/Program/SafetyTask/StationTag.txt", 'r') as file:
			lines = file.readlines()
		new_lines = []
		for line in lines:
			if lines.index(line)==1:	
				for i in Range(len(Rblist)):
					new_line = line.replace("R01", str(i + 1))
					new_lines.append(new_line)
			else:
				new_lines.append(line)
		return new_lines		

	def safety_StationMain(self, Rblist,Toollist):
		with open("Resource/Program/SafetyTask/StationMain.txt", 'r') as file:
			lines = file.readlines()
		new_lines = []
		for line in lines:
			if lines.index(line)==7:	
				for robot in Rblist:
					new_line = line.replace("RB01", robot)
					new_lines.append(new_line)
			if lines.index(line) == 8:
				for tooling in Toollist:
					new_line = line.replace("TL01", tooling)
					new_lines.append(new_line)
			else:
				new_lines.append(line)
		return new_lines

	def Safety_Mods(self,Station_Name, SIOlist):
		with open("Resource/Program/SafetyTask/StationMod.txt", 'r') as file:
			lines = file.readlines()
		new_lines = lines
		copied_lines = []
		for SIO in SIOlist:
			for line in lines[5:14]:
				line = line.replace("Module 1", "Module " + str(SIOlist.index(SIO) + 1))
				copied_lines.append(line.replace("SIO_Name", SIO))
		del new_lines[5:14]
		new_lines[5:5] = copied_lines
		lens = len(new_lines)
		count = len(SIOlist)
		for i in range(lens-4,lens-1):
			Mods = ["Mod" + str(i) for i in range(1, count+1)]
			new_XIC = join_XIC(new_lines[i], "Mod1", Mods)
			new_lines[i] = new_XIC
		new_lines = [line.replace("Station_Name", Station_Name) for line in new_lines]
		return new_lines

	def Estop(self, NumofEstops, Station_Name, Zone_Name):
		if NumofEstops > 0:
			with open("Resource/Program/SafetyTask/Estop.txt", 'r') as file:
				lines = file.readlines()
			lines = [line.replace("Station_Name", Station_Name) for line in lines]
			lines = [line.replace("Zone_Name", Zone_Name) for line in lines]
			copied_lines = []
			for i in range(2, NumofEstops+1):
				for line in lines[5:15]:
					copied_lines.append(line.replace("E1", "E" + str(i)))
			insert_index = len(lines) - 1
			lines[insert_index:insert_index] = copied_lines
		else: lines = []
		return lines

	def LC(NumofLC, Station_Name, Zone_Name):
		if NumofLC > 0:
			with open("Resource/Program/SafetyTask/LC.txt", 'r') as file:
				lines = file.readlines()
			lines = [line.replace("Station_Name", Station_Name) for line in lines]
			lines = [line.replace("Zone_Name", Zone_Name) for line in lines]
			copied_lines = []
			for i in range(NumofLC):
				for line in lines[13:30]:
					copied_lines.append(line.replace("LC1", "LC" + str(i + 1)))
			del lines[13:30]
			insert_index = len(lines) - 100
			lines[insert_index:insert_index] = copied_lines
		else: lines = []
		return lines

	def AccLC(self, NumofAccLC, Station_Name, Zone_Name):
		if NumofAccLC > 0:
			with open("Resource/Program/SafetyTask/AccLC.txt", 'r') as file:
				lines = file.readlines()
			lines = [line.replace("Station_Name", Station_Name) for line in lines]
			lines = [line.replace("Zone_Name", Zone_Name) for line in lines]
		else: lines = []
		return lines

	def operator(self, NumofOP, Station_Name, Zone_Name):
		if NumofOP > 0:
			with open("Resource/Program/SafetyTask/Operator.txt", 'r') as file:
				lines = file.readlines()
			new_lines = [line.replace("Station_Name", Station_Name) for line in lines]
			new_lines = [line.replace("Zone_Name", Zone_Name) for line in new_lines]
		else: new_lines = []
		return new_lines

	def SPD(self, NumofSPD, Station_Name, Zone_Name):
		if NumofSPD > 0:
			with open("Resource/Program/SafetyTask/SPD.txt", 'r') as file:
				lines = file.readlines()
			lines = [line.replace("Station_Name", Station_Name) for line in lines]
			lines = [line.replace("Zone_Name", Zone_Name) for line in lines]
			copied_lines = []
			for i in range(NumofSPD):
				for line in lines[5:10]:
					copied_lines.append(line.replace("SPD1", "SPD" + str(i + 1)))
			del lines[5:10]
			insert_index = len(lines) - 1
			lines[insert_index:insert_index] = copied_lines
		else: lines = []
		return lines

	def ICSD(self, hasICSD, Station_Name):
		if hasICSD:
			with open("Resource/Program/SafetyTask/StationICSD.txt", 'r') as file:
				lines = file.readlines()
			new_lines = [line.replace("Station_Name", Station_Name) for line in lines]
		else:
			new_lines = []
		return new_lines

	def safetyRobot(Self, Rblist, Station_Name, Zone_Name):
		if len(Rblist) > 0:
			with open("Resource/Program/SafetyTask/Robot.txt", 'r') as file:
				lines = file.readlines()
			lines = [line.replace("Station_Name", Station_Name) for line in lines]
			lines = [line.replace("Zone_Name", Zone_Name) for line in lines]
			new_lines = []
			i = 1
			for robot in Rblist:
				for line in lines:
					if "RB01" in line:						
						new_lines.append(line.replace("RB01", "RB0" + str(i)))
					else:
						new_lines.append(line.replace("Robot_Name", robot))
				i+=1
			return new_lines

	def safetyTooling(self, Toollist, Station_Name, Zone_Name):
		if len(Toollist) > 0:
			with open("Resource/Program/SafetyTask/Tooling.txt", 'r') as file:
				lines = file.readlines()
			lines = [line.replace("Station_Name", Station_Name) for line in lines]
			lines = [line.replace("Zone_Name", Zone_Name) for line in lines]
			new_lines = []
			i = 1
			for tooling in Toollist:
				tool_name = tooling.replace(Station_Name,"")
				for line in lines:
					if "TL1" in line:						
						new_lines.append(line.replace("TL1", tool_name))
					else:
						new_lines.append(line.replace("FX1", "FX" + str(i)))
				i+=1
			return new_lines

	def safety_StationSummary(self, Station_Name, Zone_Name):
		with open("Resource/Program/SafetyTask/StationSummary.txt", 'r') as file:
			lines = file.readlines()
		lines = [line.replace("Station_Name", Station_Name) for line in lines]
		lines = [line.replace("Zone_Name", Zone_Name) for line in lines]
		return lines

	def safetyDrive(self, Drivelist, Station_Name, Zone_Name):
		if len(Drivelist) > 0:
			with open("Resource/Program/SafetyTask/Drive.txt", 'r') as file:
				lines = file.readlines()
			lines = [line.replace("Station_Name", Station_Name) for line in lines]
			lines = [line.replace("Zone_Name", Zone_Name) for line in lines]
			new_lines = []
			i = 1
			for drive in Drivelist:
				drive_name = drive.replace(Station_Name,"")
				for line in lines:
					if "TT1" in line:						
						new_lines.append(line.replace("TT1", drive_name))
					else:
						new_lines.append(line.replace("Servo_Name", drive_name + "SRV1"))
				i+=1
			return new_lines

	def safety_ZoneMain(self, Zone_Name):
		with open("Resource/Program/SafetyTask/ZoneMain.txt", 'r') as file:
			lines = file.readlines()
		lines = [line.replace("Zone_Name", Zone_Name) for line in lines]
		return lines

	def safety_ZoneCommon(self,Zone_Name, Zone_index):
		with open("Resource/Program/SafetyTask/ZoneCommon.txt", 'r') as file:
			lines = file.readlines()
		lines = [line.replace("Zone_Name", Zone_Name) for line in lines]
		if Zone_index > 1:
			del lines[4:6]
		return lines

	def Gate(self, Gatelist, Zone_Name):
		if len(Gatelist) > 0:
			with open("Resource/Program/SafetyTask/Gate.txt", 'r') as file:
				lines = file.readlines()
			lines = [line.replace("Zone_Name", Zone_Name) for line in lines]
			new_lines = []
			copied_lines = []
			for line in lines:	
				new_str = ""			
				if "[" in line:
					str_OTE = join_OTE(line, "Gate_Name", Gatelist)
					new_lines.append(str_OTE)								
				else: new_lines.append(line)
			for gate in Gatelist:
				for line in lines[25:33]:
					copied_lines.append(line.replace("Gate_Name", gate))
			del lines[25:33]
			insert_index = len(lines) - 1
			new_lines[insert_index:insert_index] = copied_lines
		else: new_lines = []
		return new_lines

	def ZoneSftyIn(self, Stationlist, Gatelist, Rblist, Drivelist, CNVlist, Zone_Name, Next_Zone):
		with open("Resource/Program/SafetyTask/ZoneSftyIn.txt", 'r') as file:
			lines = file.readlines()
		lines = [line.replace("Zone_Name", Zone_Name) for line in lines]
		lines = [line.replace("Next_Zone", Next_Zone) for line in lines]
		new_lines = []
		n = len(Rblist)
		mid = n // 2
		Rblist1 = Rblist[:mid + n % 2]
		Rblist2 = Rblist[mid + n % 2:]
		for line in lines:
			if "[" in line:
				line = join_XIC(2, line, "Gate_Name", Gatelist)
				line = join_XIC(2, line, "Robot_Name", Rblist)
				line = join_XIC(1, line, "Station_Name", Stationlist)
			elif "EStops1" in line or "Enbld1" in line:
				line = join_XIC(1, line, "Robot_Name", Rblist1, "XIC(Robot_NameSfty.Int.SftyIntEnbld)XIO(Robot_NameSfty.Int.SftyChanged)")
				line = join_XIC(1, line, "Robot_Name", Rblist1)
			elif "EStops2" in line or "Enbld2" in line:
				line = join_XIC(1, line, "Robot_Name", Rblist2, "XIC(Robot_NameSfty.Int.SftyIntEnbld)XIO(Robot_NameSfty.Int.SftyChanged)")
				line = join_XIC(1, line, "Robot_Name", Rblist2)
			else:
				line = join_XIC(1, line, "Station_Name", Stationlist)
				line = join_XIC(1, line, "Gate_Name", Gatelist)
				line = join_XIC(1, line, "Drive_Name", Drivelist)
				line = join_XIC(1, line, "Robot_Name", Rblist)
				line = join_XIC(1, line, "CNV_Name", CNVlist)
			new_lines.append(line)
		return new_lines

	def safety_ZoneSummary(self, Zone_Name):
		with open("Resource/Program/SafetyTask/ZoneSummary.txt", 'r') as file:
			lines = file.readlines()
		lines = [line.replace("Zone_Name", Zone_Name) for line in lines]
		return lines

	def ZoneSftyOut(self, Zone_Name, Zone_index):
		with open("Resource/Program/SafetyTask/ZoneSftyOut.txt", 'r') as file:
			lines = file.readlines()
		lines = [line.replace("Zone_Name", Zone_Name) for line in lines]
		lines = [line.replace("Z1", "Z" + str(Zone_index)) for line in lines]
		return lines


