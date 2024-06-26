from datetime import datetime
import os
import sys
from typing import Literal
import numpy as np
import pandas as pd
import re

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
        df[datetime_column] = pd.to_datetime(df[datetime_column], errors='coerce')
        
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
        - y_col (str): column on y axis
        - x_col (str): column on x axis
        

        Returns:
        - DataFrame: A DataFrame where each row corresponds to an assignee,
                    and each column corresponds to a status.
                    The values represent the count of issues in each status for each assignee.
        """
        grouped_df = df.groupby([y_col, x_col]).size().unstack(fill_value=0).reset_index()
        
        return grouped_df

    @staticmethod
    def pivot_dataframe_by_col(df: pd.DataFrame, y_col: str, x_col: str, value_col: str, calculation: str =  "sum") -> pd.DataFrame:
        """
        Pivots two columns of a DataFrame and computes the sum of values from another column.

        Parameters:
        - df (pd.DataFrame): The DataFrame containing the data.
        - y_col (str): The name of the column to be on the y-axis.
        - x_col (str): The name of the column to be on the x-axis.
        - value_col (str): The name of the column whose values will be summed.

        Returns:
        - pd.DataFrame: A DataFrame where each row corresponds to a unique value in y_col,
                        each column corresponds to a unique value in x_col,
                        and the values represent the sum of values from value_col.
        """
        # Group by y_col and x_col, and sum the values in value_col
        if calculation == "sum":
            grouped_df = df.groupby([y_col, x_col])[value_col].sum().unstack(fill_value=0).reset_index()
        if calculation == "mean":
            grouped_df = df.groupby([y_col, x_col])[value_col].mean().unstack(fill_value=0).reset_index()
        

        return grouped_df

    @staticmethod
    def add_days_since_last_log_column(df: pd.DataFrame, new_column_name: str, datetime_column: str, error_value: any = 0) -> pd.DataFrame:
        df["date"] = pd.to_datetime(df[datetime_column], errors = 'coerce').dt.date
        today = datetime.now().date()
        df["today"] = today
        df[new_column_name] = np.where(df["date"].isnull(), error_value, (today - df["date"]).astype(str).str.slice(0,1))
        df = Pandas.remove_columns(df = df,columns_to_remove=["date", "today"])
        return df

    @staticmethod
    def load_json_to_dataframe(file_path: str, values_key: str = "") -> pd.DataFrame:
        """
        Load a JSON file into a pandas DataFrame where each key in the "values_key" dictionary becomes a column.

        Parameters:
        - file_path (str): The file path to the JSON file.
        - values_key (str): The key containing the "values" dictionary in the JSON file.

        Returns:
        - pd.DataFrame: The DataFrame containing the JSON data.
        """
        try:
            # Load JSON file into a DataFrame
            df = pd.read_json(file_path)
            
            # If the data is nested under a specific key, extract it
            if values_key in df:
                values_dict = df[values_key].to_list()
                df = pd.DataFrame(values_dict)
            
            return df
        except Exception as e:
            print(f"Error loading JSON file: {e}")
            return pd.DataFrame()  # Return an empty DataFrame in case of error
    
    @staticmethod
    def get_cell_value_by_condition(df: pd.DataFrame, search_column: str, search_value: str, return_column: str) -> list:
        """
        Get the value of a cell in a specific column based on the value of another cell in a different column.

        Parameters:
        - df (pd.DataFrame): The DataFrame to search.
        - search_column (str): The name of the column to search.
        - search_value (str): The value to search for in the search_column.
        - return_column (str): The name of the column from which to return the value.

        Returns:
        - list: A list of values from the return_column that correspond to the search condition.
        """
        # Filter the DataFrame based on the search condition
        filtered_df = df[df[search_column] == search_value]
        
        # Return the values from the return_column
        return filtered_df[return_column].tolist()

    @staticmethod
    @DeprecationWarning
    def remove_rows_before_datetime(df: pd.DataFrame, datetime_column: str, threshold_datetime: pd.Timestamp) -> pd.DataFrame:
        """
        Remove rows from a DataFrame where the values in a datetime column are before a specified datetime.

        Parameters:
        - df (pd.DataFrame): The DataFrame to filter.
        - datetime_column (str): The name of the column containing the datetime values.
        - threshold_datetime (pd.Timestamp): The threshold datetime before which rows will be removed.

        Returns:
        - pd.DataFrame: The filtered DataFrame.
        """
        # Convert the datetime column to pandas datetime object
        df[datetime_column] = pd.to_datetime(df[datetime_column])
        
        # Filter the DataFrame based on the condition
        filtered_df = df[df[datetime_column] >= threshold_datetime]
        
        return filtered_df

    @staticmethod
    @DeprecationWarning
    def remove_rows_after_datetime(df: pd.DataFrame, datetime_column: str, threshold_datetime: pd.Timestamp) -> pd.DataFrame:
        """
        Remove rows from a DataFrame where the values in a datetime column are after a specified datetime.

        Parameters:
        - df (pd.DataFrame): The DataFrame to filter.
        - datetime_column (str): The name of the column containing the datetime values.
        - threshold_datetime (pd.Timestamp): The threshold datetime before which rows will be removed.

        Returns:
        - pd.DataFrame: The filtered DataFrame.
        """
        # Convert the datetime column to pandas datetime object
        df[datetime_column] = pd.to_datetime(df[datetime_column])
        
        # Filter the DataFrame based on the condition
        filtered_df = df[df[datetime_column] <= threshold_datetime]
        
        return filtered_df
    
    @staticmethod
    def remove_rows_before_or_after_datetime(df: pd.DataFrame, datetime_column: str, threshold_datetime: pd.Timestamp, before_or_after: Literal['before', 'after']) -> pd.DataFrame:
        """
        Remove rows from a DataFrame where the values in a datetime column are after a specified datetime.

        Parameters:
        - df (pd.DataFrame): The DataFrame to filter.
        - datetime_column (str): The name of the column containing the datetime values.
        - threshold_datetime (pd.Timestamp): The threshold datetime before which rows will be removed.
        - before_or_after (str): Accepts 'before' or 'after'

        Returns:
        - pd.DataFrame: The filtered DataFrame.
        """

        if before_or_after.lower() not in ['before', 'after']:
            print("Wrong parameter for before_or_after. Must be either 'before' or 'after'. We even accept capitalization! Correct this and run the code again.")
            sys.exit()

        # Convert the datetime column to pandas datetime object
        df[datetime_column] = pd.to_datetime(df[datetime_column])
        
        # Filter the DataFrame based on the condition
        if before_or_after.lower() == 'before':
            filtered_df = df[df[datetime_column] >= threshold_datetime]
        elif before_or_after.lower() == 'after':
            filtered_df = df[df[datetime_column] <= threshold_datetime]
        
        return filtered_df


    @staticmethod
    def remove_rows_by_values(df: pd.DataFrame, column: str, values_to_remove: list) -> pd.DataFrame:
        """
        Remove rows from a DataFrame where the specified column contains certain values.

        Parameters:
        - df (pd.DataFrame): The DataFrame to filter.
        - column (str): The name of the column to filter by.
        - values_to_remove (list): A list of values to remove from the specified column.

        Returns:
        - pd.DataFrame: The filtered DataFrame.
        """
        # Filter the DataFrame based on the condition
        filtered_df = df[~df[column].isin(values_to_remove)]
        
        return filtered_df

    @staticmethod
    def read_and_concat_csv(folder_path: str, filename_prefix: str, filename_col: str = "filenumber") -> pd.DataFrame:
        """
        Read multiple CSV files from a folder with a common filename prefix and concatenate them into a single DataFrame.

        Parameters:
        - folder_path (str): The path to the folder containing the CSV files.
        - filename_prefix (str): The common prefix of the CSV filenames.

        Returns:
        - pd.DataFrame: A single DataFrame containing the concatenated data from all CSV files,
                        with an additional column indicating the source filename.
        """
        # Initialize an empty list to store DataFrames
        dfs = []

        # Iterate over files in the folder
        for file in os.listdir(folder_path):
            # Check if the file is a CSV file and starts with the specified prefix
            if file.endswith('.csv') and file.startswith(filename_prefix):
                # Extract the file number from the filename
                file_number = file[len(filename_prefix):-4]  # Remove prefix and '.csv' extension
                # Read the CSV file into a DataFrame
                df = pd.read_csv(os.path.join(folder_path, file))
                # Add a new column with the file number
                df[filename_col] = file_number
                # Append the DataFrame to the list
                dfs.append(df)

        # Concatenate all DataFrames into a single DataFrame
        concatenated_df = pd.concat(dfs, ignore_index=True)
        
        return concatenated_df

    @staticmethod
    def calculate_date_difference(df: pd.DataFrame, column1: str, column2: str) -> pd.Series:
        """
        Calculate the date difference between two columns containing datetime strings in a DataFrame.

        Parameters:
        - df (pd.DataFrame): The DataFrame containing the datetime columns.
        - column1 (str): The name of the first datetime column.
        - column2 (str): The name of the second datetime column.

        Returns:
        - pd.Series: A Series containing the date differences in days.
        """
        # Convert datetime strings to pandas datetime objects
        df[column1] = pd.to_datetime(df[column1], errors='coerce')
        df[column2] = pd.to_datetime(df[column2], errors='coerce')
        
        # Calculate the date difference, handling NaT values
        date_diff = (df[column1] - df[column2]).dt.days
        
        return date_diff

    @staticmethod
    def group_by(df: pd.DataFrame, group_col: str, value_col: str, aggregation:str = "sum") -> pd.DataFrame:
        """
        Groups the values of multiple columns according to the values of another column with different aggregations.

        Parameters:
        - df (DataFrame): The DataFrame containing the data.
        - group_col (str): The column to group by.
        - value_cols (dict[str, str]): A dictionary where keys are the columns whose values to aggregate,
                                        and values are the corresponding aggregation functions.

        Returns:
        - DataFrame: A DataFrame where each row corresponds to a unique value in `group_col`,
                    and the aggregated values of each `value_col` for each group.
        """
        
        return df.pivot_table(index=group_col, values=value_col, aggfunc=aggregation).reset_index()
        
    @staticmethod
    def value_counts( df: pd.DataFrame, column: str, value_to_count: any) -> int:
        """Counts value occurrences in a column

        Args:
            df (pd.DataFrame): df to count
            column (str): selected column
            value_to_count (any): value to be counted. Should work with any data type

        Returns:
            int: number of occurrences of the value_to_count
        """        
        return df[column].value_counts()[value_to_count]

    @staticmethod
    def set_value_by_condition(df: pd.DataFrame, column_to_change: str, column_to_search: str, search_value: any, value_to_set: any) -> pd.DataFrame:
        """Sets value in cell based on condition (on the same or different col)

        Args:
            df (pd.DataFrame): df to read
            column_to_change (str): col to change value
            column_to_search (str): col to search for value
            search_value (any): value to be searched in column_to_search
            value_to_set (any): new value in column_to_change

        Returns:
            pd.DataFrame: the whole df
        """        
        df[column_to_change].mask(df[column_to_search] == search_value, value_to_set, inplace = True)
        return df


    @staticmethod
    def list_unique_values_in_col(df: pd.DataFrame, column: str) -> list:
        """Lists unique values in a col in a df

        Args:
            df (pd.DataFrame): df to search
            column (str): col to search

        Returns:
            list: 
        """        
        return df[column].unique().tolist()

    @staticmethod
    def create_df_from_list(value_list: list, col_name: str) -> pd.DataFrame:
        """ Creates df with a single column.

        Args:
            value_list (list): list of values to insert in df
            col_name (str): name of the column

        Returns:
            pd.DataFrame: pandas dataframe
        """        
        df = pd.DataFrame(value_list, columns=[col_name])
        return df

    @staticmethod
    def create_df_from_list_of_dicts(list_of_dicts: list) -> pd.DataFrame:
        return pd.DataFrame.from_dict(list_of_dicts) 




