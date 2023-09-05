#!/bin/bash

# Replace script1.py and script2.py with the names of your Python scripts
SCRIPT1="normalM.py"
SCRIPT2="deleteM.py"

# Initialize a variable to indicate the first run
FIRST_RUN=1

# Run the script in an infinite loop
while true; do

  # Check if script1 is running
  PID1=$(ps -fA | grep python | grep $SCRIPT1 | awk '{print $2}')

  # Check if script2 is running
  PID2=$(ps -fA | grep python | grep $SCRIPT2 | awk '{print $2}')

  # If it is the first run, run the first script
  if [ $FIRST_RUN -eq 1 ]; then
    echo "Running $SCRIPT1"
    python3 $SCRIPT1

    # Set the variable to 0 to indicate that it is not the first run anymore
    FIRST_RUN=0
  fi

  # If both of the PIDs are empty, run the second script
  if [ -z "$PID1" ] && [ -z "$PID2" ]; then
    echo "Running $SCRIPT2"
    python3 $SCRIPT2
  fi

  # Wait for some time before checking again
  sleep 10

done