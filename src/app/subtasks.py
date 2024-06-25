import time
from src.helper.pandas import Pandas as Pd
from src.helper.file_helper import FileHelper
import core.config.settings as settings

# Subtasks per Sprint

## Open files/sprints.csv
df_sprints_file: str = FileHelper.concatenate_path_and_filename(folder_path = settings.files_path, filename = settings.sprints_df_name)
sprints_df = Pd.read_csv(file_path=df_sprints_file)
## Reduce columns
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
##Create new columns
tasks_col = settings.number_tasks
subtasks_col = settings.number_subtasks
sprints_df[tasks_col] = 0
sprints_df[subtasks_col] = 0
## Add data to new columns
sprint_ids = sprints_df[settings.sprint_id_col].unique().tolist()
for sprint_id in sprint_ids:
    #Open corresponding sprint csv
    cur_sprint_file_name=f"{settings.previous_sprints_prefix}{sprint_id}.csv"
    cur_df_sprints_file: str = FileHelper.concatenate_path_and_filename(folder_path = settings.files_path, filename = cur_sprint_file_name)
    df_cur_sprint = Pd.read_csv(file_path=cur_df_sprints_file)
    #Count Tasks, Stories and Bugs
    n_issues = 0
    for issue_type in settings.valid_issue_types:
        try:
            n_issues = n_issues + Pd.value_counts(df = df_cur_sprint, column=settings.jira_issue_type_col_name, value_to_count=issue_type)
        except:
            pass
    sprints_df = Pd.set_value_by_condition(
        df = sprints_df, column_to_change = tasks_col, column_to_search = settings.sprint_id_col,
        search_value = sprint_id, value_to_set = n_issues)
    #Count Sub-Tasks
    n_subtasks = Pd.value_counts(df = df_cur_sprint, column=settings.jira_issue_type_col_name, value_to_count=settings.subtask_issue_type)
    sprints_df = Pd.set_value_by_condition(
        df = sprints_df, column_to_change = subtasks_col, column_to_search = settings.sprint_id_col,
        search_value = sprint_id, value_to_set = n_subtasks)
##Save files
n_subtasks_per_task = settings.n_subtasks_per_task
sprints_df[n_subtasks_per_task] = round(sprints_df[subtasks_col] / sprints_df[tasks_col],2)
Pd.save_df_to_csv(df = sprints_df, relative_path=settings.files_path, file_name=settings.sprints_df_name)

# Subtasks per person per sprint
values_list_of_dicts = []
for sprint_id in sprint_ids:
    #Open corresponding sprint csv
    cur_sprint_file_name=f"{settings.previous_sprints_prefix}{sprint_id}.csv"
    cur_df_sprints_file: str = FileHelper.concatenate_path_and_filename(folder_path = settings.files_path, filename = cur_sprint_file_name)
    df_cur_sprint = Pd.read_csv(file_path=cur_df_sprints_file)
    for assignee in settings.assignee_list:
        df_filtered_tasks = df_cur_sprint.loc[(df_cur_sprint[settings.jira_assignee_col_name] == assignee) & (df_cur_sprint[settings.jira_issue_type_col_name].isin(settings.valid_issue_types))]
        df_filtered_subtasks = df_cur_sprint.loc[(df_cur_sprint[settings.jira_assignee_col_name] == assignee) & (df_cur_sprint[settings.jira_issue_type_col_name] == settings.subtask_issue_type)]
        n_tasks = len(df_filtered_tasks)
        n_subtasks = len(df_filtered_subtasks)
        values_list_of_dicts.append({
            "sprint_id": sprint_id,
            settings.jira_assignee_col_name: assignee,
            settings.number_tasks: n_tasks,
            settings.number_subtasks: n_subtasks
                                     })
df_tasks_subtasks_per_assignee = Pd.create_df_from_list_of_dicts(values_list_of_dicts)
Pd.save_df_to_csv(df = df_tasks_subtasks_per_assignee, relative_path=settings.output_path, file_name = settings.subtasks_per_assignee_per_sprint_csv)

df_total_subtasks_per_assignee = Pd.group_by(df = df_tasks_subtasks_per_assignee, group_col=settings.jira_assignee_col_name, value_col=settings.number_subtasks, aggregation="sum")
Pd.save_df_to_csv(df = df_total_subtasks_per_assignee, relative_path=settings.output_path, file_name = settings.total_subtasks_per_assignee_csv)