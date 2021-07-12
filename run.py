from lammpsHT.parser import Parser



parser = Parser('auto.in')
print(parser.layers[0].write_first_layer())