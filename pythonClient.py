
import time, sys
import threading

from erlport.erlterms import Atom
from erlport.erlang import set_message_handler, call, cast

global erlPID, serverPID, testVar

	
################################################
def startServer(msgErlPID, servPID):
	global testVar
	testVar = 0
	#erlPID = msgErlPID
	#serverPID = servPID
	#runGameServer()
	t = threading.Thread(target = runGameServer)
	t.start()
	#while(1):
	#	pass

#def startServer():
#	global testVar
#	testVar = 0
	#erlPID = msgErlPID
	#serverPID = servPID
	#runGameServer()
#	t = threading.Thread(target = runGameServer)
#	t.start()
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
	
	#res = call(Atom("scrabble"), Atom("sendMoveResult"), [tupac])
	print("erlPID is")
	print(erlPID)
        cast(erlPID, Atom("madeMove"))
	

	#print(res)
	print("Finished sending thing")

def register_handler(dest):
	global testVar, erlPID
	print(dest)
	erlPID = dest
	testVar = 0
        def handler(message):
		global testVar
		print(message)
		testVar += 1
		print(testVar)
	set_message_handler(handler)
	return Atom("ok")

def main():
	print("Python running")
	runGame(0,0)



if __name__ == '__main__':
	main()
