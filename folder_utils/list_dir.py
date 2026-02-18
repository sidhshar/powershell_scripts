import os
import csv
from datetime import datetime
from dotenv import load_dotenv
import sys

load_dotenv()

root_path = os.getenv("ROOT_PATH")
output_file = os.getenv("OUTPUT_CSV")
error_log = "permission_errors.csv"

if not root_path:
    sys.exit("ERROR: ROOT_PATH not set in .env")

if not output_file:
    sys.exit("ERROR: OUTPUT_CSV not set in .env")

if not os.path.exists(root_path):
    sys.exit(f"ERROR: ROOT_PATH does not exist: {root_path}")

os.makedirs(os.path.dirname(output_file), exist_ok=True)

with open(output_file, mode='w', newline='', encoding='utf-8') as csvfile, \
     open(error_log, mode='w', newline='', encoding='utf-8') as errorfile:

    writer = csv.writer(csvfile)
    error_writer = csv.writer(errorfile)

    writer.writerow([
        "Type",
        "Name",
        "Full Path",
        "Extension",
        "Size (MB)",
        "Created",
        "Last Modified",
        "Depth"
    ])

    error_writer.writerow(["Path", "Error"])

    for root, dirs, files in os.walk(root_path, onerror=None):

        depth = root.replace(root_path, "").count(os.sep)

        # Directories
        for dir_name in dirs:
            full_path = os.path.join(root, dir_name)
            try:
                stat = os.stat(full_path)
                writer.writerow([
                    "Directory",
                    dir_name,
                    full_path,
                    "",
                    "",
                    datetime.fromtimestamp(stat.st_ctime),
                    datetime.fromtimestamp(stat.st_mtime),
                    depth
                ])
            except Exception as e:
                error_writer.writerow([full_path, str(e)])

        # Files
        for file in files:
            full_path = os.path.join(root, file)
            try:
                stat = os.stat(full_path)
                writer.writerow([
                    "File",
                    file,
                    full_path,
                    os.path.splitext(file)[1],
                    round(stat.st_size / (1024 * 1024), 2),
                    datetime.fromtimestamp(stat.st_ctime),
                    datetime.fromtimestamp(stat.st_mtime),
                    depth
                ])
            except Exception as e:
                error_writer.writerow([full_path, str(e)])

print(f"Inventory export completed: {output_file}")
print(f"Permission errors logged to: {error_log}")
