class GRO:
    def __init__(self, 
                 file_path: str):
        self.file_path = file_path
        self.gro_line = {}       
        self.atom_number = 0
        self.dimension = ""
        self.read_gro

    @staticmethod
    def resname_number_index(s: str):
        index = 0
        while(s[index].isdigit()):
            index += 1
        return index
    
    @property
    def read_gro(self):
        with open(self.file_path, "r", encoding="utf-8") as f:
            _ = f.readline()
            self.atom_number = int(f.readline().strip())
            resname_tmp = None
            resname_index = 0
            for i in range(self.atom_number):
                line_list = f.readline().strip().split()
                if (resname_tmp==None) or (line_list[0]!=resname_tmp): # 新载入一个残基信息
                    resname_index += 1
                    resname_tmp = line_list[0]
                    self.gro_line[resname_index] = [line_list[0][GRO.resname_number_index(line_list[0]):],
                                                    [line_list[1]], 
                                                    [(eval(line_list[3]), eval(line_list[4]), eval(line_list[5]))]]

                else:      # 不载入残基信息
                    self.gro_line[resname_index][1].append(line_list[1])
                    self.gro_line[resname_index][2].append((eval(line_list[3]), eval(line_list[4]), eval(line_list[5])))

            self.dimension = f.readline().strip()

    def replace_resname(self,
                        start: int,     # 从1开始
                        end: int,
                        resname: str):
        for i in range(start, end):
            self.gro_line[i][0] = resname

    def replace_name(self,
                     start: int,     # 从1开始
                     end: int,
                     name: list):
        for i in range(start, end):
            self.gro_line[i][1] = name

    def write_gro(self,
                  file_path: str):
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("Built with modGro.py\n")
            f.write(f"{self.atom_number}\n")
            atom_index = 1
            for i in range(len(self.gro_line)):
                for j in range(len(self.gro_line[i+1][1])):
                    f.write(f"{str(i+1)+self.gro_line[i+1][0]:>8}"
                            f"{self.gro_line[i+1][1][j]:>7}"
                            f"{atom_index:>5}"
                            f"{self.gro_line[i+1][2][j][0]:>8.3f}"
                            f"{self.gro_line[i+1][2][j][1]:>8.3f}"
                            f"{self.gro_line[i+1][2][j][2]:>8.3f}\n")
                    atom_index += 1
            f.write(self.dimension+"\n")

print("modGro: A tool for modifying gro file")
print("Version 1.0, release date: 2024-Nov-27")
print("Programmed by Jian Zhang (jian_zhang@cug.edu.cn)\n")
print("Please input the file path of .gro")
file_path = input()
gro_object = GRO(file_path)
print(f"\nThe number of atoms: {gro_object.atom_number}\n"
      f"The number of residues: {len(gro_object.gro_line)}")
while True:
    print(f"0 Save\n"
        f"1 Change residue name\n"
        f"2 Change atom name")
    input_inf = input().strip()
    match input_inf:
        case "0":
            gro_object.write_gro("./fix.gro")
            break
        case "1":
            start_index = int(input("Please enter the starting value (from 1)"+\
                                " of the serial number of the residue whose name is to be changed.\n"))
            end_index = int(input("Please enter the ending value for the serial number"+\
                                  " of the residue for which the name change is required (not included)\n"))
            change_residue_name = input("Please enter the changed residue name\n").strip()
            gro_object.replace_resname(start_index, end_index, change_residue_name)
        case "2":
            start_index = int(input("Please enter the serial number of the beginning of the residue whose atomic name needs to be changed.\n"))
            end_index = int(input("Please enter the serial number of the ending of the residue whose atomic name needs to be changed.\n"))
            print(f"The number of atoms in these residues: {len(gro_object.gro_line[start_index][1])}\nPlease enter the changed atomic name")
            atom_name_list = []
            for i in range(len(gro_object.gro_line[start_index][1])):
                atom_name_list.append(input().strip())
            gro_object.replace_name(start_index, end_index, atom_name_list)

        case _:
            print("Invalid input")



