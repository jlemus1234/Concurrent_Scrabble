# Calls an erlang function from within Python
# Companion erlang file of functions is erlFromPy.erl


from ~/Desktop/comp50cp/groupProject/erlport.erlitems import Atom
from ~/Desktop/comp50cp/groupProject/erlport.erlitems import call

## "Currenty each Erlang function will be called in a new erlang process"
## This isn't what we want really. Should probably try to do all of this with 
## the message passing components. 

## P is the instance (PID), pids is the module (name of python file)
## pids is the function (in the python file), and [] is an array with arguments
python:call(P, pids, pids, [])

def runs():
	print("test")
	return 0

def pids():
	print("pids")
	# Call erlang functions -- in this case we are calling the "self"
	# function, which just returns the pid of the erlang process. 
	# call(module, function, arguments) 
	# Atom is the type it accepts, casting strings to it
	Pid1 = call(Atom("erlang"), Atom("self"), [])
	Pid2 = call(Atom("erlang"), Atom("self"), [])
	return [Pid1, Pid2] 
	# Because each function is run in a new process, this will generate
	# two new PIDs, which will be returned to the python instance

