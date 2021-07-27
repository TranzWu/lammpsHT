from lammpsHT.collect import Parser

parser = Parser('retrieve.out')

print(parser.Ncolumns)
parser.write()