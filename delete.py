import oci
import time
from contextlib import redirect_stdout
from datetime import datetime, timedelta, timezone

# Variables
private_ip_id = "private_ip_ip"
gmt_plus_330 = timezone(timedelta(hours=3, minutes=30))
compartment_id = "compartment_id"
delete_interval = 50  # in minutes

# Create a default config using DEFAULT profile in default location
config = oci.config.from_file()

# Initialize service client with default config file
core_client = oci.core.VirtualNetworkClient(config)

last_deleted = datetime.now()
last_assigned = datetime.now()

def time_since_last_assigned():
    delta = datetime.now() - last_assigned
    minutes, seconds = divmod(delta.total_seconds(), 60)
    return f"{int(minutes)}m {int(seconds)}s"

def should_exclude_ip(ip_address):
    with open('excluded_ips.txt') as f:
        excluded_ips = [line.strip() for line in f]

    if ip_address.startswith("130.61."):
        return True

    if ip_address.startswith("193.123"):
        return True

    if ip_address.startswith("158.101."):
        return True

    if ip_address in excluded_ips:
        return True

    return False

# Delete the current public IP
try:
    response = core_client.get_public_ip_by_private_ip_id(
        get_public_ip_by_private_ip_id_details=oci.core.models.GetPublicIpByPrivateIpIdDetails(
            private_ip_id=private_ip_id))
    public_ip_id = response.data.id
    core_client.delete_public_ip(public_ip_id=public_ip_id)
    print("Current public IP deleted. Proceeding with the rest of the code...")
except oci.exceptions.ServiceError as e:
    if e.status == 404:
        print("No public IP assigned. Proceeding with the rest of the code...")
    else:
        print("An error occurred while deleting the current public IP:", e)
        exit(1)

while True:
    try:
        # Get public IP by private IP ID
        response = core_client.get_public_ip_by_private_ip_id(
            get_public_ip_by_private_ip_id_details=oci.core.models.GetPublicIpByPrivateIpIdDetails(
                private_ip_id=private_ip_id))

        public_ip = response.data.ip_address
        public_ip_id = response.data.id

        print(datetime.now(gmt_plus_330).strftime("%H:%M:%S"), "Public IP: ", public_ip, "Time since last assigned: ", time_since_last_assigned())

        # Check if it's time to delete the public IP
        if (datetime.now() - last_deleted).total_seconds() >= delete_interval * 60:
            print(datetime.now(gmt_plus_330).strftime("%H:%M:%S"), "Deleting public IP...")

            # Delete IP
            core_client.delete_public_ip(public_ip_id=public_ip_id)

            last_deleted = datetime.now()
    except oci.exceptions.ServiceError as e:
        if e.status == 404:
            print(datetime.now(gmt_plus_330).strftime("%H:%M:%S"), "No public IP assigned. Assigning a new one...")

            while True:
                # Create new IP
                response = core_client.create_public_ip(
                    create_public_ip_details=oci.core.models.CreatePublicIpDetails(
                        compartment_id=compartment_id,
                        lifetime="EPHEMERAL",
                        private_ip_id=private_ip_id))

                new_public_ip = response.data.ip_address

                if should_exclude_ip(new_public_ip):
                    print(datetime.now(gmt_plus_330).strftime("%H:%M:%S"), "New IP", new_public_ip, "is excluded. Reassigning...")
                    # Delete IP
                    core_client.delete_public_ip(public_ip_id=response.data.id)
                    time.sleep(2)  # Add a 2-second delay here
                else:
                    break

            last_assigned = datetime.now()
            print(datetime.now(gmt_plus_330).strftime("%H:%M:%S"), "New IP: ", new_public_ip)
        else:
            print(datetime.now(gmt_plus_330).strftime("%H:%M:%S"), "An error occurred:", e)

    time.sleep(10)