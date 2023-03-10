
# 通过简单例子学习meshtaichi

## 这个repo干嘛的？

这是一个meshtaichi的简单的教程。仅仅是为了记录我自己学习摸索meshtaichi的过程。这不是官方的教程哦。有错误随时提issue。如果代码对你有帮助，随时抄走。

meshtaichi是最近（22年年底）taichi刚推出的加速有网格拓扑的仿真计算（比如说软体仿真和布料仿真）的工具。大概原理就是让有拓扑相邻的单元的内存读取和访问更快一点，因为保证了memory locality啥的。从而达到了1.4x-6x的加速（官方自己声称的) 。他们还发了个SIGGRAPH。具体的请看他们的 repo: https://github.com/taichi-dev/meshtaichi

注意: 安装的时候，名字是 meshtaichi_patcher 而不是meshtaichi。patcher的意思是补丁。

licences: take-what-ever-you-want

meshtaichi tutorial

## tutorial列表

tut01: 如何导入表面网格和四面体网格？ 导入个三角面兔子和四面体犰狳。[视频讲解](https://www.bilibili.com/video/BV1T54y1P7Ur/?share_source=copy_web&vd_source=ad002c814962fc699cf9d167be8f2bb4)

tut02: 如何导出mesh为ply序列？导出的序列可以读入houdini之类的软件。[视频讲解](https://www.bilibili.com/video/BV1e54y137xq/)

tut03: 从Houdini/tetgen中输入四面体网格。