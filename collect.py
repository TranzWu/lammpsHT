import numpy as np
from pandas import DataFrame
from toy_model.three_D import Effusion

layer_1 = 10
layer_2 = [200, 400, 600, 800, 1000, 1200, 1400, 1600, 1800, 2000]
layer_3 = [5, 7, 9, 11, 13, 15, 17, 19]
layer_4 = [-5, -7, -9]
Columns = ['pressure', 'hole_distance', 'fluid_content', 'random_seed', 'timestep', 'weight_loss']
DF = DataFrame(columns=Columns)
total_jobs = 2400

path = ''
df = {}
count = 0
for layer4 in range(len(layer_4)):
    df[Columns[0]] = [layer_4[layer4]]
    for layer3 in range(len(layer_3)):
        df[Columns[1]] = [layer_3[layer3]]
        for layer2 in range(len(layer_2)):
            df[Columns[2]] = [layer_2[layer2]]
            for layer1 in range(layer_1):
                path = f'layer4_{layer4}/layer3_{layer3}/layer2_{layer2}/layer1_{layer1}/dump.crack'
                df[Columns[3]] = [layer1]
                try:
                    eff = Effusion(f'{path}')
                    eff.run()
                    df[Columns[-1]] = [eff.effusion_rate]
                    dff = df.copy()
                    dff = DataFrame(dff)
                    DF = DF.append(dff)
                    count += 1
                    print(f"current progress: {count/total_jobs * 100:.2f}%", end="\r")
                except OSError:
                    print(f"Cannot open file: {path}\n")
    path = ''
DF.to_csv("data", index=False)
