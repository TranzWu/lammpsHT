from lammpsHT.layerParser import Layer

class Parser(Layer):
	def __init__(self, filename):
		self.filename = filename

	@property
	def input(self):
		with open(self.filename, 'r') as f:
			return f.readlines()

	@property
	def Nlayers(self):
		return self.key_value('Nlayers')

	@property
	def is_current_highest(self):
		return self.key_value('is_current_highest')

	@property
	def file_to_read(self):
		for line in self.input:
			if 'file_to_read' in line:
				return line.split()[-1]

	@property
	def Columns(self):
		for line in self.input:
			if 'Columns' in line:
				return self.reformat(line.split('Columns')[-1])



	def split_euqal_sign(self, text):
		return self.reformat(text.split(" = ")[-1])

	@property
	def parameters(self):
		prms = {}
		for i in range(self.Nlayers):
			if i == self.Nlayers - 1 and self.is_current_highest:
				fl = 'run_this.py'
			else:
				fl = f'layer_{i+1}.py'

			with open(fl, 'r') as f:
				rad = f.readlines()

			for line in rad:
				if i == 0:
					if 'N_ensemble' in line:
						p = self.split_euqal_sign(line)
						break
				else:
					if 'line_0_0' in line:
						p = self.split_euqal_sign(line)
						break
			prms[i+1] = p

		return prms

	@property
	def Library(self):
		start = [i for i, l in enumerate(self.input) if 'Library' in l][0] + 1
		end = [i for i, l in enumerate(self.input) if 'End library' in l][0]
		lib = self.input[start:end]
		lib = [self.reformat(l) for l in lib]
		return [l for l in lib if l]

	@property
	def Code(self):
		start = [i for i, l in enumerate(self.input) if 'Code' in l][0] + 1
		end = [i for i, l in enumerate(self.input) if 'End code' in l][0]
		code = self.input[start:end]
		code = [self.reformat(l) for l in code]
		return [l for l in code if l]

	def write_library(self, text):
		text.append('import numpy as np\n')
		text.append('from pandas import DataFrame\n')
		for l in self.Library:
			text.append(f'{l}\n')
		text.append('\n')
		return text

	def write_parameters(self, text):
		for i in range(self.Nlayers):
			text.append(f'layer_{i+1} = {self.parameters[i+1]}\n')

		text.append(f'Columns = {self.Columns}\n')
		text.append(f'DF = DataFrame(columns=Columns)\n')
		text.append('\n')
		return text

	def write_for_loop(self, text):
		b = '    '
		b_max = b * self.Nlayers
		text.append("path = ''\n")
		text.append('df = {}\n')
		for i in range(self.Nlayers):

			if i != self.Nlayers - 1:
				text.append(f'{i*b}for layer{self.Nlayers-i} in range(len(layer_{self.Nlayers - i})):\n')
				l = '{layer' + f'{self.Nlayers-i}' + '}'
				text.append(f"{(i+1)*b}path = path + f'layer{self.Nlayers-i}_{l}/'\n")
				text.append(f"{(i+1)*b}df[Columns[layer{self.Nlayers-i}] = [layer_{self.Nlayers-i}[layer{self.Nlayers-i}]]]\n")
			else:
				text.append(f'{i*b}for layer{self.Nlayers-i} in range(layer_{self.Nlayers - i}):\n')
				l = '{layer' + f'{self.Nlayers-i}' + '}'
				text.append(f"{(i+1)*b}path = path + f'layer{self.Nlayers-i}_{l}/{self.file_to_read}'\n")
				text.append(f"{(i+1)*b}df[Columns[layer{self.Nlayers-i}] = [layer{self.Nlayers-i}]]\n")
		
				text.append(f'{b_max}try:\n')
				for c in self.Code:
					text.append(f'{b_max}{b}{c}\n')

		return text


	def write(self):
		text = []
		text = self.write_library(text)
		text = self.write_parameters(text)
		text = self.write_for_loop(text)

		with open('collect.py', 'w') as f:
			for i in text:
				f.write(i)

