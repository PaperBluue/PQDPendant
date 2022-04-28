import os


def a():
    txt = open(f"{os.getcwd()}/save1.txt", mode="w+")
    txt.write(
        "2022-04-28--22:07:00\ngifNum img2\npositionX 0\npositionY 207\nremovable_flag 0\nsize_times 100\npos_x 400\npos_y 400\n******")
    txt.close()
    txt = open(f"{os.getcwd()}/pdsStatus.txt", mode="w+")
    txt.write("2022-04-28--22:40:14\npdName save1\npdLog save1.txt\n")
    txt.close()
