# CMake Quick Project (CQP)

CQP is used to initialize, manage, build and distribute CMake projects using Python.
- [CMake Quick Project (CQP)](#cmake-quick-project-cqp)
	- [Requirements](#requirements)
		- [Python 3](#python-3)
		- [CMake](#cmake)
	- [Quick Start](#quick-start)
	- [Using the CLI](#using-the-cli)
		- [`cmake`](#cmake-1)
			- [`gen`](#gen)
			- [`newbin`](#newbin)
			- [`newlib`](#newlib)
			- [`sync`](#sync)
		- [`doc`](#doc)
			- [`-i`](#-i)
			- [`-a`](#-a)
			- [`-d`](#-d)

## Requirements

### Python 3
Python 3 is the main driver of the CLI.
Run `python --version` to find out 

You also need to use pip to install TOML for Python:
```cmd
pip install toml
```

### CMake
Obviously
By default, CMake 3.23 is used.

## Quick Start
Quickly create a new project by installing the [Source Code](https://github.com/scongebop/cmake-quick-project/releases/tag/stable-v1.0) and using the CLI as normal

Replace `<NAME>` with what you want to name you project

## Using the CLI
This is the reference for CQP CLI
### `cmake`
```
python project.py cmake
```
Used to interact with the CMake CLI.
#### `gen`
```
python project.py cmake gen
```
Used to generate build files with CMake.
See [project.toml.md](project.toml.md) to learn how to configure CMake without having to write an extremely long line of random text.

#### `newbin`
```
python project.py cmake newbin <PACKAGE_PATH>
```
Creates a new executable package at `PACKAGE_PATH`.

#### `newlib`
```
python project.py cmake newlib <PACKAGE_PATH>
```
Creates a new library package at `PACKAGE_PATH`.

#### `sync`
```
python project.py cmake sync <PACKAGE_PATH>
```
Synchronizes the `package.toml` file in `PACKAGE_PATH` with the `CMakeLists.txt` in the same directory.

### `doc`
```
python project.py doc
```
Used to document the project

#### `-i`
```
python project.py doc -i <FILENAME>
```
Used to document individual files.

#### `-a`
```
python project.py doc -a
```
Goes through your filesystem and documents any `.c`, `.cpp`, `.h` and `.hpp` files it comes across.
Also creates Index.md files to note any other docs files.

#### `-d`
```
python project.py doc -d
```

Does the opposite of `-a`, goes through the filesystem and deletes .md files.
It ignores README.md files.
