import os
from nlp_plantform.center.nodetree import NodeTree
from nlp_plantform.plug_in.input.ntree_from_string_plaintext_form import input_from_string_plaintext_form

def input_ntree_from_file(filePath: str) -> NodeTree:
    """ read a plain text file, and genera the node.

    :param filePath: A path string of a plain text file.
    :return: A node corresponding to the file.
    """
    # param detection
    if not os.path.isfile(filePath):
        raise RuntimeError("the input path is not of a file")
    # get content of the file
    with open(filePath, "r+", encoding='utf8') as f:
        fileStr = f.read()
    # get basename of the file
    fileBasename = os.path.basename(filePath)
    # create the node
    node = input_from_string_plaintext_form(fileStr)
    node.add_label({"file": True})
    #
    return node
