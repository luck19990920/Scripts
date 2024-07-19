`DipOrient.tcl`是使用VMD计算某种分子的偶极矩与某矢量的余弦值的脚本。
### 使用方法
若在windows系统下，将`DipOrient.tcl`放在VMD的安装目录下，若在Linux系统下，则将`DipOrient.tcl`放在结构文件同级目录下。随后，在VMD中输入`source DipOrient.tcl`。最后，输入以下类似的命令得到结果文件`dipz.txt`：
``` tcl
DipOrient "resname SOL" 0 2000 0 0 1
```
上面的命令中，
* `resname SOL`为你要计算偶极矩的分子，应符合VMD中选择语句的要求
* `0`与`2000`分别为开始和结束统计的帧数
* `0 0 1`为需要统计与偶极矩夹角的矢量
