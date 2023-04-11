# 阿森纳不败赛季传球路线图探索 01

statsbomb 有一些有趣的公开数据，比如梅西的职业生涯，阿森纳的不败赛季，最近在上足球数据可视化的课程，刚好拿来玩一玩。

通过 competitions 找到英超联赛 0304赛季的 id，其中只有阿森纳的比赛，这次随便获取一场比赛来试手，2004 年 4 月 25 日北伦敦德比，阿森纳在白鹿巷球场 2:2 战平热刺，高举起英格兰超级联赛冠军奖杯，就它了。

## import


```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mplsoccer import Pitch, Sbopen

match_id = 3749068
```


```python
parser = Sbopen()
events, related, freeze, tactics = parser.event(match_id)
```


```python
# 检查一下数据集
events.info()
```

    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 3156 entries, 0 to 3155
    Data columns (total 77 columns):
     #   Column                          Non-Null Count  Dtype  
    ---  ------                          --------------  -----  
     0   id                              3156 non-null   object 
     1   index                           3156 non-null   int64  
     2   period                          3156 non-null   int64  
     3   timestamp                       3156 non-null   object 
     4   minute                          3156 non-null   int64  
     5   second                          3156 non-null   int64  
     6   possession                      3156 non-null   int64  
     7   duration                        2355 non-null   float64
     8   match_id                        3156 non-null   int64  
     9   type_id                         3156 non-null   int64  
     10  type_name                       3156 non-null   object 
     11  possession_team_id              3156 non-null   int64  
     12  possession_team_name            3156 non-null   object 
     13  play_pattern_id                 3156 non-null   int64  
     14  play_pattern_name               3156 non-null   object 
     15  team_id                         3156 non-null   int64  
     16  team_name                       3156 non-null   object 
     17  tactics_formation               3 non-null      float64
     18  player_id                       3145 non-null   float64
     19  player_name                     3145 non-null   object 
     20  position_id                     3145 non-null   float64
     21  position_name                   3145 non-null   object 
     22  pass_recipient_id               801 non-null    float64
     23  pass_recipient_name             801 non-null    object 
     24  pass_length                     879 non-null    float64
     25  pass_angle                      879 non-null    float64
     26  pass_height_id                  879 non-null    float64
     27  pass_height_name                879 non-null    object 
     28  end_x                           1571 non-null   float64
     29  end_y                           1571 non-null   float64
     30  body_part_id                    899 non-null    float64
     31  body_part_name                  899 non-null    object 
     32  sub_type_id                     322 non-null    float64
     33  sub_type_name                   322 non-null    object 
     34  x                               3139 non-null   float64
     35  y                               3139 non-null   float64
     36  outcome_id                      434 non-null    float64
     37  outcome_name                    434 non-null    object 
     38  under_pressure                  670 non-null    float64
     39  counterpress                    82 non-null     float64
     40  off_camera                      65 non-null     float64
     41  aerial_won                      38 non-null     object 
     42  out                             34 non-null     float64
     43  ball_recovery_recovery_failure  11 non-null     object 
     44  pass_switch                     38 non-null     object 
     45  foul_committed_advantage        5 non-null      object 
     46  foul_won_advantage              5 non-null      object 
     47  technique_id                    50 non-null     float64
     48  technique_name                  50 non-null     object 
     49  pass_assisted_shot_id           16 non-null     object 
     50  pass_goal_assist                3 non-null      object 
     51  shot_open_goal                  1 non-null      object 
     52  shot_statsbomb_xg               23 non-null     float64
     53  end_z                           19 non-null     float64
     54  shot_key_pass_id                16 non-null     object 
     55  shot_first_time                 8 non-null      object 
     56  goalkeeper_position_id          23 non-null     float64
     57  goalkeeper_position_name        23 non-null     object 
     58  pass_cross                      15 non-null     object 
     59  dribble_overrun                 3 non-null      object 
     60  ball_recovery_offensive         2 non-null      object 
     61  pass_shot_assist                13 non-null     object 
     62  foul_won_defensive              9 non-null      object 
     63  pass_deflected                  2 non-null      object 
     64  half_start_late_video_start     2 non-null      object 
     65  substitution_replacement_id     5 non-null      float64
     66  substitution_replacement_name   5 non-null      object 
     67  foul_committed_card_id          2 non-null      float64
     68  foul_committed_card_name        2 non-null      object 
     69  dribble_nutmeg                  1 non-null      object 
     70  shot_one_on_one                 1 non-null      object 
     71  pass_cut_back                   1 non-null      object 
     72  block_offensive                 1 non-null      object 
     73  foul_committed_penalty          1 non-null      object 
     74  foul_won_penalty                1 non-null      object 
     75  bad_behaviour_card_id           1 non-null      float64
     76  bad_behaviour_card_name         1 non-null      object 
    dtypes: float64(26), int64(10), object(41)
    memory usage: 1.9+ MB



