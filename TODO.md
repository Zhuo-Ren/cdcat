注释
- 对包含关系不做处理。例如[“两架失事客机”]和["两次事故中的客机"]是共指的。
  但和[“埃航客机”, "狮航客机"]不是共指的，这是包含关系。如果不这样处理，
  就会遇到共指爆炸的问题。例如["埃航客机"]和["客机"]、["失事客机"]共指，且
  ["狮航客机"]和["坠海客机"]共指，那么有6种组合都和["两架失事客机"]共指，而
  这些共指显然是重复的。应该用instanc间的包含关系来描述。
  
待完成：
- 离散指称的标注。
    - 目前是node["id"][支持](<to20221228234749>)，例如"n:folder1/text1.raw.txt:1-2;5-7"，但node_obj.text[不支持](<to20221228234911>)，因为raw_obj.__getitem__()[不支持](<to20221228234825>)。
- 配置文件中的PRELIMINARY_CODE目前只在对象构造函数中执行一遍，因此需要把执行结果注册到[builtins.__dict__](<to20221228234933>)。理想的方法是lable对象初始化和每次赋值时，先执行一遍。
- 完善单元测试。
