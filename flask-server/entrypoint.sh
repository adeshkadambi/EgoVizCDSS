#!/bin/bash --login
# The --login ensures the bash configuration is loaded,
# enabling Conda.
# set -uo pipefail
conda activate handobj
exec python server_HOmodel.py 