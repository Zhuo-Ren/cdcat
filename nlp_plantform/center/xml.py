from typing import Dict, List, Tuple, Union
from nlp_plantform.center.new_instance import Instance
from nlp_plantform.center.new_instancepool import InstancePool
from  nlp_plantform.center.nodetree import NodeTree
import xmltodict

"""info的格式如下，包含了instancepool和nodes"""
"""
{
	"instancepool":{
		"0":{},
		"1":{},
		"3":{}

	},
	"nodes":{
		"0":{"child":["0-0","0-1"]},
		"0-0":{},
		"0-1"
	}
}
"""
"""接口"""
def from_xml(xml_path : str) -> Tuple[InstancePool,NodeTree]:
	xml_etree = open(xml_path, 'r')
	xmlStr = xml_etree.read()
	# xmt to dict
	xml_dict = xmltodict.parse(xmlStr)
	"""1建骨架（没有label的node和instance）"""
	p = InstancePool(info=xml_dict["instancepool"], load_label=False)
	"""因为class Node太复杂没讲，所以这句先注释掉"""
	"""rootnood = Node(load_label = False)"""

	"""到目前，所有i和n就都建好了"""
	return Tuple[InstancePool,NodeTree]
