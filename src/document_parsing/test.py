

## Let's explore the Pathlib library

from pathlib import Path

def read_minerU_output():
        """
        It takes the address of the folder where minerU has stored its output and will access the markdown and json files
        from it. It is upto us to use whichever we want to out of these two output files.

        **Args:**
        minerU_output_path (path): It is the path of the folder where minerU has stored its parsed output files.

        **Returns:**
        Parsed_JSON_file : It is the parsed data in json format.
        Parsed_markdown_file : It is the parsed data in markdown format.

        """
    ## Let's explore the Pathlib library

        # set directory
        new_cwd_path = Path("C:\\Users\\Hp\\Documents\\AI Projects docs\\RAG")
        # How to find the file using extension & then read those files & then save them in another folder.
        for files in new_cwd_path.glob("*.json"):
            list_of_json_files = [files.name][0]

        # create folder in the same directory
        parsed_output_path = new_cwd_path.joinpath("parsed_output","layout.json")
        # read the json file in the RAG folder
        dummy_parsed_json_path = new_cwd_path.joinpath(f"{list_of_json_files}")
        content_json_file = dummy_parsed_json_path.read_text(encoding="utf-8")

        # move file to folder parsed_output
        with parsed_output_path.open(mode='wb') as file:
            file.write(dummy_parsed_json_path.read_bytes())

        return content_json_file


content_of_parsed_file = read_minerU_output()
print(content_of_parsed_file)