import os
import datetime
import shutil

# IMPORTANT VARIABLES
FILE_PREFIX = 'GoPro'
FILE_FORMAT = 'MP4'
SRC_PATH = 'E:/DCIM/100GOPRO'
DST_PATH = 'C:/Users/prana/code/dst'

# Get the list of all files in the directory
file_list = os.listdir(SRC_PATH)
file_count = 0
for file in file_list:
    if FILE_FORMAT in file:
        file_count += 1

# Loop through each file in the list
cp_count = 1
for file_name in file_list:
    if FILE_FORMAT in file_name:
        file_path = os.path.join(SRC_PATH, file_name)

        # Get the creation time of the file
        creation_time = os.path.getmtime(file_path)

        # Convert the creation time to a formatted date and time string
        date_time_str = datetime.datetime.fromtimestamp(creation_time).strftime('%Y_%m_%d_%H_%M_%S')

        # Create new file name
        new_file_name = "{}_{}.{}".format(date_time_str, FILE_PREFIX, file_name.split('.')[1])

        # Check if the new file name already exists
        if os.path.exists(os.path.join(DST_PATH, new_file_name)):
            i = 1
            while os.path.exists(os.path.join(DST_PATH, "{}_f{}_{}.{}".format(date_time_str, i, FILE_PREFIX, file_name.split('.')[1]))):
                i += 1
            new_file_name = "{}_f{}_{}.{}".format( date_time_str, i, FILE_PREFIX, file_name.split('.')[1])

        # Copy and Rename the file
        dest_path = os.path.join( DST_PATH, new_file_name )
        shutil.copyfile( file_path, dest_path)
        print( f'copied {cp_count} of {file_count} files' )
        cp_count += 1

print( "\nFiles copied and renamed successfully" )
