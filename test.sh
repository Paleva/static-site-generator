#!/bin/bash

PYTHONPATH="${PWD}:${PWD}/src" python3 -m unittest discover -s tests
# python3 -m unittest discover -s tests