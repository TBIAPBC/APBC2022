A6 - Robot Race
===============

Dear APBC wizzards,

for the grand finale of our class, the team project, we are going to
play a game. Your main task in this project is to write players (as
python classes, more below - also how to integrate robots written in other
languages)---at least a naive one and a smart one. We
implemented the game server (which you are invited to extend).

This task should be team work, so make use the possibilities to discuss
ideas and even share code via Github and/or offline. The more actively
you contribute and discuss details of the game the more fun this will
be :).


## Rules

### The general setting

The game can be played with an (almost) arbitrary number of robots
competing with each other on an n x m board. The board contains walls
'#' (and is surrounded by walls---not shown).
For n=m=10 (note that in real life, we use different parameters
than in the example; e.g. n=m=35 or more), this could like:
```
. # . . . # . . . #
. # . . . . . . . .
. # . # . . . # . .
. # . # . . . # . .
. # # # . . . # # .
. . . . . . . # . .
. . . . . . . # . .
. . . # # # # # . .
. # . . . . . . . .
. # . . . . . . . .
```

In the beginning, the playing robots are placed at random
positions. In addition, the server places a pot of gold '$'
somewhere.
```
. # . . . # . . . #
. # . . . . . . . .
. # . # . . . # . .
. # . # A . . # . $
. # # # . . . # # .
. . B . . . . # . .
. . . . . . . # . .
. . . # # # # # . .
. # . . . . . C . .
. # . . . . . . . .
```

Each robot holds an amount of gold coins and has a health
status. Robots start out with 100 gold coins and 100% health. Note that our
robots are quite short-sighted and receive only partial information of
the board and position of their opponents.

### A round of the game

The game proceeds in rounds. In each round, each robot is provided
with information about its immediate neighborhood limited by the
visibility range v in each direction (up, down, left, right, as well
as in all 'diagonals' up-left, up-right, etc); moreover, it somehow
senses the position of the pot of gold. At the beginning of each
round, robots get 1 new gold coin (they are going to need
it). If health is below 100%, it also heals by 10% points.

For visibility v=2, the first robot 'sees'

```
_ _ _ _ _ _ _ _ _ _
_ _ . . . . . _ _ _
_ _ . # . . . _ _ _
_ _ . # a . . _ _ $
_ _ # # . . . _ _ _
_ _ b . . . . _ _ _
_ _ _ _ _ _ _ _ _ _
_ _ _ _ _ _ _ _ _ _
_ _ _ _ _ _ _ _ _ _
_ _ _ _ _ _ _ _ _ _
```

In addition, the robot is informed about the health status of all
robots in the visibility range and the amount of gold in the pot.

The robot is first asked whether and where to set mines. Then, it is asked where to move.

In further extensions, robots could moreover take shots (before they move) and buy healing packs (after they moved). We are
going to play without these extensions.

#### Mines

Players can set as many mines as they want (as long as they have enough gold).
Mines are charged by direct distance from the player, a mine in distance k is charged like k moves.

It is only allowed to set mines on empty fields (= no Walls,other Mines, Players or Gold) and within the map.
If these placement rules are ignored the mine is not set, however the player is still charged.
When the expiry time is reached mines are removed
;currently after 3 rounds, set with parameter mineExpiryTime.

Crashing into mines decreases health like crashing into walls
On the map Mines are represented as &.

#### Moving

Each round, the robot can choose how many steps to move, but each move gets more expensive.

Each single move / step (or in the extension shots, or buying health packs) counts as action and costs gold coins, such that k actions cost in total
```
cost(k) = sum { i | i=1..k }
```

Each single move changes to a neighbored field. If robots make several moves per round, the moves are performed in turns.
The attempt to move into a wall causes a health damage of c=25%.
Crashing into another robot causes a health damage randomly chosen between c=15 and c=20% (the same also happens to the other robot).
After the first crash, all remaining moves are
cancelled.  Note that robots are allowed to move out of their
visibility range. Moreover, any attempt of moving out of the board is
treated like moving against a wall.

After all moves are performed, the robots are informed about their
updated position and health status.


### The pot of gold

When the gold pot is set up, it contains 100 coins.
Per action of any robot, magically one additional gold coin appears in the pot.
After a certain number of rounds (currently 20, set with the parameter goldPotTimeOut) the gold pot is emptied.
It will re-appear at some random other field, again filled with 100 coins.

