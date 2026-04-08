#!/bin/bash
source venv/bin/activate
python - << 'PY'
from echo_crew import run_echo
run_echo()
PY
