from src.helper.graph_gen import Graph
from src.helper.pandas import Pandas as Pd
from src.helper.file_helper import FileHelper

import src.core.config.settings as settings


# Hours per User
hour_user_file: str = FileHelper.concatenate_path_and_filename(folder_path=settings.output_path, filename=settings.user_status_report_file_name)   
hour_user_df = Pd.read_csv(file_path = hour_user_file)

Graph.create_bar_chart(df = hour_user_df, x = settings.jira_assignee_col_name, y = settings.total_logged_hours_col_name)
Graph.save_plot(folder_path=settings.output_path, file_name=settings.logged_hours_per_assignee_graph, title= "Logged Hours per Person")
Graph.create_bar_chart(df = hour_user_df, x = settings.jira_assignee_col_name, y = settings.days_since_last_log_col_name)
Graph.save_plot(folder_path=settings.output_path, file_name=settings.days_since_last_log_per_user_graph, title= "Days Since Last Work Log")
y_columns = ["Rejected", "To Refine", "Ready to Develop", "In Progress", "Blocked", "In Review", "Done"]
color_mapping = {"Rejected": "silver", "To Refine": "gray", "Ready to Develop": "dimgray", "In Progress": "skyblue", "Blocked": "firebrick", "In Review": "seagreen", "Done": "lime"}
Graph.create_stacked_bar_chart(df=hour_user_df, x = settings.jira_assignee_col_name, y_columns = y_columns, colors=color_mapping)
Graph.save_plot(folder_path=settings.output_path, file_name=settings.issues_status_per_user_graph, title= "Issues Status per User")

issue_status_report_file: str = FileHelper.concatenate_path_and_filename(folder_path=settings.output_path, filename=settings.issues_status_report_file_name)   
issue_status_report_df = Pd.read_csv(file_path = issue_status_report_file)
y_columns = [settings.time_hours_col_name, settings.issue_count_col_name]
x_values = ["Rejected", "To Refine", "Ready to Develop", "In Progress", "Blocked", "In Review", "Done"]
Graph.create_multi_bar_chart(df = issue_status_report_df, x_column = settings.jira_status_col_name, x_values = x_values, y_columns = y_columns)
Graph.save_plot(folder_path=settings.output_path, file_name=settings.hours_and_count_per_status_graph, title= "Sprint Status")
