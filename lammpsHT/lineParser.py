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


	@property
	def parameter(self):
		prms = []
		for line in self.input:
			if 'parameter' in line:
				clean = line.split('parameter')
				if 'random' in clean[1]:
					prms.append(self.reformat(clean[1]))
				else:
					prms.append(eval(self.reformat(clean[1])))
		return prms


	

if __name__ == '__main__':
	inp = ['    Line pressure 1\n',
	 '        index 5\n', 
	 '        parameter [-0.5, -1.0, -1.5, -2, -2.5, -3]  \n', 
	 '\n']
	line = Line(inp)
	print(line.parameter)
