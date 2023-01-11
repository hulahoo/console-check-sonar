"""Config for logger"""

from sys import stdout
from logging import DEBUG, Formatter, getLogger, StreamHandler

formatter = Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S',
)

logger = getLogger('console_api')
logger.setLevel(DEBUG)

console = StreamHandler(stdout)
console.setLevel(DEBUG)
console.setFormatter(formatter)

logger.addHandler(console)
