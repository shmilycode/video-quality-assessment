### 环境

python3 及本代码引用的子模块:

``` shell
pip3 install numpy opencv-python pyzbar scikit-image qrcode pillow
```

还是其他这里没提到，但你可以会出现的报错，本人已经和谷歌通过信了，保证你的所有问题都可以通过谷歌搜索解决。

### 为视频添加二维码标签

为YUV视频逐帧添加标签，标签信息从0开始，到全部帧都加上信息为止，逐帧加1，生成的二维码处于图像左上角，大小为 `150x150`。

```python
python3 qrhandler.py --videoname /mnt/f/code/video_set/sport.yuv --dimension 1280x720 --format I420
```

#### 参数：

videoname: 需要进行处理的视频名称，现只支持YUV格式视频文件

dimension: 视频尺寸参数，如 "1280x720"

format: 视频颜色格式，现只支持 "I420"

#### 输出：

与输入文件处于相同目录下，名称为输入文件名称加 `.out` 后缀，如输入 `test.yuv`，则生成成功后为 `test.yuv.out`

在得到输出文件后，将文件用于压缩变换或传输，后得到损坏的视频，就可以进行下一步的视频质量评估。

### 视频质量评估

将两个视频进行对比评估，得出PSNR分数和帧率变化曲线。

```python
python3 assess.py --input args.json
```

### 参数

input: 包含所有输入参数的文件，文件中包含的信息主要如下：

    raw_videos: 用于对比的原视频，一般是没有经过压缩或传输的效果较好的视频

    test_videos: 测试视频，一般是经过压缩或传输后的视频，信息有损坏，需要与原视频进行对比得出分析结果

    framerate: 原视频帧率，不是测试视频的帧率，因为测试视频可能由于丢帧等因素，导致帧率较低

    dimension: 视频尺寸参数，原视频和测试视频的尺寸应该是完全相同的,

    color_format: 视频颜色参数，原视频和测试视频相同，只支持 "I420"
    
    duration: 原视频在固定帧率下的播放时长

    titles: 每个结果的标题

### 如何获得一个可用的YUV视频源

使用ffmpeg可以轻松对屏幕进行录制，以生成指定的YUV文件，

ubuntu 下使用命令:

``` shell
ffmpeg -f x11grab -t 20 -r 15 -s 1280x720 -i :0.0+0,200  -pix_fmt yuv420p out.yuv
```

windows下使用命令：
``` shell
ffmpeg -f gdigrab -framerate 15 -offset_x 0 -offset_y 200 -video_size 1280x720 -i desktop  -pix_fmt yuv420p out.yuv
```

以上命令会进行桌面录制，并生成一个帧率为15，分辨率为1280x720，时长为20秒，录制位置从桌面（0，200）坐标开始的 `YUV420p` 的视频。如果需要验证录制的视频是否可用，可以使用ffplay进行播放：

```shell
ffplay -f rawvideo -video_size 1280*720 out.yuv 
```