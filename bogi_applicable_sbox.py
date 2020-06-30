import os
import pickle
import tarfile

__THIS_FILE_DIR__ = os.path.dirname(os.path.realpath(__file__))
__DATA_DIR__ = os.path.join(__THIS_FILE_DIR__, "data")


#data file describtions
__DATA_FILE_LIST__ = [
	os.path.join(__DATA_DIR__, "bogi_applicable_pxe_class.pickle"),			#2,413  BOGI-applicable PXE classes are stored in a list.
	os.path.join(__DATA_DIR__, "opt_bogi_applicable_pxe_class.pickle"), 	#20     Optimal BOGI-applicable PXE classes are stored in a list.
	os.path.join(__DATA_DIR__, "opt_bogi_applicable_pe_class.pickle"), 		#4,608  Optimal BOGI-applicable PE  classes are stored in a list.
	os.path.join(__DATA_DIR__, "opt_bogi_applicable_xe_class.pickle"),      #10,368 Optimal BOGI-applicable XE  classes are stored in a list.
	os.path.join(__DATA_DIR__, "opt_bogi_applicable_xei_class.pickle"),     #1,728  Optimal BOGI-applicable XEI classes are stored in a list.
	os.path.join(__DATA_DIR__, "software_code.pickle"),            			#The best B-implementation codes in software.
	os.path.join(__DATA_DIR__, "hardware_UMC180nm_code.pickle"),            #The best B-implementation codes with UMC180nm standard cell library.
	os.path.join(__DATA_DIR__, "hardware_TSMC65nm_code.pickle"),            #The best B-implementation codes with TSMC65 standard cell library.
]

__LOAD__DATA_SIZE__LIST__ = [
	2413,
	20,
	4608,
	10368,
	1728,
]

__LOAD__DATA_LIST__ = [
	[], #0 - bogi_applicable_pxe_class.pickle
	[], #1 - opt_bogi_applicable_pxe_class.pickle
	[], #2 - opt_bogi_applicable_pe_class.pickle
	[], #3 - opt_bogi_applicable_xe_class.pickle
	[], #4 - opt_bogi_applicable_xei_class.pickle
	#codes dict load
	[], #5 - software_code.pickle
	[], #6 - hardware_UMC180nm_code.pickle
	[], #7 - hardware_TSMC65nm_code.pickle
]

def __get_dict_rst_str__(rst_dict):
	Long_line = 0
	for k in rst_dict.keys():
		if len(k) > Long_line:
			Long_line = len(k)
	rst_str = ""
	for k in rst_dict.keys():
		rst_str+=eval('''\"%%-%ds ~ %%s\\n\"%%(k, str(rst_dict[k]))'''%(Long_line))
	return rst_str

__PE_INTERVAL__ 	= [0, 256, 512, 768, 1024, 1280, 1536, 1792, 2048, 2176, 2304, 2560, 2816, 3072, 3328, 3584, 3840, 4096, 4352, 4480, 4608]
__XE_INTERVAL__ 	= [0, 576, 1152, 1728, 2304, 2880, 3456, 4032, 4608, 4896, 5184, 5760, 6336, 6912, 7488, 8064, 8640, 9216, 9792, 10080, 10368]
__XEI_INTERVAL__ 	= [0, 96, 192, 288, 384, 480, 576, 672, 768, 816, 864, 960, 1056, 1152, 1248, 1344, 1440, 1536, 1632, 1680, 1728]



def __filecheck_then_uncomp__():
	for l in __DATA_FILE_LIST__:
		if os.path.isfile(l) == False:
			comp_l = l + ".gz"
			if os.path.isfile(comp_l) == False:
				raise NameError("%s is required"%(os.path.relpath(comp_l)))
			tar = tarfile.open(comp_l)
			print("Getting %s..."%(os.path.relpath(l)))
			tar.extractall(__DATA_DIR__)
			tar.close()

__filecheck_then_uncomp__()


