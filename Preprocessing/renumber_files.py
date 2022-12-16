# # -*- coding: utf-8 -*-
# """
# Created on Wed Jul 13 23:16:20 2022

# @author: Sanjana_N_Shastry
# """

# importing os module
import os

# Function to rename multiple files
def main():
    folder = 'C://Users//shree//Desktop//data//train//A'
    for count, filename in enumerate(os.listdir(folder)):
            dst = f"{str(count)}.jpg"
            src =f"{folder}/{filename}" # foldername/filename, if .py file is outside folder
            dst =f"{folder}/{dst}"
    		
    		# rename() function will
    		# rename all the files
            os.rename(src, dst)

# Driver Code
if __name__ == '__main__':
	
	# Calling main() function
	main()
