# 阿森纳不败赛季传球路线图探索 02

上篇文章选取了其中一场的比赛，其主力阵容除了右边前卫帕洛尔，其余都是不败赛季夺冠的常规主力，这次的探索目标为整个赛季的所有比赛，作为常规主力的十一人传球路线图

首先是获取 38 场比赛的数据集

## import


```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mplsoccer import Pitch, Sbopen
```


```python
# 获取所有比赛的 id
parser = Sbopen()
matches = parser.match(competition_id=2, season_id=44)
```


```python
# 获取所有比赛的事件数据集
events = []
for match_id in matches['match_id']:
    data = parser.event(match_id)
    # data[0] 为 event
    events.append(data[0])
```

## 获取需要的数据

现在需要找到首发 11 人的 player_id, 这一步手动来完成了，也就是上一篇文章的首发阵容 id，然后把帕洛尔换成永贝里


```python
invincible_11 = [
    20015,
    40222, 38412, 15637, 12529,
    15754, 40221, 15515, 19312,
    15042, 15516,
]
```


```python
# 手动获取一场全部 11 人阵容的比赛
lineup = parser.lineup(3749257)
invincible_11 = pd.merge(
    pd.DataFrame({'player_id': invincible_11}),
    lineup[['player_id', 'player_nickname',]],
    on='player_id'
)
```

接下来设置过滤条件，和上一篇文章差不多：

1. 对手的事件
2. 失败的传球
3. 传球队员与接球队员是否 invincible_11


```python
def mask(events):
    _filter = (
    events.type_name == 'Pass') & (
    events.team_name == "Arsenal") & (
    events.player_id.isin(invincible_11.player_id)) & (
    events.pass_recipient_id.isin(invincible_11.player_id)) & (
    events.outcome_name.isnull())
    
    passes = events.loc[_filter, [
        'x', 'y', 'end_x', 'end_y',
        'player_id', 'player_name', 'pass_recipient_name', 'pass_recipient_id'
    ]]
    return passes
```


```python
passes = pd.concat([mask(event) for event in events])
```


```python
passes = passes.reset_index()
passes.head()
```




<div>
<table>
  <thead>
    <tr>
      <th></th>
      <th>index</th>
      <th>x</th>
      <th>y</th>
      <th>end_x</th>
      <th>end_y</th>
      <th>player_id</th>
      <th>player_name</th>
      <th>pass_recipient_name</th>
      <th>pass_recipient_id</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>4</td>
      <td>61.0</td>
      <td>40.1</td>
      <td>61.4</td>
      <td>43.6</td>
      <td>15516.0</td>
      <td>Thierry Henry</td>
      <td>Dennis Bergkamp</td>
      <td>15042.0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>12</td>
      <td>37.6</td>
      <td>2.9</td>
      <td>23.4</td>
      <td>24.7</td>
      <td>12529.0</td>
      <td>Ashley Cole</td>
      <td>Sulzeer Jeremiah ''Sol' Campbell</td>
      <td>15637.0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>31</td>
      <td>11.1</td>
      <td>9.7</td>
      <td>7.7</td>
      <td>21.5</td>
      <td>12529.0</td>
      <td>Ashley Cole</td>
      <td>Sulzeer Jeremiah ''Sol' Campbell</td>
      <td>15637.0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>75</td>
      <td>17.7</td>
      <td>11.5</td>
      <td>26.2</td>
      <td>8.1</td>
      <td>12529.0</td>
      <td>Ashley Cole</td>
      <td>Robert Pirès</td>
      <td>19312.0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>97</td>
      <td>25.3</td>
      <td>29.3</td>
      <td>30.0</td>
      <td>49.1</td>
      <td>38412.0</td>
      <td>Kolo Habib Touré</td>
      <td>Laureano Bisan-Etame Mayer</td>
      <td>40222.0</td>
    </tr>
  </tbody>
</table>
</div>



## 画图


