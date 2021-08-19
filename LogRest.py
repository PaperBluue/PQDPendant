import os

txt = open(f"{os.getcwd()}/log.txt", mode="w+")
txt.write("2021-8-18--1:27:30\ngifNum img0\npositionX 1800\npositionY 800\nremovable_flag 1\ncheck paperblue\n******")
txt.close()
