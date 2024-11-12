import numpy as np

class RotationPy:
    def __init__(self,
                 *,
                 element: None|list[str] = None,       # 分子所含元素列表 list[str]
                 coordinate: None|list[tuple] = None,  # 分子坐标列表 list[tuple]
                 xyz_file: None|str = None):           # xyz文件路径
    
        if (element != None) and (coordinate != None):
            self._element = element
            self._coordinate = coordinate
            if len(self._element) != len(self._coordinate):
                raise ValueError("len(element) != len(coordinate)")
            
        elif xyz_file != None:
            self._element = []
            self._coordinate = []
            with open(xyz_file, "r", encoding="utf-8") as f:
                atom_n = int(f.readline().strip())
                _ = f.readline()
                for i in range(atom_n):
                    line = f.readline().strip().split()
                    self._element.append(line[0])
                    self._coordinate.append(tuple([float(line[1]), float(line[2]), float(line[3])]))
        else:
            raise ValueError("Parameters Error!!!")
                
        self._rotation_coordinate = None

    @staticmethod
    def _axis_unit(axis: np.ndarray):       # 矢量归一化
        return axis / np.linalg.norm(axis)

    @staticmethod
    def _rotation_matrix(axis: np.ndarray,  # 旋转的轴
                         rad: float):       # 旋转的弧度
        matrix = [[np.cos(rad)+(1-np.cos(rad))*axis[0]*axis[0], \
                   (1-np.cos(rad))*axis[0]*axis[1]-np.sin(rad)*axis[2], \
                   (1-np.cos(rad))*axis[0]*axis[2]+np.sin(rad)*axis[1]],
                  [(1-np.cos(rad))*axis[0]*axis[1]+np.sin(rad)*axis[2], \
                   np.cos(rad)+(1-np.cos(rad))*axis[1]*axis[1], \
                   (1-np.cos(rad))*axis[1]*axis[2]-np.sin(rad)*axis[0]],
                  [(1-np.cos(rad))*axis[0]*axis[2]-np.sin(rad)*axis[1], \
                   (1-np.cos(rad))*axis[1]*axis[2]+np.sin(rad)*axis[0], \
                    np.cos(rad)+(1-np.cos(rad))*axis[2]*axis[2]]]
        
        return matrix

    def rotation(self,
                 rad: float,
                 axis: np.ndarray):
        axis = RotationPy._axis_unit(axis)
        self._rotation_coordinate = []
        for coord in self._coordinate:
            coord_ndarry = np.array(coord)
            coord_rotation_ndarry = np.dot(RotationPy._rotation_matrix(axis, rad), coord_ndarry)
            self._rotation_coordinate.append(tuple([coord_rotation_ndarry[0], \
                                                    coord_rotation_ndarry[1], \
                                                    coord_rotation_ndarry[2]])) 

    def rotation_by_bond(self,
                         rad: float,
                         bond: list):
        vector_1 = np.array(self._coordinate[int(bond[0]-1)])        # 此处原子序号从1开始
        vector_2 = np.array(self._coordinate[int(bond[1]-1)])
        axis = RotationPy._axis_unit(vector_2-vector_1)
        self.rotation(rad, axis)

    @property
    def rotation_coordinate(self):
        if self._rotation_coordinate == None:
            raise ValueError("Please use 'rotation' method firstly!!!")
        else:
            for i in range(len(self._element)):
                print(f"{self._element[i]}: ({self._rotation_coordinate[i][0]:.4f} "
                      f"{self._rotation_coordinate[i][1]:.4f} "
                      f"{self._rotation_coordinate[i][2]:.4f})")

    def write_xyz(self,
                  path: str):
        
        if self._rotation_coordinate == None:
            raise ValueError("Please use 'rotation' method firstly!!!")
        
        with open(path, "w", encoding="utf-8") as f:
            f.write(f"{len(self._element)}\nWritten by RotationPy\n")
            for i in range(len(self._element)):
                f.write(f"{self._element[i]:>5}{self._rotation_coordinate[i][0]:>10.4f}"
                        f"{self._rotation_coordinate[i][1]:>12.4f}"
                        f"{self._rotation_coordinate[i][2]:>12.4f}\n")
                           



