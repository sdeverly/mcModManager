mcModManager
============

Python script to install Minecraft mod on Mac, could work on other platform as well, provided that the minecraft.jar file location is changed.

To use it, download a Minecraft mod, save it somewhere, and then run :

<code>mcModManager.py -i <i>a_name</i> <i>full_path_to_your_downloaded_mod</i></code>

To activate an installed mod, run :

<code>mcModManager.py -a <i>a_name</i></code>

The original minecraft.jar is preserved with the "original" name. So to go back to the original install, do :

<code>mcModManager.py -a original</code>

