
import time, sys
import threading
#sys.path.insert(0, '~/Desktop/comp50cp/groupProject/erlport/')
#sys.path.insert(0, '~/Desktop/Concurrent_Scrabble/ErlportTests/erlport/priv/python2/erlport')

from erlport.erlterms import Atom
from erlport.erlang import call

#from ~/Desktop/comp50cp/groupProject/erlport.erlitems import Atom
#from ~/Desktop/comp50cp/groupProject/erlport.erlitems import call


global erlPID, serverPID, testVar

def runGame(msgErlPID, servPID):
	global erlPID, serverPID
	erlPID = msgErlPID
	serverPID = servPID
	count = 5
	while(1):
		print("Running game")
		if count % 5 == 0:
			callErl()
		time.sleep(5)
		count += 1


def callErl():
	print("msgErl")
	print(serverPID)

	tileArray = [('a', 1, 1, 1), ('b', 2, 2, 2)] 
	direction = 'r'
	start_pos = (0, 0)
	
	tupac = (tileArray, direction, start_pos)

	res = call(Atom("scrabble"), Atom("send_messages"), [serverPID, tupac])
	#res = call(Atom("scrabble"), Atom("send_messages"), [serverPID])
	#res = call(Atom("erlang"), Atom("self"), [])
	print(res)
	
################################################
#def startServer(msgErlPID, servPID):
#	global testVar
#	testVar = 0
#	erlPID = msgErlPID
#	serverPID = servPID
	#runGameServer()
	#t = threading.Thread(target = runGameServer)
	#t.start()
	#while(1):
	#	pass

def startServer():
	global testVar
	testVar = 0
	#erlPID = msgErlPID
	#serverPID = servPID
	#runGameServer()
	#t = threading.Thread(target = runGameServer)
	#t.start()
	#while(1):
	#	pass

def updateStateTest():
	global testVar
	print("Called update state test")
	testVar+=1
	print(testVar)

def runGameServer():
	global testVar
	count = 5
	while(1):
		print("Running server module")
		if count % 5 == 0:
			sendMoveResult()
			print(testVar)
		time.sleep(2)
		count += 1

def sendMoveResult():
	print("Sending move result")
        res = "success"
	board = [[('a', 1, 1, 1), ('b', 2, 2, 2)], [('c', 3, 3, 3), ('d', 4, 4, 4)]]
	scores = (10, 15, 20, 30)
	tile_old_new = ([('e', 5, 5, 5)], [()])
	tupac = (res, board, scores, tile_old_new)
	
	res = call(Atom("scrabble"), Atom("sendMoveResult"), [tupac])
	print(res)
	print("Finished sending thing")


def main():
	print("Python running")
	runGame(0,0)



if __name__ == '__main__':
	main()
