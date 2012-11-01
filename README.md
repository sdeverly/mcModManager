mcModManager
============

Python script to install Minecraft mod on Mac, could work on other platform as well, provided that the minecraft.jar file location is changed.

To use it, download a Minecraft mod, save it somewhere, and then run :
mcModManager.py -i <a name> <full path to your downloaded mod>

To activate an installed mod, run :
mcModManager.py -a <a name>

The original minecraft.jar is preserved with the "original" name. So to go back to the original install, do :
mcModManager.py -a original

