from src.helper.file_helper import FileHelper
import src.core.config.settings as settings

# Create input folder
FileHelper.create_folder_if_not_exists(settings.files_path)
# Create output folder
FileHelper.create_folder_if_not_exists(settings.output_path)


"""
"""
import src.app.get_from_jira
import src.app.work_log
import src.app.issues_status
