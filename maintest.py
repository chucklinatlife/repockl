#~~~~_~~~BROADCOM~~~_~~~~~ pdnanalysis/PythonServer/Lamc/ANMv2/main.py
#~_./~\._,/~~~~\,_./~\._~~ PROJECT: Revision of Associative Net Mapping
#~~Connecting Everything~~ 
#~~~~~~~~~~~~~~~~~~~lamc~~ 
#**********************************************************************************************
import subprocess, os
import re, pprint,json, os, sys, argparse
import xml.etree.ElementTree as ET
import functions, spdfunctions, mappingfunctions, cadenceSelect, brdfileParse, spdfileParse, mapSupport
import sendEmail

#print_pretty = pprint.PrettyPrinter()
pp = pprint.PrettyPrinter(indent=4)
yes_list = 'y'

def main():
	Debug = False
	Interactive = False


	#new capacitor dictionary
	rpt_capDict = {}
	comp_dictx = {}
	good_dict = {}
	#global mismatch list
	bad_list = []
	dni_list = []
	xml_file_name = 'BRCM-Decap-Lib-all-SPICE-extended_new-with-brcmPN.xml'

	#component value conversion key
	comp_convert = {'K': 1000, 'u': 10**-6, 'n': 10**-9, 'H':1, 'F':1, 'm':10**-3, 'p':10**-12, 'M':10**6,'G':10**9}
	#part number list
	pn_list = []

	#flags
	searchNode_flag = 'y'
	map_flag = 'y'



	#Start program

	#Check Operating System
	if os.name == "nt":
		Windows = True
	else:
		Windows = False

	#if no additional arguments given: parse the xmlconfig file
	if not len(sys.argv) > 1:
		print 'Reading xml configuration file\n'
		xmlconfig = 'config.xml'
		tree = ET.parse(xmlconfig)
		root = tree.getroot()
		xml_user_dict = {}
		for child in root:
			xml_user_dict[child.tag] = child.attrib["name"]
		#set xml_dict to args_dict
		args_dict = xml_user_dict
		#args_dict = sorted(args_dict.iterkeys())


	else:
		parser = argparse.ArgumentParser()
		parser.add_argument("-b", "--BRD", help="please input brd file name")
		parser.add_argument("-v", "--VRM_COMP", help="please input vrm component")
		parser.add_argument("-s", "--SINK_COMP", help="please input sink component")
		parser.add_argument("-l", "--VRM_L_COMP", help="please input vrm inductor")
		parser.add_argument("-n", "--NET_TO_ANALYZE", help = "please input net to analyze")
		parser.add_argument("-ven", "--VENDOR", help = "please select a vendor")
		parser.add_argument("-g", "--REF", help = "define ground")
		parser.add_argument("-mcm", "--MCM", help = "define a mcm file")
		parser.add_argument("-dc", "--DC", help ="define PowerDC")
		#OptimizePI arguments
		parser.add_argument("-si", "--SI", help ="define OptimizePI")
		parser.add_argument("-soc", "--SOC_COMP", help="define SOC_COMP for OptimizePI")
		parser.add_argument("-rail", "--RAIL_CPM", help="define RAIL_CPM for OptimizePI")
		parser.add_argument("-oref", "--OBS_REF", help = "define Observation Point Ref")
		parser.add_argument("-opos", "--OBS_POS", help = "define Observation Point Pos")
		args = parser.parse_args()
		args_dict = vars(args)
		#append DECAP XML to parser dict
		args_dict["DECAP_XML"] = xml_file_name
		#args_dict = sorted(args_dict.iterkeys())






	#Checks user input argument parameters (if any)
	check_input = 1
	while check_input:
		pp.pprint('-----------------------')
		pp.pprint(args_dict)
		stop_q = raw_input('Is this correct? (y/n) ')
		if stop_q == filter(lambda x: re.search( yes_list, x), stop_q):
			check_input = 0
		else:
			sys.exit()

	'''-----------------------------------------------------------------
	BRD FILE PARSE
	-----------------------------------------------------------------'''
	if args_dict["BRD"] is not None:
		brd_file_name = args_dict["BRD"]
		brd_file_name = brd_file_name + '.brd'
		pp.pprint(brd_file_name)
		
	brd_file_parser = brdfileParse.brdfileParse(args_dict, xml_file_name, Windows)
	if Windows:
		brd_file_parser.genBatch("pkg.bat")
	else:
		brd_file_parser.run_brd2rpt()
	# elif Interactive:
		# brd_file_name = raw_input("enter a board file: ")

	# else:
		# brd_file_name = '200-128228-0001_01.brd'
		
	# if Debug:
		# pp.pprint(brd_file_name)
	# #generation of RPT file done
	pp.pprint('done generating RPT file')

	#example line of RPT
	#S!R2818!RESC1608_IS0603Q!100!500011-00!
	#extract the components
	'''-------------------------------------------------------------
	EXTRACT RPT
	-------------------------------------------------------------'''
	rpt_file = os.path.realpath("compExtract.rpt")
	#rpt_cap_data = complete rpt cap dictionary
	rpt_cap_data = brd_file_parser.parse_rpt(rpt_file)
	if Debug:
		pp.pprint(rpt_cap_data)
		
	'''-------------------------------------------------------------
	PARSE XML
	-------------------------------------------------------------'''
	#xml_data = parsed xml data, brcm_xml_data = passed brcm pn
	xml_data, xmlCaps = brd_file_parser.parse_xml()
	#compared rpt with xml
	parsed_xmlrpt = brd_file_parser.compare_xml(rpt_cap_data,xml_data)
	#write more files for analyzing
	brd_file_parser.writeFiles(parsed_xmlrpt,xml_data,rpt_cap_data)
	#read spd file
	'''----------------------------------------------
	SPD FILE PARSE 
	-------------------------------------------------'''
	pp.pprint("Generating spdfile")
	spd_file_parser = spdfileParse.spdfileParse(args_dict, Windows)
	#short_segment = spd_file_parser.readspd()
	#if user input mcm
	if args_dict["MCM"]:
		spd_file_parser.readspd_pkg()
		print 'Done generating pkg spd file\n'
	#grab name	
	spd_file_parser.readspd()
	#run spd file
	spd_file_parser.runspdWindows()
	#extract
	complist_dict, netlist_dict = spd_file_parser.open_spd()
	#look up components
	if Interactive:
		searchNode_flag = raw_input("Look Up Component Connections? (y/n) ")
	if searchNode_flag == filter( lambda x: re.search(yes_list, x), searchNode_flag):
		mappingfunctions.lookUp(complist_dict,netlist_dict)
	#map components
	# if Interactive:
		# map_flag = raw_input("Map components? (y/n) ")


	if map_flag == 'y':
		#ask for parameters
		mapConnection = mapSupport.mapSupport(args_dict["BRD"],args_dict, complist_dict, netlist_dict)
		mapDict = mapConnection.map_components()
		link_path = mapConnection.find_link()
		print link_path
		#cap_dict = cap connection nodes dict
		cap_dict, sort_list = mapConnection.find_caps(link_path)
		newAllCaps_list, capstoReplace = mapConnection.writeCap_connect(parsed_xmlrpt, link_path, cap_dict, sort_list)
		replacedCAPS, replacedList = mapConnection.replaceCaps(capstoReplace, newAllCaps_list, xml_data, xmlCaps)
		mapConnection.writeNewCapFile(replacedCAPS, link_path, sort_list)
		
		
		#mapDict = mappingfunctions.map_components(args_dict, complist_dict,netlist_dict)
		#calculate the link
		#link_path = mappingfunctions.find_link(netlist_dict, complist_dict, mapDict)
		#pp.pprint("------------------------------------------------------------")
		#pp.pprint(link_path)
		#pp.pprint("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
		#find the decoupled caps in link
		#cap_dict, sort_list = mappingfunctions.find_caps(link_path, netlist_dict)
		#write out cap connections
		#newAllCaps_list, capstoReplace = mappingfunctions.writeCap_connect(parsed_xmlrpt, link_path, cap_dict, sort_list)
		#replace the capacitors
		#replacedCAPS, replacedList = mappingfunctions.replaceCaps(capstoReplace, newAllCaps_list, xml_data, xmlCaps)
		#mappingfunctions.writeNewCapFile(replacedCAPS, link_path, sort_list)
	'''-----------------------------------------------------------------------
	Write TCL
	-----------------------------------------------------------------------'''
	#grab data from match_path
	pp.pprint(link_path)
	#can filter with input
	path = os.getcwd()
	mapDict["REF"] = args_dict["REF"]
	pp.pprint(args_dict)
	if args_dict["VENDOR"] == "CADENCE":
		cadenceSelection = cadenceSelect.cadenceSelect(path, args_dict, link_path, mapDict, replacedList, replacedCAPS, netlist_dict, complist_dict, cap_dict, Windows)
		pp.pprint(Windows)
		#check for PowerDC
		if int(args_dict["DC"]) == 1:
			cadenceSelection.prepareTclScriptDC()
			sendEmail.sendSimpleEmail(args_dict["USER"]+'@broadcom.com', 'PDNAnalysis Status', 'DC TCL Script Done')
			#run DC simulation
			
		#check for OptimizePI
		if int(args_dict["SI"]) == 1:
			if args_dict["MCM"]:
				cadenceSelection.prepareTclScriptSI()
				cadenceSelection.prepareTclScriptSI_2()
				cadenceSelection.runTclSI()
				sendEmail.sendSimpleEmail(args_dict["USER"]+'@broadcom.com', 'PDNAnalysis Status', 'OptimizePI Done')
			
			
	
