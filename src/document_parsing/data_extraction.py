

## Let's create the rough subprocess and test it 
import subprocess
from subprocess import CalledProcessError, TimeoutExpired
from pathlib import Path
import time
import json

## Parsing Module Workflow
"""

Class MinerU_Parser:

    1- Parse_user_document
    2- Run_minerU (Done)
    3- Read_minerU_output (Done)
    4- Format_the_minerU_output (Done)
    6- Check_installations

"""

# Lets create the MinerU Parser class 

class MinerU_Parser():
    """
    This class contains the behavior of converting word-doc to pdf and parsing pdf.
    """

    # lets initialize the instance attributes
    def __init__(self,data_file_path):

        self.data_file_path = data_file_path
    

    # lets define the Run_minerU method
    def run_minerU(self):
        """
        This method takes the data file path as an input, and initiate the subprocess() that executes the external program MinerU
        to parse the provided document.

        **Args:**
        data_file_path (path): It is the file path of the user input file that minerU will parse.

        **Returns:**
        subprocess_minerU_output (path): It is the path of the folder that minerU returns which contains all sort of parsed data, JSON, Markdown etc.

        **Raises:**
        It raises either CalledProcessError or TimeoutExpiredError if external programs gives error or gets hang & block indifinitely. 
        

        Optimization:
        1- Limit on extraction pages not working
        2- Output directory address not followed by the subprocess
        3- Doubtful even if command line is being completed read by minerU or it is only reading first input of command which is start of minerU & Input file.

        """
        try:
            
            # lets define the subprocess for minerU
            data_file_path = self.data_file_path

            subprocess_minerU_output = subprocess.run(["C:\\Users\\Hp\\AppData\\Local\\Programs\\MinerU\\MinerU.exe", "--path", f"{data_file_path}", "--output", "C:\\Users\\Hp\\Documents\\AI Projects docs\\RAG\\Parsed_output", 
                                            "--method", "auto", 
                                            "--backend", "pipeline", 
                                            "--start", "0", 
                                            "--end", "2"],
                                            check=True,
                                            capture_output= True
                                            ,cwd="C:\\Users\\Hp\\Documents\\AI Projects docs\\RAG" )
            
            self.MinerU_code = subprocess_minerU_output.returncode
            self.MinerU_output = subprocess_minerU_output.stdout.decode("utf-8")

            return  self.MinerU_output, self.MinerU_code
        

        except CalledProcessError as e:
            if self.MinerU_code != 0:
                raise("Output of the subproces is non-zero here is the CalledProcessError {e}")
        except TimeoutExpired as e:
            if self.MinerU_code != 0:
                raise("Subprocess got hanged or blocked indefinitely - here is the timeoutexpired error {e}") 
            

    # Lets create the method to read the output file of the minerU output
    def read_minerU_output(self):
        """
        It takes the address of the folder where minerU has stored its output and will access json file and markdown file
        from it. It is upto us to use whichever we want to out of these two output files.

        **Args:**
        minerU_output_path (path): It is the path of the folder where minerU has stored its parsed output files.

        **Returns:**
        content_of_json : It is the parsed data in json format.
        content_of_md: It is the parsed data in the markdown file.

        
        AREAS OF IMPROVEMENT:
        Need to align the directory of the MinerU output with this as for now, we need to manually pass the address.

        """

        # Wait for reading the output until subprocess is completed.
        mineru_returncode = self.MinerU_code
        while mineru_returncode != 0:
            time.sleep(4)

        # set directory
        new_cwd_path = Path("C:\\Users\\Hp\\MinerU")
        
        #content_of_cwd = list(new_cwd_path.iterdir())
        
        folders_cwd = []
        for items in new_cwd_path.iterdir():
            if items.is_dir():
                  folders_cwd.append(items)
        output_dir = str(folders_cwd[1])   
        json_output_path = (Path(output_dir)).joinpath("layout.json")
        md_output_path = (Path(output_dir)).joinpath("full.md")
        
        content_of_json =  json_output_path.read_text(encoding="utf-8")
        # let's convert this raw text into JSON
        self.content_of_json = json.loads(content_of_json)
        self.content_of_md = md_output_path.read_text(encoding="utf-8")
              
         
        return self.content_of_json


        # Lets create the method to format the output of the minerU & get the knowledge units for Text & Tables
    def format_minerU_output(self):

            """
            It takes the JSON output of the minerU, and fetches the information elements required to create the knowledge units. 

            **Args:**
            self.content_of_json (markdown): It is the parsed output in the JSON format.
            ABS_PATH (Path): It is the absolute path that we need to use in order to convert the relative path of the table_image to the
            absolute path. For now, we do not have the output of minerU path and our input path same (Because minerU is not running command statement correctly)
            so, we are manually bringing the path of the minerU output manually. Otherwise, we would just have to import it using path.cwd().
            
            **Returns:**
            self.content_list (list): It is the list of the knowledge units that contains the information about part of the document.

            **Raises:**

            """
            # lets get the input of the function
            minerU_raw_output = self.content_of_json
            ABS_PATH = Path("C:\\Users\\Hp\\MinerU")


            PDF_INFO = minerU_raw_output.get("pdf_info","")
            content_list = []
            table_images_folder = []


            # Let's get the directory path of the output of the minerU so, that we can create the absolute path of the table images. 
            for items in ABS_PATH.iterdir():
                if items.is_dir():
                    table_images_folder.append(items)
            ABS_PATH_OUTPUT = table_images_folder[1]
            

            # Lets get all the knowledge units in the content list
            for page in PDF_INFO:
                page_no = page.get("page_idx","")
                discarded_block = page.get("discarded_blocks","")
                para_blocks = page.get("para_blocks","")
                for para_dict_details in para_blocks:
                    para_label = para_dict_details.get("type","")
                    if para_label not in ["table", "text", "title"]:
                        continue
                    
                    # Knowledge units of textual content 
                    if para_label in ["text", "title"]:
                        para_lines = para_dict_details.get("lines","")
                        for lines_dict_details in para_lines:
                            spans_details = lines_dict_details.get("spans","")
                            for span_dict_details in spans_details:
                                    content_of_span = span_dict_details.get("content","")
                                    content_type_of_span = span_dict_details.get("type","")
                                    if content_type_of_span not in ["text"]:
                                        continue
                                    knowledge_unit = {"page_no.":page_no, "raw_content":content_of_span, "content type": para_label}
                                    content_list.append(knowledge_unit)

                    # Knowledge units of tabular content
                    elif para_label == "table":
                        table_blocks = para_dict_details.get("blocks","")
                        for table_block in table_blocks:
                            table_block_lines = table_block.get("lines","")
                            for lines_dict_details in table_block_lines:
                                spans_details = lines_dict_details.get("spans","")
                                for table_span_dict_details in spans_details:
                                        table_of_block_line = table_span_dict_details.get("image_path","")
                                        content_type_of_span = table_span_dict_details.get("type","")
                                        table_caption = table_span_dict_details.get("content","")
                                        # Lets convert the relative path of the table image to the absolute path

                                        ABS_table_image_path = ABS_PATH_OUTPUT.joinpath(f"images/{table_of_block_line}")
                                        if content_type_of_span not in  ["table", "text"]:
                                            continue
                                        if content_type_of_span == "table":
                                            knowledge_unit = {"page_no.":page_no, "table_image_path":ABS_table_image_path, "content_type": para_label}
                                        if content_type_of_span == "text": 
                                            knowledge_unit = {"page_no.":page_no, "table_caption":table_caption, "content_type": para_label}

                                        content_list.append(knowledge_unit)
                    


            return content_list

    # Lets create the method to check the installations
    def check_minerU_installation(self):
        """
        This method checks the installation of the required tools to run the parser module. For parsing the document,
        we need to have minerU installed in the system and therefore, it is important to check if the user has installed
        it correctly or not. This is more like check function to ensure that the pre-requisites of running the program are
        completed or not.        
        
        """
        try:

            minerU_subprocess_kwargs = {
                "capture_output": True,
                "text": True,
                "encoding": "utf-8",
                "check": True
            }

            
            # let's ensure that while checking, console window on Windows remains hidden
            # import platform to check the system
            import platform
            if platform.system == "Windows":
                minerU_subprocess_kwargs["creationflags"] = subprocess.CREATE_NO_WINDOW

            run_minerU_for_checking = subprocess.run(["C:\\Users\\Hp\\AppData\\Local\\Programs\\MinerU\\MinerU.exe", "--version"], **minerU_subprocess_kwargs)

            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False


# Lets run the module with the main function

def main():

    """
    This function takes the file from the user in order to parse it,
    and also gives us its knowledge units. 
    
    """
    minerU_testing = MinerU_Parser(data_file_path="C:\\Users\Hp\\Documents\\AI Projects docs\\RAG\\RAG_for_Anything.pdf")

    run_minerU = minerU_testing.run_minerU()
    read_minerU = minerU_testing.read_minerU_output()
    format_minerU = minerU_testing.format_minerU_output()

    print(format_minerU)

main()