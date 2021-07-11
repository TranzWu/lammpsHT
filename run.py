from lammpsHT.parser import Parser



parser = Parser('auto.in')
print(parser.layers[1].lines[0].identifier)