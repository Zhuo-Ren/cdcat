import logging
logging.basicConfig(
            format='%(asctime)s %(levelname)s:%(name)s:%(message)s',
            level=logging.DEBUG
        )

"""
import logging
import sys

rootLogger = logging.getLogger()  # 如果getLogger函数没有参数，就返回root logger
rootLogger.setLevel(logging.DEBUG)
streamHandler = logging.StreamHandler(stream=sys.stdout)  # sys.stderr
streamHandler.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    fmt='%(message)s', datefmt=None, style='%'
)  # %(levelname)s
streamHandler.setFormatter(formatter)
rootLogger.addHandler(streamHandler)
"""