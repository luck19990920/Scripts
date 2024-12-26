import argparse
import MDAnalysis as MDA
import warnings
from tqdm import tqdm
import numpy as np

warnings.filterwarnings("ignore")

######################################################### 设置参数 ######################################################################
parser = argparse.ArgumentParser(description="A Python script to calculate  number of ions passing through the membrane in MD by VMD")
parser.add_argument("-top", "--topology", type=str, help="topology file")
parser.add_argument("-tra", "--trajectory", type=str, help="trajectory file")
parser.add_argument("-d", "--direction", type=str, choices=["x", "y", "z"], default="z", help="the direction of ion transport")
parser.add_argument("-b", "--begin", type=int, default=0, help="the index of frames to start the calculation")
parser.add_argument("-e", "--end", type=int, default=-1, help="the index of frames to finish the calculation")
parser.add_argument("-i", "--ion", type=str, help="string of the selection of ions")
parser.add_argument("-m", "--membrane", type=str, help="string of the selection of membrane")
parser.add_argument("-s", "--skip", type=int, default=1, help="the step to calculate")
parser.add_argument("-o", "--output", type=str, default="./data_accro.txt", help="Path to the file where the final data will be saved")

######################################################### 统计 ######################################################################
args = parser.parse_args()
u = MDA.Universe(args.topology, args.trajectory)
membranes = u.select_atoms(args.membrane)
ions = u.select_atoms(args.ion)
demension = ["x", "y", "z"].index(args.direction)
tmp_set = set([])
ls_stage_1 = [0]
ls_stage_2 = [0]
for ts in tqdm(u.trajectory[args.begin:args.end:args.skip]):
    memb_min_coordinate = np.min(membranes.positions[:,demension])
    memb_max_coordinate = np.max(membranes.positions[:,demension])
    ions_coordinate = ions.positions[:,demension]
    ions_in_channel = np.argwhere((ions_coordinate >= memb_min_coordinate) & (ions_coordinate <= memb_max_coordinate))
    ions_in_channel_set = set(ions_in_channel.reshape(-1))
    ls_stage_1.append(len(ions_in_channel_set) - len(tmp_set & ions_in_channel_set) + ls_stage_1[-1])      # 进入孔道的个数
    ls_stage_2.append(len(tmp_set) - len(tmp_set & ions_in_channel_set) + ls_stage_2[-1])                  # 离开孔道的个数
    tmp_set = ions_in_channel_set

np.savetxt(args.output, np.stack((np.arange(len(ls_stage_1[1:])),\
                         np.array(ls_stage_1[1:]),
                         np.array(ls_stage_2[1:]))))


