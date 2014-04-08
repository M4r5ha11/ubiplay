# What

A file-system based, web music player, using the `<audio>` tag.

# Under the hood

Ubiplay is written in Python, using [Flask][].

[Flask]: http://flask.pocoo.org/

# Configuring it

Copy `ubiplay/settings-sample.py` to `ubiplay/settings.py`.

Edit `ubiplay/settings.py`.

# Starting it

    python ubiplay/main.py

Or to run it as a daemon:

    python ubiplay/main.py --daemon ~/tmp/ubiplay.pid --log ~/tmp/ubiplay.log