```python
# 计算位置和大小
scatter = pd.DataFrame()
for i, _id in enumerate(passes['player_id'].unique()):
    pass_x = passes.loc[passes['player_id'] == _id]['x'].to_numpy()
    pass_y = passes.loc[passes['player_id'] == _id]['y'].to_numpy()
    rec_x = passes.loc[passes['pass_recipient_id'] == _id]['end_x'].to_numpy()
    rec_y = passes.loc[passes['pass_recipient_id'] == _id]['end_y'].to_numpy()
    scatter.at[i, 'player_id'] = _id
    
    # 计算每个点的 x 和 y，位置为传球和接球的平均值
    scatter.at[i, 'x'] = np.mean(np.concatenate([pass_x, rec_x]))
    scatter.at[i, 'y'] = np.mean(np.concatenate([pass_y, rec_y]))
    
    # 计算传球数
    scatter.at[i, 'count'] = passes.loc[
        passes['player_id'] == _id].count().iloc[0]
```


```python
# 位置大小
scatter['marker_size'] = scatter['count'] / scatter['count'].max() * 3000
```


```python
# 合并名字
scatter = pd.merge(
    scatter,
    invincible_11,
    on='player_id'
)
```


```python
# 计算球员之间的传球次数
passes['pair_key'] = passes.apply(
    lambda x: '-'.join(sorted([str(x['player_id']), 
                               str(x['pass_recipient_id'])])),
    axis=1,
)
lines = passes.groupby(['pair_key']).x.count().reset_index()
lines.rename({'x': 'pass_count'}, axis='columns', inplace=True)

# 设定一个阈值，可以尝试研究它在更改时如何变化
lines = lines[lines['pass_count'] > 4 * 38]

# 绘制球场
pitch = Pitch(line_color='grey')
fig, ax = pitch.grid(
    grid_height=0.9, title_height=0.06, axis=False,
    endnote_height=0.04, title_space=0, endnote_space=0,
)
# 球场上的位置
pitch.scatter(
    scatter.x, scatter.y, s=scatter.marker_size, 
    color='red', edgecolors='grey', linewidth=1, alpha=0.8,
    ax=ax['pitch'], zorder=3,
)

# 填充球员名字
for i, row in scatter.iterrows():
    pitch.annotate(
        row.player_nickname, xy=(row.x, row.y), c='black', 
        va='center', ha='center', weight="bold", 
        size=14, ax=ax["pitch"], zorder=4,
    )
    
for i, row in lines.iterrows():
    player1 = float(row['pair_key'].split('-')[0])
    player2 = float(row['pair_key'].split('-')[1])
    
    # 取球员的平均位置在他们之间画一条线
    player1_x = scatter.loc[scatter['player_id'] == player1]['x'].iloc[0]
    player1_y = scatter.loc[scatter['player_id'] == player1]['y'].iloc[0]
    player2_x = scatter.loc[scatter['player_id'] == player2]['x'].iloc[0]
    player2_y = scatter.loc[scatter['player_id'] == player2]['y'].iloc[0]
    passes_count = row['pass_count']
    # 调整线宽，传球的次数越多，线越宽
    line_width = passes_count / lines['pass_count'].max() * 15

    pitch.lines(
        player1_x, player1_y, player2_x, player2_y,
        alpha=0.8, lw=line_width, zorder=2, color='red', ax=ax['pitch']
    )
    
fig.suptitle('Invincible 11', fontsize=30)
plt.show()

```


    
![invincible_11_passing_networks.png](https://s2.loli.net/2023/04/15/LN5KPG6efpjFRMC.png)
    


## 结论

高中时期我和好友无数次在实况足球里面模拟这一套 442，现在看到还原出来蛮感慨

1. 莱曼的出球线路，图雷，较少直接找两个边后卫，很少开大脚
2. 图雷担任出球中卫
3. 劳伦这一侧的球权比想象中多
4. 吉尔伯托在后场出球系统中几乎和维埃拉同样重要，但他没有向前传球的路线
5. 托后三人组，坎贝尔，图雷，吉尔伯托
6. 阿什利科尔 - 皮雷 - 亨利是主要的推进线路
7. 永贝里的主要进攻路线是传中找亨利
8. 皮雷当之无愧的进攻核心
9. 所有的进攻球都在找亨利
10. 博格坎普可能受制于出场时间，并没有想象中重要
