## Linux命令
* 本节例举常用Linux命令
```angular2html
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

