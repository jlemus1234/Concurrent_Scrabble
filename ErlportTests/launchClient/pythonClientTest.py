# test

from erlport.erlterms import Atom
from erlport.erlang import set_message_handler, cast

def main():
	print("running main funcion")
	# launch the msg handler
	# launch the game loop

## python:call(instance, Module, Function, Arguments) -> Result
## This can be used with some python instance (PID) received from
## python:start() to make a specific call to something. 

## 


# function that creates a handler, sets it to serve as the current handler, and returns ok. The handler accepts some message, and immediately sends it to some erlang process. 
def register_handler(dest):
        def handler(message): ## This makes a handler
		cast(dest, message) ## Sending a message to an erlang pid (dest). 
    	set_message_handler(handler) ## Set the handler so that python uses it
	return Atom("ok")


def msgHandler():
    	# erlport msghandler


def gameLoop():
        print("Entering the game loop")
        while(1):
		pass
