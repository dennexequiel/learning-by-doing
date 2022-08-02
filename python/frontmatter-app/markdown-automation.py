import pandas as pd
import os
import sys

# Constants
CSV_FILE_PATH = "media_pickups.csv"
OUTPUT_PATH = "markdowns"
FILE_NAME_COL_NAME = "file_name"
FRONT_MATTER_TYPE = "toml"  # Accepted values are toml and yaml only


class MarkdownSettings:
    def __init__(self, src, output_path, file_name_col_name, front_matter_type):
        self.__src = src
        self.__file_name_col_name = file_name_col_name
        self.__output_path = output_path
        self.__front_matter_type = front_matter_type

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


if __name__ == "__main__":
    markdown_settings = MarkdownSettings(CSV_FILE_PATH, OUTPUT_PATH, FILE_NAME_COL_NAME, FRONT_MATTER_TYPE)

    # Create collection directory
    if not os.path.isdir(markdown_settings.get_output_path):
        os.mkdir(markdown_settings.get_output_path)
    else:
        pass

    # Check CSV
    if os.path.exists(markdown_settings.get_src):
        df = pd.read_csv(markdown_settings.get_src, encoding='unicode_escape')
    else:
        print("Can't find CSV file")
        sys.exit()

    # Check Frontmatter Type
    if markdown_settings.get_front_matter_type == "toml":
        global fm_identifier
        fm_identifier = "+++"

        global fm_value_symbol
        fm_value_symbol = " = "
    else:
        fm_identifier = "---"
        fm_value_symbol = " : "

    # Get all CSV headers
    attribute_list = df.columns

    # Loop through rows & Create each md
    for index, row in df.iterrows():
        markdown = open(markdown_settings.get_output_path + "\\" +
                        row[markdown_settings.get_file_name_col_name].strip() + ".md", "w+")

        markdown.write(fm_identifier + "\n")

        # Add the attributes & values inside the md file
        for col_header in attribute_list:
            if col_header == markdown_settings.get_file_name_col_name:
                continue
            else:
                if type(row[col_header]) is bool:
                    markdown.write(str(col_header) + fm_value_symbol + str(row[col_header]).strip().lower() + "\n")
                else:
                    markdown.write(str(col_header) + fm_value_symbol + str(row[col_header]).strip() + "\n")

        markdown.write(fm_identifier)
        markdown.close()

    print("Task Completed!")
