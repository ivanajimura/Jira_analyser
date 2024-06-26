from src.helper.pandas import Pandas as Pd
from src.helper.file_helper import FileHelper
import core.config.settings as settings
from datetime import datetime, timedelta

folder_path = settings.files_path
work_log_file_name = settings.work_log_file_name
jira_input_file_name = settings.input_file_name


# Sprints
sprints_df = Pd.read_csv(file_path= FileHelper.concatenate_path_and_filename(folder_path=folder_path, filename=settings.sprints_df_name))

#sprints_df = Pd.extract_datetime_components(df = sprints_df, datetime_column=settings.sprint_start_date_col)
#Pd.save_df_to_csv(df = sprints_df, relative_path=settings.output_path, file_name=settings.sprints_df_name) ## moved to previous_sprints.py

# Get start date of current sprint
"""
sprint_start_year = Pd.get_cell_value_by_condition(
    df = sprints_df, search_column = "state", search_value="active", return_column="Year"
)[0]

sprint_start_month = Pd.get_cell_value_by_condition(
    df = sprints_df, search_column = "state", search_value="active", return_column="Month"
)[0]
sprint_start_day = Pd.get_cell_value_by_condition(
    df = sprints_df, search_column = "state", search_value="active", return_column="Day"
)[0]

sprint_start_date = datetime(year = 2024, month = 6, day = 3)
"""

sprint_start_year = Pd.get_cell_value_by_condition(
    df = sprints_df, search_column = "id", search_value = settings.selected_sprint, return_column = "Year"
    )[0]
sprint_start_month = Pd.get_cell_value_by_condition(
    df = sprints_df, search_column = "id", search_value = settings.selected_sprint, return_column = "Month"
    )[0]
sprint_start_day = Pd.get_cell_value_by_condition(
    df = sprints_df, search_column = "id", search_value = settings.selected_sprint, return_column = "Day"
    )[0]
sprint_start_date: datetime = datetime(year=sprint_start_year, month=sprint_start_month, day=sprint_start_day)
sprint_end_date: datetime = sprint_start_date + timedelta(days = 14) #TODO improve this

jira_export_file: str = FileHelper.concatenate_path_and_filename(folder_path = folder_path, filename = jira_input_file_name)
complete_issues_df = Pd.read_csv(file_path=jira_export_file)

# Work Log
work_log_df = Pd.read_csv(file_path=jira_export_file)
work_log_df = Pd.extract_work_log_columns(df = work_log_df)
work_log_df = Pd.extract_work_logs(df = work_log_df)
work_log_df = Pd.add_combined_column(df = work_log_df, source_column = settings.issue_key_col_name, fixed_value = settings.jira_issue_url_prefix, new_column_name = settings.issue_link_col_name)
work_log_df = Pd.extract_datetime_components(df = work_log_df, datetime_column = settings.date_time_col_name)
work_log_df = Pd.add_hours_column(df = work_log_df, seconds_column = settings.time_seconds_col_name, new_column_name = settings.time_hours_col_name)
work_log_df = Pd.add_minutes_column(df = work_log_df, seconds_column = settings.time_seconds_col_name, new_column_name = settings.time_minutes_col_name)
#work_log_df = Pd.remove_rows_before_datetime(df = work_log_df, datetime_column= settings.date_time_col_name, threshold_datetime=sprint_start_date)
#work_log_df = Pd.remove_rows_after_datetime(df = work_log_df, datetime_column= settings.date_time_col_name, threshold_datetime=sprint_end_date)
work_log_df = Pd.remove_rows_before_or_after_datetime(df = work_log_df, datetime_column= settings.date_time_col_name, threshold_datetime=sprint_start_date, before_or_after='before')
#Remove after not being used because work log in Jira is saved with the date when the log is made, not the day defined by the user
#work_log_df = Pd.remove_rows_before_or_after_datetime(df = work_log_df, datetime_column= settings.date_time_col_name, threshold_datetime=sprint_end_date, before_or_after='after')
### get estimate for each issue
work_log_df = Pd.join_dataframes(df1=work_log_df, df2=complete_issues_df, on1=settings.issue_key_col_name, on2 = settings.jira_key_col_name, how="left")
columns_to_keep = [
                            settings.username_col_name,
                            settings.issue_key_col_name,
                            settings.summary_col_name,
                            settings.work_log_description_col_name,
                            settings.jira_issue_type_col_name,
                            settings.date_time_col_name,
                            settings.issue_link_col_name,
                            "Year", "Month", "Day", "Hour", "Minute",       # TODO Refactor this
                            settings.time_hours_col_name,
                            settings.time_minutes_col_name,
                            settings.jira_original_estimate_col_name
                        ]
work_log_df = work_log_df[columns_to_keep]
### convert original estimate to hours
work_log_df[settings.jira_original_estimate_col_name] = work_log_df[settings.jira_original_estimate_col_name] / 3600
Pd.save_df_to_csv(df = work_log_df, relative_path = settings.output_path, file_name = settings.work_log_file_name)

# Log per user
user_log_df = Pd.process_work_log(df = work_log_df, group_by_col = settings.username_col_name, orig_time_col = settings.time_hours_col_name, orig_date_col = settings.date_time_col_name)
user_log_rename_mapping: dict[str: str] = {settings.date_time_col_name: settings.latest_log_date_time_col_name, settings.time_hours_col_name: settings.total_logged_hours_col_name}
user_log_df = Pd.rename_columns(df = user_log_df, mapping = user_log_rename_mapping)
Pd.save_df_to_csv(df = user_log_df, relative_path = settings.output_path, file_name = settings.user_log_file_name)

# Log per issue
aggregate_functions_dict = {settings.time_hours_col_name: "sum"}
issue_log_df = Pd.aggregate_by_column(df = work_log_df, group_by_column = settings.issue_key_col_name, agg_functions = aggregate_functions_dict)
Pd.save_df_to_csv(df = issue_log_df, relative_path = settings.output_path, file_name = settings.issues_log_file_name)

