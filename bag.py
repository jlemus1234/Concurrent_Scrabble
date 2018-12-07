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
        self.bag.append(Tile("a"))
        self.bag.append(Tile("b"))
        self.bag.append(Tile("c"))
        self.bag.append(Tile("d"))
        self.bag.append(Tile("e"))
        self.bag.append(Tile("f"))
        self.bag.append(Tile("g"))
        self.bag.append(Tile("h"))
        self.bag.append(Tile("i"))
        self.bag.append(Tile("j"))
        self.bag.append(Tile("k"))
        self.bag.append(Tile("l"))
        self.bag.append(Tile("m"))
        self.bag.append(Tile("n"))
        self.bag.append(Tile("o"))
        self.bag.append(Tile("p"))
        self.bag.append(Tile("q"))
        self.bag.append(Tile("r"))
        self.bag.append(Tile("s"))
        self.bag.append(Tile("t"))
        self.bag.append(Tile("u"))
        self.bag.append(Tile("v"))
        self.bag.append(Tile("w"))
        self.bag.append(Tile("x"))
        self.bag.append(Tile("y"))
        self.bag.append(Tile("z"))
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
