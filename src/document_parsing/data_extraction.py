

## Let's create the rough subprocess and test it 
import subprocess
from subprocess import CalledProcessError, TimeoutExpired
from pathlib import Path
import time

## Parsing Module Workflow
"""

Class MinerU_Parser:

    1- Parse_user_document
    2- Run_minerU (Done)
    3- Read_minerU_output (Done)
    4- Format_the_minerU_output 
    5- Run_LibreOffice
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
        
        self.content_of_json =  json_output_path.read_text(encoding="utf-8")
        self.content_of_md = md_output_path.read_text(encoding="utf-8")
              
         
        return self.content_of_md, self.content_of_json


    # Lets create the method to format the output of the minerU

    def format_minerU_output(self):

        """
        It takes the JSON output of the minerU, and fetches the information elements required to create the knowledge units. 

        **Args:**
        self.content_of_json (markdown): It is the parsed output in the JSON format.
        
        **Returns:**
        self.content_list (list): It is the list of the knowledge units that contains the information about part of the document.

        **Raises:**

        Features of content list: Content_list(content_data, content_type, content_metadata)
        STEPS TO CREATE A CONTENT LIST:
        1- PDF info contains the dict, which contains multiple "Paras" as strings of dictionaries.
        2- Each "Para" contains the LIST of Dictionaries as value.
        3- In the list, each dictionary contains "lines" as string.
        4- lines contain the LIST of Dictionary as value.
        5- Dictionary contains "Span" as string, and LIST of Dictionary as value.
        6- Dictionary contains the "type" and "content" as string & their values represent the data type & raw content.

        """
        # lets get the input of the function
        minerU_raw_output = self.content_of_json



        return PDF_INFO

