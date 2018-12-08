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
-export([join_game/1, send_messages/2, get_server_messages/1, 
	printMoveDump/1, send_to_pyclient/2]).

%% External exports
-export([start_link/0, stop/0]).

%% gen_server callbacks
-export([init/1, handle_call/3, handle_cast/2, terminate/2, handle_info/2]).


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
	{noreply, PyPid}.

%%--------------------------------------------------------------------
%% Function: handle_info/2
%% 
%%--------------------------------------------------------------------
handle_info(Info, PyPid) ->
	io:format("~s~n", ["Server received some info"]),
	python:cast(PyPid, Info),
	{noreply, PyPid}.
	
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
	get_server_messages(Pypid),
	io:format("~s~n", ["finished gmTest"]).

% Await any messages sent from the game server
get_server_messages(Pypid) ->
	receive {r, Message} ->
			io:format("~s~n", [Message]);
		Something ->
			io:format("~s~n", ["got something from server"]),
			io:format("~p~n", [Something]),
			python:cast(Pypid, Something)
	end,
	get_server_messages(Pypid).

% Helps python instances do a gen_server:cast for joining
send_messages(PID, Message) ->
	io:format("~s~n", ["Trying to send message"]),
	gen_server:cast(PID, Message).

% Used by game server to send data to clients
send_to_pyclient(PyPid, Message) ->
	io:format("~s~n", ["Trying to send message to pyclient"]),
	io:format("~p~n", [PyPid]),
	io:format("~p~n", [Message]),
	PyPid ! Message.

% Convenience function for printing out the elements of a tuple
printMoveDump({TileArr, Dir, Start_pos}) ->
	io:format("~s~n", ["printMoveDump"]),
	io:format("~p~n", [TileArr]),
	io:format("~p~n", [Dir]),
	io:format("~p~n", [Start_pos]).
