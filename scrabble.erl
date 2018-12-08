%%%
%%% File	: scrabble.erl
%%% Author	: Jose Lemus
%%% Description : A scrabble server that lets you host a four player game
%%% November 29, 2018
%%%--------------
-module(scrabble).
-behaviour(gen_server).

%%---------------
% imports
%%---------------
%% client
%send_messages/1
-export([join_game/1, send_messages/2, get_server_messages/1, printMoveDump/1, send_to_pyclient/2]).

%% External exports
-export([start_link/0, stop/0]).

%% server_test_functions
-export([gmTest/1]).
-export([broadcastMoveResult/1, printMoveResult/1, gotNewMove/0]).

%% gen_server callbacks
-export([init/1, handle_call/3, handle_cast/2, terminate/2]).


%%====================================================================
%% External functions
%%====================================================================
%%--------------------------------------------------------------------
%% Function: start_link/0
%% Description: Starts the server
%%--------------------------------------------------------------------
start_link() ->
    gen_server:start_link({local, scrabble}, scrabble, [], []).


%%--------------------------------------------------------------------
%% Function: stop/0
%% Description: Stops the server
%%--------------------------------------------------------------------
stop() ->
    gen_server:cast({scrabble, node()}, stop).




%%====================================================================
%% Server functions
%%====================================================================

%% state in this case is the number of players
%% potentially whether or not the game has begun

%%--------------------------------------------------------------------
%% Function: init/1
%% Description: Initiates the server
%% Returns: {ok, State}          |
%%          {ok, State, Timeout} |
%%          ignore               |
%%          {stop, Reason}
%%--------------------------------------------------------------------
init([]) ->
    %process_flag(trap_exit, true),
    io:format("~s~n", ["calling init"]),
    {ok, Pypid} = python:start([{python_path, "."}]), % Create python node
    python:call(Pypid, middle_for_game, register_handler, [self()]),
    python:call(Pypid, middle_for_game, start, [self()]),
    {ok, Pypid}.


%%--------------------------------------------------------------------
%% Function: handle_call/3
%% Description: Handling call messages
%% Returns: {reply, Reply, State}          |
%%          {reply, Reply, State, Timeout} |
%%          {noreply, State}               |
%%          {noreply, State, Timeout}      |
%%          {stop, Reason, Reply, State}   | (terminate/2 is called)
%%          {stop, Reason, State}            (terminate/2 is called)
%%--------------------------------------------------------------------
%handle_call(Request, From, State) ->
handle_call({list}, _From, State) ->
	io:format("~s~n", ["got a list call"]),
	{reply, gotList, State}.


%%--------------------------------------------------------------------
%% Function: handle_cast/2
%% Description: Handling cast messages
%% Returns: {noreply, State}          |
%%          {noreply, State, Timeout} |
%%          {stop, Reason, State}            (terminate/2 is called)
%%--------------------------------------------------------------------

handle_cast(stop, State) ->
	{stop, shutdown, State};
handle_cast(Anything, PyPid) ->
	io:format("~s~n", ["Server received some cast"]),
	python:cast(PyPid, Anything),
	{noreply, PyPid};
handle_cast(_X, State) ->
	io:format("~s~n", ["Got unmatched message"]),
	{noreply, State}.



%%--------------------------------------------------------------------
%% Function: terminate/2
%% Description: Shutdown the server
%% Returns: any (ignored by gen_server)
%%--------------------------------------------------------------------
terminate(_Reason, State) ->
    shutdown_msg(State),
    ok.

%%--------------------------------------------------------------------
%%% Internal Functions
%%--------------------------------------------------------------------
shutdown_msg(Subscriptions) ->
    ShutdownAlert = fun ({_Room, Client, _Name}) ->
                            Client ! {message, "Game server has gone down"} end,
    lists:foreach(ShutdownAlert, Subscriptions).

broadcastMoveResult(MoveResult) ->
	io:format("~s~n", ["sending move result"]).
	%io:format("~p~n", MoveResult).
	%printMoveResult(MoveResult).


