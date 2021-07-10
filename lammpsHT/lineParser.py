class Line():
	def __init__(self, input):
		self.input = input

	@property
	def first(self):
		assert('Line' in self.input[0])
		clean = self.input[0].split()
		return clean

	@property
	def identifier(self):
		return self.first[1]

	@property
	def NParameter(self):
		return int(self.first[2])

	@property
	def index(self):
		idx = []
		for line in self.input:
			if 'index' in line:
				clean = line.split()
				idx.append(int(clean[1]))
		return idx

	@property
	def parameter(self):
		prms = []
		for line in self.input:
			if 'parameter' in line:
				clean = line.split('parameter')
				prms.append(clean[1])
		return prms
	

if __name__ == '__main__':
	inp = ['    Line pressure 1\n',
	 '        index 5\n', 
	 '        parameter [-0.5, -1.0, -1.5, -2, -2.5, -3]  \n', 
	 '\n']
	line = Line(inp)
	print(line.index)
