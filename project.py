# This is a project manager CLI.
# It is intended for you to execute this script using the `project` bash script in the same
# directory as this python script.
# Example usage: `project newb -n binary_app`
import toml
import re
import sys
import os
from genericpath import isdir, isfile

# A Class used for generating documentation
class doc_gen:
	def doc_file(self,filen:list[str]):
		for f in filen:
			currfile_src = open(f,"rt")
			currfile_doc = open(f + ".md","wt")
			is_prevline_code = False
			is_prevline_doc = False
			for srcline in currfile_src.readlines():
				if "///c" in srcline:
					if not is_prevline_code:
						currfile_doc.write("```\n")
					is_prevline_code = True
					currfile_doc.write(srcline.replace("///c",""))
				elif "///" in srcline:
					is_prevline_doc = True
					currfile_doc.write(srcline.replace("/// ","").replace("///",""))
				else:
					if is_prevline_code:
						currfile_doc.write("```\n")
					elif is_prevline_doc:
						currfile_doc.write("\n")
			currfile_doc.close()
			currfile_src.close()
	def dir_trawler(self,path:str="",deletedocs:bool = False)->list[str]:
		files:list[str]=[]
		dirs:list[str]=[]
		for f_or_d in os.listdir():
			if isdir(f_or_d): # This is a directory
				os.chdir(f_or_d)
				subd = self.dir_trawler(path + f_or_d + "/",deletedocs)
				if len(subd) > 0:
					dirs.append(path + f_or_d + "/")
					for f in subd:
						files.append(f)
				os.chdir("..")
			elif isfile(f_or_d): # this is a file
				if f_or_d.endswith((".c",".cpp",".h",".hpp")) and not deletedocs:
					files.append(path + f_or_d)
				elif f_or_d.endswith(".md") and deletedocs:
					files.append("")
					if f_or_d != "README.md":
						os.remove(f_or_d)
		if len(files) > 0 or len(dirs) > 0 and not deletedocs:
			indexf = open("Index.md","wt")
			indexlist = ""
			if isfile("README.md"):
				indexlist += "It is recommended to read [this](README.md) before you continue\n"
			indexlist += "\n"
			for f in files:
				indexlist += f"- [{f.split('/')[-1]}]({f.split('/')[-1] + '.md'})\n"
			for d in dirs:
				indexlist += f"- [{d.split('/')[-2]}]({d+ 'Index.md'}) DIRECTORY\n"
			
			indexf.write(f"This file was automatically generated with CQP\n{indexlist}")
			indexf.close()
		return files
	def __init__(self) -> None:
		pass

# A class used to generate/manage a directory that contains a CMakeLists.txt file
class package_handler:
	package_toml_config = {
		"source_files":[],
		"include_files":[],
		"package_type":"",
		"subdirectories":[],
		"link_libraries":[]
	}
	def __newpack(self,path:str)->str:
		if not path.endswith("/"):
			path += "/"
		os.makedirs(path + "src/")
		os.makedirs(path + "include/")
		return path
	def __newcmake(self,path:str, type:str):
		packtoml = open(path + "package.toml","wt")
		self.package_toml_config['package_type'] = type
		packtoml.write(toml.dumps(self.package_toml_config))
		packtoml.close()

		cmaketxt = open(path + "CMakeLists.txt","wt")
		def check_type(type):
			if type == "binary":
				return "executable"
			elif type == "library":
				return "library"
		cmaketxt.write(f"""set(PROJECT_SOURCE_FILES
 #PSF
)
set(PROJECT_INCLUDE_FILES
 #PIF
)
set(PROJECT_LINK_LIBRARIES
 #PLL
)
set(PROJECT_DIR {path.split("/")[-2]})
cmake_minimum_required(VERSION 3.23)
project(${'{PROJECT_DIR}'})

add_{check_type(type)}(${'PROJECT_DIR'}
	${'{PROJECT_SOURCE_FILES}'}
	${'{PROJECT_INCLUDE_FILES}'}
)

target_include_directories(${'{PROJECT_DIR}'} PUBLIC
	"include"
)
#CQPend

# You may put any custom settings down here.
# CQP will not change anything after `#CQPend`


""")
		cmaketxt.close()
	
	def newlib(self,path:str):
		path = self.__newpack(path)
		self.__newcmake(path,"library")

	def newbin(self,path:str):
		path = self.__newpack(path)
		self.__newcmake(path,"binary")

	# Used
	def add_file(self,path:str):
		if not path.endswith("/"):
			path += "/"
		back_to_original = os.getcwd()
		os.chdir(path)
		self.package_toml_config = toml.loads(open("package.toml").read())
		self.package_toml_config["source_files"] = []
		self.package_toml_config["include_files"] = []
		def get_src_files(path:str)->list[str]:
			if path.endswith("/"):
				os.chdir(path.split("/")[-2])
			else:
				os.chdir(path.split("/")[-1])

			files = []
			for f_or_d in os.listdir():
				if isfile(f_or_d) and f_or_d.endswith(("c","cpp","h","hpp")):
					files.append(path + "/" + f_or_d)
				elif  isdir(f_or_d):
					for d in get_src_files(path + "/" + f_or_d):
						files.append(d)
			os.chdir("..")
			return files
		for srcfile in get_src_files("src"):
			self.package_toml_config['source_files'].append(srcfile)
		
		for incfile in get_src_files("include"):
			self.package_toml_config['include_files'].append(incfile)
		
		open("package.toml","wt").write(toml.dumps(self.package_toml_config))
		os.chdir(back_to_original)
	
	
	# Synchronizes a package's `package.toml` file and `CMakeLists.txt` file.
	def sync_package(self, path:str):
		if not path.endswith("/"):
			path += "/"
		packfile = open(path + "package.toml","rt")
		self.package_toml_config = toml.loads(packfile.read())
		packfile.close()
		rfile = open(path + "CMakeLists.txt")
		rfile = rfile.readlines()
		wfile = open(path + "CMakeLists.txt","wt")
		
		cqpend = False
		for fline in rfile:
			if cqpend == False:
				if "#PSF" in fline:
					for f in self.package_toml_config["source_files"]:
						wfile.write(f"\"{f}\" ")
					wfile.write("#PSF\n")
				elif "#PIF" in fline:
					for f in self.package_toml_config["include_files"]:
						wfile.write(f"\"{f}\" ")
					wfile.write("#PIF\n")
				elif "#PLL" in fline:
					for l in self.package_toml_config['link_libraries']:
						wfile.write(f"{l} ")
					wfile.write("#PLL\n")
				elif "add_subdirectory" in fline:
					continue
				elif "#CQPend" in fline:
					for d in self.package_toml_config['subdirectories']:
						wfile.write(f"add_subdirectory({d})\n")
					wfile.write("#CQPend\n")
					cqpend = True
				else:
					wfile.write(fline)
			else:
				wfile.write(fline)
		wfile.close()
	def __init__(self) -> None:
		pass

