

## Let's create the rough subprocess and test it 
import subprocess
from subprocess import CalledProcessError, TimeoutExpired
import shlex

## Parsing Module Workflow
"""

Class MinerU_Parser:

    1- Parse_user_document
    2- Run_minerU
    3- Read_minerU_output
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
        output_file_path (path): It is the path of the folder that minerU returns which contains all sort of parsed data, JSON, Markdown etc.

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

            subprocess_minerU_output = subprocess.run([r"C:\\Users\\Hp\\AppData\\Local\\Programs\\MinerU\\MinerU.exe", "--path", f"{data_file_path}", "--output", "C:\\Users\\Hp\\Documents\\AI Projects docs\\RAG\\Parsed_output", 
                                            "--method", "auto", 
                                            "--backend", "pipeline", 
                                            "--start", "0", 
                                            "--end" "2"],
                                            check=True,
                                            capture_output= True
                                            )
            
            MinerU_error = subprocess_minerU_output.returncode
            MinerU_output = subprocess_minerU_output.stdout.decode("utf-8")

            return MinerU_output, MinerU_error
        

        except CalledProcessError as e:
            if MinerU_error != 0:
                raise("Output of the subproces is non-zero here is the CalledProcessError {e}")
        except TimeoutExpired as e:
            if MinerU_error != 0:
                raise("Subprocess got hanged or blocked indefinitely - here is the timeoutexpired error {e}") 
            











parse_data = MinerU_Parser(data_file_path="C:\\Users\Hp\\Documents\\AI Projects docs\\RAG\\RAG_for_Anything.pdf")
minerU_output = parse_data.run_minerU()
print(minerU_output)