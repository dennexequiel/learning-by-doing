import pandas as pd
import os
import sys

# Constants
CSV_FILE_PATH = "media_pickups.csv"  # Path to the CSV file
OUTPUT_PATH = "markdowns"  # Output directory for the markdown files
FILE_NAME_COL_NAME = "file_name"  # Column name in the CSV file that contains the file names
FRONT_MATTER_TYPE = "toml"  # Front matter type for the markdown files. Accepted values are 'toml' and 'yaml' only

# Class to hold the settings for generating markdown files
class MarkdownSettings:
    def __init__(self, src, output_path, file_name_col_name, front_matter_type):
        self.__src = src
        self.__file_name_col_name = file_name_col_name
        self.__output_path = output_path
        self.__front_matter_type = front_matter_type

    # Getters and setters for the class properties
    @property
    def get_src(self):
        return self.__src

    @get_src.setter
    def set_src(self, src):
        self.__src = src

    @property
    def get_file_name_col_name(self):
        return self.__file_name_col_name

    @get_file_name_col_name.setter
    def set_file_name_col_name(self, file_name_col_name):
        self.__file_name_col_name = file_name_col_name

    @property
    def get_output_path(self):
        return self.__output_path

    @get_output_path.setter
    def set_output_path(self, output_path):
        self.__output_path = output_path

    @property
    def get_front_matter_type(self):
        return self.__front_matter_type

    @get_front_matter_type.setter
    def set_front_matter_type(self, front_matter_type):
        self.__front_matter_type = front_matter_type

# Main function
if __name__ == "__main__":
    # Initialize the MarkdownSettings object
    markdown_settings = MarkdownSettings(CSV_FILE_PATH, OUTPUT_PATH, FILE_NAME_COL_NAME, FRONT_MATTER_TYPE)

    # Create the output directory if it doesn't exist
    if not os.path.isdir(markdown_settings.get_output_path):
        os.mkdir(markdown_settings.get_output_path)

    # Check if the CSV file exists
    if os.path.exists(markdown_settings.get_src):
        df = pd.read_csv(markdown_settings.get_src, encoding='unicode_escape')
    else:
        print("Can't find CSV file")
        sys.exit()

    # Check the front matter type and set the corresponding identifiers and value symbols
    if markdown_settings.get_front_matter_type == "toml":
        fm_identifier = "+++"
        fm_value_symbol = " = "
    else:
        fm_identifier = "---"
        fm_value_symbol = " : "

    # Get all the column headers from the CSV file
    attribute_list = df.columns

    # Loop through each row in the CSV file and create a markdown file for each
    for index, row in df.iterrows():
        # Open a new markdown file
        markdown = open(markdown_settings.get_output_path + "\\" +
                        row[markdown_settings.get_file_name_col_name].strip() + ".md", "w+")

        # Write the front matter identifier to the file
        markdown.write(fm_identifier + "\n")

        # Write each attribute and its value to the file
        for col_header in attribute_list:
            if col_header == markdown_settings.get_file_name_col_name:
                continue
            else:
                if type(row[col_header]) is bool:
                    markdown.write(str(col_header) + fm_value_symbol + str(row[col_header]).strip().lower() + "\n")
                else:
                    markdown.write(str(col_header) + fm_value_symbol + str(row[col_header]).strip() + "\n")

        # Write the closing front matter identifier to the file
        markdown.write(fm_identifier)
        markdown.close()

    print("Task Completed!")