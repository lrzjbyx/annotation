# annotation
数据标注工具


---
#### 使用
```python
python main.py
```


---
#### 功能
* 矩形多角度标注
* 圆/椭圆多角度标注
* 圆弧/椭圆弧标注

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
> ***矩形标注***
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
      "raws": []
    }
```

---
#### 声明
* 适合数据标注使用

---
#### 联系
> jackmca@163.com




