from src.helper.graph_gen import Graph
from src.helper.pandas import Pandas as Pd
from src.helper.file_helper import FileHelper

import src.core.config.settings as settings


# Hours per User
hour_user_file: str = FileHelper.concatenate_path_and_filename(folder_path=settings.output_path, filename=settings.user_status_report_file_name)   
hour_user_df = Pd.read_csv(file_path = hour_user_file)
Graph.create_bar_chart(df = hour_user_df, x = settings.jira_assignee_col_name, y = settings.total_logged_hours_col_name)
Graph.save_plot(folder_path=settings.output_path, file_name=settings.logged_hours_per_assignee_graph, title= "Logged Hours per Person")

# Work Log per sprint
wl_per_sprint_file: str = FileHelper.concatenate_path_and_filename(folder_path=settings.output_path, filename=settings.work_log_per_sprint_file_name)   
wl_per_sprint_df = Pd.read_csv(file_path = wl_per_sprint_file)
Graph.create_line_graph(df = wl_per_sprint_df, x_col=settings.sprint_id_col, y_cols=[settings.time_hours_col_name], colors={settings.time_hours_col_name: "skyblue" })
Graph.save_plot(folder_path=settings.output_path, file_name=settings.wl_per_sprint_graph, title= "Logged Hours per Sprint")


# Days since Last Work Log
Graph.create_bar_chart(df = hour_user_df, x = settings.jira_assignee_col_name, y = settings.days_since_last_log_col_name)
Graph.save_plot(folder_path=settings.output_path, file_name=settings.days_since_last_log_per_user_graph, title= "Days Since Last Work Log")

# Number of Issue Status per User
y_columns = ["Rejected", "To Refine", "Ready to Develop", "In Progress", "Blocked", "In Review", "Done"]
color_mapping = {"Rejected": "silver", "To Refine": "gray", "Ready to Develop": "dimgray", "In Progress": "skyblue", "Blocked": "firebrick", "In Review": "seagreen", "Done": "lime"}
Graph.create_stacked_bar_chart(df=hour_user_df, x = settings.jira_assignee_col_name, y_columns = y_columns, colors=color_mapping)
Graph.save_plot(folder_path=settings.output_path, file_name=settings.issues_status_per_user_graph, title= "Issues Status per User")

# Added Value per User
added_value_file: str = FileHelper.concatenate_path_and_filename(folder_path=settings.output_path, filename=settings.issues_status_report_added_value_file_name)   
added_value_df = Pd.read_csv(file_path = added_value_file)
y_columns = ["Rejected", "To Refine", "Ready to Develop", "In Progress", "Blocked", "In Review", "Done"]
color_mapping = {"Rejected": "silver", "To Refine": "gray", "Ready to Develop": "dimgray", "In Progress": "skyblue", "Blocked": "firebrick", "In Review": "seagreen", "Done": "lime"}
Graph.create_stacked_bar_chart(df=added_value_df, x = settings.jira_assignee_col_name, y_columns = y_columns, colors=color_mapping)
Graph.save_plot(folder_path=settings.output_path, file_name=settings.added_value_per_status_graph, title= "Added Value per User")

# Added value per Sprint
av_per_sprint_file = FileHelper.concatenate_path_and_filename(folder_path=settings.output_path, filename=settings.added_value_per_sprint_csv_name)
av_per_sprint_df = Pd.read_csv(file_path=av_per_sprint_file)
y_columns = [settings.jira_ready, settings.jira_in_progress, settings.jira_done]
color_mapping = {settings.jira_ready: "dimgray", settings.jira_in_progress: "skyblue", settings.jira_done: "lime"}
Graph.create_stacked_bar_chart(df = av_per_sprint_df, x = settings.sprint_id_col, y_columns=y_columns, colors=color_mapping)
Graph.save_plot(folder_path=settings.output_path, file_name=settings.added_value_per_sprint_graph, title= "Added Value per Sprint")

