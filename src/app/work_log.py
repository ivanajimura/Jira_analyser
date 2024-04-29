from src.helper.pandas import Pandas as Pd
from src.helper.file_helper import FileHelper
import core.config.settings as settings

folder_path = settings.files_path
work_log_file_name = settings.work_log_file_name
jira_input_file_name = settings.input_file_name

# Work Log
jira_export_file: str = FileHelper.concatenate_path_and_filename(folder_path = folder_path, filename = jira_input_file_name)
work_log_df = Pd.read_csv(file_path=jira_export_file)
work_log_df = Pd.extract_work_log_columns(df = work_log_df)
work_log_df = Pd.extract_work_logs(df = work_log_df)
work_log_df = Pd.add_combined_column(df = work_log_df, source_column = settings.issue_key_col_name, fixed_value = settings.jira_issue_url_prefix, new_column_name = settings.issue_link_col_name)
work_log_df = Pd.extract_datetime_components(df = work_log_df, datetime_column = settings.date_time_col_name)
work_log_df = Pd.add_hours_column(df = work_log_df, seconds_column = settings.time_seconds_col_name, new_column_name = settings.time_hours_col_name)
work_log_df = Pd.add_minutes_column(df = work_log_df, seconds_column = settings.time_seconds_col_name, new_column_name = settings.time_minutes_col_name)
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