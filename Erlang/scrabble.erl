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
%% client exports
-export([join_game/1, send_messages/1, send_messages/2, get_messages/1, printMoveDump/1]).

%% server exports
-export([gmTest/1]).
-export([sendMoveResult/1, printMoveResult/1, gotNewMove/0]).


%%---------------
%% Server
%%---------------

sendMoveResult(MoveResult) -> 
	io:format("~s~n", ["got move result"]).
	%io:format("~p~n", MoveResult).
	%printMoveResult(MoveResult).


printMoveResult({Result, Board, Scores, {OldTiles, NewTiles}}) ->
	io:format("~s~n", ["Printing move result"]),
	io:format("~p~n", [Result]),
	io:format("~p~n", [Board]),
	io:format("~p~n", [Scores]),
	io:format("~p~n", [OldTiles]),
	io:format("~p~n", [NewTiles]).



gmTest(NodeName) -> 
	{ok, Pypid} = python:start([{python_path, "."}]), % Create python node
	Receiver = spawn_link(scrabble, get_messages, [Pypid]),
	python:call(Pypid, pythonTestGame, startServer, [self(), NodeName]).
	%timer:sleep(1000),
	%python:call(Pypid, pythonTestGame, updateStateTest, []),
	%timer:sleep(1000),
	%python:call(Pypid, pythonTestGame, updateStateTest, []).


% simple test function for sending python data
gotNewMove()->
	io:format("~s~n", ["Got new move"]).

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

send_messages(ServerPID, MoveDump) ->
	io:format("~w~n", [something2]),
	io:format("~p~n", [MoveDump]),
	printMoveDump(MoveDump).


printMoveDump({TileArr, Dir, Start_pos}) ->
	io:format("~s~n", ["printMoveDump"]),
	io:format("~p~n", [TileArr]),
	io:format("~p~n", [Dir]),
	io:format("~p~n", [Start_pos]).