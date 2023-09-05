# OCI Instance Automation

## Introduction

This repository contains Python and Shell scripts that help automate the process of launching, managing, and terminating instances on Oracle Cloud Infrastructure (OCI). The code is specifically designed to automate the process of changing IP addresses at a desired interval.

## Prerequisites

1. Python 3.x
2. Oracle Cloud Infrastructure CLI
3. OCI Python SDK

## Code Example

The repository includes Python code with functions for IP management on OCI instances. Below is an example:

\`\`\`python
# Import required modules
import oci
import time
...
\`\`\`

> **Note**: The complete code can be found in the repository.

## Installation

\`\`\`bash
git clone https://github.com/your_username/OCI_Instance_Automation.git
cd OCI_Instance_Automation
pip install -r requirements.txt
\`\`\`

## Usage

### How the Automation Works

1. **Initialize**: The script starts by importing the necessary modules and setting up the OCI client.
2. **User Choices**: The user is presented with different choices for running the script.
3. **Manage Public IP**: Depending on the user's choice, the script either assigns a new public IP or deletes the current one.
4. **Exclusions**: The script can exclude specific IP addresses or ranges.
5. **Logging**: The script prints the status of the public IP and the time since it was last assigned.
6. **Killing Processes**: If you need to terminate the automation process, you can use the `kill.sh` script.

### Benefits

1. **Efficiency**: Reduces the manual effort needed to manage instances.
2. **Consistency**: Ensures that public IPs are managed according to the specified rules.
3. **Flexibility**: User choices allow for custom run modes.

### Important Notice

The user must receive the API key to interact with the Oracle server from another server using OCI CLI. For more information, please read Oracle's official documentation.

## Contributing

Feel free to contribute. Please open an issue first for major changes.

## License

[Mozilla Public License 2.0](LICENSE.md)
