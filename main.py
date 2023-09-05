# Import the required modules
import oci
import time
from contextlib import redirect_stdout
from datetime import datetime, timedelta, timezone

# Define the variables
private_ip_id = "private_ip_id" # The ID of the private IP to be assigned or deleted
gmt_plus_330 = timezone(timedelta(hours=3, minutes=30)) # The timezone for displaying the time
compartment_id = "compartment_id" # The ID of the compartment where the public IP is created
delete_interval = 50  # The interval in minutes for deleting the public IP

# Create a default config using DEFAULT profile in default location
config = oci.config.from_file()

# Initialize service client with default config file
core_client = oci.core.VirtualNetworkClient(config)

# Initialize the last deleted and last assigned times to the current time
last_deleted = datetime.now()
last_assigned = datetime.now()

# Define a function to calculate the time since the last public IP was assigned
def time_since_last_assigned():
    # Calculate the difference between the current time and the last assigned time
    delta = datetime.now() - last_assigned
    # Convert the difference to minutes and seconds
    minutes, seconds = divmod(delta.total_seconds(), 60)
    # Return a formatted string with the minutes and seconds
    return f"{int(minutes)}m {int(seconds)}s"

# Define a function to check if an IP address should be excluded from being assigned
def should_exclude_ip(ip_address):
    # Open the file that contains the list of excluded IPs
    with open('excluded_ips.txt') as f:
        # Read each line and strip any whitespace characters
        excluded_ips = [line.strip() for line in f]

    # Check if the IP address starts with any of the prefixes that are excluded
    if ip_address.startswith("130.61."):
        return True

    if ip_address.startswith("193.123"):
        return True

    if ip_address.startswith("158.101."):
        return True

    # Check if the IP address is in the list of excluded IPs
    if ip_address in excluded_ips:
        return True

    # If none of the above conditions are met, return False
    return False

# Add this line before the while loop to set the start time to the current time
start_time = datetime.now()

# Ask the user for their choice of running mode
print("Please choose an option:")
print("1. Run the code normally")
print("2. Delete the current public IP and then run the code normally")
print("3. Run the code with a custom start time")
choice = int(input(f"Enter your choice (1, 2 or 3): "))

# Delete the current public IP if the user chose option 2
if choice == 2:
    try:
        # Get the public IP by private IP ID using the core client
        response = core_client.get_public_ip_by_private_ip_id(
            get_public_ip_by_private_ip_id_details=oci.core.models.GetPublicIpByPrivateIpIdDetails(
                private_ip_id=private_ip_id))
        # Get the ID of the public IP from the response data
        public_ip_id = response.data.id
        # Delete the public IP using the core client and the public IP ID
        core_client.delete_public_ip(public_ip_id=public_ip_id)
        # Print a message indicating that the current public IP was deleted successfully
        print("Current public IP deleted. Proceeding with the rest of the code...")
    except oci.exceptions.ServiceError as e:
        # Handle any service errors that might occur while deleting the public IP
        if e.status == 404:
            # If the status code is 404, it means that no public IP was assigned to begin with
            print("No public IP assigned. Proceeding with the rest of the code...")
        else:
            # If any other status code is returned, it means that something went wrong while deleting the public IP
            print("An error occurred while deleting the current public IP:", e)
            exit(1) # Exit the program with an error code of 1

# Add this condition to check if the user chose option 3
elif choice == 3:
    # Use a while loop to keep asking for a valid input from the user
    while True:
        # Ask the user for a number between 0 and delete_interval that represents how many minutes ago they want to start from
        start_minutes = int(input(f"Enter a number between 0 and {delete_interval}: "))
        # Check if the input is valid, i.e., within the range of 0 and delete_interval (inclusive)
        if 0 <= start_minutes <= delete_interval:
            # Adjust the start time by subtracting the input minutes from it using timedelta object
            start_time = start_time - timedelta(minutes=start_minutes)
            # Set the last deleted and last assigned times to the start time
            last_deleted = start_time
            last_assigned = start_time
            # Print a message indicating that the code will run with a custom start time
            print("Running the code with a custom start time...")
            break # Exit the loop
        else:
            # If the input is invalid, print a message asking the user to enter a valid number
            print(f"Invalid input. Please enter a number between 0 and {delete_interval}.")
            # Continue the loop until a valid input is entered

# Start an infinite loop that will run until the program is terminated
while True:
    try:
        # Get the public IP by private IP ID using the core client
        response = core_client.get_public_ip_by_private_ip_id(
            get_public_ip_by_private_ip_id_details=oci.core.models.GetPublicIpByPrivateIpIdDetails(
                private_ip_id=private_ip_id))

        # Get the IP address and the ID of the public IP from the response data
        public_ip = response.data.ip_address
        public_ip_id = response.data.id

        # Print the current time, the public IP, and the time since it was last assigned
        print(datetime.now(gmt_plus_330).strftime("%H:%M:%S"), "Public IP: ", public_ip, "Time since last assigned: ", time_since_last_assigned())

        # Check if it's time to delete the public IP by comparing the current time and the last deleted time
        if (datetime.now() - last_deleted).total_seconds() >= delete_interval * 60:
            # If the difference is greater than or equal to the delete interval in seconds, print a message
            # indicating that the public IP will be deleted
            print(datetime.now(gmt_plus_330).strftime("%H:%M:%S"), "Deleting public IP...")

            # Delete the public IP using the core client and the public IP ID
            core_client.delete_public_ip(public_ip_id=public_ip_id)

            # Update the last deleted time to the current time
            last_deleted = datetime.now()
    except oci.exceptions.ServiceError as e:
        # Handle any service errors that might occur while getting or deleting the public IP
        if e.status == 404:
            # If the status code is 404, it means that no public IP was assigned at the moment
            print(datetime.now(gmt_plus_330).strftime("%H:%M:%S"), "No public IP assigned. Assigning a new one...")

            # Use another while loop to keep trying to assign a new public IP until a valid one is obtained
            while True:
                # Create a new public IP using the core client and passing in the required details such as
                # compartment ID, lifetime, and private IP ID
                response = core_client.create_public_ip(
                    create_public_ip_details=oci.core.models.CreatePublicIpDetails(
                        compartment_id=compartment_id,
                        lifetime="EPHEMERAL",
                        private_ip_id=private_ip_id))

                # Get the new IP address from the response data
                new_public_ip = response.data.ip_address

                # Check if the new IP address should be excluded from being assigned using the defined function
                if should_exclude_ip(new_public_ip):
                    # If yes, print a message indicating that the new IP is excluded and needs to be reassigned
                    print(datetime.now(gmt_plus_330).strftime("%H:%M:%S"), "New IP", new_public_ip, "is excluded. Reassigning...")
                    # Delete the new IP using the core client and passing in its ID from the response data
                    core_client.delete_public_ip(public_ip_id=response.data.id)
                    time.sleep(2)  # Add a 2-second delay here to avoid hitting any rate limits or errors
                else:
                    # If no, break out of the loop as a valid new IP has been obtained
                    break

            # Update the last assigned time to the current time
            last_assigned = datetime.now()
            # Print a message showing the new IP address that was assigned
            print(datetime.now(gmt_plus_330).strftime("%H:%M:%S"), "New IP: ", new_public_ip)
        else:
            # If any other status code is returned, it means that something went wrong while getting or deleting the
            # public IP
            print(datetime.now(gmt_plus_330).strftime("%H:%M:%S"), "An error occurred:", e)

    # Add a 10-second delay before repeating the loop to avoid hitting any rate limits or errors
    time.sleep(10)
