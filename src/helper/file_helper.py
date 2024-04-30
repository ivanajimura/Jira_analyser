import os

class FileHelper:
    @staticmethod
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
    
    @staticmethod
    def create_folder_if_not_exists(folder_path: str):
        """
        Create a folder if it does not exist.

        Parameters:
            folder_path (str): The path of the folder to create.
        """
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            print(f"Folder '{folder_path}' created.")
        else:
            print(f"Folder '{folder_path}' already exists.")

    @staticmethod
    def remove_file(path: str, file_name: str) -> None:
        """
        Remove a file.

        Parameters:
        - path (str): The path to the file.
        - file_name (str): The name of the file to be removed.
        """
        file_path = os.path.join(path, file_name)
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"File '{file_name}' removed successfully.")
        else:
            print(f"File '{file_name}' does not exist.")