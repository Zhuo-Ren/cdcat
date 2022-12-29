cdcat v1 是2020.9.11的版本。
cdcat v2 是2020.10.20的版本。
cdcat v3 正在开发。

# install
python 3.7
pytest 7.2.0
pytest-html 3.2.0
flask 2.2.2

# config
在使用项目中的instance、node等数据结构前，必须进行配置！config.py负责管理所有配置文件。
## center config
最核心的配置文件称为center config，通过以下方式引入：
```python
from nlp_platform.center.config import Config
Config.load_config(config_name="center_config", config_dir="config_label.json")  
# 这意味着把当前目录下的config_label.json作为center config读入。
```
center config长这样：
```json
{
  "Instance": {},
  "Node": {},
  "Relation": {}
}
```
依次分别对应instance(pool)，node(pool)和table(pool)的配置。我们在讲instance(pool)，node(pool)和table(pool)时分别详述。

# center
## Corpus
corus.py中定义了最顶层的数据类型Corpus。Corpus对象有raw，tp，np，ip四个属性，分别对应Raw对象（存储文本），TablePool对象（存储表），NodePool对象（存储token、mention等直接对应文本的东西）和InstancePool对象（存储instance等不直接对应文本的东西）。
## Instance

### Instance.config
使用Instance类前先要配置center config。Instance类的静态属性config保存center config中关于instance的那部分。center config中针对instance的配置长这样：
```json
{
  "Instance": {
        "PRELIMINARY_CODE": "import datetime \nimport random",
        "LABELS": {
            "id": {
                "required": "True",
                "type": "SimpleLabel",
                "value_type_hint": "isinstance(value, str)",
                "value_init": "'i:%s%03d'%(datetime.datetime.now().strftime('%Y%m%d%H%M%S%d'),random.randint(0,999))"
            },
            "desc": {
                "required": "True",
                "type": "SimpleLabel",
                "value_type_hint": "isinstance(value, str)",
                "value_init": "self['owner']['id']['value']"
            },
            "type": {
                "type": "SimpleLabel",
                "value_type_hint": "isinstance(value, str)",
                "value_init": "'none'",
                "value_optional": ["none", "entity", "event"]
            }
        }
  
  }
}
```
这里主要配置Instance对象应该具有什么标签，如上例就是说一个Instance类的实例应该具有id，desc，type三个标签。具体到每个标签：
* required项：
    * 本项可选。
    * 值域：字符串“True”或“False”。
    * 说明当前标签是否必填。如必填就是True（如id）；如可选就是False，或直接不写这项（如type）。
* type项：
    * 本项必选。
    * 值域：字符串。
    * 说明标签类型。在labeltypes.py的最末尾有一个列表，列出当前可用的所有标签类型，选填即可。
* value_type_hint项： 
    * 本项必选。
    * 值域：字符串。
    * 在对一个此类标签进行赋值时，会自动进行值的合法性检测，本项用于说明如何判定标签值的合法性。本项的值是一个字符串，这个字符串的内容是可执行的python语句。这个python语句可以通过关键字value来获取当前标签的值，然后进行判定，并返回True或False。返回True就认为赋值成功。
* value_optional项：
    * 本项可选。
    * 值域：字符串。
    * 说明标签值的可选项，例如“性别”标签的值只能从“男”和“女”中选择。作用就是当在GUI上展示时，通过下拉菜单展示可选的值。
    
### instance.pool

一个实例instance_obj通常都会注册到一个实例池instancepool_obj。

保存如果一个Instance obj被添加到某个InstancePool obj，则this_instance_obj.pool = this_instancepool_obj。否则为None。

instance_obj和instancepool_obj的关系是双向的：`instancepool_obj["id_of_a_instance_obj"] = instance_obj`，同时`instance_obj.pool = instancepool_obj`。

设置instance_obj.pool有两种方法：
* 可以通过Instance类的构造函数的pool参数来指定一个instance_obj要注册到哪个instancepool_obj，通过这种方式注册时，会自动维护双向关系，即不但实现`instance_obj.pool = instancepool_obj`，而且自动实现`instancepool_obj["id_of_a_instance_obj"] = instance_obj`。
* 可以直接赋值instance_obj.pool，但是这样不会自动维护双向关系，即只实现`instance_obj.pool = instancepool_obj`，而不实现`instancepool_obj["id_of_a_instance_obj"] = instance_obj`。

### instance[标签名]

Instance类是dict类的子类。

如果你在center config中为instance定制了某个标签，那么Instance类实例就会具有这个标签，并可以通过字典的形式访问：`a_instance_obj["name_of_label"] = label_obj`，`a_instance_obj["name_of_label"]["value"]= "value_of_this_label"`。具体参见Label类的介绍。

### instance.to_info()
