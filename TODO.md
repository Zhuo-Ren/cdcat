注释
- 对包含关系不做处理。例如[“两架失事客机”]和["两次事故中的客机"]是共指的。
  但和[“埃航客机”, "狮航客机"]不是共指的，这是包含关系。如果不这样处理，
  就会遇到共指爆炸的问题。例如["埃航客机"]和["客机"]、["失事客机"]共指，且
  ["狮航客机"]和["坠海客机"]共指，那么有6种组合都和["两架失事客机"]共指，而
  这些共指显然是重复的。应该用instanc间的包含关系来描述。
  
待完成：
- node的标签系统配置
  - value_tyep = instance的标签类型
- input和output的格式支持
- debug: 如果curNode已指向一个instance
- 为每个节点添加“来源”属性，以应对以下情况：
    - XXX宣布XXX将XXX
    - 新华社 XXX 报道
  
  这个功能通过node标签系统中，instance类型标签的功能实现。
- instance list可拖动
- ajax期间鼠标暂停

已完成：
- debug：选中文本红色消失
- 翻译配置文件