class BOGI_PXE_CLASS():

	def __get_rst_dict__(self):
		rst_dict = dict()
		rst_dict["Index"] 	 		= self.pxe_idx
		rst_dict["Representive"] 	= self.pxe_repre
		rst_dict["Size"]         	= self.pxe_size
		rst_dict["Uniformity"] 		= self.pxe_uniformity
		rst_dict["Linearity"]		= self.pxe_linearity
		rst_dict["Nonlinearity"]	= self.pxe_nonlinearity
		return rst_dict

	def __init__(self, idx=0):
		## Setting
		global __DATA_FILE_LIST__
		global __LOAD__DATA_SIZE__LIST__
		global __LOAD__DATA_LIST__

		file_idx 	= 0		
		datafilen 	= __DATA_FILE_LIST__[file_idx]
		list_size 	= __LOAD__DATA_SIZE__LIST__[file_idx]
		loaded_data = __LOAD__DATA_LIST__[file_idx]
		################

		###Check Loaded Data
		if loaded_data == []:
			f = open(datafilen, "rb")
			loaded_data = pickle.load(f)
			__LOAD__DATA_LIST__[file_idx] = loaded_data
			f.close()
		self.__loaded_data__ = loaded_data
		self.num_tot_pxe_classes = len(self.__loaded_data__)
		if self.num_tot_pxe_classes != list_size:
			raise NameError("Size of Loaded List Must be %d"%(list_size))
		################

		###Arrange Info
		if idx >= self.num_tot_pxe_classes:
			raise NameError("Input index(%d) is out of %d"%(idx, self.num_tot_pxe_classes))
		self.pxe_idx 			 = idx
		self.pxe_repre           = self.__loaded_data__[idx][0]
		self.pxe_size            = self.__loaded_data__[idx][1]
		self.pxe_uniformity      = self.__loaded_data__[idx][2]
		self.pxe_linearity       = self.__loaded_data__[idx][3]
		self.pxe_nonlinearity    = self.__loaded_data__[idx][4]
		self.rst_dict            = self.__get_rst_dict__()
		#################

	def __repr__(self):
		return __get_dict_rst_str__(self.rst_dict)
	
	def __str__(self):
		return __get_dict_rst_str__(self.rst_dict)

	def print_all(self, range_list):
		for idx in range_list:
			print(BOGI_PXE_CLASS(idx))

class OPT_BOGI_PE_CLASS():
	def __get_rst_dict__(self):
		rst_dict = dict()
		rst_dict["PE Index"]	  				      = self.pe_idx
		rst_dict["PXE Index"]					      = self.pxe_idx
		rst_dict["Size"]         				      = self.pe_size
		rst_dict["Representive"] 				   	  = self.pe_repre
		rst_dict["Implementation Cost(BGC-Software)"] = self.pe_software
		rst_dict["Implementation Cost(GEC-UMC180mn)"] = self.pe_UMC180nm
		rst_dict["Implementation Cost(GEC-TSMC65nm)"] = self.pe_TSMC65nm
		return rst_dict

	def __init__(self, idx=0):
		## Setting
		global __DATA_FILE_LIST__
		global __LOAD__DATA_SIZE__LIST__
		global __LOAD__DATA_LIST__

		file_idx 	= 2		
		datafilen 	= __DATA_FILE_LIST__[file_idx]
		list_size 	= __LOAD__DATA_SIZE__LIST__[file_idx]
		loaded_data = __LOAD__DATA_LIST__[file_idx]
		################

		###Check Loaded Data
		if loaded_data == []:
			f = open(datafilen, "rb")
			loaded_data = pickle.load(f)
			__LOAD__DATA_LIST__[file_idx] = loaded_data
			f.close()
		self.__loaded_data__ = loaded_data
		self.num_tot_pe_classes = len(self.__loaded_data__)
		if self.num_tot_pe_classes != list_size:
			raise NameError("Size of Loaded List Must be %d"%(list_size))
		################

		###Arrange Info
		if idx >= self.num_tot_pe_classes:
			raise NameError("Input index(%d) is out of %d"%(idx, self.num_tot_pe_classes))

		

		self.pe_idx 			 = idx
		self.pxe_idx             = self.__loaded_data__[idx][0]
		self.pe_repre            = self.__loaded_data__[idx][1]
		self.pe_size             = self.__loaded_data__[idx][2]
		self.pe_codename         = self.__loaded_data__[idx][3]
		self.pe_software         = self.__loaded_data__[idx][4]
		self.pe_UMC180nm         = self.__loaded_data__[idx][5]
		self.pe_TSMC65nm         = self.__loaded_data__[idx][6]
		self.pe_sboxes           = self.__loaded_data__[idx][7]
		self.rst_dict            = self.__get_rst_dict__()

		#code load
		##Check Loaded Data
		if __LOAD__DATA_LIST__[5] == []: #software
			f = open(__DATA_FILE_LIST__[5], "rb")
			__LOAD__DATA_LIST__[5] = pickle.load(f)
			f.close()
		self.pe_software_code = __LOAD__DATA_LIST__[5][self.pe_codename]

		if __LOAD__DATA_LIST__[6] == []: #hardware_UMC180nm
			f = open(__DATA_FILE_LIST__[6], "rb")
			__LOAD__DATA_LIST__[6] = pickle.load(f)
			f.close()
		self.pe_UMC180nm_code = __LOAD__DATA_LIST__[6][self.pe_codename]

		if __LOAD__DATA_LIST__[7] == []: #hardware_TSMC65nm
			f = open(__DATA_FILE_LIST__[7], "rb")
			__LOAD__DATA_LIST__[7] = pickle.load(f)
			f.close()
		self.pe_TSMC65nm_code = __LOAD__DATA_LIST__[6][self.pe_codename]

		#################

	def __repr__(self):
		return __get_dict_rst_str__(self.rst_dict)
	
	def __str__(self):
		return __get_dict_rst_str__(self.rst_dict)

