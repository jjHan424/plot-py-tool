import imageio
import os
dir = r"E:\1Master_2\3-IUGG\Result_Server\Heat_Save\2021310_GEC"

file_name = os.listdir(dir)
frame = []
for cur_file in file_name:
    frame.append(imageio.imread(os.path.join(dir,cur_file)))
    print(cur_file)
imageio.mimsave(os.path.join(dir,"EPN_GER_2021310.gif"),frame,'GIF',duration = 200)