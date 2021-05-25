class Raw(dict):
    def __getitem__(self, k):
        if k: # 符合格式
            pass
        else:
            return super().__getitem__(k)