class OPT_BOGI_XE_CLASS():
	def __get_rst_dict__(self):
		rst_dict = dict()
		rst_dict["XE Index"]	  				      = self.xe_idx
		rst_dict["PXE Index"]					      = self.pxe_idx
		rst_dict["Size"]         				      = self.xe_size
		rst_dict["Representive"] 				   	  = self.xe_repre
		rst_dict["Input BOGI Spectrum"]               = self.xe_inbg
		rst_dict["Output BOGI Spectrum"]              = self.xe_outbg
		rst_dict["Is XE_I"]							  = self.is_xei
		return rst_dict

	def __init__(self, idx=0):
		## Setting
		global __DATA_FILE_LIST__
		global __LOAD__DATA_SIZE__LIST__
		global __LOAD__DATA_LIST__

		file_idx 	= 3		
		datafilen 	= __DATA_FILE_LIST__[file_idx]
		list_size 	= __LOAD__DATA_SIZE__LIST__[file_idx]
		loaded_data = __LOAD__DATA_LIST__[file_idx]
		################

		###Check Loaded Data
		if loaded_data == []:
			f = open(datafilen, "rb")
			loaded_data = pickle.load(f)
			__LOAD__DATA_LIST__[file_idx] = loaded_data
			f.close()
		self.__loaded_data__ = loaded_data
		self.num_tot_xe_classes = len(self.__loaded_data__)
		if self.num_tot_xe_classes != list_size:
			raise NameError("Size of Loaded List Must be %d"%(list_size))
		################

		###Arrange Info
		if idx >= self.num_tot_xe_classes:
			raise NameError("Input index(%d) is out of %d"%(idx, self.num_tot_xe_classes))

		

		self.xe_idx 			 = idx
		self.pxe_idx             = self.__loaded_data__[idx][0]
		self.xe_repre            = self.__loaded_data__[idx][1]
		self.xe_size             = self.__loaded_data__[idx][2]
		self.xe_inbg             = self.__loaded_data__[idx][3][0]
		self.xe_outbg            = self.__loaded_data__[idx][3][1]
		self.xe_ddt              = self.__loaded_data__[idx][4]
		self.xe_sqlat            = self.__loaded_data__[idx][5]		
		self.xe_sboxes           = self.__loaded_data__[idx][6]

		#check XE_I
		self.is_xei = True
		for idx in range(4):
			if self.xe_inbg[idx] == "b" and self.xe_outbg[idx] == "b":
				self.is_xei = False
				break
		
		self.rst_dict            = self.__get_rst_dict__()
		#################



	def __repr__(self):
		return __get_dict_rst_str__(self.rst_dict)
	
	def __str__(self):
		return __get_dict_rst_str__(self.rst_dict)