Another game mode exists, where the amount of gold in the pot decreases with each action of a robot after a certain time.
This mode is enabled by setting the parameter goldDecrease to True.
The time after which this happens is set with the parameter goldDecreaseTime and is currently half of the gold pot time-out.

Robots claim the gold pots contents simply by moving to the field of the pot.
After the gold pot was claimed a new one is placed, again filled with 100 coins and the time-out is started anew.

It is possible to play the game with multiple gold pots.
To keep the gold pots time-out in sync, all gold pots are emptied and relocated once one of them gets claimed by a robot.

### Winning the game

A game is performed for a pre-determined number of rounds
(e.g. 2000). After game over, the robot with the most gold coins wins.


## Technical / Implementational Issues

Each robot is implemented as a python class. The class must implement
methods for each step of a turn (currently only moving, since robots are not supposed to shoot or buy health
packs), which return the actions the robots wants to perform.
All information (which the robot is allowed to know) is provided to the
robot by the server (initially at construction, and in each turn).
It will as well get a record of the game parameters.

Have a look at the test players in test-RobotRace.py and the code in game_utils.py
to get a better idea of how to implement the bots.

When asked for actions, the robots should reply in relatively short
time (rather fractions of a seconds, otherwise games will turn
boring; currently there is no enforced time limit, so please take care!). If
calls raise exceptions, the response is counted as defining no
action. If invalid actions are requested, they are charged with gold
coins without performing any action. After the first invalid action,
no other actions are performed in the same step of the round.

We provide you with a python base class that specifies the exact
interface of the robot classes. Your robot classes can inherit this
class.

As usual submit your code via Github. Provide a python module
```
YOURNAME-RobotRace.py
```

that can be imported by our game server and specifies your Robots.
The module must as well define the variable players containing a list
of all robot objects in the class, i.e. players would be defined like this
```
players = [ NaiveRobot(), SupersmartAndFancyBot(), TestBot2() ]
```

### How to write Non-Python bots

Bots written in other languages than python should be written such
that they provide a command line interface as follows:

```
YOURNAME-RobotRace <command>
```

The program receives information as a yaml record from standard input and writes
a yaml record to standard output. Please look up yourself how to parse
yaml files in your language of choice.

There are three different commands (corresponding to the three methods
'reset', 'round_begin', and 'move') that have to be implemented by a
Player class). The yaml input records will contain exactly the
information passed to these methods (see program file player_base.py).

One can than rather easily write a wrapper YOURNAME-RobotRace.py that
wraps the non-python program with the described interface into an
Python class of type Player.

Players are allowed to store information in a file YOURNAME-PLAYERNAME.dat in the current directory (Python players don't need this, but for others it could be useful.)

### Testing your bots

Copy your bots module to A6 and and compete against the provided test players by running runRobotRace.py; one also needs to slightly adapt the file runRobotRace.py: register your module in robot_module_names. Test you robots offline and try to get some non-crashing bot(s) ready for our meetings.

### Some words about strategy

To avoid being totally clueless, a robot should take the direction to
the gold pot into account when moving. Since the map is labyrinthic,
it should likely try to develop an idea of the map and then plan short(est)
paths to the gold. Always moving one step closer to the gold is already much better than randomly tumbling around or ignoring walls.

Of course, the fun starts where you run for gold (and outrun others)
instead of crawling towards the pot. However, recall that running (making more than one move per round) is costly, so this is about finding a good balance (even if catching the pot should be generally quite attractive).
A next major issue is to avoid unintentionally crashing into other bots.

## Milestones

### Milestone 1 (after two weeks, second team project meeting 2 June 2021)

  * Think about all the constants in the game and possible variations --- such that we can discuss

  * Learn about shortest path algorithms

  * See that you understand how to go on (and/or think about questions
    for the meeting)

  * Look at the code; start implementing

### Milestone 2 (after another two weeks, meeting 16 June 2021)

  * Write some naive player until the in-between meeting (which e.g. could perform random actions, move always only
    by one towards the pot, hide somewhere etc.)

  * Let's see that we can plug first things together. Can we already
    watch some (more or less) naive robots fight for gold?

### Milestone 3 (after another two weeks, final meeting 30 June 2021)

  * We want to plug everything together and play a tournament.

  * Your smart robots should be able to play each others and the naive
    players. Eventually, your smart robots should typically beat the naive
    players.
