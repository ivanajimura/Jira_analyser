from jira import JIRA
import requests
from requests import Response
import os
from requests.auth import HTTPBasicAuth
import urllib.parse

import src.core.config.settings as settings


class Jira:

    @staticmethod
    def connect_to_jira(jira_instance: str, token: str) -> JIRA:
        """
        Connect to a Jira instance using an authentication token.

        Parameters:
        - jira_instance (str): The URL of the Jira instance.
        - token (str): The API token for authentication.

        Returns:
        - JIRA: A JIRA object representing the connection to the Jira instance.
        """
        options = {'server': jira_instance, 'headers': {'Authorization': f'Bearer {token}'}}
        return JIRA(options=options)

    @staticmethod
    #Possibly already deprecated
    def collect_project_issues(jira: JIRA, project_id: str, jql_query: str = None) -> list:
        """
        Collect issues from a specific project ID based on search parameters.

        Parameters:
        - jira (JIRA): A JIRA object representing the connection to the Jira instance.
        - project_id (str): The ID of the project from which to collect issues.
        - jql_query (str, optional): JQL query string to filter the issues. Defaults to None.

        Returns:
        - List: A list of issues from the specified project based on the search parameters.
        """
        if jql_query:
            issues = jira.search_issues(jql_query, expand='changelog')
        else:
            issues = jira.search_issues(f'project={project_id}')
        return issues
    

    @staticmethod
    def parse_jql_into_url(jql_query: str, base_url: str = settings.csv_download_prefix):
        # Encode the JQL query
        encoded_query = urllib.parse.quote(jql_query)
        # Construct the full URL
        return base_url + f'jqlQuery={encoded_query}'

    @staticmethod
    def download_csv_from_jql(username: str, password: str, csv_url: str, folder_path: str = settings.files_path, file_name = settings.input_file_name):
        # Define the file path where the CSV file will be saved
        file_path = os.path.join(folder_path, file_name)
        # Create a session with authentication headers
        session = requests.Session()
        session.auth = HTTPBasicAuth(username = username, password = password)
        # Send a GET request to download the CSV file
        response: Response = session.get(url = csv_url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Write the content of the response to a file
            with open(file_path, 'wb') as file:
                file.write(response.content)
            
            print(f'CSV file saved to: {file_path}')
        else:
            print(f'Failed to download CSV file. Status code: {response.status_code}')