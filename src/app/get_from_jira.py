import src.core.config.settings as settings
import src.core.config.user_config as user_config
from src.service.jira import Jira

jira = Jira.connect_to_jira(jira_instance = user_config.jira_instance, token = user_config.jira_token)

# Get Issues
current_sprint_query: str = f"project='{settings.jira_project}' AND sprint in openSprints()"
download_link = Jira.parse_jql_into_url(jql_query = current_sprint_query, base_url= settings.csv_download_prefix)

Jira.download_csv_from_jql(
    username = user_config.jira_username,
    password = user_config.jira_password,
    csv_url = download_link,
    folder_path = settings.files_path,
    file_name=settings.input_file_name
)



