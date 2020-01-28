import unittest
from rain import Reader
import time

class TestConnect(unittest.TestCase):
    reader = Reader()  #("tmr:///com4") #("tmr://10.100.10.60:8046")
    #reader.Connect()