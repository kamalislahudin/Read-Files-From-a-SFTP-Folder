import paramiko
import pandas as pd
from io import BytesIO

# Define SFTP server details
sftp_host = 'your_sftp_server'
sftp_port = 22
sftp_username = 'your_username'
sftp_password = 'your_password'
remote_path = '/home/file/'

# Create an SSH client
client = paramiko.SSHClient()
client.load_system_host_keys()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# Connect to the SFTP server
client.connect(sftp_host, port=sftp_port, username=sftp_username, password=sftp_password)
# Open an SFTP session
sftp = client.open_sftp()
# Retrieve the list of files in the remote folder
files = sftp.listdir(remote_path)
# Create an empty list to store dataframes
dataframes = []

# Read and process each file
for file in files:
    file_path = remote_path + file  # Get the full path of the file
    sftp_file = sftp.open(file_path, 'r')
    data = sftp_file.read()
    sftp_file.close()

    # Convert the bytes data to BytesIO
    data_object = BytesIO(data)

    # Create a DataFrame from the BytesIO object, excluding the header
    column_names = ["column1", "column2", "column3", ... "column64"]
    df = pd.read_csv(data_object, sep=',', quotechar='"', header=None, names=column_names, skiprows=1)
    dataframes.append(df)

# Close the SFTP connection
sftp.close()
client.close()

# Concatenate the list of DataFrames into one DataFrame
combined_df = pd.concat(dataframes, ignore_index=True)