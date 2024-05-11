# CostaPy
Python Web Framework. Build with Bottle and Mako.

## License

CostaPy

Copyright (C) 2022  Dita Aji Pratama

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see https://www.gnu.org/licenses/.

## Requirement & Installation

You need this libraries to use CostaPy:
- bottle
- gunicorn
- mako

You can install it with run this command

    sh install.sh

Here is the completed command

    sudo apt-get install -y python3-pip
    pip install --upgrade pip
    pip install bottle
    pip install gunicorn
    pip install mako

## Usage

Use this command to start the web service

    python3 costa.py

You can use nohup too and running it in the background like this

    nohup python3 costa.py &

## Configuration

### Global Variable (config/globalvar.py)

`globalvar.py` is the place for storing your Global Variable.

`baseurl` </br>
Is the variable for your base URL (without `/` in the end).

`title` </br>
Is the variable for your web title.

### Directory (config/directory.py)

`directory.py` is the place for storing your path. It is useful to calling the path more efficiently.

## Handling the modules

Handling the module is in `handler.py`.
