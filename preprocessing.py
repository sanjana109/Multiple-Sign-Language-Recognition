import csv
import os

import cv2
import numpy as np

from image_processing import func

minValue = 70

if not os.path.exists('data2'):
    os.makedirs('data2')
if not os.path.exists('data2/train/'):
    os.makedirs('data2/train')
if not os.path.exists('data2/test'):
    os.makedirs('data2/test')
path = 'train'
path1 = 'data2'
a = ['label']

for i in range(64*64):
    a.append("pixel"+str(i))

#outputLine = a.tolist()


label = 0
var = 0
c1 = 0
c2 = 0

path2 = "D:\\6th SEM\\6th_sem_projects\\AIML\\FInal project demo\\Sign-Language-to-Text-master\\data\\asl_alphabet_train"

print("before processing...")
print((path))

dirnames = os.listdir(path2)
print(dirnames)
for dirname in dirnames:
    print("during processing...")
    print(dirname)
    for (direcpath, direcnames, files) in os.walk(path2+"\\"+dirname):
        if not os.path.exists(path1+"/train/"+dirname):
            os.makedirs(path1+"/train/"+dirname)
        # if not os.path.exists(path1+"/test/"+dirname):
        #    os.makedirs(path1+"/test/"+dirname)
        # num=0.75*len(files)
        # print("#####")
        num = 100000000000000000
        i = 0
        for file in files:
            var += 1
            actual_path = path2+"\\"+dirname+"\\"+file
            actual_path1 = path1+"\\"+"train\\"+dirname+"\\"+file
            # actual_path2=path1+"\\"+"test\\"+dirname+"\\"+file
            img = cv2.imread(actual_path, 0)
            bw_image = func(actual_path)
            if i < num:
                c1 += 1
                cv2.imwrite(actual_path1, bw_image)
            # else:
            c2 += 1
            cv2.imwrite(actual_path1, bw_image)

            i = i+1

    label = label+1
print("after processing...")
print(var)
print(c1)
print(c2)
