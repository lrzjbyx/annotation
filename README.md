# annotation
数据标注工具


---
#### 使用
```python
python main.py
```
#### 安装
```python
pip install -r requirements.txt
```
#### 配置
> 配置文件在config中
```python
configure = {
    "tag":[
        {
            "label":"矩形标注",
            "color": [255,0,255,100]
        }
        ,
        {
            "label":"圆形标注",
            "color": [0,255,255,100]
        },
        {
            "label": "椭圆标注",
            "color": [255,0,0,100]
        },
        {
            "label": "直线标注",
            "color": [90,10,20,100]
        },
        {
            "label": "圆弧标注",
            "color": [0,0,205,100]
        },
        {
            "label": "椭圆形标注",
            "color": [249,255,100,100]
        },

    ],
    "sequence":["从左到右", "从右到左","从上到下","从下到上"],
    "linked":["上下关联", "左右关联","无关联"],
    "image_format":["bmp","jpg","png","tif","jfif"],
    "align_height":600,
    "align_width":180,
    "cls_model_dir":"model/ch_ppocr_mobile_v2.0_cls_infer",
    "det_model_dir":"model/ch_PP-OCRv3_det_infer",
    "rec_model_dir":"model/ch_PP-OCRv3_rec_infer"
}
```
---
#### 功能
* 矩形多角度标注
* 圆/椭圆多角度标注
* 圆弧/椭圆弧标注
* 曲线文字对齐
* OCR 文字识别


---

#### 截图
![工具](pic/readme.jpg)


----

#### 生成标签注释

> ***标注类型***
```python
circle = 1
line = 2
rectangle = 3
ellipse = 4
circle_arc = 5
ellipse_arc = 6
```
> ***直线***
```python
{
  "group": "组号2",
  "relationship": "无关联",
  "links": [
    {
      "name": "line-0",            # 名称
      "entity": {
        "x": 0.0,
        "y": 0.0,
        # 外接矩形  x,y,w,h  其实x y 都是相对位置  (rect.x+x,rect.y+y) 为真实坐标
        "rect": [
          65.37764350453176, 247.67237763487145, 402.3371585502923,
          9.853302123436833
        ],                              
        "rotation": 349,                # 旋转角度    math.radians(rotation) 转成弧度
        "text": "XXXXXXXXXXXXXXXX",   # 文本
        "type": 2,                   # 标注类型
        "sequence": "从左到右",       #文本读取书顺序
        "l": 402.3371585502923,     #线段的长度
        "h": 58                     #线段的宽度
      }
    }
  ]
}
```
> ***椭圆***
```python
{
  "group": "组号1",
  "relationship": "无关联",
  "links": [
    {
      "name": "ellipse_arc-0",
      "entity": {
        "x": 0.0,
        "y": 0.0,
        "rect": [
          51.89943636773438, 65.65679772002902, 404.97315108015994,
          266.8523162816074
        ],
        "rotation": 351,                # 椭圆弧旋转角度
        "text": "XXXXXXXXXXXXXXXX",
        "type": 6,
        "sequence": "从左到右",           # 文本顺序
        "startAngle": 5616,             # 椭圆弧起始位置
        "spanAngle": 3088,              # 椭圆弧跨度
        "a": 202.48657554007997,        # 椭圆弧长轴
        "b": 133.4261581408037,         # 椭圆弧长轴 
        "h": 89                         # 椭圆宽度
      }
    }
  ]
}
```
> ***圆弧***
```python
{
  "group": "组号1",
  "relationship": "无关联",
  "links": [
    {
      "name": "circle_arc-0",
      "entity": {
        "x": -214.35045317220548,
        "y": -205.28700906344415,
        "rect": [
          253.26586102719034, 242.26586102719034, 149.09365558912373,
          149.09365558912373
        ],
        "rotation": 0,              # 旋转角度
        "text": "XXXXXXXXXXXX",    # 文本标注
        "sequence": "从左到右",      # 文本顺序
        "type": 5,                  # 标注类型
        "startAngle": 4752,         #圆弧开始位置     math.radians(startAngle/16) 转换成 弧度
        "spanAngle": 4480,          #圆弧跨度        math.radians(spanAngle/16) 转换成 弧度
        "r": 74.54682779456186,     # 圆弧半径
        "h": 48                     # 圆弧宽度
      }
    }
  ]
}
```
> ***矩形标注***（圆区域标注、椭圆区域标注类似）
```python
    {
      "x": -184.21450151057402,
      "y": -107.17522658610271,
      "rect": [
        191.14199395770393, 111.3323262839879, 211.85800604229604,
        215.25679758308164
      ],
      "rotation": 0,
      "type": 3,
      "groups": [
        {
          "group": "组号1",
          "relationship": "无关联",
          "links": [
            {
                # 组中 线条、圆弧、椭圆弧标注
            },
            {
                # 组中 线条、圆弧、椭圆弧标注
            }
          ]
        }
      ],
      "raws": []  # 未放到组中的数据
    }
```

---
#### 声明
* 适合数据标注
* 适用于学习、科研
---
#### 联系
* [jackm](jackmca@163.com)
* [ieyqin](ieyqin@gs.zzu.edu.cn)
* [iesqbai](iesqbai@gs.zzu.edu.cn)
* [lhlxr](lhlxr@gs.zzu.edu.cn)
* [wangshiyi](wangshiyi@gs.zzu.edu.cn)


