> How to run the game?


1. create virtual environment which contains the packages from min_requirements.txt (I suggest using anaconda
for this purpose)

2. run main.py

________________________________________________________________________________________________________________________
> How To Implement a new robot into the game?


1. Ideally, 1 robot class per file! Make sure you follow the guidelines for creating a robot class like giving it a
name and put the robot class in the player-list inside the file.

2. Don't modify code from the existing files in game, except you know what you're doing! If you have to change
dependencies, create a new utility file for your robot or even a new directory

3. Import your robot in Game/register_robots.py. Type the name of the robot you want later to have it displayed in the
settings screen as key and the path from Game to your robot class file as value. Make sure you only write the filename
except the ".py".

4. Adjust the import statements in your freshly added files. Typically, you have only to update the game dependencies by
referring to the Game directory (i.e.: from game_utils import ... -> from Game.game_utils import ...).

5. You're done! :)

________________________________________________________________________________________________________________________
> The images aren't loading anymore!

Click the pause button and wait for a couple of seconds. This bug will occur on big maps and by using a lot of robots.
Unfortunately, it is not trivial to fix.

________________________________________________________________________________________________________________________