# **PQDPendant**<font color=#005e2a size=3>--PyQt Desktop Pendant 专属于你的屏幕摆件</font>

## 使用介绍
1. 双击 ` PQDPendant.exe` 即可打开
2. 打开后桌面右下角将出现默认gif
3. 左键拖动可更改小人位置
4. 右键可弹出设置框,设置框中
   * `关闭设置` 可关闭设置框
   * `关闭软件` 可关闭程序
   * `锁定` 可锁定摆件现有位置
   * 下拉框 `img0` 可选择已添加的摆件
   * `位置重置` 可用于重置摆件位置
   * 拖动`滑块`可调整摆件大小，滑条末端数字为放大百分比<br>
   上限为500%，下限为20%
5. 添加/删除摆件
   * 可往`img`文件夹中添加新文件夹，命名随意
   * 新文件夹中放置摆件GIF图，并且将GIF图命名为`0.gif`
   * 再次打开软件即可在下拉框 `img0` 可选择已添加的摆件
   * 删除摆件仅需将该摆件gif所在的文件夹删除即可
6. 外部修改摆件log
   * `log.txt`文件中存放了程序正常退出前的设置参数
   * 以下为`log.txt`文件内容示例
     ```
     2021-09-27--09:47:23 
     gifNum img4
     positionX 1886
     positionY 1028
     removable_flag 0
     size_times 77
     pos_x 308
     pos_y 308
     check paperblue
     ******
     ```
     其中，可供修改的有`gifNum`、`positionX`、`positionY`、`removable_flag`、`size_times`<br>
     除了`gifNum`后为为文件夹名外，其余都为整数<br>
     第一行为上一次退出的日期时间<br>
     第二行为选择的摆件文件夹名<br>
     第三四行为摆件上一次退出时的位置，<br>
     第五行为摆件是否可移动，0为不可动，1为可动<br>
     第六行为摆件放大百分比<br>
     第七八行为摆件上次退出时的窗口大小，不建议对此项进行修改！<br>
     第九十行为文件校验<br>
   * 一般来说，若`log.txt`损坏(如异常退出)，将复制`log0.txt`中的初始设置至`log.txt`中<br>
     无需用户二次操作。 <br>
     但若出现log文件丢失、设置栏无法打开的情况下，需用户手动添加或更改log文件<br>
     即在`PQDPendant.exe`所在目录下新建`log.txt`和`log0.txt`，<br>
     并将示例内容复制至`log.txt`和`log0.txt`中。<br>
     注意：`******`后不得有空格或换行
     
