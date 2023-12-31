# 一些读取环境变量的探讨

## python-decouple

我最早使用，到现在也一直在用的包了，基本覆盖了日常使用的需求，简单，可读性也很好

```python
def test_decoupe_config() -> None:
    foobar = config('FOOBAR')
    assert foobar == 'foobar'

    assert config('NUMBER') == '1'
    assert config('NUMBER', cast=int) == 1

    with pytest.raises(UndefinedValueError):
        assert not config('FOO')

    foo = config('FOO', default=None)
    assert foo is None
```

但是它在一些静态工具里面会丢失类型提示，比如 pyright `foobar = config('FOOBAR')` 会被推断为类型 `bool | Unknown`，以至于每次要正确设置类型的时候需要 `foobar: str | None = config('FOOBAR')`

它的主类 `def __call__(self, *args, **kwargs):`，也不能支持参数的补全提示

## python-dotenv

推荐用法之一是统一调用函数 `load_dotenv()`，它的具体细节是这样：

```python
def set_as_environment_variables(self) -> bool:
    """
    Load the current dotenv as system environment variable.
    """
    if not self.dict():
        return False

    for k, v in self.dict().items():
        if k in os.environ and not self.override:
            continue
        if v is not None:
            os.environ[k] = v

    return True
```

把读取到的 .env 通过 `os.environ[k] = v` 写到环境变量，使用时 `os.getenv()` 读取即可，好处是使用逻辑比较统一，但我个人并不喜欢这样用，因为会污染到环境变量

不过它提供一个用来专门读取 .env 的函数 dotenv_values

```python
def test_dotenv_values() -> None:
    dotenv = dotenv_values('.env')
    foobar = dotenv['FOOBAR']
    assert foobar == 'foobar'

    assert dotenv['NUMBER'] == '1'

    with pytest.raises(KeyError):
        assert not dotenv['FOO']

    foo = dotenv.get('FOO')
    assert foo is None
```

默认是读取 `.env`，也可以传入其他文件名，返回值是一个 dict，使用就和操作 dict 一样，可以通过 `.get` 返回 `str | None`，也可以直接抛出 `KeyError`，很方便。还可以通过解包的形式读取多个配置以及环境变量

```python
config = {
    **dotenv_values(),
    **dotenv_values('.env.test'),
    **os.environ,
}
```

缺点是纯手动，也没有自带的类型转换，其实关系不大，无论是简单的还是复杂的转换无非就是自己多写这行代码还是通过参数传入逻辑的区别。也有单个读取 `get_key()`

```python
def test_dotenv_get_key() -> None:
    foobar = get_key('.env', 'FOOBAR')
    assert foobar == 'foobar'

    foo = get_key('.env', 'FOO')
    assert foo is None
```

```python
def get(key: str) -> str | None:
    if (value := get_key('.env', key)) is not None:
        return value
    return os.getenv(key)
```

缺点还是纯手动。但它依然是使用者最多的包，很适合用来在此基础上开发更多的功能

## pydantic-settings

pydantic-settings 便是使用了 python-dotenv 支持 .env 读取

```python
class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
    )

    FOOBAR: str | None = None
    NUMBER: int | None = None


def test_pydantic_settings() -> None:
    settings = Settings()
    assert settings.FOOBAR == 'foobar'
    assert settings.NUMBER == 1
```

通过 pydantic 优秀的验证和转换，可以实现很好的类型转换。如果项目中使用了 pydantic 可以优先使用它

## starlette.config

starlette.config 在我看来是 python-decouple 最完美的替代品了，而且它和 python-decouple 也算是渊源颇深。用法基本一致

```python
def test_starlette_config() -> None:
    config = Config('.env')
    foobar = config('FOOBAR')
    assert foobar == 'foobar'

    assert config('NUMBER') == '1'
    assert config('NUMBER', cast=int) == 1
    assert config('NUMBER', cast=bool) is True

    with pytest.raises(KeyError):
        assert not config('FOO')

    foo = config('FOO', default=None)
    assert foo is None
```

类型提示，参数补全的问题被解决掉了，同时它还有一个实现的很有意思的 Secret 类用来读取敏感数据

```python
class Secret:
    """
    Holds a string value that should not be revealed in tracebacks etc.
    You should cast the value to `str` at the point it is required.
    """

    def __init__(self, value: str):
        self._value = value

    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        return f"{class_name}('**********')"

    def __str__(self) -> str:
        return self._value

    def __bool__(self) -> bool:
        return bool(self._value)
```

```python
def test_starlette_config_secret() -> None:
    config = Config('.env')
    secret = config('FOOBAR', cast=Secret)
    assert repr(secret) == "Secret('**********')"
    assert str(secret) == 'foobar'
```

没有用加密手段却规避了在调试时的信息泄露。但它的不方便之处在于，不可能为了只使用而安装整个 Starlette。于是大多数时候都是用 python-dotenv 自己写一个读取的类
