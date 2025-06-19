#!/bin/bash -x

export PYTHONPATH="$PYTHONPATH:$PWD"
pytest tests
