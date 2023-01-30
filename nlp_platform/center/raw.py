class Raw(dict):
    #字典的子类，存储文件路径与文件名
    def __getitem__(self, key):
        def dict_get(obj_dict, objkey, default):
            tmp = obj_dict
            if '/' not in objkey:
                return tmp[objkey]
            elif '/' in objkey:
                l = objkey.split('/')
                a = obj_dict
                for i in l:
                    a = a[i]
                return a

            elif '\\' in objkey:
                l = objkey.split('\\')
                a = obj_dict
                for i in l:
                    a = a[i]
                return a
            return default
        if key[:2] == 'n:':
            search_content = []
            search_path = key.split(':')[1]
            search_index = key.split(':')[2]
            index_list = search_index.split('-')
            obj_dict = self
            # print(search_path)
            ret = dict_get(obj_dict, search_path, None)
            if int(index_list[0]) < len(ret) and int(index_list[1]) < len(ret) + 1:
                for i in range(int(index_list[0]), int(index_list[1])):
                    search_content.append(ret[i])
                search_content = ''.join(search_content)
                return search_content
            else:
                raise RuntimeError("索引范围不正确")  # return KeyError
        elif '/' in key:  # 例如 1/10ecb
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

    def to_info(self, key):
        def dict_get(obj_dict, objkey, default):
            tmp = obj_dict
            if '/' not in objkey:
                return tmp[objkey]
            elif '/' in objkey:
                l = objkey.split('/')
                a = obj_dict
                for i in l:
                    a = a[i]
                return a

            elif '\\' in objkey:
                l = objkey.split('\\')
                a = obj_dict
                for i in l:
                    a = a[i]
                return a
            return default
        if key[:2] == 'n:':
            search_content = []
            search_path = key.split(':')[1]
            search_index = key.split(':')[2]
            index_list = search_index.split('-')
            search_file = search_path.split('/')[-1]
            obj_dict = self
            # print(search_path)
            search_middle_path=search_path.split('/')
            search_middle_path_len=len(search_middle_path)
            ret = dict_get(obj_dict, search_path, None)
            if int(index_list[0]) < len(ret) and int(index_list[1]) < len(ret) + 1:
                search_token = set()
                token_dict = {}
                temp_token = 1
                ret_index = 0
                for i in ret:
                    token_dict.update({ret_index: temp_token})
                    ret_index += 1
                    if i == " ":
                        temp_token += 1
                for j in range(int(index_list[0]), int(index_list[1])):
                    search_token.add(token_dict[j])
                token_list = []
                for i in search_token:
                    token_list.append(i)
                token_str=""
                for i in token_list:
                    token_str=str(i)+","
                return token_list

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
            return self.to_info(key)
