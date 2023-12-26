# 基于领域特定语言的客服机器人设计与实现

## 特点领域情景描述

本程序提供了一种简单的文法来描述自助话费机器人的应答逻辑。文法实现了查询、应答、等待回复等用户最常使用的功能。

## 特定领域脚本语言定义

### 命令解释

所有的命令均支持大小写通用；

+ step（STEP）：函数定义头，其后跟一个函数名，到下一个step内容为此函数语句内容。

  ```
  step pro1
     ······
     ······
     ······
  step pro2
  ```

+ speak ：bot回答内容的命令，默认为字符串，多个字符串可以使用‘+’进行连接，注意必须要包含一个变量。

  ```
  speak &name + " is not a valid option, type to back:"
  speak  "感谢您的使用！" +&name+  "再见"
  ```

+ listen & silence: 聆听命令，silence后面跟一个数字，即等待时间，超时未输入进入silence 后接的函数。

  ```
  listen 10
  ········
  ········
  silence ty
  ```

+ branch : 分支命令，后面接一个字符串和函数，若输入内容和字符串相同，则跳转到对应的函数。

  ```
  branch "1", pro1
  branch "2", pro2
  ```

+ default :后面跟一个函数，默认跳转，若branch和silence都没有发生跳转，到这一步会进行跳转。

  ```
  default pro1
  ```

+ compute: 计算命令，跟一个变量、符号、输入、解释，将变量和输入进行操作。

  ```
  compute &balance + input,compute
  ```

+ exit: 退出命令，单词，读到此句结束并退出分析。

  ```
  step c1
      ······
  exit
  ```

### 注释

使用‘#’开头的行定义为注释，解析器忽略此行，但位置仍然记录。

### 变量

使用&开头的字符视为变量，默认为name和balance。

### 额外规定

+ 脚本必须有入口和出口，入口默认为第一项函数，出口为exit语句的位置

## 程序设计

### 风格

#### 代码注释风格

采用reStructuredText风格：

类有清晰的注释，类方法注明功能、参数、返回值

```python
def loadUser(self,path2):
        """
        加载用户文件
        :param path2 : the path of the user's config
        """
        
 class Interpret:
    """
    解释器 类型
    :param path1 :脚本路径
    :param path2 :用户路径
    """
```

#### 命名风格

- 类名统一使用大驼峰命名法，如： `Interpret, Parsers`等
- 类的公开接口和变量使用小驼峰命名法，如： `loadUser，silenceFlag`等

### 结构设计

程序结构分为4块：

依赖关系如下图

```
dsl-------->interface<---------+
|                /|\           |
|                 |            |
|                 |            |
|                 |            |
|               parsers        |
|                /|\           |
|                 |            |
|                 |            |
+----------->interpreter-------+
```

dsl : 主程序，运行起整个程序；

interface：结构体定义，定义了整个dsl所需的主要的类；

parsers：对脚本进行文法分析，将代码块分析为语法树；

interpret：解释语法树，传入输入并打印输出。

### 功能

本程序实现了对dsl文法脚本的解析运行，能保留运行痕迹，并且为功能拓展提供接口。

### 数据结构设计

#### 语法树

语法树由类Ast管理：

```python
class Ast:
    """
    语法树 类型
    """
    def __init__(self):
        self.varT = {} #语法树变量表
        self.hashT = {}#语句列表
        self.entry = "" #入口
        self.exit = [] #出口

```

记录了脚本变量表、每一句的语句类型，入口、出口信息。

hashT字典以行号为键，存放了每一句对应的类：

```python
#{1:Speak(),2:Listen()}
```

不同的类在分析时有不同的跳转逻辑，所有信息均记录在interface.py中。

#### 运行环境

运行环境由Env来管理：

```python
class Env:
    """
    环境类型
    """
    def __init__(self):
        self.varT = {} #环境变量表
        self.step = 0 #当前step
        self.user = "" #用户名称
        self.balance = 0 #余额
        self.record = [] #聊天记录
        self.cin = ""#上一个输入
```

每个interpret实体下初始化一个环境，同一脚本语言的interpret共享一个语法树，实现了环境的单独存放与语法树的共用，有提供多线程服务的潜力。

### 接口

#### 程序间接口

不同文件间使用python的导入：

```python
from parsers import *
from interface  import *
from wait import *
```

函数的调用需要使用类方法：

```python
if __name__ == "__main__":
    path = "config/exp.txt"
    c1 = Interpret()
    #print(c1.env.varT)
    c1.run()
    c1.toFile()
```

程序报错不打印，将错误信息添加到相应结构体中，供高层程序调用：

```python
if len(stepId)!= 1 or stepId[0] == '':
            error="Step 句柄定义函数格式错误,位置："+str(self.curLine)+"行。"
            self.error.append(error)
```

与拓展程序之间数据传输使用类来管理,可以更好的序列化为json，如：

```python
class Answer:
    """
    回答类型
    """
    def __init__(self):
        self.args = ""#文本
        self.end = False#结束标识
        self.listen = 0#监听时间

```



#### 人机接口

本程序使用控制台终端实现人机接口，通过重写input_with_timeout( )方法即可实现人机功能的拓展。

此外本程序实现了一个简单的前端网页界面（位置：html/index.html），但是由于端口原因，服务器连接总是失败。

![image-20231225112108255](C:\Users\22230\AppData\Roaming\Typora\typora-user-images\image-20231225112108255.png)

### 测试

test.py文件，使用自动化测试框架pytest

测试覆盖范围：

+ Interpret模块：配置文件载入，语法树解释，运行结果
+ Parsers模块：脚本文件载入，进行文法分析，语法树生成
+ wait 函数：线程交互，能否超时返回
+ 总流程：按dsl流程运行，比对结果

#### 测试桩

对于单个模块的测试均需要构造一个临时的其它模块， 或是提供一个临时的语法数测试执行。

本测试使用测试桩来代替模块Parsers，能返回一个正确的分析之后的语法树，在词语树基础上进行程序运行。

#### 自动化测试

测试文件引入自动化框架pytest，只需要运行命令即可自动化测试文件内函数：

```powershell
PS > pytest test.py
========================================================================== test session starts ===========================================================================
platform win32 -- Python 3.9.18, pytest-7.4.0, pluggy-1.0.0
rootdir: F:\repository\py_dsl\utils
plugins: anyio-3.5.0
collected 5 items

test.py .....                                                                                                                                                       [100%]

=========================================================================== 5 passed in 0.06s ============================================================================ 
```

## 使用说明

本程序使用python3.9环境编写。

安装依赖：

```powershell
pip install pytest
pip install re
pip install json
```

脚本文件：

字符串编写，行之间用‘\n’分割。

用户文件：

为两行，第一行为用户昵称，第二行为用户的余额。
