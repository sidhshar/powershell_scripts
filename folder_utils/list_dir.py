import os
import csv
from datetime import datetime
from dotenv import load_dotenv
import sys

# Load .env file
load_dotenv()

root_path = os.getenv("ROOT_PATH")
output_file = os.getenv("OUTPUT_CSV")

# Validate configuration
if not root_path:
    sys.exit("ERROR: ROOT_PATH not set in .env")

if not output_file:
    sys.exit("ERROR: OUTPUT_CSV not set in .env")

if not os.path.exists(root_path):
    sys.exit(f"ERROR: ROOT_PATH does not exist: {root_path}")

# Ensure output directory exists
os.makedirs(os.path.dirname(output_file), exist_ok=True)

with open(output_file, mode='w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
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

    for root, dirs, files in os.walk(root_path):
        depth = root.replace(root_path, "").count(os.sep)

        # Directories
        for dir_name in dirs:
            full_path = os.path.join(root, dir_name)
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

        # Files
        for file in files:
            full_path = os.path.join(root, file)
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

print(f"Inventory export completed: {output_file}")
