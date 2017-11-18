#!/bin/bash

rm -rf env
find . -type d -name "__pycache__" -exec rm -rf {} \;
find . -type f -name "*.pyc" -delete
find . -type f -name "*~" -delete
