#!/home/chunzhiw/anaconda3/bin/python
import argparse
import numpy as np
import random

parser = argparse.ArgumentParser()
parser.add_argument("-inp", "--input", help="input file", type=str)
parser.add_argument("-l", "--line", help="string to help target the specific line", type=str)
parser.add_argument("-idx", "--index", help="tell the program the positions of the targeted string to be varied")
parser.add_argument("-n", "--new", help="the values that subsitute the original ones", type=str)
parser.add_argument("-o", "--output", help="The name of the new output file")

argps = parser.parse_args()

#assert statements
assert argps.input, "No input file"
assert argps.line, "No marker to target the line"
assert argps.index, "No index to determine the parameters"
assert argps.new, "No new values"

#get the parameters from the command line
inp = argps.input
marker = argps.line
idx = argps.index.split()
new = argps.new.split()
idx = [int(i) for i in idx]
new = [i if i != "random" else random.randint(0, 9999) for i in new]
#print(new)
assert len(idx) == len(new), "Number of index don't match with number of new values"

if argps.output:
    oup = argps.output
else:
    oup = inp

#print(idx)
with open(inp, 'r') as f:
    rad = f.readlines()

#clean the data and put them in the list
data = [i.split() for i in rad]

#now find the target line
marker_complete = '#@@' + marker
target_line = [idx for idx, ele in enumerate(data) if marker_complete in ele][0]

#print(target_line)

#now change the parameters
n_parm = len(idx)
for i in range(n_parm):
    data[target_line][idx[i]] = new[i]
#print(data[target_line])

#now write the data to the current directory
rad_str = [[str(j) for j in i] for i in data]
rad_str_com = [' '.join(i) for i in rad_str]
with open(oup, 'w') as f:
    for i in rad_str_com:
        f.write(i)
        f.write('\n')

        