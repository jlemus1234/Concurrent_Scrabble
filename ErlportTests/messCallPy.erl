%% Testing passing messages to python from Erlang
%% 
-module(messCallPy).

-export([testing/0, test/0]).

callPy() ->
	{ok,Pypid} = python:start([{python_path, "."}]),
	A = python:call(Pypid, testErlport, hello, []),
	B = python:call(Pypid, testErlport, testArray, [[1,2,3]]),
	io:format("~s~n", ["finishedTest"]),
	C = [5 | B],
	C.

## Probably want the communications from client/game servers to be 
## done with a gen server.
msgErl(Pid) -> 
	gotPid.


runs() ->
	io:format("~s~n", ["test"]).