# 阿森纳不败赛季传球路线图探索 04

这一次探索单个球员的进攻传球路线。首先还是画出热区图，准备数据的部分和前面一篇相同，就不重复写了，直接跳到 danger_passes


```python
import pandas as pd
import matplotlib.pyplot as plt
from mplsoccer import Pitch, Sbopen, VerticalPitch
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
      <th>player_id</th>
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
      <td>15515.0</td>
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
      <td>26014.0</td>
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
      <td>12529.0</td>
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
      <td>19312.0</td>
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
      <td>26014.0</td>
    </tr>
  </tbody>
</table>
</div>



## 探索单个球员

作为威胁传球的核心，首先来探索皮雷，手动在名单里获取皮雷的 id，然后过滤


```python
bins = (6, 5)
```


```python
pires = danger_passes.loc[danger_passes['player_id'] == 19312]
```


```python
def plot_player_passes(player, passes):
    pitch = Pitch(line_zorder=2, line_color="grey")
    fig, ax = pitch.grid(
        grid_height=0.9,
        title_height=0.06,
        axis=False,
        endnote_height=0.04,
        title_space=0,
        endnote_space=0,
    )

    bin_statistic = pitch.bin_statistic(
        player.x,
        player.y,
        statistic="count",
        bins=bins,
        normalize=False,
    )

    # 制作热区图
    pcm = pitch.heatmap(
        bin_statistic, 
        cmap="Reds", 
        # edgecolor="grey", 
        ax=ax["pitch"],
    )

    # 绘制传球路线
    pitch.arrows(
        passes.x,
        passes.y,
        passes.end_x,
        passes.end_y,
        color="black",
        alpha=1,
        width=2,
        ax=ax["pitch"],
    )

    fig.suptitle(f"{player.iloc[0].player_name}", fontsize=30)
    plt.show()
```


```python
plot_player_passes(pires, pires)
```


    
![attacking_play_pires_01.png](https://s2.loli.net/2023/04/29/6ujT13XKcx7EnOg.png)
    


这样的路线看起来未免杂乱，这里使用 Opta 的一种传球表现图：球场分成 10 * 10 的区域，每一块区域传球次数越多颜色越深，箭头表示此区域的平均传球方向


```python
bins = (10, 10)
```


```python
def binning_groupby_mean(player):
    x_bins = [i for i in range(0, 121, 120 // bins[0])]
    y_bins = [i for i in range(0, 81, 80 // bins[1])]
    player['x_bin'] = pd.cut(player['x'], x_bins)
    player['y_bin'] = pd.cut(player['y'], y_bins)
    return player.groupby(['x_bin', 'y_bin']).mean()
```


```python
mean_passes = binning_groupby_mean(pires)
plot_player_passes(pires, mean_passes)
```


    
![attacking_play_pires_02.png](https://s2.loli.net/2023/04/29/OtbKrZBPfMTLyaF.png)
    


边路进攻核心活动区域，次数最多的是左路肋部区域，在较少拿球的区域传球的距离比较长，到了不是自己的位置会将球传到熟悉的区域而不是就地组织，很少有长距离传中路线


```python
vieira = danger_passes.loc[danger_passes['player_id'] == 15515]
mean_passes = binning_groupby_mean(vieira)
plot_player_passes(vieira, mean_passes)
```


    
![attacking_play_vieira.png](https://s2.loli.net/2023/04/29/DmBf7sAeSutwWM1.png)
    


覆盖了整个中场，核心传球区域与皮雷很近，传球选择路线更偏向左路


```python
henry = danger_passes.loc[danger_passes['player_id'] == 15516]
mean_passes = binning_groupby_mean(henry)
plot_player_passes(henry, mean_passes)
```


    
![attacking_play_henry.png](https://s2.loli.net/2023/04/29/dv3SfFq8Z4QpCXb.png)
    


与印象不同的是，在中路禁区前沿有着大量的传球，且都是向前的路线，往禁区送出了大量的威胁球，所以在进球同时会收获那么多的助攻


```python
player = danger_passes.loc[danger_passes['player_id'] == 15042]
mean_passes = binning_groupby_mean(player)
plot_player_passes(player, mean_passes)
```


    
![attacking_play_bergkamp.png](https://s2.loli.net/2023/04/29/tPTJrEHj97U5pd1.png)
    


活动位置更像是进攻型中场，传球也大多找的禁区前的队友


```python
player = danger_passes.loc[danger_passes['player_id'] == 15754]
mean_passes = binning_groupby_mean(player)
plot_player_passes(player, mean_passes)
```


    
![attacking_play_ljungberg.png](https://s2.loli.net/2023/04/29/GVHYfwemKSIEyX2.png)
    


与皮雷不一样的是，就地选择进攻传球更为频繁，习惯性活动范围固定在几块，可能与他场上位置更多变有关

传球路线图就到这里了，下一次探索些别的
