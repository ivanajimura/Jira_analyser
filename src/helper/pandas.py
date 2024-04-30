import os
import pandas as pd
import src.core.config.settings as settings

class Pandas:

    @staticmethod
    def read_csv(file_path: str) -> pd.DataFrame:
        """
        Read the CSV file into a pandas DataFrame.
        
        Parameters:
        - file_path (str): The path to the CSV file.
        
        Returns:
        - df (pandas DataFrame): The DataFrame containing the data.
        """
        df: pd.DataFrame = pd.read_csv(file_path)
        return df

    @staticmethod
    def extract_work_log_columns(df: pd.DataFrame) -> pd.DataFrame:
        """
        Extract specific columns (Summary, Issue key, Log Work) from the Jira DataFrame.
        
        Parameters:
        - df (pandas DataFrame): The DataFrame containing the Jira data.
        
        Returns:
        - extracted_df (pandas DataFrame): The DataFrame containing the extracted columns.
        """
        # Select columns based on name patterns
        summary_col: pd.DataFrame = df.filter(like=settings.jira_summary_col_name)
        issue_key_col: pd.DataFrame = df.filter(like=settings.jira_key_col_name)
        log_work_cols: pd.DataFrame = df.filter(like=settings.jira_log_work_col_name)
        
        # Concatenate selected columns into a new DataFrame
        extracted_df: pd.DataFrame = pd.concat([summary_col, issue_key_col, log_work_cols], axis=1)
        
        return extracted_df

    @staticmethod
    def extract_work_logs(df: pd.DataFrame) -> pd.DataFrame:
        """
        Extract work log entries from a DataFrame with multiple Log Work columns.
        
        Parameters:
        - df (pandas DataFrame): The DataFrame containing the Log Work columns.
        
        Returns:
        - result_df (pandas DataFrame): The DataFrame containing the extracted work log entries.
        """
        result_rows: list = []
        
        for index, row in df.iterrows():
            issue_key = row[settings.jira_key_col_name]
            summary = row[settings.jira_summary_col_name]
            
            for log_work_col in df.filter(like=settings.jira_log_work_col_name).columns:
                log_work_entry = row[log_work_col]
                
                if pd.notna(log_work_entry):
                    parts = log_work_entry.split(';')
                    description = parts[0].strip() if len(parts) >= 1 else None
                    date_time = parts[1].strip()
                    username = parts[2].strip()
                    time_seconds = int(parts[3].strip())
                        
                    result_rows.append({
                        settings.username_col_name: username,
                        settings.issue_key_col_name: issue_key,
                        settings.summary_col_name: summary,
                        settings.work_log_description_col_name: description,
                        settings.date_time_col_name: date_time,
                        settings.time_seconds_col_name: time_seconds
                    })
        
        result_df: pd.DataFrame = pd.DataFrame(result_rows)
        return result_df

    @staticmethod
    def extract_datetime_components(df: pd.DataFrame, datetime_column: str) -> pd.DataFrame:
        """
        Extract year, month, day, hour, and minute components from a datetime column in a DataFrame.
        
        Parameters:
        - df (pandas DataFrame): The DataFrame containing the datetime column.
        - datetime_column (str): The name of the datetime column.
        
        Returns:
        - df (pandas DataFrame): The DataFrame with additional columns for year, month, day, hour, and minute.
        """
        # Convert the datetime column to pandas datetime object
        df[datetime_column] = pd.to_datetime(df[datetime_column], format='%d/%b/%y %I:%M %p')
        
        # Extract year, month, day, hour, and minute components
        df['Year'] = df[datetime_column].dt.year
        df['Month'] = df[datetime_column].dt.month
        df['Day'] = df[datetime_column].dt.day
        df['Hour'] = df[datetime_column].dt.hour
        df['Minute'] = df[datetime_column].dt.minute
        
        return df

    @staticmethod
    def add_minutes_column(df: pd.DataFrame, seconds_column: str, new_column_name: str) -> pd.DataFrame:
        """
        Add a new column to the DataFrame with time in seconds converted to minutes (rounded down).

        Parameters:
        - df (pandas DataFrame): The DataFrame containing the seconds column.
        - seconds_column (str): The name of the column containing time in seconds.
        - new_column_name (str): The name for the new column to be added.

        Returns:
        - df (pandas DataFrame): The DataFrame with the new column added.
        """
        df[new_column_name] = df[seconds_column] / 60  # Convert seconds to minutes
        df[new_column_name] = df[new_column_name].astype(int)  # Round down to nearest integer
        return df

    @staticmethod
    def add_hours_column(df: pd.DataFrame, seconds_column: str, new_column_name: str) -> pd.DataFrame:
        """
        Add a new column to the DataFrame with time in seconds converted to hours (rounded to 2 decimal places).

        Parameters:
        - df (pandas DataFrame): The DataFrame containing the seconds column.
        - seconds_column (str): The name of the column containing time in seconds.
        - new_column_name (str): The name for the new column to be added.

        Returns:
        - df (pandas DataFrame): The DataFrame with the new column added.
        """
        df[new_column_name] = df[seconds_column] / 3600  # Convert seconds to hours
        df[new_column_name] = df[new_column_name].round(2)  # Round to 2 decimal places
        return df
    
    @staticmethod
    def save_df_to_csv(df: pd.DataFrame, relative_path: str, file_name: str) -> None:
        """
        Save a DataFrame to a CSV file.

        Parameters:
        - df (pandas DataFrame): The DataFrame to be saved.
        - relative_path (str): The relative path to the directory where the CSV file will be saved.
        - file_name (str): The name of the CSV file.

        Returns:
        - None
        """
        # Ensure the directory exists
        os.makedirs(relative_path, exist_ok=True)
        
        # Construct the file path
        file_path = os.path.join(relative_path, file_name)
        
        # Save the DataFrame to CSV
        df.to_csv(file_path, index=False)

    @staticmethod
    def process_work_log(df: pd.DataFrame, group_by_col: str, orig_time_col: str, orig_date_col: str) -> pd.DataFrame:
        """
        Process the work log DataFrame to generate a new DataFrame with aggregated information.

        Parameters:
        - work_log_df (pandas DataFrame): The DataFrame containing the work log data.

        Returns:
        - pandas DataFrame: A new DataFrame containing aggregated information for each user.
        """
        # Group by username
        grouped_df = df.groupby(group_by_col)
        
        # Aggregate total logged hours and most recent log for each user
        aggregated_df = grouped_df.agg({
            orig_time_col: 'sum',                       # Total logged hours
            orig_date_col: lambda x: x.max().strftime('%Y-%m-%d %H:%M:%S')  # Most recent log
        })
              
        # Reset index to make 'username' a regular column
        aggregated_df = aggregated_df.reset_index()
        
        return aggregated_df

    @staticmethod
    def rename_columns(df: pd.DataFrame, mapping: dict) -> pd.DataFrame:
        """
        Rename columns of a DataFrame based on a mapping dictionary.

        Parameters:
        - df (pandas DataFrame): The DataFrame to rename columns for.
        - mapping (dict): A dictionary mapping original column names to new column names.

        Returns:
        - pandas DataFrame: The DataFrame with renamed columns.
        """
        df = df.rename(columns=mapping)
        return df
    
    @staticmethod
    def add_combined_column(df: pd.DataFrame, source_column: str, fixed_value: str, new_column_name: str) -> pd.DataFrame:
        """
        Add a new column to a DataFrame by combining a fixed value with a value from an existing column.

        Parameters:
        - df (pandas DataFrame): The DataFrame to add the new column to.
        - source_column (str): The name of the column from which to extract the value.
        - fixed_value (Any): The fixed value to combine with the column value.
        - new_column_name (str): The name of the new column to be added.

        Returns:
        - pandas DataFrame: The DataFrame with the new combined column added.
        """
        df[new_column_name] = fixed_value + df[source_column]
        return df

    @staticmethod
    def select_columns(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
        """
        Select and return only the specified columns from a DataFrame.

        Parameters:
        - df (pandas DataFrame): The DataFrame to select columns from.
        - columns (list of str): A list of column names to select.

        Returns:
        - pandas DataFrame: The DataFrame containing only the specified columns.
        """
        return df[columns]

    @staticmethod
    def aggregate_by_column(df: pd.DataFrame, group_by_column: str, agg_functions: dict[str, str]) -> pd.DataFrame:
        """
        Aggregate a DataFrame by a certain column using specified aggregation functions.

        Parameters:
        - df (pandas DataFrame): The DataFrame to aggregate.
        - group_by_column (str): The name of the column to group by.
        - agg_functions (dict): A dictionary where keys are column names and values are aggregation functions
                                (e.g., {'column1': 'sum', 'column2': 'mean'}).

        Returns:
        - pandas DataFrame: The aggregated DataFrame.
        """
        return df.groupby(group_by_column).agg(agg_functions).reset_index()
    
    @staticmethod
    def join_dataframes(df1: pd.DataFrame, df2: pd.DataFrame, on1: str, on2: str, how: str) -> pd.DataFrame:
        """
        Join two DataFrames on different columns with a specified join type.

        Parameters:
        - df1 (pandas DataFrame): The first DataFrame.
        - df2 (pandas DataFrame): The second DataFrame.
        - on1 (str): The column name in the first DataFrame to join on.
        - on2 (str): The column name in the second DataFrame to join on.
        - how (str): The type of join ('inner', 'left', 'right', 'outer').

        Returns:
        - pandas DataFrame: The joined DataFrame.
        """
        return pd.merge(df1, df2, left_on=on1, right_on=on2, how=how)

    @staticmethod
    def remove_columns(df: pd.DataFrame, columns_to_remove: list[str]) -> pd.DataFrame:
        """
        Remove specified columns from a DataFrame.

        Parameters:
        - df (pandas DataFrame): The DataFrame to remove columns from.
        - columns_to_remove (list of str): List of column names to remove.

        Returns:
        - pandas DataFrame: DataFrame with specified columns removed.
        """
        return df.drop(columns=columns_to_remove)

    @staticmethod
    def pivot_dataframe(df, y_col: str, x_col: str) -> pd.DataFrame:
        """
        Pivots two columns of a dataframe

        Parameters:
        - df (DataFrame): The DataFrame containing the issues data.
        - assignee_col (str): The name of the column to be on the y axis.
        - status_col (str): The name of the column to be on the x axis.

        Returns:
        - DataFrame: A DataFrame where each row corresponds to an assignee,
                    and each column corresponds to a status.
                    The values represent the count of issues in each status for each assignee.
        """
        grouped_df = df.groupby([y_col, x_col]).size().unstack(fill_value=0).reset_index()
        
        return grouped_df













































