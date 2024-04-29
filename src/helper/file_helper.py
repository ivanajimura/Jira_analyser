import os

class FileHelper:
    def concatenate_path_and_filename(folder_path: str, filename: str) -> str:
        """
        Concatenate a folder path and a file name.
        
        Parameters:
        - folder_path (str): The path to the folder.
        - filename (str): The name of the file.
        
        Returns:
        - full_path (str): The concatenated full path.
        """
        full_path: str = os.path.join(folder_path, filename)
        return full_path