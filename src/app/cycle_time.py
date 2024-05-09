from src.helper.pandas import Pandas as Pd
from src.helper.file_helper import FileHelper
import core.config.settings as settings

folder_path: str = settings.files_path
issues_status_file_name: str = settings.issues_status_file_name
jira_input_file_name: str = settings.input_file_name

jira_export_file: str = FileHelper.concatenate_path_and_filename(folder_path = folder_path, filename = jira_input_file_name)
complete_issues_df = Pd.read_csv(file_path=jira_export_file)

# Cycle Time
## Cycle Time is the delta between the conclusion of a task and the moment it was first put in progress
## Two custom fields were created in Jira "Custom field (Date Time Concluded)" and "Custom field (Date Time Started)"
## The calculations must take into consideration that some issues may not have or either field filled in.

all_issues_df = Pd.read_and_concat_csv(folder_path = folder_path, filename_prefix = settings.previous_sprints_prefix, filename_col = settings.sprint_id_col)
columns_to_keep: list = [
        settings.jira_summary_col_name,
        settings.jira_key_col_name,
        settings.jira_status_col_name,
        settings.jira_description_col_name,
        settings.jira_epic_col_name,
        settings.jira_issue_type_col_name,
        settings.jira_assignee_col_name,
        settings.jira_original_estimate_col_name,
        settings.jira_datetime_created_col_name,
        settings.jira_datetime_started_col_name,
        settings.jira_datetime_concluded_col_name,
        settings.sprint_id_col
]
all_issues_df = all_issues_df[columns_to_keep]
all_issues_df[settings.cycle_time_col] = Pd.calculate_date_difference(df = all_issues_df, column1 = settings.jira_datetime_concluded_col_name, column2 = settings.jira_datetime_started_col_name)
all_issues_df[settings.lead_time_col] = Pd.calculate_date_difference(df = all_issues_df, column1 = settings.jira_datetime_concluded_col_name, column2 = settings.jira_datetime_created_col_name)

cycle_time_df = Pd.group_by(df = all_issues_df, group_col=settings.sprint_id_col, value_col= settings.cycle_time_col, aggregation="mean")
lead_time_df = Pd.group_by(df = all_issues_df, group_col=settings.sprint_id_col, value_col= settings.lead_time_col, aggregation="mean")
cycle_lead_time_df = Pd.join_dataframes(df1 = cycle_time_df, df2 = lead_time_df, on1= settings.sprint_id_col, on2=settings.sprint_id_col, how = "outer")
Pd.save_df_to_csv(df = cycle_lead_time_df, relative_path=settings.output_path, file_name=settings.cycle_time_csv_name)