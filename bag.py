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
	self.start_tiles = (['a'] * 12 +
                   ['b'] *  2 +
                   ['c'] *  2 +
                   ['d'] *  4 +
                   ['e'] * 12 +
                   ['f'] *  2 +
                   ['g'] *  3 +
                   ['h'] *  2 +
                   ['i'] *  9 +
                   ['j'] *  1 +
                   ['k'] *  1 +
                   ['m'] *  2 +
                   ['n'] *  6 +
                   ['o'] *  8 +
                   ['p'] *  2 +
                   ['q'] *  1 +
                   ['r'] *  6 +
                   ['s'] *  4 +
                   ['t'] *  6 +
                   ['u'] *  4 +
                   ['v'] *  2 +
                   ['w'] *  2 +
                   ['x'] *  1 +
                   ['y'] *  2 +
                   ['z'] *  1)
        self.initialize_bag()
        self.lock = threading.Lock()


    def initialize_bag(self):
        """ Add the default 98 tiles to bag """
        for i in range(len(self.start_tiles)):
            self.bag.append(Tile(self.start_tiles[i], start_id=i))
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

    