class bundler
config = toml.loads(open("project.toml").read())

if __name__ == "__main__":
	documentation = doc_gen()
	STATE_DEFAULT = 1
	STATE_DOC_SINGLEFILE = 2
	STATE_CMAKE_NEWBINARY = 3
	STATE_CMAKE_NEWLIBRARY = 4
	STATE_CMAKE_SYNCPACK = 5
	state = 0
	
	SUBC_CMAKE = 1
	SUBC_BUNDLE = 2
	SUBC_DOC = 3
	subcommand = 0
	for argument in sys.argv:
		if subcommand == 0:
			if argument == "doc":
				subcommand = SUBC_DOC
			elif argument == "cmake":
				subcommand = SUBC_CMAKE
			elif argument == "bundle":
				subcommand = SUBC_BUNDLE
		#SECTION Doc Subcommand
		elif subcommand == SUBC_DOC:
			if state == 0:
				if argument == "-i":
					state = STATE_DOC_SINGLEFILE
				elif argument == "-a":
					documentation.doc_file(documentation.dir_trawler())
					break
				elif argument == "-d":
					documentation.dir_trawler(deletedocs=True)
					break
			elif state == STATE_DOC_SINGLEFILE:
				if argument.endswith((".cpp","c","h","hpp")):
					documentation.doc_file([argument])
				else:
					print(f"The file {argument} has a file extension that is not 'c', 'cpp', 'h', 'hpp'")
		# !SECTION
		# SECTION CMake Subcommand
		elif subcommand == SUBC_CMAKE:
			if state == 0:
				# A path for generating build files using CMake
				if argument == "gen":
					cmake_command =f"cmake -S . -B build -G \"{config['cmake_config']['generator']}\" "
					for i in config["cmake_config"]["extra_variables"]:
						cmake_command += f"-D {i} "
					if config["cmake_config"]["c_compiler"] != 0:
						cmake_command += f"-D CMAKE_C_COMPILER={config['cmake_config']['c_compiler']} "
					if config['cmake_config']['cpp_compiler'] != 0:
						cmake_command += f"-D CMAKE_CXX_COMPILER={config['cmake_config']['cpp_compiler']} "
					os.system(cmake_command)
					break
				# Used to branch off to a process to create a new executable
				elif argument== "newbin":
					state = STATE_CMAKE_NEWBINARY
				# Used to branch off to a process to create a new library
				elif argument == "newlib":
					state = STATE_CMAKE_NEWLIBRARY
				# Used to synchronize the package.toml file with the CMakeLists.txt in a directory
				elif argument == "sync":
					state = STATE_CMAKE_SYNCPACK
			elif state == STATE_CMAKE_NEWBINARY:
				pack = package_handler()
				pack.newbin(argument)
				print(f"Succesfully created a new executable package `{argument}`\nYou may need to manually add `{argument}` as a subdirectory\n")

			elif state == STATE_CMAKE_NEWLIBRARY:
				pack = package_handler()
				pack.newlib(argument)
				print(f"Succesfully created a new library package `{argument}`\nYou may need to manually add `{argument}` as a subdirectory\n")

			elif state == STATE_CMAKE_SYNCPACK:
				pack = package_handler()
				pack.add_file(argument)
				pack.sync_package(argument)
		# !SECTION

open("project.toml","wt").write(toml.dumps(config))