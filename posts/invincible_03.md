# 阿森纳不败赛季传球路线图探索 03

这次用热区图的形式来探索，与平时所看的全场比赛事件分布热区图不一样的是，用的是危险传球——这次把射门前 15 秒内的传球都视为危险传球。

前面获取数据部分和上一篇大致相同

## import


```python
import pandas as pd
import matplotlib.pyplot as plt
from mplsoccer import Pitch, Sbopen, VerticalPitch
```


```python
parser = Sbopen()
matches = parser.match(competition_id=2, season_id=44)
matches_events = []
for match_id in matches['match_id']:
    data = parser.event(match_id)
    events.append(data[0])
```

## 获取危险传球

获取阿森纳所有比赛的射门和准确传球，且传球不是定位球，然后寻找射门前 15 秒的传球，对于时间需要考虑上下半场，伤停补时的特殊处理


```python
danger_passes = pd.DataFrame()
for events in matches_events:
    # 上下半场
    for period in [1, 2]:
        # 只保留没有定位球的准确传球
        pass_filter = (
            events.team_name == 'Arsenal') & (
            events.type_name == "Pass") & (
            events.outcome_name.isnull()) & (
            events.period == period) & (
            events.sub_type_name.isnull())
        passes = events.loc[
            pass_filter, 
            [
                "x", "y", "end_x", "end_y", 
                "minute", "second", "player_name",
            ],
        ]
        # 只保留阿森纳的射门
        shot_filter = (
            events.team_name == 'Arsenal') & (
            events.type_name == "Shot") & (
            events.period == period)
        shots = events.loc[shot_filter, ["minute", "second"]]
        shot_times = shots['minute'] * 60 + shots['second']
        
        # 设置为射门前 15 秒
        shot_anchor = 15
        shot_start = shot_times - shot_anchor
        
        # 处理时间
        shot_start = shot_start.apply(lambda i: i if i > 0 else (period - 1) * 45)
        pass_times = passes['minute'] * 60 + passes['second']

        pass_to_shot = pass_times.apply(
            lambda x: True in ((shot_start < x) & (x < shot_times)).unique())

        # 只保留危险传球
        danger_passes_period = passes.loc[pass_to_shot]
        danger_passes = pd.concat(
            [danger_passes, danger_passes_period], 
            ignore_index=True
        )
```


```python
danger_passes.head()
```




<div>
<table>
  <thead>
    <tr>
      <th></th>
      <th>x</th>
      <th>y</th>
      <th>end_x</th>
      <th>end_y</th>
      <th>minute</th>
      <th>second</th>
      <th>player_name</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>52.6</td>
      <td>54.3</td>
      <td>54.6</td>
      <td>45.0</td>
      <td>8</td>
      <td>4</td>
      <td>Patrick Vieira</td>
    </tr>
    <tr>
      <th>1</th>
      <td>69.9</td>
      <td>28.5</td>
      <td>102.0</td>
      <td>26.9</td>
      <td>8</td>
      <td>8</td>
      <td>Eduardo César Daude Gaspar</td>
    </tr>
    <tr>
      <th>2</th>
      <td>102.0</td>
      <td>26.9</td>
      <td>104.7</td>
      <td>37.6</td>
      <td>8</td>
      <td>10</td>
      <td>Ashley Cole</td>
    </tr>
    <tr>
      <th>3</th>
      <td>60.0</td>
      <td>45.6</td>
      <td>68.9</td>
      <td>33.9</td>
      <td>12</td>
      <td>7</td>
      <td>Robert Pirès</td>
    </tr>
    <tr>
      <th>4</th>
      <td>68.5</td>
      <td>33.9</td>
      <td>79.1</td>
      <td>31.1</td>
      <td>12</td>
      <td>9</td>
      <td>Eduardo César Daude Gaspar</td>
    </tr>
  </tbody>
</table>
</div>



## 绘制热区图

这次在球场上使用 6 * 5 的格子来制作，其中宽度区域对应中肋边路，六块长度区域在瓜迪奥拉的战术板经常能看到


```python
pitch = Pitch(line_zorder=2, line_color='grey')
fig, ax = pitch.grid(
    grid_height=0.9, title_height=0.06, axis=False,
    endnote_height=0.04, title_space=0, endnote_space=0
)

bin_statistic = pitch.bin_statistic(
    danger_passes.x, danger_passes.y, 
    statistic='count', bins=(6, 5), normalize=False,
)

# 绘制热区图
pcm = pitch.heatmap(
    bin_statistic, cmap='Reds', edgecolor='black', ax=ax['pitch']
)

# 绘制说明
ax_cbar = fig.add_axes((1, 0.093, 0.03, 0.786))
cbar = plt.colorbar(pcm, cax=ax_cbar)

fig.suptitle('Danger passes by Arsenal', fontsize=30)
plt.show()
```


    
![arsenal_0304_danger_pass_heatmap.png](https://s2.loli.net/2023/04/19/9yWTgXGkQbl2vKf.png)
    


## 绘制参与危险传球最多球员的图表

为了更加清晰的探索，将球员参与的传球次数绘制出来

这次偷个懒就不与 nickname 结合了


```python
passes_count = danger_passes.groupby(['player_name']).x.count()

ax = passes_count.plot.barh(passes_count)
ax.set_xlabel('Number of danger passes')
ax.set_ylabel('')
plt.show()
```


    
![number_of_arsenal_0304_danger_pass.png](https://s2.loli.net/2023/04/19/IO2bqtkSLTKjhCg.png)
    


## 结论

1. 维埃拉-皮雷-亨利占据了形成射门的大多数传球，球会经过他们很多次，是整个进攻体系的核心
2. 博格坎普受限于出场(21次首发8次替补)，他的进攻参与度重要性不亚于 1
3. 亨利作为终结者，在进攻传球网络中也有如此重要的数据，全能
4. 左路肋部区域承担了推进至禁区的大多任务，
5. 右路参与的控球大多数会通过中路交到左路，少部分会在右路传到禁区