receiveMoveResult(MoveResult) ->
	io:format("~s~n", ["received move result"]).

printMoveResult({Result, Board, Scores, {OldTiles, NewTiles}}) ->
	io:format("~s~n", ["Printing move result"]),
	io:format("~p~n", [Result]),
	io:format("~p~n", [Board]),
	io:format("~p~n", [Scores]),
	io:format("~p~n", [OldTiles]),
	io:format("~p~n", [NewTiles]).



gmTest(NodeName) ->
	{ok, Pypid} = python:start([{python_path, "."}]), % Create python node
	%Receiver = spawn_link(scrabble, get_messages, [Pypid]),
	python:call(Pypid, pythonClient, register_handler, [self()]),
	%python:call(Pypid, pythonClient, startServer, []),
	python:call(Pypid, pythonClient, startServer, [self(), NodeName]),
	%timer:sleep(1000),
	python:cast(Pypid, update), % This would be being sent from another erlang process
	loop(Pypid),
	io:format("~s~n", ["finished gmTest"]).
	%python:call(Pypid, pythonClient, updateStateTest, []).
	%timer:sleep(1000),
	%python:call(Pypid, pythonClient, updateStateTest, []).


loop(Pypid) ->
        io:format("~s~n", ["looping"]),
        receive
                 Something ->
                         io:format("~s~n", ["got something"]),
                         io:format("~p~n", [Something])
         end,
         io:format("~s~n", ["fin looped"]),
         python:cast(Pypid, update), % This would be being sent from another erlang proces

         loop(Pypid).


% simple test function for sending python data
gotNewMove()->
	io:format("~s~n", ["Got new move"]).

%%====================================================================
%% Client functions
%%====================================================================

join_game(NodeName) ->
%% Set up the python process
	{ok, Pypid} = python:start([{python_path, "."}]), % Create python node
%% Set up a listener
	%%Receiver = spawn_link(scrabble, get_server_messages, [Pypid]),
%% Game server's pid
	GameServer = {scrabble, NodeName},
%% Set up the python message handler
	python:call(Pypid, middle_for_player, register_handler, [self()]),
	python:call(Pypid, middle_for_player, start, [self(), GameServer]),
%% Listen to client
	%get_client_messages(GameServer, Pypid),
	get_server_messages(Pypid),
	io:format("~s~n", ["finished gmTest"]).


get_client_messages(GameServer, Pypid) ->
	io:format("~s~n", ["looping"]),
	receive
		Something ->
			io:format("~s~n", ["got something"]),
			io:format("~p~n", [Something]),
			%gen_server:cast(GameServer, message)
			gen_server:cast(GameServer, Something)
	end,
	io:format("~s~n", ["fin looped"]),
	%python:cast(Pypid, update), % This would be being sent from another erlang process
	get_client_messages(GameServer, Pypid).



get_server_messages(Pypid) ->
	%receive {message, MessageText} ->
	receive Something ->
		io:format("~s~n", ["got something from server"]),
		io:format("~p~n", [Something]),
		%Pypid ! Something
		python:cast(Pypid, something)
	end,
	get_server_messages(Pypid).

%% might be useful for processing input
%% Send your shit to this function

send_messages(PID, Message) ->
	io:format("~s~n", ["Trying to send message"]),
	gen_server:cast(PID, Message).


%	io:format("~s~n", [ServerPID]),
%	1.

send_to_pyclient(PyPid, Message) ->
	io:format("~s~n", ["Trying to send message to pyclient"]),
	python:cast(PyPid, Message).


%send_messages(Anything) ->
%	io:format("~w~n", ["trying to send with 1 argument"]).


%send_messages(ServerPID, MoveDump) ->
%	io:format("~w~n", [something2]),
%	io:format("~p~n", [MoveDump]),
%	printMoveDump(MoveDump).


printMoveDump({TileArr, Dir, Start_pos}) ->
	io:format("~s~n", ["printMoveDump"]),
	io:format("~p~n", [TileArr]),
	io:format("~p~n", [Dir]),
	io:format("~p~n", [Start_pos]).
