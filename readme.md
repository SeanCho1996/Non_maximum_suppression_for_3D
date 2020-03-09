# 非极大抑制算法在3D图像上的实现
## 非极大抑制算法在传统二维图像的原理与应用
请参阅[这篇文章](https://www.jianshu.com/p/742bbcba2794)
## 3D NMS算法的原理
与二维情况下类似，3D NMS的输入仍为一组bounding box的坐标，他们的权重得分以及一个iou阈值。需要注意的是，在二位情况下，对于每个bounding box，需要的两个坐标分别是box左上角的点和右下角的店，但在三维情况下，需要的两个坐标是最前面左下角的点和最后面右上角的点，因为python中的三维坐标系默认如下图所示 </br>
![python axis](https://ibb.co/1GRNFyw)