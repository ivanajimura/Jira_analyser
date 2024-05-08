import time
import src.core.config.settings as settings
import src.core.config.user_config as user_config

from src.service.jira import Jira

from src.helper.pandas import Pandas as Pd
from src.helper.file_helper import FileHelper



# Get sprints
sprint_download_link = settings.jira_sprints_url
Jira.download_csv_from_jql(
    username = user_config.jira_username,
    password = user_config.jira_password,
    csv_url = sprint_download_link,
    folder_path = settings.files_path,
    file_name=settings.sprints_file_name
)

# Open files/sprints.csv
folder_path: str = settings.files_path
sprints_file_name: str = settings.sprints_file_name

sprints_file: str = FileHelper.concatenate_path_and_filename(folder_path = folder_path, filename = sprints_file_name)
sprints_df = Pd.read_csv(file_path=sprints_file)

# Save to CSV
sprints_df = Pd.load_json_to_dataframe(
    file_path=FileHelper.concatenate_path_and_filename(
                                            folder_path = folder_path, filename= settings.sprints_file_name),
    values_key = settings.sprints_key)
df = Pd.extract_datetime_components(df = sprints_df, datetime_column=settings.sprint_start_date_col)
Pd.save_df_to_csv(df = sprints_df, relative_path=settings.output_path, file_name=settings.sprints_df_name)


# Reduce columns
columns_to_keep = [
                    settings.sprint_id_col,
                    settings.sprints_state_col,
                    settings.sprint_start_date_col,
                    settings.sprint_end_date_col,
                    settings.sprint_name_col,
                    settings.sprint_link_col,
                    settings.sprint_goal_col,
]
sprints_df = sprints_df[columns_to_keep]

# Download issues from other sprints
sprint_ids = sprints_df[settings.sprint_id_col].unique().tolist()

for sprint_id in sprint_ids:
    time.sleep(2)
    previous_sprint_query: str = f"project='{settings.jira_project}' AND sprint = {sprint_id}"
    download_link = Jira.parse_jql_into_url(jql_query = previous_sprint_query, base_url= settings.csv_download_prefix)
    Jira.download_csv_from_jql(
        username = user_config.jira_username,
        password = user_config.jira_password,
        csv_url = download_link,
        folder_path = settings.files_path,
        file_name=f"issues_sprint_{sprint_id}.csv"
    )