class OPT_BOGI_XEI_CLASS():
	def __get_rst_dict__(self):
		rst_dict = dict()
		rst_dict["XEI Index"]	  				      = self.xei_idx
		rst_dict["XE Index"] 						  = self.xe_idx                 
		rst_dict["PXE Index"]					      = self.pxe_idx
		rst_dict["Size"]         				      = self.xei_size
		rst_dict["Representive"] 				   	  = self.xei_repre
		rst_dict["Input BOGI Spectrum"]               = self.xei_inbg
		rst_dict["Output BOGI Spectrum"]              = self.xei_outbg
		rst_dict["(DR13, LR13)64"]                    = (self.xei_dr64_13, self.xei_lr64_13)
		rst_dict["(DR12, LR12)128"]                    = (self.xei_dr128_12, self.xei_lr128_12)
		return rst_dict

	def __init__(self, idx=0):
		## Setting
		global __DATA_FILE_LIST__
		global __LOAD__DATA_SIZE__LIST__
		global __LOAD__DATA_LIST__

		file_idx 	= 4		
		datafilen 	= __DATA_FILE_LIST__[file_idx]
		list_size 	= __LOAD__DATA_SIZE__LIST__[file_idx]
		loaded_data = __LOAD__DATA_LIST__[file_idx]
		################

		###Check Loaded Data
		if loaded_data == []:
			f = open(datafilen, "rb")
			loaded_data = pickle.load(f)
			__LOAD__DATA_LIST__[file_idx] = loaded_data
			f.close()
		self.__loaded_data__ = loaded_data
		self.num_tot_xei_classes = len(self.__loaded_data__)
		if self.num_tot_xei_classes != list_size:
			raise NameError("Size of Loaded List Must be %d"%(list_size))
		################

		###Arrange Info
		if idx >= self.num_tot_xei_classes:
			raise NameError("Input index(%d) is out of %d"%(idx, self.num_tot_xei_classes))

		

		self.xei_idx 			 = idx
		self.xe_idx              = self.__loaded_data__[idx][0]
		self.pxe_idx             = self.__loaded_data__[idx][1]
		self.xei_repre           = self.__loaded_data__[idx][2]
		self.xei_size            = self.__loaded_data__[idx][3]
		self.xei_inbg            = self.__loaded_data__[idx][4][0]
		self.xei_outbg           = self.__loaded_data__[idx][4][1]
		self.xei_ddt             = self.__loaded_data__[idx][5]
		self.xei_sqlat           = self.__loaded_data__[idx][6]
		self.xei_dr64            = self.__loaded_data__[idx][7]
		self.xei_lr64            = self.__loaded_data__[idx][8]
		self.xei_dr64_elapsed    = self.__loaded_data__[idx][9]
		self.xei_dr64_elapsed    = self.__loaded_data__[idx][10]
		self.xei_dr128           = self.__loaded_data__[idx][11]
		self.xei_lr128           = self.__loaded_data__[idx][12]
		self.xei_dr128_elapsed   = self.__loaded_data__[idx][13]
		self.xei_dr128_elapsed   = self.__loaded_data__[idx][14]	
		self.xei_sboxes          = self.__loaded_data__[idx][15]

		#for 64-bit, 13-Round
		if self.xei_dr64 != None:
			self.xei_dr64_13 = self.xei_dr64[12]
		else:
			self.xei_dr64_13 = None
		if self.xei_lr64 != None:
			self.xei_lr64_13 = self.xei_lr64[12]
		else:
			self.xei_lr64_13 = None

		##for 128-bit, 12-Round
		if self.xei_dr128 != None:
			self.xei_dr128_12 = self.xei_dr128[11]
		else:
			self.xei_dr128_12 = None
		if self.xei_lr128 != None:
			self.xei_lr128_12 = self.xei_lr128[11]
		else:
			self.xei_lr128_12 = None
		
		self.rst_dict            = self.__get_rst_dict__()
		#################
	def __repr__(self):
		return __get_dict_rst_str__(self.rst_dict)
	
	def __str__(self):
		return __get_dict_rst_str__(self.rst_dict)

