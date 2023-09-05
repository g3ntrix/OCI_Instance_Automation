# OCI Instance Automation

## Introduction

This repository contains Python and Shell scripts that help automate the process of launching, managing, and terminating instances on Oracle Cloud Infrastructure (OCI). The code is specifically designed to automate the process of changing IP addresses at a desired interval.

## Prerequisites

1. Python 3.x
2. Oracle Cloud Infrastructure CLI
3. OCI Python SDK

## Scripts

This repository includes four scripts:

- `main.py`: This is the main script that runs on the server where you want to change the IP address. It uses the OCI API to create and delete ephemeral public IPs for a private IP. It also allows you to exclude certain IP addresses or ranges from being assigned. It has three input options for running the script: normal mode, delete mode, and custom start time mode.
- `normal.py`: This is a modified version of `main.py` that runs in normal mode by default. It is useful for avoiding the requests/time period limit of the OCI API.
- `delete.py`: This is another modified version of `main.py` that runs in delete mode by default. It deletes the current public IP before running the rest of the code. It is useful for changing the IP manually when needed.
- `check.sh`: This is a shell script that checks if `normal.py` or `delete.py` are running and runs them accordingly. It is useful for keeping the automation process running in case of session breaks or errors.
- `kill.sh`: This is another shell script that kills `normal.py` or `delete.py` processes if they are running. It is useful for stopping the automation process when needed.

## Installation

```bash
git clone https://github.com/your_username/OCI_Instance_Automation.git
cd OCI_Instance_Automation
pip install -r requirements.txt
```

> **Note**: To create a requirements.txt file, you can use the `pip freeze > requirements.txt` command in your terminal. This will generate a text file with the names and versions of all the Python modules and packages installed in your virtual environment. Alternatively, you can manually write the names and versions of the modules and packages that you use in your project, such as `oci==2.52.0` or `tensorflow==2.3.1`, in a text file and name it requirements.txt.

> **Note**: Running check.sh in a tmux session is recommended for ease of use. Tmux is a terminal multiplexer that allows you to run multiple terminal sessions in one window. You can install tmux using `sudo apt install tmux` on Linux or `brew install tmux` on Mac. To start a tmux session, run `tmux new -s session_name` in your terminal, where session_name is the name of your session. To detach from a tmux session, press Ctrl+B and then D. To attach to a tmux session, run `tmux attach -t session_name` in your terminal.

## Usage

### How to run `main.py`

1. Open a terminal and navigate to the repository folder.
2. Run `python3 main.py`.
3. Choose an option from the menu:
    - 1: Run the code normally.
    - 2: Delete the current public IP and then run the code normally.
    - 3: Run the code with a custom start time.
4. If you choose option 3, enter a number between 0 and 50 (the delete interval in minutes) to adjust the start time.
5. The script will print the status of the public IP and the time since it was last assigned every 10 seconds.
6. To stop the script, press Ctrl+C.

### How to run `normal.py` or `delete.py`

1. Open a terminal and navigate to the repository folder.
2. Run `python3 normal.py` or `python3 delete.py`.
3. The script will run in normal mode or delete mode by default, without asking for user input.
4. The script will print the status of the public IP and the time since it was last assigned every 10 seconds.
5. To stop the script, press Ctrl+C.

### How to run `check.sh`

1. Open a terminal and navigate to the repository folder.
2. Run `./check.sh`.
3. The script will check if `normal.py` or `delete.py` are running every 10 seconds and run them accordingly.
4. If it is the first run, it will run `normal.py` by default.
5. If both scripts are not running, it will run `delete.py`.
6. To stop the script, press Ctrl+C.

### How to run `kill.sh`

1. Open a terminal and navigate to the repository folder.
2. Run `./kill.sh`.
3. The script will kill `normal.py` or `delete.py` processes if they are running.
4. The script will exit after killing the processes.

### Benefits of using this automation

By using this automation, you can:

- Save time by avoiding manual steps for changing IP addresses on OCI instances.
- Avoid errors by ensuring that public IPs are managed according to the specified rules and exclusions.
- Increase efficiency by using pre-configured images and scripts that suit your needs.

## Contributing

Feel free to contribute. Please open an issue first for major changes.

## License

[Mozilla Public License 2.0](LICENSE.md)