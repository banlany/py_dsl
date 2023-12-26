class Speak:
    """
    speak 类型
    """
    def __init__(self):
        self.type = ""#类型
        self.args = []#内容
        self.line = 0 #行号

class Listen:
    """
    listen 类型

    """
    def __init__(self):
        self.time = 0#时间
        self.line = 0#行号

class Branch:
    """
    branch 分支类型
    """
    def __init__(self):
        self.answer = ""#接收的内容
        self.goto  = ""#跳转分支id
        self.line = 0 #行号

class Silence:
    """
    silence 类型
    """
    def __init__(self):
        self.goto = ""#跳转函数的id
        self.line = 0 #行号
class Compute:
    """
    compute 类型
    """
    def __init__(self):
        self.goto = ""#跳转
        self.line = 0 #行号
        self.var = '' #参数
class Default:
    """
    默认 类型
    """
    def __init__(self):
        self.goto = ""#默认函数id
        self.line = 0 #行号
class Exit:
    """
    exit 类型
    """
    def __init__(self):
        self.line = 0 #行号

# class Vartable:
#     """
#     变量表类型
#     """
#     def __init__(self):
#         self.var = {} #变量表字典

class Ast:
    """
    语法树 类型
    """
    def __init__(self):
        self.varT = {} #语法树变量表
        self.hashT = {}#语句列表
        self.entry = "" #入口
        self.exit = [] #出口

class Env:
    """
    环境类型
    """
    def __init__(self):
        self.varT = {} #环境变量表
        self.step = "" #当前stepid
        self.user = "" #用户名称
        self.balance = 0 #余额
        self.record = [] #聊天记录
        self.cin = ""#上一个输入
class Answer:
    """
    回答类型
    """
    def __init__(self):
        self.args = ""#文本
        self.end = False#结束标识
        self.listen = 0#监听时间

class Message:
    """
    消息类型
    """
    def __init__(self):
        self.type = ""#消息类型
        self.content = ""#消息内容
        self.id = ""#消息id



if __name__ == "__main__":
    x = Speak()
    c = Listen()
    d= []
    d.append(x)
    d.append(c)
    dc = Exit()
    dc.line = 1
    print(type(d[0])==Listen)