class OPT_BOGI_PXE_CLASS():
	def get__inner_pe_info(self):
		NUM_PE      = 0
		BGC 		= []
		GEC_umc 	= []
		GEC_tsmc 	= []
		PE_IDXES    = []
		for pe_idx in range(__PE_INTERVAL__[self.pxe_idx], __PE_INTERVAL__[self.pxe_idx + 1]):
			pe = OPT_BOGI_PE_CLASS(pe_idx)
			PE_IDXES.append(pe_idx)
			NUM_PE+=1
			BGC.append(pe.rst_dict["Implementation Cost(BGC-Software)"])
			GEC_umc.append(pe.rst_dict["Implementation Cost(GEC-UMC180mn)"])
			GEC_tsmc.append(pe.rst_dict["Implementation Cost(GEC-TSMC65nm)"])
		BGC = sorted(list(set(BGC)))
		GEC_umc = sorted(list(set(GEC_umc)))
		GEC_tsmc = sorted(list(set(GEC_tsmc)))
		return [NUM_PE, BGC, GEC_umc, GEC_tsmc, PE_IDXES]

	def get__inner_xe_info(self):
		NUM_XE      = 0
		XE_IDXES    = []
		for xe_idx in range(__XE_INTERVAL__[self.pxe_idx], __XE_INTERVAL__[self.pxe_idx + 1]):
			xe = OPT_BOGI_XE_CLASS(xe_idx)
			XE_IDXES.append(xe_idx)
			NUM_XE+=1
		return [NUM_XE, XE_IDXES]

	def get__inner_xei_info(self):
		NUM_XEI      = 0
		DR_LR13_64	= []
		DR_LR12_128	= []
		XEI_IDXES   = []
		for xei_idx in range(__XEI_INTERVAL__[self.pxe_idx], __XEI_INTERVAL__[self.pxe_idx + 1]):
			xei = OPT_BOGI_XEI_CLASS(xei_idx)
			XEI_IDXES.append(xei_idx)
			NUM_XEI+=1
			if xei.rst_dict["(DR13, LR13)64"] != (None, None):
				DR_LR13_64.append(xei.rst_dict["(DR13, LR13)64"])
			if xei.rst_dict["(DR12, LR12)128"] != (None, None):
				DR_LR12_128.append(xei.rst_dict["(DR12, LR12)128"])
		DR_LR13_64  = sorted(list(set(DR_LR13_64)))
		DR_LR12_128 = sorted(list(set(DR_LR12_128)))
		return [NUM_XEI, DR_LR13_64, DR_LR12_128, XEI_IDXES]


	def __get_rst_dict__(self):
		rst_dict = dict()
		rst_dict["PXE Index(Paper)"]			  = self.pxe_idx
		rst_dict["AE  Index"]					  = self.ae_idx
		rst_dict["Size"]         				  = self.pxe_size
		rst_dict["Representive"] 				  = self.pxe_repre
		rst_dict["Uniformity"] 					  = self.pxe_uniformity
		rst_dict["Linearity"]					  = self.pxe_linearity
		rst_dict["Nonlinearity"]				  = self.pxe_nonlinearity
		pe_info = self.get__inner_pe_info()
		rst_dict["Number of PE Classes Included"] 	= pe_info[0]
		rst_dict["Available Costs(BGC-Software)"] 	= pe_info[1]
		rst_dict["Available Costs(GEC-UMC180mn)"] 	= pe_info[2]
		rst_dict["Available Costs(GEC-TSCM65nm)"] 	= pe_info[3]
		xe_info  = self.get__inner_xe_info()
		rst_dict["Number of XE Classes Included"] 	= xe_info[0]
		xei_info = self.get__inner_xei_info()
		rst_dict["Number of XEi Classes Included"] 	= xei_info[0]
		rst_dict["Available (DR13, LR13)64"]  		= xei_info[1]
		rst_dict["Available (DR12, LR12)128"] 		= xei_info[2]
		return rst_dict

	def __init__(self, idx=0):
		## Setting
		global __DATA_FILE_LIST__
		global __LOAD__DATA_SIZE__LIST__
		global __LOAD__DATA_LIST__

		file_idx 	= 1		
		datafilen 	= __DATA_FILE_LIST__[file_idx]
		list_size 	= __LOAD__DATA_SIZE__LIST__[file_idx]
		loaded_data = __LOAD__DATA_LIST__[file_idx]
		################

		###Check Loaded Data
		if loaded_data == []:
			f = open(datafilen, "rb")
			loaded_data = pickle.load(f)
			__LOAD__DATA_LIST__[file_idx] = loaded_data
			f.close()
		self.__loaded_data__ = loaded_data
		self.num_tot_pxe_classes = len(self.__loaded_data__)
		if self.num_tot_pxe_classes != list_size:
			raise NameError("Size of Loaded List Must be %d"%(list_size))
		################

		###Arrange Info
		if idx >= self.num_tot_pxe_classes:
			raise NameError("Input index(%d) is out of %d"%(idx, self.num_tot_pxe_classes))
		self.pxe_idx 			 = idx
		self.ae_idx              = self.__loaded_data__[idx][0]
		self.pxe_repre           = self.__loaded_data__[idx][1]
		self.pxe_size            = self.__loaded_data__[idx][2]
		self.pxe_sboxes          = self.__loaded_data__[idx][3]
		self.pxe_uniformity      = self.__loaded_data__[idx][4]
		self.pxe_linearity       = self.__loaded_data__[idx][5]
		self.pxe_nonlinearity    = self.__loaded_data__[idx][6]
		self.rst_dict            = self.__get_rst_dict__()
		#################

	def __repr__(self):
		return __get_dict_rst_str__(self.rst_dict)
	
	def __str__(self):
		return __get_dict_rst_str__(self.rst_dict)

