from sys import platform

if platform.startswith("win"):
    import sys
    import os
    # Print the current sys.path for debugging purposes (windows version)
    print("Current sys.path:", sys.path)
    # Add the parent directory of the current file to the Python path (Windows version)
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    # Print the updated sys.path to ensure the src directory is included
    print("Updated sys.path:", sys.path)

from src.helper.file_helper import FileHelper
import src.core.config.settings as settings

# Create input folder
FileHelper.create_folder_if_not_exists(settings.files_path)
# Create output folder
FileHelper.create_folder_if_not_exists(settings.output_path)


# Getting issues from Jira
import src.app.get_from_jira
#import src.app.previous_sprints


# Working on stuff
import src.app.work_log
import src.app.issues_status
import src.app.cycle_time
import src.app.graph_creator



