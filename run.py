from lammpsHT.parser import Parser
import sys

parser = Parser(f"auto.in")
parser.write_all()