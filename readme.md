# 非极大抑制算法在3D图像上的实现
## 非极大抑制算法在传统二维图像的原理与应用
请参阅[这篇文章](https://www.jianshu.com/p/742bbcba2794)
## 3D NMS算法的实现
### 对算法的理解
以目标检测为例，YOLO，R-CNN等算法通常会生成包含目标的多个大小形状不同的bounding box，对于一个目标，这些bounding box会大量重叠，影响后续的判断和处理，NMS算法实现的功能就是找到置信度最高的bounding box，删除冗余的候选框。
### 算法流程
算法的基本流程为：</br>
1. 计算所有bounding box的体积</br>
2. 根据置信度得分，将bounding box进行排序</br>
3. 选择置信度最高的bounding box，添加到最终输出列表中</br>
4. 计算置信度最高的bounding box与其它候选框的重叠部分的体积</br>
5. 从bounding box列表中删除IoU大于或等于阈值的bounding box（包含置信度最大的bounding box本身）</br>
6. 重复过程3~5，直至剩余bounding box列表为空。
### 输入变量
与二维情况下类似，3D NMS的输入仍为bounding box的坐标的list，他们的权重得分以及一个iou阈值。需要注意的是，在二维情况下，对于每个bounding box，需要的两个坐标分别是box左上角的点和右下角的店，但在三维情况下，需要的两个坐标是最前面左下角的点和最后面右上角的点，因为python中的三维坐标系默认如下图所示 </br>
![python axis](https://i.ibb.co/VYMGfnP/python-axis.png) </br>
可见在坐标系中靠左，靠下，靠前的点是三维坐标较小的点，所以对于一组bounding box，由两个点，6个数组成。权重得分对应于每个bounding box的置信度，iou阈值对应重叠面积占总面积的比例的舍弃阈值。</br>
### 输出
算法返回两个list，一个是已删除冗余的bounding box列表，另一个是各结果bounding box对应的置信度得分
## 测试
**test.py**文件中测试了nms_3d算法的效果，结果如下图所示
![result](https://i.ibb.co/Trz6cCf/result.png)</br>
左侧的图片中我们绘制了一大一小两个球形（蓝色）作为目标，对于大的球，假设我们得到了三个bounding box，对应图中的红黄绿三个框，他们对应的置信度分别为0.9，0.7，0.8，由于这三个框高度重合，我们希望删除黄色和绿色两个置信度相对较低的框，仅保留红色置信度0.9的框。再回到左下角的小球，由于它距离大球较远而且尺度较小，它的bounding box与我们期待保留的红色置信度0.9的大框并不重合，所以经过我们的nms_3d算法，我们应该最终得到一大一小两个红色的框，删除其余所有的候选框。</br>
右侧的图片是我们的结果，可见仅保留了我们期待的两个框。（如果我们想要保留更多的候选框，只需要调大iou阈值，这样每次迭代只会删除很少部分的框）
## 更多的测试
在**test.py**文件中，只需要修改bb1-bb4的参数（前三个值对应最前面左下角的坐标，后三个对应最后面右上角的坐标）即可调整各bounding box的大小和位置，也可以修改他们的阈值（保存在scores变量中），也可以直接复制bb1-bb4的格式添加更多候选框。文件中还提供了绘制球和长方体框架的函数，对应的参数在文件中已有介绍。使用时可以直接运行**test.py**。
## 基于C++的实现
在`./nms_cpp/nms_cpp`文件夹中有nms_3d算法的C++实现，其基本思路与上文完全一致，生成的`pyd`文件在`./nms_cpp/x64/Debug`文件夹中，使用时将该路径添加到python任务路径并直接
```python
import nms_cpp
bb_score = nms_cpp.nms_3d(bbs, scores, iou_threshold)
```
即可使用，简单的测试程序在文件**text_cpp.py**中实现。