class XEI_PE_INTERSECTION():
	
	def __get_rst_dict__(self):
		rst_dict = dict()
		rst_dict["PXE Index(Paper)"]			  = self.pxe_idx
		rst_dict["XEI Index"]					  = self.xei_idx
		rst_dict["PE Index"]					  = self.pe_idx
		rst_dict["Size"]         				  = self.xeipe_size
		rst_dict["Available Costs(BGC-Software)"] = self.xeipe_software
		rst_dict["Available Costs(GEC-UMC180mn)"] = self.xeipe_UMC180nm
		rst_dict["Available Costs(GEC-TSCM65nm)"] = self.xeipe_TSMC65nm
		rst_dict["Available (DR13, LR13)64"]  	  = self.xeipe_DRLR13_64
		rst_dict["Available (DR12, LR12)128"] 	  = self.xeipe_DRLR12_128
		return rst_dict

	def __init__(self, pxe_idx, xei_idx, pe_idx):
		assert(__LOAD__DATA_SIZE__LIST__[0] > pxe_idx)
		possible_xei_idxes   = range(__XEI_INTERVAL__[pxe_idx], __XEI_INTERVAL__[pxe_idx + 1])
		if xei_idx not in possible_xei_idxes:
			raise NameError("XEi Class Index must be %d ~ %d for the %d-th BOGI-applicable PXE class"%(possible_xei_idxes[0], possible_xei_idxes[-1] - 1, pxe_idx))
		possible_pe_idxes    = range(__PE_INTERVAL__[pxe_idx], __PE_INTERVAL__[pxe_idx + 1])
		if pe_idx not in possible_pe_idxes:
			raise NameError("PE Class Index must be %d ~ %d for the %d-th BOGI-applicable PXE class"%(possible_pe_idxes[0], possible_pe_idxes[-1] - 1, pxe_idx))
		self.pxe_idx             = pxe_idx
		self.pe_idx              = pe_idx
		self.xei_idx             = xei_idx
		pe_class = OPT_BOGI_PE_CLASS(self.pe_idx)
		xei_class = OPT_BOGI_XEI_CLASS(self.xei_idx)
		self.xeipe_pe_class      = pe_class
		self.xeipe_xei_class     = xei_class
		self.xeipe_sboxes        = list(set(xei_class.xei_sboxes).intersection(set(pe_class.pe_sboxes)))
		self.xeipe_size          = len(self.xeipe_sboxes)
		self.xeipe_software      = pe_class.pe_software
		self.xeipe_UMC180nm      = pe_class.pe_UMC180nm
		self.xeipe_TSMC65nm      = pe_class.pe_TSMC65nm
		self.xeipe_DRLR13_64     = (xei_class.xei_dr64_13, xei_class.xei_lr64_13)
		self.xeipe_DRLR12_128    = (xei_class.xei_dr128_12, xei_class.xei_lr128_12)
		self.rst_dict            = self.__get_rst_dict__()
	
	def print_sboxes(self):
		for s in self.xeipe_sboxes:
			print(s)

	def __repr__(self):
		return __get_dict_rst_str__(self.rst_dict)
	
	def __str__(self):
		print("S-boxes List")
		self.print_sboxes()
		print("="*60)
		return __get_dict_rst_str__(self.rst_dict)		
		
		

