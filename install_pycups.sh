#!/bin/bash
apt-get update && apt-get install -y libcups2-dev cups gcc python3-dev
pip install --no-cache-dir pycups
