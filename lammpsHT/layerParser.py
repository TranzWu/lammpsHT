from lammpsHT.lineParser import Line
import pathlib

class Layer():
	def __init__(self, inp, filename):
		self.input = inp
		self.filename = filename

	@property
	def isFirst(self):
		return "N = 1" in self.input[0]

	@property
	def index(self):
		clean = self.input[0].split()
		return clean[2]

	@property
	def N_ensemble(self):
		if self.isFirst:
			line = [i for i in self.input if "N_ensemble" in i]
			clean = line[0].split()
			return int(clean[2])
	
	@property
	def njobs(self):
		for line in self.input:
			if 'njobs' in line:
				clean = line.split()
				return int(clean[2])
	
	@property
	def cores(self):
		for line in self.input:
			if 'cores' in line:
				clean = line.split()
				return int(clean[2])

	

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
			return self.input[start+1: end]
	
	@property
	def post(self):
		if self.isFirst:
			for idx, line in enumerate(self.input):
				if 'POST' in line:
					start = idx
				if 'END post' in line:
					end = idx
			return self.input[start+1: end]
			

	def write_first_layer(self):
		path = str(pathlib.Path(__file__).parent)
		path = f"{path}/template/parallel_template.py"
		with open(path, 'r') as f:
			rad = f.readlines()
		return rad


	def write_to_file(self):
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

