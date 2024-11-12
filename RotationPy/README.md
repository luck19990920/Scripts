`RotationPy`类是用于对分子进行旋转的类。相关解释如下。
*Class* RotationPy(*, *element*=*None*, *coordinate*=*None*, *xyz_file*=*None*) <br>
参数解释：<br>
* *element*(*None*, *list[str]*): 分子中原子名列表, 若为*None*，则直接从`xyz`文件中提取 
* *coordinate*(*None*, *list[tuple]*): 分子中原子的坐标列表, 若为*None*，则直接从`xyz`文件中提取
* *xyz_file*(*None*, *str*): `xyz`文件路径
  
注意：上述参数均为关键词参数。此外，若*element*, *coordinate*与*xyz_file*均不为*None*, 则以*element*, *coordinate*中的数据为准。若提供*xyz_file*，则可以不提供*element*和*coordinate*。

方法：<br>
* *rotation*(*rad*, *axis*): 将分子整体绕着轴*axis*旋转*rad*弧度。其中，*rad*为*float*类型，*axis*为*numpy.ndarry*类型 <br>
  旋转后的结果可通过*rotation_coordinate*属性获得
* *rotation_by_bond*(*rad*, *bond*)：将分子绕着键*bond*旋转*rad*弧度。其中，*rad*为*float*类型，*bond*为*list*，其中为键两端的原子序号(从1开始) <br>
  旋转后的结果可通过*rotation_coordinate*属性获得
* *write_xyz*(*path*)：将旋转后的分子坐标写入`xyz`文件中，写入的`xyz`文件路径为*path* <br>
  调用该方法前需先调用*rotation*或*rotation_by_bond*方法

属性：<br>
* *rotation_coordinate*：打印出完成旋转后的分子坐标信息。调用此属性前需先执行*rotation*或*rotation_by_bond*方法

实例：
```python
import numpy as np

H2O = RotationPy("D:/python_case/Scripts/RotationPy/H2O.xyz")
H2O.rotation(np.pi/2, np.array([0, 0, 1]))
H2O.write_xyz("D:/python_case/Scripts/RotationPy/H2O_rotation.xyz")
```

  