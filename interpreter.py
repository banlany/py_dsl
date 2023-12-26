from parsers import *
from interface  import *
from wait import *
import copy
class Interpret:
    """
    解释器 类型
    :param path1 :脚本路径
    :param path2 :用户路径
    """
    def __init__(self,path1="config/exp.txt",path2 = "config/user.txt"):
        lexer = Parsers(path1)
        lexer.parse(path1)
        self.env = Env()
        self.env.varT = copy.deepcopy(lexer.ast.varT)
        self.loadUser(path2)
        self.ast = lexer.ast
        entry = self.ast.entry
        entryLine = findKey(self.ast.hashT,entry)
        self.env.record = []
        # self.record = []
        if entryLine == -1:
            print("未找到入口,请检测文件")
        self.env.step = entryLine+1#进入语法树
        
    
    def loadUser(self,path2):
        """
        加载用户文件
        :param path2 : the path of the user's config
        """
        try:
            with open(path2, "r", encoding="utf-8") as f:
                conf= f.read()
            self.env.user = conf.split("\n")[0] #用户名
            self.env.balance = float(conf.split("\n")[1])#余额
            self.env.varT['name'] = self.env.user
            self.env.varT['balance'] = self.env.balance
            f.close()
        except:
            print("用户文件不存在，使用默认文件")
    def run(self):
        """
        运行解释器
        """
        
        silenceFlag = False
        cin = ""
        while type(self.ast.hashT[self.env.step]) != type(Exit):
            self.saveRecord()
            line = self.ast.hashT[self.env.step]
            if type(line)== type(Speak()):
                val  = line.args
                #print(val)
                message = ''
                for x in val:
                    #print(x)
                    if x[0] == '&':
                        var = x[1:]
                        value = self.env.varT[var]
                        message+=str(value)
                    else: 
                        message+=x
                
                print('bot :  {message}'.format(message=message))
                m = []
                m.append(message)
                m.append('bot')
                self.env.record.append(m)
                try:
                    if type(self.ast.hashT[self.env.step+1]) == type(Listen()):
                        cin = input_with_timeout(self.ast.hashT[self.env.step+1].time)
                        m = []
                        m.append(cin)
                        m.append('user')
                        self.env.record.append(m)
                    else:
                        tp = self.ast.hashT[self.env.step+1]
                        if type(tp) == type(Branch()) or type(tp) == type(Default()) or type(tp) == type(Compute()):
                            cin = input()
                            m = []
                            m.append(cin)
                            m.append('user')
                            self.env.record.append(m)
                            #print(cin)
                        else:
                            #print("程序结束")
                            return -1
                except:
                    print('error speak')
                
                self.env.step += 1
            elif type(line)== type(Listen()):
                if cin == -1:
                    silenceFlag = True
                else:
                    silenceFlag = False
                self.env.step += 1
            elif type(line)== type(Branch()):
                if silenceFlag == False:
                    #print('answer:'+str(line.answer))
                    #print('cin:'+str(cin))
                    if line.answer == cin: 
                        #print('yes')
                        if findKey(self.ast.hashT,line.goto) == -1:
                            print("branch分支错误,位置："+str(self.env.step)+'行')
                        else:
                            self.env.step = findKey(self.ast.hashT,line.goto)+1
                            #print('前往'+str(self.env.step))
                    else:
                        self.env.step += 1
                else:
                    self.env.step += 1
            elif type(line)== type(Silence()):
                if silenceFlag == True:
                    if findKey(self.ast.hashT,line.goto) == -1:
                        print("silence指向错误,位置："+str(self.env.step)+'行')
                    else:
                        self.env.step = findKey(self.ast.hashT,line.goto)+1
                else:
                    self.env.step+=1
            elif type(line)== type(Compute()):
                try:
                    #print(cin)
                    cin = float(cin)
                    #print(self.env.varT)
                    self.env.varT[line.var]+=cin
                    #print(self.env.varT[line.var])
                    self.env.balance=self.env.varT[line.var]#增加计算值
                except:
                    print('error type,need to be num')
                    return -1
                else:
                    self.env.step += 1
            elif type(line)== type(Default()):
                self.env.step = findKey(self.ast.hashT,line.goto)+1
                silenceFlag = 0
            elif type(line)== type(str):
                print('error code')
                return -1
            else:
                return -1
            if self.env.step == 0:
                return -1
    def toFile(self,path="config/user.txt"):
        with open(path,'w',encoding="utf-8") as f:
            f.write(str(self.env.user)+'\n')
            f.write(str(self.env.balance))
        f.close()
    def saveRecord(self,path="record/record.txt"):
        with open(path,'w',encoding="utf-8") as f:
            f.write(str(self.env.user)+'\n')
            f.write(str(self.env.record)+'\n')
            f.write(str(self.env.step))
        f.close()
            


def findKey(dict:dict,value):
    """
    由value找key
    :param dict :the dictionary
    :param value :value want to find
    :return var :the key of value
    """

    for key in dict.keys():
        if dict[key] == value:
            return key
    return -1



if __name__ == "__main__":
    path = "config/exp.txt"
    c1 = Interpret()
    #print(c1.env.varT)
    c1.run()
    c1.toFile()
    