```python
# 查看有哪些事件
events['type_name'].unique()
```




    array(['Starting XI', 'Half Start', 'Pass', 'Ball Receipt', 'Carry',
           'Block', 'Ball Recovery', 'Pressure', 'Duel', 'Clearance',
           'Foul Committed', 'Foul Won', 'Dribbled Past', 'Dribble', 'Shot',
           'Goal Keeper', 'Dispossessed', 'Interception', 'Miscontrol',
           '50/50', 'Offside', 'Half End', 'Substitution', 'Error',
           'Tactical Shift', 'Bad Behaviour'], dtype=object)



由于换人了以后阵容战术就会变动，所以绘制首发传球图需要在第一次换人之前，找到第一次换人的事件

然后过滤掉：

1. 对手的事件
2. 换人之后的事件，也就是index 小于 sub 的事件
3. 失败的传球


```python
first_sub = events.loc[
    events['type_name'] == 'Substitution'].loc[
    events['team_name'] == "Arsenal"].iloc[0]
first_sub
```




    id                         7900f48c-1308-4aa5-9ec8-37af5c06a6d7
    index                                                      2335
    period                                                        2
    timestamp                                       00:21:42.293000
    minute                                                       66
                                               ...                 
    block_offensive                                             NaN
    foul_committed_penalty                                      NaN
    foul_won_penalty                                            NaN
    bad_behaviour_card_id                                       NaN
    bad_behaviour_card_name                                     NaN
    Name: 2334, Length: 77, dtype: object




```python
_filter = (
    events.type_name == 'Pass') & (
    events.team_name == "Arsenal") & (
    events.index < first_sub['index']) & (
    events.outcome_name.isnull())
```


```python
_filter.head()
```




    0    False
    1    False
    2    False
    3    False
    4     True
    dtype: bool




```python
# 获取必要的数据
passes = events.loc[_filter, [
    'x', 'y', 'end_x', 'end_y',
    'player_id', 'player_name', 'pass_recipient_name', 'pass_recipient_id'
]]
```


```python
passes.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
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
      <th>4</th>
      <td>60.0</td>
      <td>40.0</td>
      <td>62.3</td>
      <td>43.5</td>
      <td>15516.0</td>
      <td>Thierry Henry</td>
      <td>Dennis Bergkamp</td>
      <td>15042.0</td>
    </tr>
    <tr>
      <th>6</th>
      <td>62.0</td>
      <td>43.5</td>
      <td>47.2</td>
      <td>30.7</td>
      <td>15042.0</td>
      <td>Dennis Bergkamp</td>
      <td>Patrick Vieira</td>
      <td>15515.0</td>
    </tr>
    <tr>
      <th>9</th>
      <td>47.2</td>
      <td>29.5</td>
      <td>38.2</td>
      <td>12.1</td>
      <td>15515.0</td>
      <td>Patrick Vieira</td>
      <td>Ashley Cole</td>
      <td>12529.0</td>
    </tr>
    <tr>
      <th>12</th>
      <td>38.2</td>
      <td>12.1</td>
      <td>31.7</td>
      <td>26.3</td>
      <td>12529.0</td>
      <td>Ashley Cole</td>
      <td>Sulzeer Jeremiah ''Sol' Campbell</td>
      <td>15637.0</td>
    </tr>
    <tr>
      <th>15</th>
      <td>28.8</td>
      <td>29.5</td>
      <td>48.4</td>
      <td>38.8</td>
      <td>15637.0</td>
      <td>Sulzeer Jeremiah ''Sol' Campbell</td>
      <td>Gilberto Aparecido da Silva</td>
      <td>40221.0</td>
    </tr>
  </tbody>
</table>
</div>



## 计算位置和大小

对于每个球员，计算传球和接球的平均位置，然后计算每个球员到接球球员的传球次数，传球线路的粗细与之成正比


```python
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
    
