from datetime import datetime

selected_sprint = 14        # select sprint number here

sprint_duration_days = 14
current_dateTime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")



files_path = r"files"
output_path = r"output"
input_file_name = "jira_export.csv"


# JIRA
jira_instance_url = "https://studio.mse.dei.uc.pt/jira/"
jira_project = "MSE23-24"
csv_download_prefix = "https://studio.mse.dei.uc.pt/jira/sr/jira.issueviews:searchrequest-csv-all-fields/temp/SearchRequest.csv?"

jira_summary_col_name = "Summary"
jira_key_col_name = "Issue key"
jira_log_work_col_name = "Log Work"
jira_status_col_name = "Status"
jira_description_col_name = "Description"
jira_epic_col_name = "Custom field (Epic Link)"
jira_sprint_cols_name = "Sprint"
jira_issue_url_prefix = "https://studio.mse.dei.uc.pt/jira/browse/"
jira_issue_type_col_name = "Issue Type"
jira_assignee_col_name = "Assignee"
jira_original_estimate_col_name = "Original Estimate"
jira_datetime_started_col_name = "Custom field (Date Time Started)"
jira_datetime_concluded_col_name = "Custom field (Date Time Concluded)"
jira_datetime_created_col_name = "Created"


jira_sprints_url = "https://studio.mse.dei.uc.pt/jira/rest/agile/1.0/board/3/sprint"
# Sprints
sprints_file_name = "sprints_json.json"
sprints_df_name = "sprints.csv"
sprints_key = "values"
sprint_id_col = "id"
sprints_state_col = "state"
sprint_closed_state_col = "closed"
sprint_active_state_col = "active"
sprint_start_date_col = "startDate"
sprint_end_date_col = "endDate"
sprint_name_col = "name"
sprint_link_col = "self"
sprint_goal_col = "goal"
previous_sprints_prefix = "issues_sprint_"


# Generic DataFrame settings
issue_link_col_name = "Link"

# Work Log
work_log_file_name = "work_log.csv"
date_time_col_name = "date_time"
issue_key_col_name = "issue_key"
summary_col_name = "summary"
username_col_name = "username"
work_log_description_col_name = "description"
time_seconds_col_name = "log_in_seconds"
time_minutes_col_name = "log_in_minutes"
time_hours_col_name = "log_in_hours"

# User log
latest_log_date_time_col_name = "latest_log"
days_since_last_log_col_name = "days_since_last_log"
total_logged_hours_col_name = "total_logged_hours"
user_log_file_name = "user_log.csv"

# Issue log
issues_log_file_name = "issue_log.csv"

# Issues Status
issues_status_file_name = "issue_status.csv"
issue_count_col_name = "issue_count"
issues_status_report_file_name = "issue_status_report.csv"
issues_status_report_added_value_file_name = "issue_status_report_added_value.csv"
user_status_report_file_name = "user_status_report.csv"


# Added value
added_value_csv_name = "added_value_report.csv"

# Cycle Time
cycle_time_csv_name = "cycle_time.csv"
cycle_time_col = "cycle_time"
lead_time_col = "lead_time"
sprints_to_consider =[1, 3, 12] 

#Sub-tasks
number_tasks = "n tasks"
number_subtasks = "n subtasks"
subtask_issue_type = "Sub-task"
n_subtasks_per_task = "n subtasks per task"
valid_issue_types = ["Task", "Bug", "Story"]


# Graphs
logged_hours_per_assignee_graph = f"logged_hours_per_assignee-{current_dateTime}.png"
days_since_last_log_per_user_graph = f"days_since_last_log_per_user-{current_dateTime}.png"
issues_status_per_user_graph = f"issues_per_status_per_user-{current_dateTime}.png"
hours_and_count_per_status_graph = f"logged_hours_and_count_per_status-{current_dateTime}.png"
added_value_per_status_graph = f"added_value_per_user-{current_dateTime}.png"
cycle_lead_time_graph = f"cycle_lead_time-{current_dateTime}.png"
subtasks_per_task_per_sprint_graph = f"n_subtasks_per_task_per_sprint-{current_dateTime}.png"
subtasks_per_sprint_graph = f"n_subtasks_per_sprint-{current_dateTime}.png"
tasks_subtasks_per_sprint_graph = f"n_tasks_subtasks_per_sprint-{current_dateTime}.png"