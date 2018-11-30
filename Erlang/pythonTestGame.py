
import time, sys
#sys.path.insert(0, '~/Desktop/comp50cp/groupProject/erlport/')
#sys.path.insert(0, '~/Desktop/Concurrent_Scrabble/ErlportTests/erlport/priv/python2/erlport')

from erlport.erlterms import Atom
from erlport.erlang import call

#from ~/Desktop/comp50cp/groupProject/erlport.erlitems import Atom
#from ~/Desktop/comp50cp/groupProject/erlport.erlitems import call


global erlPID, serverPID

def runGame(msgErlPID, servPID):
	global erlPID, serverPID
	erlPID = msgErlPID
	serverPID = servPID
	count = 5
	while(1):
		print("Running game")
		if count % 5 == 0:
			msgErl()
		time.sleep(5)
		count += 1


def msgErl():
	print("msgErl")
	


def main():
	print("Python running")
	runGame(0,0)



if __name__ == '__main__':
	main()
