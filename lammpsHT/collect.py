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

	@property
	def Ncolumns(self):
		col = eval(self.Columns)
		return len(col)

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

	@property
	def Data_object(self):
		for line in self.input:
			if 'Data_object' in line:
				return line.split()[-1]

	@property
	def Data_dimension(self):
		return self.key_value('Data_dimension')

	def write_library(self, text):
		text.append('import numpy as np\n')
		text.append('from pandas import DataFrame\n')
		for l in self.Library:
			text.append(f'{l}\n')
		text.append('\n')
		return text

	def write_parameters(self, text):
		sum_jobs = 1
		for i in range(self.Nlayers):
			text.append(f'layer_{i+1} = {self.parameters[i+1]}\n')
			if i == 0:
				sum_jobs = sum_jobs * int(self.parameters[1])
			else:
				sum_jobs = sum_jobs * len(eval(self.parameters[i+1]))

		text.append(f'Columns = {self.Columns}\n')
		text.append(f'DF = DataFrame(columns=Columns)\n')
		text.append(f'total_jobs = {sum_jobs}\n')
		text.append('\n')

		return text

	def write_for_loop(self, text):
		b = '    '
		b_max = b * self.Nlayers
		text.append("path = ''\n")
		text.append('df = {}\n')
		text.append('count = 0\n')
		path = ''
		for i in range(self.Nlayers):

			if i != self.Nlayers - 1:
				text.append(f'{i*b}for layer{self.Nlayers-i} in range(len(layer_{self.Nlayers - i})):\n')
				l = '{layer' + f'{self.Nlayers-i}' + '}'
				path = f'{path}layer{self.Nlayers-i}_{l}/'
				#text.append(f"{(i+1)*b}path = path + f'layer{self.Nlayers-i}_{l}/'\n")
				text.append(f"{(i+1)*b}df[Columns[{i}]] = [layer_{self.Nlayers-i}[layer{self.Nlayers-i}]]\n")
			else:
				text.append(f'{i*b}for layer{self.Nlayers-i} in range(layer_{self.Nlayers - i}):\n')
				l = '{layer' + f'{self.Nlayers-i}' + '}'
				text.append(f"{b_max}path = f'{path}layer1_{l}/{self.file_to_read}'\n")
				text.append(f"{(i+1)*b}df[Columns[{i}]] = [layer{self.Nlayers-i}]\n")
		
				text.append(f'{b_max}try:\n')
				for c in self.Code:
					text.append(f'{b_max}{b}{c}\n')
				if self.Data_dimension == 1:
					text.append(f'{b_max}{b}df[Columns[-1]] = {self.Data_object}\n')
				if self.Data_dimension == 2:
					text.append(f'{b_max}{b}for i in range(len({self.Data_object})):\n')
					text.append(f'{b_max}{b}{b}dff = df.copy()\n')
					text.append(f'{b_max}{b}{b}dff[Columns[-2]] = [i]\n')
					text.append(f'{b_max}{b}{b}dff[Columns[-1]] = [{self.Data_object}[i]]\n')
				text.append(f'{b_max}{b}{b}dff = DataFrame(dff)\n')
				text.append(f'{b_max}{b}{b}DF = DF.append(dff)\n')
				text.append(f'{b_max}{b}count += 1\n')
				text.append(f'{b_max}{b}print(f"current progress: {{count/total_jobs * 100:.2f}}%", end="\\r")\n')
				text.append(f'{b_max}except OSError:\n')
				text.append(f'{b_max}{b}print(f"Cannot open file: {{path}}\\n")\n')
		text.append(f"{b}path = ''\n")
		text.append('DF.to_csv("data", index=False)\n')
		return text


	def write(self):
		text = []
		text = self.write_library(text)
		text = self.write_parameters(text)
		text = self.write_for_loop(text)

		with open('collect.py', 'w') as f:
			for i in text:
				f.write(i)

