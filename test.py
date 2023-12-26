import pytest
from parsers import *
from interpreter import *
from interface import *
from wait import *
import time
import sys

def test_parser():
    """
    Test the parser
    """
    parser = Parsers()
    parser.parse()
    ast =  Ast()
    ast = parser.ast
    print(ast.hashT)
    right = {}
    right[1] = "hello"
    right[2] = Speak()
    right[3] = Listen()
    right[4] = Branch()
    right[5] = Branch()
    right[6] = Silence()
    right[7] = Default()
    right[9] = "ty"
    right[10] = Speak()
    right[11] = Exit()
    right[12] = "sj"
    right[13] = Speak()
    right[14] = Compute()
    right[15] = Speak()
    right[16] = Default()
    right[17] = "c1"
    right[18] = Speak()
    right[19] = Exit()
    for key in ast.hashT.keys():
        assert type(ast.hashT[key]) == type(right[key])
def test_zhuang(capsys):
    """
    测试桩,同时测试interpret功能
    """
    ast = Ast()
    ast.hashT = {}
    ast.hashT[1]= 'hello'
    ast.hashT[2]= Speak()
    ast.hashT[2].args = ['请问', '&name', '你要', '进行什么？充值请按2，退出请按1']
    ast.hashT[3]= Exit()
    i = Interpret()
    i.ast.hashT = ast.hashT
    i.run()
    captured = capsys.readouterr()
    assert captured.out == "bot :  请问hhye你要进行什么？充值请按2，退出请按1\n"
def test_interpret(capsys):
    """
    测试interpret功能
    """
    i = Interpret('config/exp1.txt','config/user.txt')
    captured = capsys.readouterr()
    assert captured.out == ""
def test_wait(capsys):
    
    x = input_with_tieout(10)
    print(x)
    captured = capsys.readouterr()
    assert captured.out == "None\n"
def test_all(capsys):
    stdout = sys.stdout
    stdin = sys.stdin
    try:
        with open("config/config.txt", "r") as f:
            config = f.read()
        config = config.split("\n")
        script_path = config[0]
        user_path = config[1]
        f.close()
    except:
        print("Error: config not found!")
        script_path = "config/exp.txt"
        user_path = "config/user.txt"
    i = Interpret(script_path,user_path)
    with open('./test/out.txt') as f:
            out = f.readline()
    with open('./test/in2.txt') as f:
            example_out = f.readline()
    assert out == 'bot :  hhyethank you for using our service'

#运行命令： pytest test.py
