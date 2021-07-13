from lammpsHT.parser import Parser



parser = Parser('auto.in')
print(parser.layers[1].write_to_file())