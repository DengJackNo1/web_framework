import logging

logger = logging.Logger('MyServer', level=logging.ERROR)

# fh = logging.FileHandler('log.log', 'a', encoding='utf-8')
sh = logging.StreamHandler()
formatter = logging.Formatter(
    fmt='%(asctime)s -->> %(name)s ->%(levelname)s ->>%(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)
# fh.setFormatter(formatter)
sh.setFormatter(formatter)
# logger.addHandler(fh)
logger.addHandler(sh)