# 位置大小
scatter['marker_size'] = scatter['count'] / scatter['count'].max() * 1500
```


```python
scatter
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>player_id</th>
      <th>x</th>
      <th>y</th>
      <th>count</th>
      <th>marker_size</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>15516.0</td>
      <td>73.757692</td>
      <td>33.834615</td>
      <td>10.0</td>
      <td>306.122449</td>
    </tr>
    <tr>
      <th>1</th>
      <td>15042.0</td>
      <td>66.135897</td>
      <td>37.082051</td>
      <td>15.0</td>
      <td>459.183673</td>
    </tr>
    <tr>
      <th>2</th>
      <td>15515.0</td>
      <td>54.474194</td>
      <td>33.134409</td>
      <td>49.0</td>
      <td>1500.000000</td>
    </tr>
    <tr>
      <th>3</th>
      <td>12529.0</td>
      <td>52.920313</td>
      <td>7.568750</td>
      <td>35.0</td>
      <td>1071.428571</td>
    </tr>
    <tr>
      <th>4</th>
      <td>15637.0</td>
      <td>36.142857</td>
      <td>19.846429</td>
      <td>13.0</td>
      <td>397.959184</td>
    </tr>
    <tr>
      <th>5</th>
      <td>40221.0</td>
      <td>52.817460</td>
      <td>43.530159</td>
      <td>32.0</td>
      <td>979.591837</td>
    </tr>
    <tr>
      <th>6</th>
      <td>38412.0</td>
      <td>35.815909</td>
      <td>48.084091</td>
      <td>23.0</td>
      <td>704.081633</td>
    </tr>
    <tr>
      <th>7</th>
      <td>40222.0</td>
      <td>49.040351</td>
      <td>70.389474</td>
      <td>31.0</td>
      <td>948.979592</td>
    </tr>
    <tr>
      <th>8</th>
      <td>19312.0</td>
      <td>61.132308</td>
      <td>18.466154</td>
      <td>32.0</td>
      <td>979.591837</td>
    </tr>
    <tr>
      <th>9</th>
      <td>20015.0</td>
      <td>8.210000</td>
      <td>41.750000</td>
      <td>8.0</td>
      <td>244.897959</td>
    </tr>
    <tr>
      <th>10</th>
      <td>24972.0</td>
      <td>68.381081</td>
      <td>67.370270</td>
      <td>15.0</td>
      <td>459.183673</td>
    </tr>
  </tbody>
</table>
</div>



## 球员名及号码

由于事件数据集只有简单的球员名字和 id，绘制图片时使用名字全称过长，比如 Laureano Bisan-Etame Mayer 这位大哥估计不少人反应不过来是谁，Lauren 就明白了。

需要从另一个数据集中获取


```python
lineup = parser.lineup(match_id)
```


```python
arsenal = lineup.loc[lineup['team_name'] == 'Arsenal']
scatter = pd.merge(
    scatter, 
    arsenal[['player_id', 'player_nickname', 'jersey_number']], 
    on='player_id'
)
```

## 计算传球线路宽度

计算线路宽度，需要根据传球和接球的组合对传球数据框进行分组，并计算他们之间的传球次数。最后一步设置了忽略传球次数少于 2 次的球员的阈值。可以尝试不同的值，根据可视化背后的信息调整它


```python
# 计算球员之间的传球次数
passes['pair_key'] = passes.apply(
    lambda x: '-'.join(sorted([str(x['player_id']), 
                               str(x['pass_recipient_id'])])),
    axis=1,
)
lines = passes.groupby(['pair_key']).x.count().reset_index()
lines.rename({'x': 'pass_count'}, axis='columns', inplace=True)
```


```python
# 设定一个阈值，可以尝试研究它在更改时如何变化
lines = lines[lines['pass_count'] > 2]
```


```python
lines.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>pair_key</th>
      <th>pass_count</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>1</th>
      <td>12529.0-15515.0</td>
      <td>20</td>
    </tr>
    <tr>
      <th>2</th>
      <td>12529.0-15516.0</td>
      <td>4</td>
    </tr>
    <tr>
      <th>3</th>
      <td>12529.0-15637.0</td>
      <td>8</td>
    </tr>
    <tr>
      <th>4</th>
      <td>12529.0-19312.0</td>
      <td>21</td>
    </tr>
    <tr>
      <th>7</th>
      <td>12529.0-40221.0</td>
      <td>6</td>
    </tr>
  </tbody>
</table>
</div>



## 绘制路线


```python
# 绘制球场
pitch = Pitch(line_color='grey')
fig, ax = pitch.grid(
    grid_height=0.9, title_height=0.06, axis=False,
    endnote_height=0.04, title_space=0, endnote_space=0,
)
# 球场上的位置
pitch.scatter(
    scatter.x, scatter.y, s=scatter.marker_size, 
    color='red', edgecolors='grey', linewidth=1, alpha=1,
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
    # 调整线宽，使通过的次数越多，线越宽
    line_width = passes_count / lines['pass_count'].max() * 10

    pitch.lines(
        player1_x, player1_y, player2_x, player2_y,
        alpha=1, lw=line_width, zorder=2, color='red', ax=ax['pitch']
    )
    
fig.suptitle('2004-04-25, Tottenham Hotspur vs Arsenal', fontsize=30)
plt.show()
```


    
![ARS_VS_HOT_0304_passing_networks.png](https://s2.loli.net/2023/04/11/1GzYOeHoiubdvLF.png)
