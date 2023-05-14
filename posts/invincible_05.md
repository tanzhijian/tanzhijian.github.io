# 阿森纳不败赛季射门探索 01: xG

从 xG 开始。训练一个 xG 的模型方便之后的探索使用

## 预处理数据

由于数据同样出自 Statsbomb，所以数据集使用他们的 opendata，获取 competitions 一共有 43 个赛季的不同性质比赛可以使用，但由于比赛差异，需要去除女子足球的比赛，然后去除阿森纳不败赛季的比赛作为测试集，过滤以后还有 36 个赛季 828 场的比赛可以使用

接下来获取所有的比赛事件，以及随之的跟踪数据事件，有一些需要注意的处理方法:


```python
# 使用 mplsoccer 获取数据，每场比赛事件分别是 events, related, freeze, tactics
events = match[0]
tracks = match[2]

# 获取射门事件
# 把 Statsbomb 的坐标从 120 80 转换为 105 68 是方便之后绘图使用
shots = events.loc[events["type_name"] == "Shot"].copy()
x_formula = lambda x: x * 105 / 120
y_formula = lambda x: x * 68 / 80
shots.x = shots.x.apply(x_formula)
shots.y = shots.y.apply(y_formula)
tracks.x = tracks.x.apply(x_formula)
tracks.y = tracks.y.apply(y_formula)
```

然后过滤掉定位球射门，以及未跟踪守门员的射门以后，还剩下 19174 条射门事件，数据不算大，但可以训练模型了

## 特征提取

如何选择特征呢，既然使用 Statsbomb 的数据，不妨找找他在这方面的资料，于是找到了 Statsbomb 发布的这条推特 https://twitter.com/StatsBomb/status/1650847925197471745 已经有了答案：

> Not all xG is created equal.
>
> StatsBomb's xG model includes:
>
> * the positioning of the goalkeeper
> * the positioning of the surrounding defenders and attackers
> * the height of the ball at the moment the shot is struck

结合推特里面的视频，总结出 Statsbomb 的 xG 主要使用以下特征：

* 射门距离
* 射门角度
* 基础 xg
* 守门员的位置
* 守门员与射门的距离
* 射门是否比守门员更接近球门
* 干扰射门的防守球员
* 射门与球门形成的三角形内防守球员
* 射门与球门形成的三角形内进攻球员
* 射门时球的高度

其中干扰射门的防守球员是一个不好把握的特征，在这里假设射门时球半径 1 米内的防守球员都属于干扰射门

而射门时球的高度在没有具体的数据情况下是个更难的特征，大致原理为球的高度越高，xG 越低，脚射门比较准，而头球在同样距离的情况下更难把握住。Statsbomb 射门事件关于这一项特征 body_part_name 其中只包含了['Right Foot', 'Head', 'Left Foot', 'Other']，所以仍然需要假设。询问 chatgpt，男子足球运动员平均身高为 1.8 米（感觉偏高？），所以假设头球的高度统一为 1.8，脚下射门为 0.01, 其他可以理解为胸口，大腿等非常规部位，为 1.0

由于特征提取是一项不小的工程，所以在 GitHub 创建了一个库 https://github.com/tanzhijian/football_calculator ，如果查看时代码已经修改了，可以回滚到这篇文章写的日期，也就是 2023-05-14

## 训练模型

特征提取完毕以后可以得到一个 (19174, 10) 型状的数据集，开始创建一个神经网络进行训练，由于我并不擅长机器学习，所以随便写了一个先训练着，训练数据集和验证数据集 8:2，然后创建模型：


```python
model = tf.keras.Sequential([
    layers.Dense(10, activation="relu", input_shape=(10,)),
    layers.Dense(10, activation="relu"),
    layers.Dense(1, activation="sigmoid")
])
model.compile(
    optimizer='adam',
    loss="binary_crossentropy", 
    metrics=["accuracy"]
)
history = model.fit(
    X_train, 
    y_train, 
    validation_data=(X_val, y_val),
    batch_size=32, 
    epochs=50,
)
```

测试数据库使用不败赛季的 832 个射门事件


```python
# 计算精确度，召回率和 f1 分数
report = classification_report(y_test, y_pred)
print(report)
```

                  precision    recall  f1-score   support
    
               0       0.92      1.00      0.95       754
               1       0.75      0.12      0.20        78
    
        accuracy                           0.91       832
       macro avg       0.83      0.56      0.58       832
    weighted avg       0.90      0.91      0.88       832
    


分数有点惨，但考虑到数据库大小，推断出的特征，一些乱七八糟的假设，随便设置的神经网络，能有这样也还不错了

接下来计算 xG 并查看


```python
invincible_shots.groupby(["player_name"])["xg"].sum().sort_values(
    ascending=False
)[:5].reset_index()
```




<div>
<table>
  <thead>
    <tr>
      <th></th>
      <th>player_name</th>
      <th>xg</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Thierry Henry</td>
      <td>15.798578</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Robert Pirès</td>
      <td>6.998034</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Fredrik Ljungberg</td>
      <td>4.917759</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Dennis Bergkamp</td>
      <td>4.257910</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Kolo Habib Touré</td>
      <td>3.186363</td>
    </tr>
  </tbody>
</table>
</div>



Statsbomb 数据里面有自带计算完毕的 xG 可以作为标准


```python
invincible_shots.groupby(["player_name"])["shot_statsbomb_xg"].sum().sort_values(
    ascending=False
)[:5].reset_index()
```




<div>
<table>
  <thead>
    <tr>
      <th></th>
      <th>player_name</th>
      <th>shot_statsbomb_xg</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Thierry Henry</td>
      <td>17.330713</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Robert Pirès</td>
      <td>6.959468</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Fredrik Ljungberg</td>
      <td>5.271573</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Dennis Bergkamp</td>
      <td>4.135871</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Patrick Vieira</td>
      <td>3.469172</td>
    </tr>
  </tbody>
</table>
</div>



还是有差异，考虑到上面提到的因素，可以接受

查看一些个别的


```python
invincible_shots[["player_name", "xg", "shot_statsbomb_xg"]].head(10)
```




<div>
<table>
  <thead>
    <tr>
      <th></th>
      <th>player_name</th>
      <th>xg</th>
      <th>shot_statsbomb_xg</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Dennis Bergkamp</td>
      <td>0.153065</td>
      <td>0.193885</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Thierry Henry</td>
      <td>0.032303</td>
      <td>0.007914</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Gilberto Aparecido da Silva</td>
      <td>0.102811</td>
      <td>0.125604</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Paul Butler</td>
      <td>0.085732</td>
      <td>0.065221</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Sulzeer Jeremiah ''Sol' Campbell</td>
      <td>0.044693</td>
      <td>0.043912</td>
    </tr>
    <tr>
      <th>5</th>
      <td>Ioan Viorel Ganea</td>
      <td>0.070132</td>
      <td>0.085242</td>
    </tr>
    <tr>
      <th>6</th>
      <td>Dennis Bergkamp</td>
      <td>0.021920</td>
      <td>0.018803</td>
    </tr>
    <tr>
      <th>7</th>
      <td>Carl Cort</td>
      <td>0.062670</td>
      <td>0.051536</td>
    </tr>
    <tr>
      <th>8</th>
      <td>Ioan Viorel Ganea</td>
      <td>0.229663</td>
      <td>0.256359</td>
    </tr>
    <tr>
      <th>9</th>
      <td>Kenny Miller</td>
      <td>0.044943</td>
      <td>0.027489</td>
    </tr>
  </tbody>
</table>
</div>



暂时可以用，之后时间再来优化了
