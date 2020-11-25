'''
自定义异常
'''

class AllocateInstancepoolError(Exception):
    def __init__(self, reason):
        self.reason = reason
