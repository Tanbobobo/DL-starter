## Linux命令
* 本节例举常用Linux命令
```angular2html
mkdir: 创建目录
rm -rf：删除目录
rm：删除文件
cat: 浏览文件
cd：切换至目标路径
ls：查看当前目录
df -h：查看硬盘使用量
ps -ef | grep python：列举出运行的python程序
kill -9：以进程号关掉进程
cp -r： 将一个目录下的文件复制至另一个目录 
mv： 将一个目录下的文件复制至另一个目录
nvidia-smi：查看显卡情况
wget: 下载
zip -r：将该目录下的文件打包
unzip：解压.zip文件
```
* vim：文本编辑器
```angular2html
    vim xxx.py
    i # 编辑模式
    Esc # 命令模式
    :a,b d # 删除a至b行
    :a,b < # a至b行向左缩进
    :a,b > # a至b行向右缩进
    :wq #保存并退出
```
命令行调试
```angular2html
    import pdb
    pdb.set_trace()

```

* 命令使用
```angular2html
(base) ***:~$ mkdir happy
(base) ***:~$ cd happy
(base) ***:~/happy$ vim demo.py
(base) ***:~/happy$ ls
demo.py
(base) ***:~/happy$ cp demo.py demo_new.py
(base) ***:~/happy$ ls
demo_new.py  demo.py
(base) ***:~/happy$ mkdir path
(base) ***:~/happy$ cp -r demo_new.py ./path/
(base) ***:~/happy$ cd path/
(base) ***:~/happy/path$ ls
demo_new.py
(base) ***:~/happy/path$ rm demo_new.py
(base) ***:~/happy/path$ cd ..
(base) ***:~/happy$ ls
demo_new.py  demo.py  path
(base) ***:~/happy$ rm -rf path/
(base) ***:~/happy$ df -h
Filesystem      Size  Used Avail Use% Mounted on
udev             63G     0   63G   0% /dev
tmpfs            13G  3.2M   13G   1% /run
/dev/nvme0n1p3  329G   25G  288G   8% /
tmpfs            63G  9.1M   63G   1% /dev/shm
tmpfs           5.0M  4.0K  5.0M   1% /run/lock
tmpfs            63G     0   63G   0% /sys/fs/cgroup
/dev/loop0      128K  128K     0 100% /snap/bare/5
/dev/loop2       56M   56M     0 100% /snap/core18/2246
/dev/loop4       66M   66M     0 100% /snap/gtk-common-themes/1515
/dev/loop5       66M   66M     0 100% /snap/gtk-common-themes/1519
/dev/loop3      219M  219M     0 100% /snap/gnome-3-34-1804/72
/dev/loop6       51M   51M     0 100% /snap/snap-store/547
/dev/nvme0n1p1  476M  5.3M  470M   2% /boot/efi
/dev/sda1       3.6T  2.4T  1.1T  71% /home
tmpfs            13G   28K   13G   1% /run/user/125
tmpfs            13G  4.0K   13G   1% /run/user/1002
/dev/loop7       56M   56M     0 100% /snap/core18/2253
/dev/loop1       43M   43M     0 100% /snap/snapd/14066
/dev/loop9      219M  219M     0 100% /snap/gnome-3-34-1804/77
/dev/loop10      62M   62M     0 100% /snap/core20/1242
/dev/loop11     248M  248M     0 100% /snap/gnome-3-38-2004/87
/dev/loop12      55M   55M     0 100% /snap/snap-store/558
/dev/loop13      62M   62M     0 100% /snap/core20/1270
/dev/loop14      44M   44M     0 100% /snap/snapd/14295
tmpfs            13G  8.0K   13G   1% /run/user/1003
(base) ***:~/happy$ nvidia-smi
Mon Jan  3 14:38:24 2022
+-----------------------------------------------------------------------------+
| NVIDIA-SMI 470.57.02    Driver Version: 470.57.02    CUDA Version: 11.4     |
|-------------------------------+----------------------+----------------------+
| GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
|                               |                      |               MIG M. |
|===============================+======================+======================|
|   0  NVIDIA GeForce ...  On   | 00000000:18:00.0 Off |                  N/A |
| 30%   11C    P8    13W / 350W |   2734MiB / 24268MiB |      0%      Default |
|                               |                      |                  N/A |
+-------------------------------+----------------------+----------------------+
|   1  NVIDIA GeForce ...  On   | 00000000:5E:00.0 Off |                  N/A |
| 30%   11C    P8    15W / 350W |      8MiB / 24268MiB |      0%      Default |
|                               |                      |                  N/A |
+-------------------------------+----------------------+----------------------+

+-----------------------------------------------------------------------------+
| Processes:                                                                  |
|  GPU   GI   CI        PID   Type   Process name                  GPU Memory |
|        ID   ID                                                   Usage      |
|=============================================================================|
|    0   N/A  N/A      1221      C   ./predict                        2726MiB |
|    0   N/A  N/A      1488      G   /usr/lib/xorg/Xorg                  4MiB |
|    1   N/A  N/A      1488      G   /usr/lib/xorg/Xorg                  4MiB |
+-----------------------------------------------------------------------------+
(base) ***:~/happy$ ls
demo_new.py  demo.py
(base) ***:~/happy$ mv demo_new.py demo_old.py
(base) ***:~/happy$ ls
demo_old.py  demo.py
(base) ***:~/happy$ mkdir path
(base) ***:~/happy$ mv demo_old.py ./path/
(base) ***:~/happy$ ls
demo.py  path
(base) ***:~/happy$ cd path/
(base) ***:~/happy/path$ ls
demo_old.py
(base) ***:~/happy/path$ cd ..
(base) ***:~/happy$ ls
demo.py  path
(base) ***:~/happy$ zip -r path.zip ./path/
  adding: path/ (stored 0%)
  adding: path/demo_old.py (stored 0%)
(base) ***:~/happy$ ls
demo.py  path  path.zip
(base) ***:~/happy$ unzip path.zip
Archive:  path.zip
replace path/demo_old.py? [y]es, [n]o, [A]ll, [N]one, [r]ename: y
 extracting: path/demo_old.py
(base) ***:~/happy$ ps -ef | grep python
root        1231       1  0  2021 ?        00:00:00 /usr/bin/python3 /usr/bin/networkd-dispatcher --run-startup-triggers
root        1467       1  0  2021 ?        00:00:00 /usr/bin/python3 /usr/share/unattended-upgrades/unattended-upgrade-shutdown --wait-for-signal
root       88897       1  0  2021 ?        00:00:00 /usr/bin/python3 /usr/lib/ubuntu-release-upgrader/check-new-release -q
gaoy      759311  759139  0 14:43 pts/0    00:00:00 grep --color=auto python
gaoy     2797652       1  0  2021 ?        00:00:02 /home/gaoy/miniconda3/bin/python /home/gaoy/miniconda3/bin/jupyter-notebook --config=/home/gaoy/.jupyter/jupyter_notebook_config.py
(base) ***:~/happy$
```
