from interface import *
import re
import json
class Parsers:
    """
    文法 语法分析
    """
    def __init__(self, path="config/exp.txt"):
        try:
            with open(path, "r", encoding="utf-8") as f:
                self.code = f.read()
            self.ast = Ast()
            f.close()
        except:
            print("文件不存在")
            self.code = ""
            self.ast = Ast()
        self.curLine = 1
        self.curStep = ""
        self.error = []
    def parse(self,path="config/exp.txt"):
        """
        语法分析
        :param path: the path of the script
        """
        self.__init__(path)
        if type(self.code)!= str:
            #print('expect to load str')
            self.error.append('expect to load str')
            return
        lineList = self.code.split("\n")#按行分割
        for line in lineList:
            
            eline = line.strip()

            if len(eline) == 0:
                self.curLine += 1
                continue
            if eline[0] == '#':
                self.curLine += 1
                continue
            self.parseLine(eline)
            self.curLine += 1
        self.valide()
        return self.ast
    
    def parseLine(self,line):
        """
        解析一行
        :param line: one row of the script
        """
        strings = re.findall("\"(.*?)\"",line) #获取脚本文件字符串
        
        token = line.split(" ")
        self.parseToken(token, strings)

    def parseToken(self,token:[], strings:[]):
        """
        解析一个token
        :param token: list of the line divided by ' '
        :param string : get the string in " "
        """
        token_key = token[0].lower()#转为小写
        s = ''.join(token[1:]) #取剩余内容
        if token_key == 'step':
            self.stepProc(s)
        elif token_key == 'branch':
            self.branchProc(s,strings)
        elif token_key == 'listen':
            self.listenProc(s)
        elif token_key == 'speak':
            self.speakProc(s,strings)
        elif token_key == 'silence':
            self.silenceProc(s)
        elif token_key == 'compute':
            self.computeProc(s)
        elif token_key == 'default':
            self.defaultProc(s)
        elif token_key == 'exit':
            self.exitProc()
        else:
            print('error token:',token)

    #step ok
    def stepProc(self,code:str):
        """
        process line startwith step or upper
        :param code: line without the first word
        """
        stepId = code.split(' ')
        if len(stepId)!= 1 or stepId[0] == '':
            error="Step 句柄定义函数格式错误,位置："+str(self.curLine)+"行。"
            self.error.append(error)
        else:
            id = stepId[0]
        self.ast.hashT[self.curLine] = id
        if len(self.ast.hashT)== 1:#语法树第一个step
            self.ast.entry = id
        self.curStep = id
    #branch "hello",hellopro
    def branchProc(self,code:str,strings:list):
        """
        process line start with branch or upper
        :param code: line without the first word
        :param strings: list of string type in script
        """
        args1 = code.split(',')
        args = []
        for a in args1:
            a = a.replace('"','')
            args.append(a)
        #print(args)
        if len(args)!= 2 or args[0] == '' or args[1] == '':
            error = "Branch 句柄定义函数格式错误,位置："+str(self.curLine)+"行。"
            self.error.append(error)
        else:
            node = Branch()
            node.answer = args[0].replace('"','')
            node.goto = args[1].strip()
            node.line = self.curLine
            self.ast.hashT[self.curLine]=node
    #speak &name + "bubu"
    #speak "ddddd" + &class + "eeeeee"
    def speakProc(self,code:str,strings:list):
        """
        process line start with speak or upper
        :param code: line without the first word
        :param strings: list of string type in script
        """
        args1 = code.split('+')
        args=[]
        #print(strings)
        for a in args1:
            a = a.replace('"','')
            args.append(a)
        #print(args)
        if len(args)!=0:#长度不为0
            # if len(args)== 2:
            #     self.ast.varT[name[1:].strip()]=''
            #     node = Speak()
            #     node.args.append(name[1:].strip())
            #     for i in strings:
            #         node.args.append(i.strip()) 
            # elif len(args)== 3:
            #     self.ast.varT[name2[1:].strip()]=''
            #     node = Speak()
            #     node.args.append(name2[1:].strip())
            #     for i in strings:
            #         node.args.append(i.strip())
            # else:
            #     print("Speak 句柄定义函数格式错误,位置："+str(self.curLine)+"行。")
            #print(args)
            node = Speak()
            t =0
            for a in args:
                if a[0]=='&':
                    self.ast.varT[a[1:].strip()]=''
                    node.args.append(a)
                else:
                    node.args.append(strings[t].replace('"',''))
                    t+=1
                
            node.line = self.curLine
            self.ast.hashT[self.curLine]=node
            #print(node.args)
        else:
            error = "Speak 句柄定义函数格式错误,位置："+str(self.curLine)+"行。"
            #print("Speak 句柄定义函数格式错误,位置："+str(self.curLine)+"行。")
            self.error.append(error)
    #listen 1
    def listenProc(self,code:str):
        """
        process line start with listen or upper
        :param code: line without the first word
        
        """
        args = code.split(' ')
        if len(args)!= 1 or args[0] == '':
            error = "Listen 句柄定义函数格式错误,位置："+str(self.curLine)+"行。"
            #print("Listen 句柄定义函数格式错误,位置："+str(self.curLine)+"行。")
            self.error.append(error)
        else:
            time = int(args[0])
            node = Listen()
            node.time = time
            node.line = self.curLine
            self.ast.hashT[self.curLine]=node
    #silence silenceppp
    def silenceProc(self,code:str):
        """
        process line start with silence or upper
        :param code: line without the first word
     
        """
        args = code.split(' ')
        if len(args)!= 1 or args[0] == '':
            error = "Silence 句柄定义函数格式错误,位置："+str(self.curLine)+"行。"
            #print("Silence 句柄定义函数格式错误,位置："+str(self.curLine)+"行。")
            self.error.append(error)
        else:
            next = args[0]
            node = Silence()
            node.goto = next
            node.line = self.curLine
            self.ast.hashT[self.curLine]=node
    # compute &balance + input,chargeproc
    def computeProc(self,code:str):
        """
        process line start with compute or upper
        :param code: line without the first word

        """
        args = code.split(',')
        if len(args)!= 2 or args[0] == '' or args[1] == '':
            error = "Compute 句柄定义函数格式错误,位置："+str(self.curLine)+"行。"
            #print("Compute 句柄定义函数格式错误,位置："+str(self.curLine)+"行。")
            self.error.append(error)
        else:
            goto = args[1]
            ct = args[0]
            args = ct.split('+')
            if len(args)!= 2 or args[0] == '' or args[1] == '':
                error = "Compute 句柄定义函数格式错误,位置："+str(self.curLine)+"行。"
                #print("Compute 句柄定义函数格式错误,位置："+str(self.curLine)+"行。")
                self.error.append(error)
            else:
                balance = args[0].strip()[1:]
                input = args[1].strip()
                
                self.ast.varT[balance]=0
                self.ast.varT[input]=0
                node = Compute()
                node.var = balance
                node.goto = goto
                node.line = self.curLine
                self.ast.hashT[self.curLine]=node
    #default xxxxx
    def defaultProc(self,code:str):
        """
        process line start with default or upper
        :param code: line without the first word

        """
        args = code.split(' ')
        if len(args)!= 1 or args[0] == '':
            error = "Default 句柄定义函数格式错误,位置："+str(self.curLine)+"行。"
            #print("Default 句柄定义函数格式错误,位置："+str(self.curLine)+"行。")
            self.error.append(error)
        else:
            next = args[0]
            node = Default()
            node.goto = next
            node.line = self.curLine
            self.ast.hashT[self.curLine]=node
    #exit 
    def exitProc(self):
        """
        process line start with exit or upper
        """
        node = Exit()
        node.line = self.curLine
        self.ast.hashT[self.curLine]=node
        self.ast.exit.append(self.curLine)
    def valide(self):
        """
        check the script
        """
        if self.ast.hashT == {}:
            error = "语法分析错误，未定义任何语句。"
            #print("语法分析错误，未定义任何语句。")
            self.error.append(error)
        elif len(self.ast.exit)==0:
            error = "语法分析错误，未定义任何退出条件。"
            #print("语法分析错误，未定义任何退出条件。")
            self.error.append(error)
            



if __name__ == "__main__":
    
    x = Parsers()
    x.parse()
    print(x.ast.hashT)
    json_str = json.dumps(dict(x.ast))
    print(json_str)
    print(x.ast.varT)
    