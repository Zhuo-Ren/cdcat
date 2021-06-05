class Raw(dict):
    def __getitem__(self, key):
        def dict_get(obj_dict, objkey, default):
            tmp = obj_dict
            for k, v in tmp.items():
                if k == objkey:
                    return v
                else:
                    if type(v) is dict:
                        ret = dict_get(v, objkey, default)
                        if ret is not default:
                            return ret
            return default

        if key[:2] == 'n:':
            search_content = []
            search_path = key.split(':')[1]
            search_index = key.split(':')[2]
            index_list = search_index.split('-')
            search_file = search_path.split('/')[-1]
            obj_dict = self
            # print(search_path)
            ret = dict_get(obj_dict, search_file, None)
            if int(index_list[0]) < len(ret) and int(index_list[1]) < len(ret) + 1:
                for i in range(int(index_list[0]), int(index_list[1])):
                    search_content.append(ret[i])
                search_content = ''.join(search_content)
                return search_content
            else:
                print("索引范围不正确")
                return KeyError
        elif '/' in key:
            l = key.split('/')
            a = self
            for i in l:
                a = a[i]
            return a
        elif '\\' in key:
            l = key.split('\\')
            a = self
            for i in l:
                a = a[i]
            return a
        else:
            return super().__getitem__(key)
