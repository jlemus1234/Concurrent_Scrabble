#!/usr/bin/python -tt
#   bag.py
#
#   COMP 50CP Fall 2018
#   Group Project: Distributed Scrabble
#
#   Modified On: December 1, 2018

""" Purpose: This module holds the implementation of the class Bag"""

import tile
import random
import threading



class Bag:
    """ Creates the bag of tiles needed to ditribute and reimburse players. 
        Contains 98 letters """
    def __init__(self):
        """ Call initialize_bag to add the default 98 tiles to bag """
        self.bag = []
        self.initialize_bag()
        self.lock = threading.Lock()

    def initialize_bag(self):
        """ Add the default 98 tiles to bag """
        self.bag.append("a")
        self.bag.append("b")
        self.bag.append("c")
        self.bag.append("d")
        self.bag.append("e")
        self.bag.append("f")
        self.bag.append("g")
        self.bag.append("h")
        self.bag.append("i")
        self.bag.append("j")
        self.bag.append("k")
        self.bag.append("l")
        self.bag.append("m")
        self.bag.append("n")
        self.bag.append("o")
        self.bag.append("p")
        self.bag.append("q")
        self.bag.append("r")
        self.bag.append("s")
        self.bag.append("t")
        self.bag.append("u")
        self.bag.append("v")
        self.bag.append("w")
        self.bag.append("x")
        self.bag.append("y")
        self.bag.append("z")
        random.shuffle(self.bag)

    def take_n_from_bag(self, n):
        """ Remove tile from bag and returns it. Used for replenishing player 
            tile rack. """
        arr = []
        for i in range(n):
            if len(self.bag) == 0:
                break
            arr.append(self.bag.pop())
        return arr

    def size_of_bag(self):
        """ Return number of tiles left in bag"""
        return len(self.bag)
