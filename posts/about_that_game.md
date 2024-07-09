# 关于 that-game

我在一些足球事件的项目中大量使用了 [kloppy](https://github.com/PySport/kloppy), 也有一些项目使用了 [socceraction](https://github.com/ML-KULeuven/socceraction) 的 spadl，这两个都可以看成“标准化的足球事件数据结构”，也就是把各个数据源的事件数据读取成一个统一的数据结构，方便后面的一系列计算。

但他们各有各的不方便。socceraction 是基于 pandas，使用 pandera 预设一些字段，也可以做数据验证。既然本质上是个 pd.DataFrame, 就有着 df 不可避免的优点和缺点，数据科学家会很习惯他的操作，但在编写实际代码的时候缺乏很好的自动补全，类型推断，在提供的字段上面也偏少：

```python
sbl = StatsBombLoader(root=data_path, getter="local")
df_games = sbl.games(competition_id=43, season_id=3).set_index("game_id")
game_id = 8657
df_teams = sbl.teams(game_id)
df_players = sbl.players(game_id)
df_events = sbl.events(game_id)

home_team_id = df_games.at[game_id, "home_team_id"]
df_actions = spadl.statsbomb.convert_to_actions(df_events, home_team_id)
```

```python
df_actions.sample(5)
```

<div>
<table>
  <thead>
    <tr>
      <th></th>
      <th>game_id</th>
      <th>original_event_id</th>
      <th>period_id</th>
      <th>time_seconds</th>
      <th>team_id</th>
      <th>player_id</th>
      <th>start_x</th>
      <th>start_y</th>
      <th>end_x</th>
      <th>end_y</th>
      <th>type_id</th>
      <th>result_id</th>
      <th>bodypart_id</th>
      <th>action_id</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2307</th>
      <td>8657</td>
      <td>206ac85d-9b2d-475f-88c7-bc4ccc2738e7</td>
      <td>2</td>
      <td>2482.471</td>
      <td>768</td>
      <td>3308.0</td>
      <td>50.3125</td>
      <td>59.075</td>
      <td>39.8125</td>
      <td>64.175</td>
      <td>21</td>
      <td>1</td>
      <td>0</td>
      <td>2307</td>
    </tr>
    <tr>
      <th>168</th>
      <td>8657</td>
      <td>5e1b54a1-a93b-4c78-a69f-4ed8c708dbd9</td>
      <td>1</td>
      <td>346.439</td>
      <td>782</td>
      <td>3101.0</td>
      <td>43.3125</td>
      <td>27.625</td>
      <td>42.4375</td>
      <td>28.475</td>
      <td>21</td>
      <td>1</td>
      <td>0</td>
      <td>168</td>
    </tr>
    <tr>
      <th>938</th>
      <td>8657</td>
      <td>19d08ada-edbc-4fe6-bfd3-00aa03977447</td>
      <td>1</td>
      <td>1821.052</td>
      <td>768</td>
      <td>3468.0</td>
      <td>98.4375</td>
      <td>30.175</td>
      <td>97.5625</td>
      <td>30.175</td>
      <td>21</td>
      <td>1</td>
      <td>0</td>
      <td>938</td>
    </tr>
    <tr>
      <th>2310</th>
      <td>8657</td>
      <td>fe9150f6-60d7-429b-8116-115f1b49a1b8</td>
      <td>2</td>
      <td>2489.351</td>
      <td>782</td>
      <td>3077.0</td>
      <td>25.8125</td>
      <td>65.025</td>
      <td>31.9375</td>
      <td>64.175</td>
      <td>21</td>
      <td>1</td>
      <td>0</td>
      <td>2310</td>
    </tr>
    <tr>
      <th>903</th>
      <td>8657</td>
      <td>9f489405-7d17-4a0b-9c77-089c49e0b056</td>
      <td>1</td>
      <td>1770.533</td>
      <td>782</td>
      <td>3176.0</td>
      <td>65.1875</td>
      <td>4.675</td>
      <td>65.1875</td>
      <td>12.325</td>
      <td>0</td>
      <td>1</td>
      <td>5</td>
      <td>903</td>
    </tr>
  </tbody>
</table>
</div>

读取过程稍显麻烦，一些在我看来的重要信息，比如 team，player，type， result， bodypart 等都是使用数字作为类别，不存在可读性，如果想要搞清楚数字代表的具体含义需要再调用一个函数：

```python
from socceraction.spadl import results_df

results_df()
```

<div>
<table>
  <thead>
    <tr>
      <th></th>
      <th>result_id</th>
      <th>result_name</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0</td>
      <td>fail</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1</td>
      <td>success</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2</td>
      <td>offside</td>
    </tr>
    <tr>
      <th>3</th>
      <td>3</td>
      <td>owngoal</td>
    </tr>
    <tr>
      <th>4</th>
      <td>4</td>
      <td>yellow_card</td>
    </tr>
    <tr>
      <th>5</th>
      <td>5</td>
      <td>red_card</td>
    </tr>
  </tbody>
</table>
</div>

都是可哈希对象，其实可以使用字符串使其更具有可读性。而且 spadl 作为为这个库主要的目的，计算 xT, VAEP 的数据结构，支持的 type 也偏少。

kloppy 是则是使用了更为灵活的基于对象的数据模型，有更多的预设读取，如果你只是用他预设的数据源进行操作没什么问题，想更多的自定义操作，他的数据类使用 python dataclass，就没办法有很好的数据验证:


```python
from kloppy.domain import Team, Ground

# 这个是正确输入
team = Team(team_id="ars", name="Arsenal", ground=Ground.HOME)

# 但即使输入一些错误的类型也不会有问题
team = Team(team_id=123, name=123, ground="HOME")
```

只能通过 mypy 之类的工具寄希望于代码执行之前检查类型，并不具有强制性。同时如果想自定义创建一个 EventDataset 需要太多步骤：

```python
from kloppy.domain import (
    BallState,
    DatasetFlag,
    EventDataset,
    Ground,
    KloppyCoordinateSystem,
    Metadata,
    Orientation,
    Period,
    PitchDimensions,
    Player,
    Point,
    Provider,
    ShotEvent,
    ShotResult,
    Team,
)
```

```python
period = Period(id=1, start_timestamp=0.0, end_timestamp=2827.0)
team = Team(team_id="ars", name="Arsenal", ground=Ground.HOME)
team_2 = Team(team_id="che", name="Chelsea", ground=Ground.AWAY)
player = Player(player_id="saka", team=team, jersey_no=7, name="Bukayo Saka")
coordinates = Point(x=100, y=50)
event = ShotEvent(
    event_id="1",
    period=period,
    timestamp=217.32,
    team=team,
    player=player,
    coordinates=coordinates,
    result=ShotResult.OFF_TARGET,
    raw_event=None,
    ball_state=BallState.ALIVE,
    ball_owning_team=team,
    related_event_ids=[],
    state={},
    qualifiers=[],
    freeze_frame=None,
)
```

```python
pitch_dimensions = PitchDimensions(x_dim=108, y_dim=68)
coordinate_system = KloppyCoordinateSystem(normalized=True, length=108, width=68)
metadata = Metadata(
    teams=[team, team_2],
    periods=[period],
    pitch_dimensions=pitch_dimensions,
    orientation=Orientation.ACTION_EXECUTING_TEAM,
    flags=DatasetFlag.BALL_OWNING_TEAM,
    provider=Provider.OTHER,
    coordinate_system=coordinate_system,
)
```

```python
custom_dataset = EventDataset(records=[event], metadata=metadata)
```

他在描述状态的时候用了大量的 enum，每一个都需要导入，以及确定每一个字段的含义。而我使用最不舒服的一点在构建 team 和 player，他在设计时使用了循环引用:

```python
@dataclass
class Player:
    team: "Team"

@dataclass
class Team:
    players: List[Player] = field(default_factory=list)
```

可以读他源代码中读取 statsbomb 的一段：
```python
        def create_team(lineup, ground_type):
            team = Team(
                team_id=str(lineup["team_id"]),
                name=lineup["team_name"],
                ground=ground_type,
                starting_formation=starting_formations[lineup["team_id"]],
            )
            team.players = [
                Player(
                    player_id=str(player["player_id"]),
                    team=team,
                    name=player["player_name"],
                    jersey_no=int(player["jersey_number"]),
                    starting=str(player["player_id"]) in player_positions,
                    position=player_positions.get(str(player["player_id"])),
                )
                for player in lineup["lineup"]
            ]
            return team
```

循环引用有什么后果不多讨论，单从使用上来说，需要先创建 team，然后创建 player，把 team 塞到 player，再把 player 塞到 team。

在使用那么久之后，我还是想自己创建一个 Events 的数据格式，便写了 that-game。

我中和了上面两个库的特性，以及长期的使用习惯，that-game 需要有以下的特点：

* 创建简单
* 方便计算
* 尽可能的扁平化
* 支持数据验证
* 支持类型推断
* 预设常用的数据源读取
* 方便导出为常用格式
* 方便不同的数据规格（主要是坐标）转换
* 兼容尽可能多的事件类型
* 方便不同数据源之间匹配和融合
* 可读性

使用 pydantic 来创建数据类可以解决大部分，常用状态使用 typing.Literal 预设字段，既能很好的配合编辑器补全，也能通过 pydantic 进行输入验证。

在创建新对象的时候，可以导入每个数据类，嫌麻烦也可以这样：

```python
from that_game import Shot

shot = Shot(
    id="0001",
    type="shot",
    period="first_half",
    seconds=62.0,
    team={"id": "ars", "name": "Arsenal"},
    player={"id": "a7", "name": "Bukayo Saka", "position": "FW"},
    location={
        "x": 100.1,
        "y": 43.2,
        "pitch": {"length": 108, "width": 68},
    },
    end_location={
        "x": 108.0,
        "y": 43.2,
        "pitch": {"length": 108, "width": 68},
    },
    pattern="open_play",
    body_part="left_foot",
    result="saved",
)
```

每个数据源之间最大的差异便是坐标系统，使用球场长宽高不同，方向不同，如何方便的转换是一个很大的问题，that-game 的 Location 可以很直观方便的转换：

```python
from that_game import Location, Pitch

location = Location(
    x=0.4,
    y=0.6,
    pitch=Pitch(length=1, width=1),
)

# 只需要设定好新的 pitch 标准
pitch = Pitch(
    length=100,
    width=100,
    length_direction="left",
    width_direction="down",
)
location.transform(pitch)
print(location.x, location.y)
```

    60.0 40.0

我会在完善 Location 类后添加更多的预设 pitch，更加方便转换。

目前支持的 type 仅有 shot 和 pass，支持的数据源也仅是 statsbomb，同时还有一个 fusion-events 的调试项目，在这里可以通过网络请求获取一些网站，比如 understat 的 events 进行操作。之后的工作重点便是添加更多的事件类型，添加更多的事件状态，添加更多的字段，比如 shot 预设计算 distance 和 angle, 以及不断调整它们之间的兼容性，更多的 loaders。这个库的难点不在于复杂度，而在于取舍，和更方便的使用。大概会用一年的时间让他变得可用吧。
