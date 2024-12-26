`modGro`是用于修改`GROMACS`中的`gro`文件的工具。`modGro.py`是`modGro`的Python源代码，`modGro.cpp`是`modGro`的C++源代码，`modGro.exe`是`modGro.cpp`编译后得到的Windows可执行文件，`modGro`是`modGro.cpp`编译后得到的Linux可执行文件 <br>

### 使用方法
运行`modGro.exe`后可以看到如下的内容：
```
modGro: A tool for modifying gro file
Version 1.0, release date: 2024-Dec-4
Programmed by Jian Zhang (jian_zhang@cug.edu.cn)

Please input the file path of .gro
```
此时，将需要处理的`gro`文件直接拉进窗口后，回车即可。可看到如下的内容：
```
The number of atoms: 2716
The number of residues: 916

MOL: 916

0 Save
1 Change residue name
2 Change atom name
```
上述的内容表明，该`gro`文件中含有2716个原子，含有916个残基。并且916个残基的残基名都为`MOL`
* 若键入`0`:将最新的`gro`文件内容输出至目录下的`fix.gro`中
* 若键入`1`:则输入需要修改残基名的残基的开始和结束的序号(从1开始)和需要修改成的名字
* 若键入`2`:则输入需要修改原子名的残基的开始和结束的序号(从1开始)和需要修改成的原子名

### 示例
更改前的.gro文件的部分内容如下：
```
Built with Packmol
 2716
    1MOL     OW    1   2.064   0.915   1.100
    1MOL      H    2   2.130   0.867   1.024
    1MOL      H    3   2.090   1.023   1.109
    2MOL     OW    4   1.165   1.983   1.082
    2MOL      H    5   1.159   1.989   1.192
    2MOL      H    6   1.207   1.885   1.053
    3MOL     OW    7   1.339   1.106   0.014
    3MOL      H    8   1.390   1.040   0.087
    3MOL      H    9   1.234   1.121   0.045
    4MOL     OW   10   1.298   2.785   0.049
    4MOL      H   11   1.406   2.769   0.072
    4MOL      H   12   1.257   2.694   0.001
    5MOL     OW   13   2.846   0.950   0.351
    5MOL      H   14   2.785   1.019   0.412
    5MOL      H   15   2.891   1.005   0.266
    6MOL     OW   16   2.592   2.361   0.095
    6MOL      H   17   2.667   2.360   0.014
    6MOL      H   18   2.563   2.465   0.119
```
`modGro`载入上述的文件后，输入以下的内容(`//`后的内容是注释)
```
1          // 修改残基名
1          // 从1号残基开始修改
5          // 修改到6号(不包括)残基
SOL        // 将残基名修改为SOL
2          // 修改原子名
1          // 从1号残基开始修改
1          // 修改到2号(不包括)残基
test1      // 第一个原子的原子名
test2      // 第二个原子的原子名
test3      // 第三个原子的原子名
0          // 保存
```
修改后得到的`fix.gro`的部分内容如下：
```
Built with modGro.py
2716
    1SOL  test1    1   2.064   0.915   1.100
    1SOL  test2    2   2.130   0.867   1.024
    1SOL  test3    3   2.090   1.023   1.109
    2SOL     OW    4   1.165   1.983   1.082
    2SOL      H    5   1.159   1.989   1.192
    2SOL      H    6   1.207   1.885   1.053
    3SOL     OW    7   1.339   1.106   0.014
    3SOL      H    8   1.390   1.040   0.087
    3SOL      H    9   1.234   1.121   0.045
    4SOL     OW   10   1.298   2.785   0.049
    4SOL      H   11   1.406   2.769   0.072
    4SOL      H   12   1.257   2.694   0.001
    5SOL     OW   13   2.846   0.950   0.351
    5SOL      H   14   2.785   1.019   0.412
    5SOL      H   15   2.891   1.005   0.266
    6MOL     OW   16   2.592   2.361   0.095
    6MOL      H   17   2.667   2.360   0.014
    6MOL      H   18   2.563   2.465   0.119
```
### 更新日志
* [2024-Dec-26] 修复了某些bug，增加了`q`选项。