import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np


sns.set_style("whitegrid")  # Apply minimalist theme

class Graph:

    @staticmethod
    def create_bar_chart(df: pd.DataFrame, x: str, y: str, colors: dict = None) -> None:
        """
        Create a bar chart using Seaborn.

        Parameters:
        - df (pd.DataFrame): The DataFrame containing the data.
        - x (str): The column name for the x-axis.
        - y (str): The column name for the y-axis.
        - colors (dict): A dictionary mapping category names to colors. Defaults to None.
        """
        plt.figure(figsize=(10, 10))
        ax = plt.gca()
        
        if colors is None:
            colors = {}
        
        if colors:
            palette = colors.values()
        else:
            palette = None
        
        sns.barplot(data=df, x=x, y=y, palette=palette)
        plt.xticks(rotation=45)  # Rotate x-axis labels by 45 degrees
        #plt.show()
    

    @staticmethod
    def create_stacked_bar_chart(df: pd.DataFrame, x: str, y_columns: list, colors: dict) -> None:
        """
        Create a stacked bar chart using Seaborn.

        Parameters:
        - df (pd.DataFrame): The DataFrame containing the data.
        - x (str): The column name for the x-axis.
        - y_columns (list): A list of column names for the y-axis.
        - colors (dict): A dictionary mapping column names to colors.
        """
        # Set up the figure and axis
        plt.figure(figsize=(10, 10))
        ax = plt.gca()
        
        # Initialize the bottom parameter for stacking
        bottom = [0] * len(df[x])
        
        # Loop through each y-column
        for y_col in y_columns:
            # Check if the current y-column exists in the DataFrame
            if y_col in df.columns:
                # Extract the color for the current y-column from the colors dictionary
                color = colors.get(y_col, None)
                
                # Create the stacked bar plot for the current y-column
                sns.barplot(data=df, x=x, y=y_col, ax=ax, color=color, bottom=bottom, label=y_col)
                
                # Add labels inside the bars
                for index, row in df.iterrows():
                    label = row[y_col]
                    if label != 0:
                        ax.text(index, bottom[index] + label / 2, str(label), ha='center', va='center', color='black', fontweight='bold')
                
                # Update the bottom parameter for stacking
                bottom += df[y_col].values
        
        # Set plot labels and title
        ax.set_xlabel(x)
        ax.set_ylabel('Count')
        ax.set_title('Stacked Bar Chart')
        
        # Show plot
        plt.xticks(rotation=45)
        plt.legend()
        plt.tight_layout()
        #plt.show()

    @staticmethod
    def save_plot(folder_path: str, file_name: str) -> None:
        """
        Save the current plot to a specified folder path with a given file name.

        Parameters:
        - folder_path (str): The folder path where the plot will be saved.
        - file_name (str): The name of the file for saving the plot.
        """
        # Check if the folder exists, if not, create it
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        
        # Save the plot to the specified file path
        file_path = os.path.join(folder_path, file_name)
        plt.savefig(file_path)
        plt.cla()


    @staticmethod
    def create_multi_bar_chart(df: pd.DataFrame, x_column: str, x_values: list, y_columns: list, colors: dict = None) -> None:
        """
        Create a bar chart with multiple bars on the y-axis, not stacked.

        Parameters:
        - df (pd.DataFrame): The DataFrame containing the data.
        - x_values (list): A list of x values in the desired order.
        - y_columns (list): A list of column names for the y-axis. The bars will be plotted for each column in the specified order.
        - colors (dict): A dictionary mapping column names to colors. Defaults to None.
        - folder_path (str): The folder path where the plot will be saved. Defaults to None.
        - file_name (str): The name of the file for saving the plot. Defaults to None.
        """
        if colors is None:
            colors = {}

        # Set up the figure and axes
        plt.figure(figsize=(10, 10))
        ax = plt.gca()

        # Define the width of each bar
        bar_width = 0.35

        # Calculate the x-coordinate for each group of bars
        x_positions = np.arange(len(x_values))

        # Plot each bar
        for i, y_col in enumerate(y_columns):
            if y_col in df.columns:
                color = colors.get(y_col, None)
                # Filter the DataFrame to include only rows with x values in the specified order
                filtered_df = df[df[x_column].isin(x_values)]
                # Use the index of each x value in the specified order to calculate the x coordinate
                x_coords = [x_positions[x_values.index(x)] + i * bar_width for x in filtered_df[x_column]]
                ax.bar(x_coords, filtered_df[y_col], color=color, width=bar_width, label=y_col)

        # Customize the plot
        ax.set_xlabel('X Axis')
        ax.set_ylabel('Values')
        ax.set_title('Multiple Bar Chart')
        ax.legend()

        # Set the x-axis tick labels
        ax.set_xticks(x_positions + bar_width * (len(y_columns) - 1) / 2)
        ax.set_xticklabels(x_values)

        # Rotate x-axis labels by 45 degrees
        plt.xticks(rotation=45)