class dog:
    def __init__(self):
        self.arg = 1
    def fun1(self, param1:"dog"):
        if __name__ == '__main__':
            param1.arg = 2
        print(1)

wang = dog("huahua")
wang.fun1()
