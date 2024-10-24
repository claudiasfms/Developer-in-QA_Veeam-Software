#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
import shutil
import time
import logging
import argparse

def setup_logging(log_file):
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s]: %(message)s",
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )

def sync_folders(source_folder, replica_folder, interval_seconds, log_file):
    setup_logging(log_file)

    while True:
        
        if not os.path.exists(source_folder):
            os.makedirs(source_folder)
            logging.info(f"Created source folder: {source_folder}")

        if not os.path.exists(replica_folder):
            os.makedirs(replica_folder)
            logging.info(f"Created replica folder: {replica_folder}")
        
        for root, dirs, files in os.walk(source_folder):
            # Calculate relative paths
            relative_path = os.path.relpath(root, source_folder)
            replica_path = os.path.join(replica_folder, relative_path)

            # Create subfolders in replica folder if they don't exist
            for dir_name in dirs:
                source_dir = os.path.join(root, dir_name)
                replica_dir = os.path.join(replica_path, dir_name)
                if not os.path.exists(replica_dir):
                    os.makedirs(replica_dir)
                    logging.info(f"Created folder: {replica_dir}")

             # Copy files to the replica folder
            for file_name in files:
                source_file = os.path.join(root, file_name)
                replica_file = os.path.join(replica_path, file_name)
                shutil.copy2(source_file, replica_file)
                logging.info(f"Copied: {source_file} to {replica_file}")

        # Remove files and folders in replica folder that don't exist in source folder
        for root, dirs, files in os.walk(replica_folder):
            for dir_name in dirs:
                replica_dir = os.path.join(root, dir_name)
                source_dir = os.path.join(source_folder, os.path.relpath(replica_dir, replica_folder))
                if not os.path.exists(source_dir):
                    shutil.rmtree(replica_dir)
                    logging.warning(f"Removed folder: {replica_dir}")

            for file_name in files:
                replica_file = os.path.join(root, file_name)
                source_file = os.path.join(source_folder, os.path.relpath(replica_file, replica_folder))
                if not os.path.exists(source_file):
                    os.remove(replica_file)
                    logging.warning(f"Removed file: {replica_file}")

        logging.info("Synchronization complete.")

        # Wait for the specified interval before the next synchronization
        time.sleep(interval_seconds)


def main():
    parser = argparse.ArgumentParser(description="Folder synchronization script")
    parser.add_argument("source_folder", help="Path to source folder")
    parser.add_argument("replica_folder", help="Path to replica folder")
    parser.add_argument("interval_seconds", type=int, help="Synchronization interval in seconds")
    parser.add_argument("log_file", help="Path to the log file")

    args = parser.parse_args()

    sync_folders(
        args.source_folder,
        args.replica_folder,
        args.interval_seconds,
        args.log_file
    )

    
if __name__ == "__main__":
    main()
"""

python main.py /path/to/source/folder /path/to/replica/folder 60 sync_log.txt
"""  
