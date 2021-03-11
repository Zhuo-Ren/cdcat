from nlp_plantform.plug_in.input.ntree_from_pickle import input_ntree_from_pickle
from nlp_plantform.config import data_path

root = input_ntree_from_pickle(path = data_path + r'/ntree.pkl')
info = root.to_info()

root.info_to_file()

"""
{
    (): {
        position: (),
        parent: None,
        child: [
            (0),
            (1),
        ],
        labels: {
            "key": value,
        }
    },
    (0,): {
        position: (),
        parent: (),
        child: [
            (0, 0),
            (0, 1),
        ],
        labels: {
            "key": value,
        }
    },
    (1,): {
    
    },
    ...,
    (40,): {
    
    },
    (0, 0): {
    
    },
    (0, 1): {
    }
}
"""
