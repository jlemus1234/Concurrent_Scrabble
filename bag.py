#!/usr/bin/python -tt
#   bag.py
#
#   COMP 50CP Fall 2018
#   Group Project: Distributed Scrabble
#
#   Modified On: December 1, 2018

""" Purpose: This module holds the implementation of the class Bag"""

from tile import Tile
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
        id = 0






        for id in range(id, id + 9):
            self.bag.append(Tile("a", start_id=id))
        for id in range(id, id + 2):
            self.bag.append(Tile("b", start_id=id))
        for id in range(id, id + 2):
            self.bag.append(Tile("c", start_id=id))
        for id in range(id, id + 4):
            self.bag.append(Tile("d", start_id=id))
        for id in range(id, id + 12):
            self.bag.append(Tile("e", start_id=id))
        for id in range(id, id + 2):
            self.bag.append(Tile("f", start_id=id))
        for id in range(id, id + 3):
            self.bag.append(Tile("g", start_id=id))
    #    for id in range(id, id + 2):
        self.bag.append(Tile("h", start_id=id))
        self.bag.append(Tile("i", start_id=id))
        self.bag.append(Tile("j", start_id=id))
        self.bag.append(Tile("k", start_id=id))
        self.bag.append(Tile("l", start_id=id))
        self.bag.append(Tile("m", start_id=id))
        self.bag.append(Tile("n", start_id=id))
        self.bag.append(Tile("o", start_id=id))
        self.bag.append(Tile("p", start_id=id))
        self.bag.append(Tile("q", start_id=id))
        self.bag.append(Tile("r", start_id=id))
        self.bag.append(Tile("s", start_id=id))
        self.bag.append(Tile("t", start_id=id))
        self.bag.append(Tile("u", start_id=id))
        self.bag.append(Tile("v", start_id=id))
        self.bag.append(Tile("w", start_id=id))
        self.bag.append(Tile("x", start_id=id))
        self.bag.append(Tile("y", start_id=id))
        self.bag.append(Tile("z", start_id=id))
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

    #start_tiles = ['a'] * 12 + ['b'] *
