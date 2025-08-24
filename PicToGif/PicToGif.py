import os
from datetime import datetime
from pathlib import Path
import pathlib
import re 
import imageio.v2 as iio
import sys
from tqdm import tqdm

# time_last = os.path.getmtime(os.path.abspath(__file__))

__version__ = "1.0"
__developer__ = "Jian Zhang"
__address__ = "jianzhang1920@gmail.com"
# __release__ = str(datetime.fromtimestamp(time_last).strftime("%Y-%b-%d"))
__release__ = "2025-Aug-23"
__savefile__ = "convert.gif"


file_extension_default = ["bmp"]
file_sort_default = False
fps_default = 5
loop_default = 0

class Pictures:
    """
    多幅图片的类
    """

    def __init__(self, 
                 directory_path:pathlib.Path,
                 file_extension = file_extension_default,
                 file_sort = file_sort_default):
        
        if not directory_path.is_dir():
            raise ValueError(f"{directory_path.absolute()} is not a directory.")
        
        self.directory_path = directory_path
        self.pictures_list = []
        self.file_extension = ["." + file  for file in file_extension]
        self.file_sort = file_sort
        self.file_len = 0
        self.save_file = self.directory_path / __savefile__
        self.read_pictures

    @property
    def read_pictures(self):
        pattern = '|'.join(re.escape(ext) for ext in self.file_extension)
        pattern = f'.*({pattern})$'

        all_files = [file for file in self.directory_path.rglob('*') if re.match(pattern, str(file))]

        for file in all_files:
            self.pictures_list.append(file)

        self.file_len = len(self.pictures_list)


    @property
    def sort_pictures(self):
        if self.file_len == 0:
            self.read_pictures
        self.pictures_list.sort(reverse=self.file_sort)

    @property
    def convert(self):
        self.sort_pictures
        picture_list = [iio.imread(p) for p in self.pictures_list]

        with iio.get_writer(self.save_file, mode="I", fps=fps_default, loop=loop_default) as writer:
            for frame in tqdm(picture_list, desc="Converting"):
                writer.append_data(frame) # type: ignore

        # iio.mimsave(self.save_file, picture_list, fps=fps_default, loop=loop_default)        # type: ignore
        print(f"{__savefile__} has been saved in {self.directory_path.absolute()} sucessfully!")


def Welcome():
    print(f"PicToGif -- A tool to combine multiple images into a gif\n"
          f"Version {__version__}, update data: {__release__}\n"
          f"Developer: {__developer__} ({__address__})\n")
    

def Main_menu():
    global file_extension_default
    global file_sort_default
    global fps_default
    global loop_default
    print(f"0   Extracted file type: {",".join(file_extension_default)}\n"
          f"1   Sort order: {"ascending" if not file_sort_default else "descending"}\n"
          f"2   Frame rate: {fps_default}\n"
          f"3   Number of cycles: {loop_default}\n"
          f"4   Start to convert\n"
          f"q   Exit the program")


def main():
    if len(sys.argv) > 1:
        path = Path(sys.argv[1])
        Welcome()
    else:
        Welcome()
        path = Path(input("Please input file path\n"))

    print(f"{path.absolute()} has been loaded!")
    while 1:
        Main_menu()
        input_index = input()
        if input_index == "0":
            global file_extension_default
            while 1:
                extension_add = input("Please input extension of file. Enter q to exit! For example, png\n")
                if extension_add == "q":
                    break
                else:
                    file_extension_default.append(extension_add)
        elif input_index == "1":
            global file_sort_default
            file_sort_default = not file_sort_default
        elif input_index == "2":
            global fps_default
            fps_default = eval(input("Input frame rate, for example, 5\n"))
        elif input_index == "3":
            global loop_default
            loop_default = eval(input("Input number of cycles. 0 represents an infinite loop\n"))
        elif input_index == "4":
            pic_object = Pictures(path)
            pic_object.convert
        elif input_index == "q":
            break
        else:
            Main_menu()


main()

