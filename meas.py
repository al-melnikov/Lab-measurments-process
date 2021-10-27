import os
import matplotlib.pyplot as plt
import pandas as pd



ROOT = f'/home/alexander/Documents/Measurments/Measurments_2021/211026/data/'
IMAGE_ROOT = f'/home/alexander/Documents/Measurments/Measurments_2021/211026/Images/'
TEST_FILE = f'/home/alexander/Documents/Measurments/Measurments_2021/211026/data/seq3/211026_1636/2_Vsd_f_004.csv'

def V_type(path):
    filename = os.path.basename(path)
    return filename.split('_')[1]


def transistor_number(path):
    filename = os.path.basename(path)
    return filename.split('_')[0]


def substrate_number(path):
    foldername = os.path.split( os.path.split(path)[0] )[0]
    return foldername[-1]


def gate_voltage(path):
    fline = open(path, 'r').readline().rstrip()
    return float(fline.split(' ')[-1])


def sd_voltage(path):
    fline = open(path, 'r').readline().rstrip()
    return float(fline.split(' ')[-1])


def meas_direction(path):
    filename = os.path.basename(path)
    return filename.split('_')[2]



def read_data(path):
    file = open(path, 'r')
    x = []
    y = []
    for i, line in enumerate(file):
        if i>4:
            p = line.split(',')
            x.append(float(p[0]))
            y.append(float(p[1]))
    file.close()
    return x, y


def data_frame(root, files):
    V_types = []
    substrate_numbers = []
    transistor_numbers = []
    paths = []
    directions = []
    for file in files:
        filename = os.path.join(root, file)
        paths.append(filename)
        V_types.append(V_type(filename))
        substrate_numbers.append(substrate_number(filename))
        transistor_numbers.append(transistor_number(filename))
        directions.append(meas_direction(filename))
    constructor_list = [substrate_numbers, transistor_numbers, V_types, paths, directions]
    df = pd.DataFrame(constructor_list, index=['substrate', 'transistor', 'V_type', 'path', 'direction']).T
    return df




for (root, dirs, files) in os.walk(ROOT, topdown = True):
    df = data_frame(root, files)
    grouped = df.groupby(['substrate', 'transistor']).agg({'path':'unique'})
    grouped = grouped.reset_index()
    grouped.head()
    for item in range(0, grouped.shape[0]):
            print(grouped.loc[[item]])
            x = []
            y = []
            fig, ax = plt.subplots(figsize=(10, 6))
            plt.xlabel("$U_{sd}, V$", fontsize=12)
            plt.ylabel("$I_{sd}, A$", fontsize=12)
            for i, path in enumerate(grouped['path'][item]):
                grouped['path'][item].sort()
                if V_type(grouped['path'][item][i]) == 'Vsd' and meas_direction(grouped['path'][item][i]) == 'f':
                    x, y = read_data(path)
                    voltage = round(gate_voltage(path))
                    label = f'$U_g = {voltage}V$'
                    ax.scatter(x, y, label=label, linewidth=0.05, s=15)
                    ax.plot(x, y, linewidth=0.6)
                    print(voltage)
            ax.legend(loc='best', framealpha=0.4)
            ax.grid(True)
            title = 'substrate ' + str(grouped['substrate'][item]) \
                         + ', transistor ' + str(grouped['transistor'][item])
            fig.suptitle(title, fontsize = 16)
            filename = IMAGE_ROOT + title.replace(' ', '_') + '.png'
            plt.savefig(filename, dpi=400)
            #plt.show()
            print(title)

