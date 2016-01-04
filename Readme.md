Adhoc Python SDK
==================

安装
------------------

SDK依赖于 [Requests](http://docs.python-requests.org/en/latest/user/quickstart/)。
依赖和 SDK 都可以通过 pip 安装：

```
pip install requests
pip install git+https://github.com/appadhoc/adhoc_python_sdk.git
```


示例
----------------

```
from adhoc import AdhocTracker

# 初始化 SDK，其中 "app_key" 换成从后台得到的 app key。
tracker = AdhocTracker("app_key")

# 获取模块开关，其中 client_id 是用户唯一标识，可以是用户 ID 等。
flags = tracker.get_flags("client_id")
print(flags)

# 上报对应的统计数据
tracker.inc_stat("client_id", "stat1", 2.0)

```


注意
---------------

获取模块开关和上报统计数据都是通过网络。所以有可能失败或阻塞整个线程。
如果有需要可以将调用代码包装在异步请求或线程池中以避免阻塞整个应用。
