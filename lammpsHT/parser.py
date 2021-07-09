from layerParser import Layer


class Parser():
	def __init__(self, file):
		self.input = file

	@property
	def text(self):
		with open(self.input, 'r') as f:
			return f.readlines()
    
	@property
	def Nlayers(self):
		for line in self.text:
			if "N_layers" in line:
				clean = line.split()
				return int(clean[1])
	
	@property
	def layers(self):
		Layers = []
		start = [idx for idx, line in enumerate(self.text) if "START" in line]
		end = [idx for idx, line in enumerate(self.text) if "END layer" in line]

		assert(len(start) == self.Nlayers)
		assert(len(end) == self.Nlayers)

		for i in range(self.Nlayers):
			layer = self.text[start[i]:end[i]]

		return layer




if __name__ == '__main__':
	parser = Parser('auto.in')
	print(parser.layers)