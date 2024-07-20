`Dipangle.tcl`是使用VMD计算离子特定溶剂化层中水分子偶极矩与水分子中O与离子之间连线夹角的余弦值的脚本。

### 使用方法
先采用<a href="https://github.com/luck19990920/gmxoutchg_py" target="_blank">gmxoutchg_py</a>中所述将结构文件对应的电荷信息使VMD读入。然后，若在windows系统下，则将`Dipangle.tcl`放在VMD的安装目录下，若在Linux系统下，则将`Dipangle.tcl`放在结构文件同级目录下。随后，在VMD中输入`source Dipangle.tcl`。最后，输入以下类似的命令得到结果文件`dip.txt`：
``` tcl
Dipangle "resname LI" 3 5
```
上面的命令中，
* `resname LI`为你所要研究的离子，应符合VMD中选择语句的要求
* `3`为溶剂化层中水分子距离的统计下限(单位：埃)
* `5`为溶剂化层中水分子距离的统计上限(单位：埃)

### 注意
* 运行上述脚本前需要使VMD读入原子电荷信息。
* gmx产生的轨迹文件需使用`-pbc mol`处理后才能使用上述脚本。
