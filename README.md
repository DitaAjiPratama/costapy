# CostaPy
a Python WSGI Web Framework. Build with Bottle and Mako.

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

# Getting Starter

## Requirement

You need a `git`, `python`, `pip`, and `venv` before using CostaPy.

Install them using the following commands on your `Debian` or `Ubuntu` system.

```bash
sudo apt update
sudo apt install git python3 python3-venv python3-pip
```

or you can use the following command to install similar packages using `brew`, the package manager for `macOS`:

```bash
brew install git python3
```
Installs Python 3 with `brew`, which includes `python3`, `pip3`, and the `venv` module. If you don't have Homebrew installed on your `macOS`, you can install it first.

or go to the [git downloads page](https://git-scm.com/downloads) and a [Python downloads page](https://www.python.org/downloads/) and download the latest version of git Python for `Windows`.

## Installation

Download from repository
```bash
git clone https://gitea.ditaajipratama.net/aji/costapy.git
```

Go to the directory and install with this command:

```bash
cd costapy
bash install.sh
```

Use `cat install.sh` if you want to see a completed command.

## Usage

Use this command below to start the web service and it will run on port `11000` by default
```bash
.venv/bin/python3 costa.py costapy-welcome
```
Here, `costapy-welcome` is the label of your service. You can replace it with any name you prefer.

## Trivia

- Why must `venv`?

  `venv` is a module in Python that provides support for creating lightweight, isolated Python environments, known as virtual environments. Each virtual environment has its own installation directories and can have its own versions of Python packages, independent of the system-wide Python environment.

  When deploying a Python application, using a virtual environment ensures that only the required packages (and their specific versions) are bundled. This reduces the risk of deploying unnecessary packages or incompatible versions that could lead to runtime errors.

  Using `venv` is a widely accepted best practice in the Python community. It encourages good habits in dependency management, ensuring that projects are self-contained and reducing the potential for "dependency hell."

  When a project is no longer needed, deleting its virtual environment is straightforward and does not affect other projects or the system's Python environment.

- Why I add `venv` on my `gitignore`?

  Committing `venv` to Git is gross. Virtual environments can contain thousands of files and their size can be in gigabytes. Committing them to Git can overload and clutter your source code repo with unnecessary files and cause confusion for anyone trying to clone and run the source code on their machine.

