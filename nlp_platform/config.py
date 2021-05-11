import os

root_path = os.path.abspath(os.path.dirname(__file__)).split('\\cdcat\\')[0]
root_path += "\\"

root_path = r"%scdcat"%root_path
data_path = r"%s/data"%root_path
