# Genetic Algorithm and Aritifical Bee Colony Visualization

This project is a small visualization on how [Genetic Algorithm](https://link.springer.com/article/10.1007/s11042-020-10139-6) and [Artificial Bee Colony](https://abc.erciyes.edu.tr/) behave in a 2D search space.

> **NOTE**: This was done for a small seminar project, the code for the algorithms is therefore not production ready.

## Installation

This project requires `Python 3.10` or newer and uses [poetry](https://python-poetry.org/) as a dependency management tool.

First you need to install `poetry` as described in the [official documentation](https://python-poetry.org/docs/#installation). After successfull installation execute the following command:

```shell
poetry install
```

This will install all dependencies and scripts.

## Start up

To start the application either use poetry directly

```shell
poetry run sim
```

or use python within the virtual environment that poetry created

```shell
python -m evo_sim
```


## Settings

The [settings.yaml](settings.yaml) file contains all the runtime settings for the application. You can change it at will. To load the new settings either restart the complete application or click on the `Refresh` button in the right bottom corner.
