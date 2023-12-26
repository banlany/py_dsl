from interface import *
from interpreter import *


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
runtime = Interpret(script_path, user_path)
runtime.run()
runtime.toFile("config/user.txt")
#print(runtime.env.record)
