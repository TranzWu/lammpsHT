from lammpsHT.lineParser import Line

class Layer():
	def __init__(self, inp):
		self.input = inp

	@property
	def isFirst(self):
		return "N = 1" in self.input[0]

	@property
	def N_ensemble(self):
		if self.isFirst:
			line = [i for i in self.input if "N_ensemble" in i]
			clean = line[0].split()
			return int(clean[-1])
	
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

	def clean_indentation(self, raw):
		assert(type(raw) == str)
		#count how many times ' ' appear before
		count = 0
		for i in raw:
			if i == ' ':
				count += 1
			else:
				break
		return raw.replace(' ', '', count)

	
	def clean_blanks(self, raw):
		assert(type(raw) == str)
		idx = 0
		l = len(raw)
		for i in range(1, l+1):
			if raw[-i] == '\n' or raw[-i] == ' ':
				idx -= 1
			else:
				break
		if idx:
			return raw[:idx]
		else:
			return raw[:]

	def reformat(self, raw):
		return self.clean_blanks(self.clean_indentation(raw))


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

