from src.helper.pandas import Pandas as Pd
from src.helper.file_helper import FileHelper
import core.config.settings as settings

folder_path: str = settings.files_path
issues_status_file_name: str = settings.issues_status_file_name
jira_input_file_name: str = settings.input_file_name

#Issues Status
jira_export_file: str = FileHelper.concatenate_path_and_filename(folder_path = folder_path, filename = jira_input_file_name)
complete_issues_df = Pd.read_csv(file_path=jira_export_file)


#Issues Status
issues_status_df = Pd.read_csv(file_path=jira_export_file)
cols_to_keep: list[str] = [settings.jira_summary_col_name, settings.jira_key_col_name, settings.jira_description_col_name, settings.jira_status_col_name, settings.jira_issue_type_col_name, settings.jira_assignee_col_name]
issues_status_df = Pd.select_columns(df = issues_status_df, columns = cols_to_keep)
issue_log_file = FileHelper.concatenate_path_and_filename(folder_path = settings.output_path, filename = settings.issues_log_file_name)
issue_log_df = Pd.read_csv(file_path = issue_log_file)
issues_status_df = Pd.join_dataframes(df1 = issues_status_df, df2 = issue_log_df, on1 = settings.jira_key_col_name, on2 = settings.issue_key_col_name, how = "left")
issues_status_df = Pd.remove_columns(df = issues_status_df, columns_to_remove = [settings.issue_key_col_name])
Pd.save_df_to_csv(df = issues_status_df, relative_path = settings.output_path, file_name = settings.issues_status_file_name)


# Issues Status Report
issues_status_df = Pd.remove_rows_by_values(df = issues_status_df, column= settings.jira_issue_type_col_name, values_to_remove=["Sub-task"])
agg_functions_mapping = {settings.time_hours_col_name: "sum", settings.jira_key_col_name: "count"}
issues_status_report_df = Pd.aggregate_by_column(df = issues_status_df, group_by_column = settings.jira_status_col_name, agg_functions = agg_functions_mapping)
issues_status_report_df = Pd.rename_columns(df = issues_status_report_df, mapping = {settings.jira_key_col_name: settings.issue_count_col_name})
Pd.save_df_to_csv(df = issues_status_report_df, relative_path = settings.output_path, file_name = settings.issues_status_report_file_name)

# Added Value Status Report
added_value_df = Pd.read_csv(file_path=jira_export_file)
added_value_df[settings.jira_original_estimate_col_name] = added_value_df[settings.jira_original_estimate_col_name]/3600
cols_to_keep: list[str] = [
                        settings.jira_summary_col_name,
                        settings.jira_key_col_name,
                        settings.jira_description_col_name,
                        settings.jira_status_col_name,
                        settings.jira_issue_type_col_name,
                        settings.jira_assignee_col_name,
                        settings.jira_original_estimate_col_name
                        ]
added_value_df = Pd.select_columns(df = added_value_df, columns = cols_to_keep)
### Add total_logged_hours
added_value_df = Pd.join_dataframes(
                        df1 = added_value_df,
                        df2 = issue_log_df,
                        on1 = settings.jira_key_col_name,
                        on2 = settings.issue_key_col_name,
                        how = "left"
                        )
added_value_df = Pd.remove_columns(df = added_value_df, columns_to_remove = [settings.issue_key_col_name])
added_value_df = Pd.remove_rows_by_values(df = added_value_df, column= settings.jira_issue_type_col_name, values_to_remove=["Sub-task"])
agg_functions_mapping = {
                        settings.time_hours_col_name: "sum",
                        settings.jira_original_estimate_col_name: "sum",
                        settings.jira_key_col_name: "count"
                        }
added_value_report_df = Pd.aggregate_by_column(
                        df = added_value_df,
                        group_by_column = settings.jira_status_col_name,
                        agg_functions = agg_functions_mapping
                        )
added_value_report_df = Pd.rename_columns(df = added_value_report_df, mapping = {settings.jira_key_col_name: settings.issue_count_col_name})
Pd.save_df_to_csv(df = added_value_report_df, relative_path = settings.output_path, file_name = settings.added_value_csv_name)

# Status per User Report
status_per_user_report_df = Pd.pivot_dataframe(df = added_value_df, y_col = settings.jira_assignee_col_name, x_col=settings.jira_status_col_name)
user_log_file = FileHelper.concatenate_path_and_filename(folder_path = settings.output_path, filename = settings.user_log_file_name)
user_log_df = Pd.read_csv(file_path = user_log_file)
status_per_user_report_df = Pd.join_dataframes(df1 = status_per_user_report_df, df2 = user_log_df, on1 = settings.jira_assignee_col_name, on2 = settings.username_col_name, how = "left")
status_per_user_report_df = Pd.remove_columns(df = status_per_user_report_df, columns_to_remove = [settings.username_col_name])
status_per_user_report_df = Pd.add_days_since_last_log_column(df = status_per_user_report_df, new_column_name=settings.days_since_last_log_col_name, datetime_column=settings.latest_log_date_time_col_name, error_value=0)
Pd.save_df_to_csv(df = status_per_user_report_df, relative_path = settings.output_path, file_name = settings.user_status_report_file_name)


# Status per User Report with Added Value
status_per_user_report_df = Pd.pivot_dataframe_by_col(
                                            df = added_value_df,
                                            y_col = settings.jira_assignee_col_name,
                                            x_col=settings.jira_status_col_name,
                                            value_col=settings.jira_original_estimate_col_name
                                            )
user_log_file = FileHelper.concatenate_path_and_filename(folder_path = settings.output_path, filename = settings.user_log_file_name)
user_log_df = Pd.read_csv(file_path = user_log_file)
status_per_user_report_df = Pd.join_dataframes(df1 = status_per_user_report_df, df2 = user_log_df, on1 = settings.jira_assignee_col_name, on2 = settings.username_col_name, how = "left")
status_per_user_report_df = Pd.remove_columns(df = status_per_user_report_df, columns_to_remove = [settings.username_col_name])
status_per_user_report_df = Pd.add_days_since_last_log_column(df = status_per_user_report_df, new_column_name=settings.days_since_last_log_col_name, datetime_column=settings.latest_log_date_time_col_name, error_value=0)
Pd.save_df_to_csv(df = status_per_user_report_df, relative_path = settings.output_path, file_name = settings.issues_status_report_added_value_file_name)
FileHelper.remove_file(path = settings.output_path, file_name = settings.user_log_file_name)
