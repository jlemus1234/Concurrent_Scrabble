%%%
%%% File	: scrabble.erl
%%% Author	: Jose Lemus
%%% Description : A scrabble server that lets you host a four player gam
%%% November 29, 2018
%%%--------------
-module(scrabble).
-behaviour(gen_server).

%%---------------
% imports

%%---------------
%% client functions
-export([join_game/1, send_messages/1, get_messages/1]).



%%---------------
%%% Client functions
%%---------------

join_game(NodeName) -> 
	{ok, Pypid} = python:start([{python_path, "."}]), % Create python node
	Receiver = spawn_link(scrabble, get_messages, [Pypid]),
	python:call(Pypid, pythonTestGame, runGame, [self(), NodeName]).
	



get_messages(Pypid) ->
	receive {message, MessageText} ->
		io:format("~s~n", [MessageText]);
	_X -> io:format("~w~n", [something])
	end,
	get_messages(Pypid).


%% might be useful for processing input
%% Send your shit to this function
%%processInput()

send_messages(ServerPID) ->
	io:format("~w~n", [something]),
	io:format("~s~n", [ServerPID]),
	1.