# Added value per Sprint (Relative)
rel_av_per_sprint_file = FileHelper.concatenate_path_and_filename(folder_path=settings.output_path, filename=settings.relative_added_value_per_sprint_csv_name)
rel_av_per_sprint_df = Pd.read_csv(file_path=rel_av_per_sprint_file)
y_columns = [settings.jira_ready, settings.jira_in_progress, settings.jira_done]
color_mapping = {settings.jira_ready: "dimgray", settings.jira_in_progress: "skyblue", settings.jira_done: "lime"}
Graph.create_line_graph(df = rel_av_per_sprint_df, x_col = settings.sprint_id_col, y_cols = y_columns, colors = color_mapping, x_label = "Sprint", y_label = "%")
Graph.save_plot(folder_path=settings.output_path, file_name=settings.rel_added_value_per_sprint_graph, title= "Relative Added Value per Sprint")

# Logged Hours, Added Value and Number of issues per status
added_value_report_file: str = FileHelper.concatenate_path_and_filename(folder_path=settings.output_path, filename=settings.added_value_csv_name)   
added_value_report_df = Pd.read_csv(file_path = added_value_report_file)
y_columns = [settings.time_hours_col_name, settings.issue_count_col_name, settings.jira_original_estimate_col_name]
x_values = ["Rejected", "To Refine", "Ready to Develop", "In Progress", "Blocked", "In Review", "Done"]
Graph.create_multi_bar_chart(df = added_value_report_df, x_column = settings.jira_status_col_name, x_values = x_values, y_columns = y_columns)
Graph.save_plot(folder_path=settings.output_path, file_name=settings.hours_and_count_per_status_graph, title= "Sprint Status")

#Cycle and Lead Time
cycle_lead_time_file = FileHelper.concatenate_path_and_filename(folder_path=settings.output_path, filename=settings.cycle_time_csv_name)
cycle_lead_time_df = Pd.read_csv(file_path=cycle_lead_time_file)
y_columns = [settings.cycle_time_col, settings.lead_time_col]
Graph.create_multi_bar_chart(df = cycle_lead_time_df, x_column=settings.sprint_id_col, x_values=settings.sprints_to_consider,y_columns=y_columns)
Graph.save_plot(folder_path=settings.output_path, file_name=settings.cycle_lead_time_graph, title= "Cycle and Lead Time per Sprint")


# Subtasks per Sprint
## Subtasks per Task per Sprint
sprints_file = FileHelper.concatenate_path_and_filename(folder_path = settings.files_path, filename = settings.sprints_df_name)
sprint_df = Pd.read_csv(file_path = sprints_file)
Graph.create_bar_chart(df = sprint_df, x = settings.sprint_id_col, y = settings.n_subtasks_per_task)
Graph.save_plot(folder_path=settings.output_path, file_name=settings.subtasks_per_task_per_sprint_graph, title = "Average Number of Subtasks per Task per Sprint")

## Subtasks per Sprint
Graph.create_bar_chart(df = sprint_df, x = settings.sprint_id_col, y = settings.number_subtasks)
Graph.save_plot(folder_path=settings.output_path, file_name=settings.subtasks_per_sprint_graph, title = "Number of Subtasks per Sprint")

## Tasks and Subtasks per Sprint
x_values = Pd.list_unique_values_in_col(df = sprint_df, column = settings.sprint_id_col)
Graph.create_multi_bar_chart(df = sprint_df, x_column=settings.sprint_id_col, x_values=x_values, y_columns=[settings.number_tasks, settings.number_subtasks])
Graph.save_plot(folder_path=settings.output_path, file_name=settings.tasks_subtasks_per_sprint_graph, title = "Number of Tasks and Subtasks per Sprint")

##Total Subtasks per Assignee
subtasks_per_assignee_file = FileHelper.concatenate_path_and_filename(folder_path=settings.output_path, filename=settings.total_subtasks_per_assignee_csv)
total_subtasks_df = Pd.read_csv(file_path=subtasks_per_assignee_file)
Graph.create_bar_chart(df = total_subtasks_df, x = settings.jira_assignee_col_name, y = settings.number_subtasks)
Graph.save_plot(folder_path=settings.output_path, file_name=settings.total_subtasks_per_assignee_graph, title = "Total Subtasks per Assignee")

