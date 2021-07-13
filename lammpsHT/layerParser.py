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
		return clean[2]

	def key_value(self, k):
		for line in self.input:
			if k in line:
				clean = line.split()
				return int(clean[1])

	@property
	def N_ensemble(self):
		if self.isFirst:
			return self.key_value('N_ensemble')
	
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
			for idx, line in enumerate(self.input):
				if 'POST' in line:
					start = idx
				if 'END post' in line:
					end = idx
			raw =  self.input[start+1: end]
			return [self.reformat(line) for line in raw]
			
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
				if self.isFirst:
					text.insert(ist, f"cores = {self.cores}\n")
					text.insert(ist, f"N_ensemble = {self.N_ensemble}\n")
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
					text.insert(count_post, f"{b}os.system('{p}')\n")
					count_post += 1
		return text

	def write_code_run(self, raw):
		text = raw[:]

		for idx, line in enumerate(raw):
			if "insert code" in line:
				count_code = idx + 1
				b = '    '
				for l in self.lines:
					for i in range(l.NParameter):

						if self.use_template:
							temp = "{template_path}"
						else:
							temp = ''

						cmd = f'python {temp}change_parameter.py '\
							  f'--input {self.filename} '\
							  f'--line {l.identifier} '\
							  f'--index {l.index[i]} '\
							  f'--new {l.parameter[i]}'
						  
						cmd_wrap = f"{b}os.system('{cmd}')\n"
						text.insert(idx + 1, cmd_wrap)
						count_code += 1
				if self.isFirst:
					lmps_cmd = f'mpirun --oversubscribe '\
							   '-np {cores} '\
							   f'lmp_mpi -in {self.filename} > output.lammps'
					lmps_wrap = f"{b}os.system(f'{lmps_cmd}')"
					text.insert(count_code, lmps_wrap)
		return text

	def write_to_file(self):
		text = self.read_from_template()
		text = self.write_parameters(text)
		if self.isFirst:
			text = self.write_pre(text)
		text = self.write_code_run(text)
		if self.isFirst:
			text = self.write_post(text)
		with open(self.output, 'w') as f:
			for line in text:
				f.write(line)
		return text

	

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

