%% Functions that are called from python



-module(erlFromPy.erl).
-export([testFunCall/0]).


testFunCall() ->
	io:format("~s~n", ["erl function called"]).
	erlfuncalled.