from lammpsHT.lineParser import Line
import pathlib

class Layer(Line):
	def __init__(self, inp, filename, N_max):
		self.input = inp
		self.filename = filename
		self.N_max = N_max

	@property
	def isFirst(self):
		return "N = 1" in self.input[0]

	@property
	def index(self):
		clean = self.input[0].split()
		return int(clean[2])

	def key_value(self, k):
		for line in self.input:
			if k in line:
				clean = line.split()
				return int(clean[1])

	@property
	def N_ensemble(self):
		if self.isFirst:
			return self.key_value('N_ensemble')
		else:
			return len(self.lines[0].parameter[0])
	
	@property
	def njobs(self):
		return self.key_value('njobs')
	
	@property
	def cores(self):
		return self.key_value('cores')

	@property
	def use_template(self):
		return self.key_value('use_template')

	@property
	def lines(self):
		Lines = []
		start = [idx for idx, line in enumerate(self.input) if "Line" in line]
		end = [idx for idx, line in enumerate(self.input) if "END line" in line]
		assert(len(start) == len(end))
		
		nlines = len(start)

		for i in range(nlines):
			line = self.input[start[i]:end[i]]
			line = Line(line)
			Lines.append(line)
		return Lines
		
	@property
	def Nlines(self):
		return len(self.lines)

	@property
	def pre(self):
		if self.isFirst:
			for idx, line in enumerate(self.input):
				if 'PRE' in line:
					start = idx
				if 'END pre' in line:
					end = idx
			raw = self.input[start+1: end]
			return [self.reformat(line) for line in raw]
		else:
			return []
	
	@property
	def post(self):
		if self.isFirst:

			return []
		else:
			return [f'python layer_{self.index - 1}.py']
			
	@property
	def template_path(self):
		path = str(pathlib.Path(__file__).parent)
		return f"{path}/template/"

	@property
	def output(self):
		if self.index == self.N_max:
			return "run_this.py"
		else:
			return f"layer_{self.index}.py"

	def read_from_template(self):
		path = f"{self.template_path}parallel_template.py"
		with open(path, 'r') as f:
			rad = f.readlines()
		return rad

	def write_parameters(self, raw):
		text = raw[:]
		for idx, line in enumerate(raw):
			ist = idx + 1
			if "insert parameters" in line:
				text.insert(ist, f"njobs = {self.njobs}\n")
				text.insert(ist, f"N_ensemble = {self.N_ensemble}\n")
				if self.isFirst:
					text.insert(ist, f"cores = {self.cores}\n")
				else:
					for i, line in enumerate(self.lines):
						for ii, prm in enumerate(line.parameter):
							text.insert(ist, f"line_{i}_{ii} = {prm}\n")
							ist += 1

				if self.use_template:
					text.insert(ist, f"template_path = {self.template_path}\n")
		return text

	def write_pre(self, text):
		raw = text[:]
		for idx, line in enumerate(raw):	
			if "insert pretreatment" in line:
				count_pre = idx + 1
				for p in self.pre:
					text.insert(count_pre, f"os.system('{p}')\n")
					count_pre += 1
		return text

	def write_post(self, text):
		raw = text[:]
		b = "    "
		for idx, line in enumerate(raw):	
			if "insert post" in line:
				count_post = idx + 1
				for p in self.post:
					text.insert(count_post, f"{b}os.system(f'{p}')\n")
					count_post += 1
				
				text.insert(count_post, f"{b}os.chdir('..')\n")
		return text

	def write_preheat(self, raw):
		text = raw[:]
		b = '    '
		for idx, line in enumerate(raw):
			if 'insert preheat' in line:
				count_heat = idx + 1
				text.insert(count_heat, f"{b}os.system(f'mkdir layer{self.index}_{{k}}')\n")
				count_heat += 1
				text.insert(count_heat, f"{b}os.system(f'cp {self.filename} layer_* run_this* layer{self.index}_{{k}}')\n")
				count_heat += 1
				text.insert(count_heat, f"{b}os.chdir(f'layer{self.index}_{{k}}')\n")
		return text

	def write_code_run(self, raw):
		text = raw[:]

		for idx, line in enumerate(raw):
			if "insert code" in line:
				count_code = idx + 1
				b = '    '
				for ii, l in enumerate(self.lines):
					for i in range(l.NParameter):

						if self.use_template:
							temp = "python {template_path}"
						else:
							temp = ''

						if self.isFirst:
							new_prm = f"'{l.parameter[i]}'"
						else:
							new_prm = f"line_{ii}_{i}[k]"

						new_var = f"{b}l_{ii}_{i}"

						text.insert(count_code, f"{new_var} = {new_prm}\n")
						count_code += 1
						new_str = '{' + f'l_{ii}_{i}' + '}'
						cmd = f'{temp}change_parameter.py '\
							  f'--input {self.filename} '\
							  f'--line {l.identifier} '\
							  f'--index {l.index[i]} '\
							  f'--new {new_str}'
						cmd_wrap = f"{b}os.system(f'{cmd}')\n"
						text.insert(count_code, f'{cmd_wrap}')
						count_code += 1

				if self.isFirst:
					lmps_cmd = f'mpirun --oversubscribe '\
							   '-np {cores} '\
							   f'lmp_mpi -in {self.filename} > output.lammps'
					lmps_wrap = f"{b}os.system(f'{lmps_cmd}')"
					text.insert(count_code, f'{lmps_wrap}\n')
		return text

	def write_to_file(self):
		text = self.read_from_template()
		text = self.write_parameters(text)
		text = self.write_preheat(text)
		text = self.write_code_run(text)
		text = self.write_post(text)
		with open(self.output, 'w') as f:
			for line in text:
				f.write(line)
		return 

	

if __name__ == '__main__':

	inp = ['N = 1 START\n', '\n', 'N_ensemble = 6\n',
	'    Line pressure 1\n', 
	'        index 5\n', 
	'        parameter [-0.5, -1.0, -1.5, -2, -2.5, -3]  \n', 
	'\n', 
	'    END line\n', 
	'\n']

	layer =  Layer(inp)
	print(layer.Nlines)

