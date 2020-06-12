import urllib.robotparser
from urllib.parse import urlparse
import os
from my_queue import dictionar_robot
dstPath= 'output'
def get_robots(baselink):
    parser = urllib.robotparser.RobotFileParser()
    domain = urlparse(baselink).netloc
    parser.set_url(baselink + '/robots.txt')
    try:
        parser.read()
        dictionar_robot[domain] = parser
    except:
            dictionar_robot[domain] = None
            parser = None
    return parser


