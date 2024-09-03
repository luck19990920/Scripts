`accromem`是统计离子跨膜数量的tcl脚本。

### 使用方法
若在windows系统下，将`accromem.tcl`放在VMD的安装目录下，若在Linux系统下，则将`accromem.tcl`放在结构文件同级目录下。随后，在VMD中输入`source accromem.tcl`。最后，输入以下类似的命令回车即可统计离子跨膜数量：
``` tcl
accromem trj.gro trj.xtc z 0 500 "resname LI" "resname MOL" 10 test.txt
```
`accromem`后按照先后顺序有如下的几个参数：

* `file_1`: `gro`文件路径
* `file_2`: `xtc`文件路径
* `direction`: 需要统计的离子的迁移方向，可以是`X/Y/Z/x/y/z`中的任意一个
* `firstFrame`: 开始统计的帧数
* `lastFrame`: 结束统计的帧数
* `ionSelection`：所要研究的离子对应的VMD选择语句
* `membrSelection`: 所要研究的膜体系对应的VMD选择语句
* `skip`: 输出离子通过膜数据到文件中的频率，**可缺省**，默认每一帧输出一次
* `fn`: 输出数据的文件路径，**可缺省**，默认为`result.txt`