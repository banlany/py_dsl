import threading
import sys


class InputThread(threading.Thread):
    def __init__(self, prompt):
        super().__init__()
        self.prompt = prompt
        self.input_text = None

    def run(self):
        try:
            self.input_text = input(self.prompt)
        except EOFError:
            pass  # 输入结束符，例如Ctrl+D


def input_with_timeout(x):
    """
    获取输入并计时，当超时时告知用户退出输入

    @param x:time
    @return:input or -1
    """
    input_prompt = ""

    input_thread = InputThread(input_prompt)
    input_thread.start()
    input_thread.join(x)

    if input_thread.is_alive():
        # 如果线程仍在运行，说明超过了x秒
        print("回答超时，请按回车键退出程序")
        return -1
    # else:
    #     print("Continuing program...")
    try:
        user_input = input_thread.input_text
        return user_input
    except:
        return -1

def input_with_tieout(x):
    """
    获取输入并计时，当超时时告知用户退出输入

    @param x:time
    @return: input or -1
    """
    y = None
    return y
# 示例调用
if __name__ == '__main__':
    result = input_with_timeout(10)
    print(result)
    for i in range(1, 10):
        i = i + 1
        print(i)