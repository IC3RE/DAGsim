# IOTA TANGLE SIMULATION

This is a single- and multi-agent simulation of the IOTA Tangle, as described in the white-paper.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Requirements

MacOS or Linux with Python 3.

### Install

If running MacOS 10.14, install command line tools, then run the headers package file (on your system) `/Library/Developer/CommandLineTools/Packages/macOS_SDK_headers_for_macOS_10.14.pkg`.

Set up a virtual environment if desired, then run:
```
sudo make
```

## Running the tests

The Python unittest module is used for testing.
Run the tests with:

```
python3 -m unittest discover
```

## Run

Run the simulation with:

```
python3 core.py
```

In this file you can also change the configurations of the simulation.

## Test

```
python3 -m unittest
```

## Authors

* Manuel Zander

## License

See LICENSE.txt

## Acknowledgments

Many thanks to Dominik Harz (nud3l) for his help and suggestions during development of this software.