import numpy as np
from pandas import DataFrame
from toy_model.three_D import Effusion

layer_1 = 5
layer_2 = [-0.1, -1.0, -1.5, -2, -2.5, -3]
layer_3 = [0, 1, 2, 3, 4]
Columns = ['pressure', 'hole_distance', 'fluid_content', 'random_seed']
DF = DataFrame(columns=Columns)

path = ''
for layer3 in range(len(layer_3)):
    path = path + f'layer3_{layer3}/'
    for layer2 in range(len(layer_2)):
        path = path + f'layer2_{layer2}/'
        for layer1 in range(layer_1):
            path = path + f'layer1_{layer1}/dump.crack'
            try:
                eff = Effusion(f'{path}')
                eff.run()