if __name__ == "__main__":
	while True:
		NUM_BOGI_APPLICABLE_PXE_CLASSES 	= 2413
		OPT_PXE_IDXES 						= [370, 390, 399, 404, 717, 720, 729, 732, 1016, 1018, 1104, 1108, 1659, 1713, 1806, 1832, 2050, 2147, 2176, 2190]
		NUM_OPT_BOGI_APPLICABLE_PXE_CLASSES	= 20
		NUM_OPT_BOGI_APPLICABLE_PE_CLASSES  = 4608
		NUM_OPT_BOGI_APPLICABLE_XE_CLASSES  = 10368
		NUM_OPT_BOGI_APPLICABLE_XEI_CLASSES = 1728

		MENU = [
			"BOGI_PXE_CLASS     (# =  2,413)",
			"OPT_BOGI_PXE_CLASS (# =     20)",
			"OPT_BOGI_PE_CLASS  (# =  4,608)",
			"OPT_BOGI_XE_CLASS  (# = 10,368)",
			"OPT_BOGI_XEI_CLASS (# =  1,728)",
			"BEST_OF_EACH_OPT_PXE_CLASS"
			"QUIT"
			]
		
		for m_idx in range(len(MENU)):
			print("%2d - %s"%(m_idx, MENU[m_idx]))
		chosen = int(input("-> "))
		print("[%s] is selected."%(MENU[chosen]))

		if chosen == 6:
			break
		
		if chosen == 0:
			##2,413 BOGI-applicable PXE classes
			BOGI_PXE_CLASS().print_all(range(NUM_BOGI_APPLICABLE_PXE_CLASSES))
		elif chosen == 1:	
			##20   Optimal BOGI-applicable PXE classes(reordered for the paper)
			B = []
			for bidx in range(NUM_OPT_BOGI_APPLICABLE_PXE_CLASSES):
				B.append(OPT_BOGI_PXE_CLASS(bidx))
				print(B[-1])
		elif chosen == 2:
			##4,608 Optimal BOGI-applicable PE  classes
			PE = []
			for bidx in range(NUM_OPT_BOGI_APPLICABLE_PE_CLASSES):
				PE.append(OPT_BOGI_PE_CLASS(bidx))
				print(PE[-1])
				#print(PE[-1].pe_software_code)
		elif chosen == 3:
			##10,368 Optimal BOGI-applicable XE  classes
			XE = []
			for bidx in range(NUM_OPT_BOGI_APPLICABLE_XE_CLASSES):
				XE.append(OPT_BOGI_XE_CLASS(bidx))
				print(XE[-1])
				#print(XE[-1].xe_ddt)
		elif chosen == 4:
			##1,728  Optimal BOGI-applicable XEI  classes
			XEI = []
			for bidx in range(NUM_OPT_BOGI_APPLICABLE_XEI_CLASSES):
				XEI.append(OPT_BOGI_XEI_CLASS(bidx))
				print(XEI[-1])
		elif chosen == 5:
			#### PAPER RESULTS ####
				#TABLE 12(DR LR)
			PXE_DRLR_CONSIDER = [
				#B0/B1
				[( -62.8301 ,  -66.0000 ), ( -62.0000 ,  -68.0000 )],
				#B2/B3
				[( -65.8301 ,  -60.0000 ), ( -62.8301 ,  -70.0000 )],
				#B4/B5
				[( -68.4150 ,  -72.0000 )],
				#B6/B7
				[( -66.8301 ,  -68.0000 ), ( -64.0000 ,  -70.0000 )],
				#B8/B9
				[( -62.4150 ,  -52.0000 ), ( -56.4150 ,  -64.0000 )],
				#B10/B11
				[( -64.0000 ,  -60.0000 ), ( -62.8301 ,  -68.0000 )],
				#B12/B13
				[( -70.0000 ,  -68.0000 )],
				#B14/B15
				[( -66.8301 ,  -60.0000 )],
				#B16/B17
				[( -71.8301 ,  -52.0000 ), ( -68.4150 ,  -70.0000 )],
				#B18/B19
				[( -64.0000 ,  -52.0000 )]
			]

			#TABLE 12(BGC GEC)
			PXE_BGCGEC_CONSIDER = [
				#B0/B1
				[(10.0, 16.66), (11.0, 16.0)],
				#B2/B3
				[(10.0, 16.66), (11.0, 16.0)],
				#B4/B5
				[(11.0, 18.33), (12.0, 18.0)],
				#B6/B7
				[(11.0, 18.33), (12.0, 18.0)],
				#B8/B9
				[(12.0, 20.33), (13.0, 20.0)],
				#B10/B11
				[(11.0, 18.33), (12.0, 18.0)],
				#B12/B13
				[(11.0, 18.33), (12.0, 18.0)],
				#B14/B15
				[(12.0, 19.99), (13.0, 19.33)],
				#B16/B17
				[(12.0, 19.66), (13.0, 19.0)],
				#B18/B19
				[(13.0, 21.33), (14.0, 21.0)],
			]

			for pxe_idx in range(20):
				DRLR = PXE_DRLR_CONSIDER[pxe_idx//2]
				COST = PXE_BGCGEC_CONSIDER[pxe_idx//2]
				RST_DICT = dict()
				print("######################%3d-th pxe class###########################"%pxe_idx)
				for xei_idx in range(__XEI_INTERVAL__[pxe_idx], __XEI_INTERVAL__[pxe_idx + 1]):
					for pe_idx in range(__PE_INTERVAL__[pxe_idx], __PE_INTERVAL__[pxe_idx + 1]):
						R = XEI_PE_INTERSECTION(pxe_idx, xei_idx, pe_idx)
						if R.xeipe_DRLR13_64 in DRLR:
							if (R.xeipe_software, R.xeipe_UMC180nm) in COST:
								KEY = (R.xeipe_DRLR13_64, (R.xeipe_software, R.xeipe_UMC180nm))
								if KEY in RST_DICT.keys():
									for s in R.xeipe_sboxes:
										RST_DICT[KEY].append(s)
								else:
									RST_DICT[KEY] = []
									for s in R.xeipe_sboxes:
										RST_DICT[KEY].append(s)
				for drlr_cost in sorted(RST_DICT.keys()):
					print("#(DR13, LR13)64 : ", drlr_cost[0])
					print("#(BGC, GEC)     : ", drlr_cost[1])
					for s in RST_DICT[drlr_cost]:
						print(s)
				print("#################################################################")	






	

				