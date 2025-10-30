

## Let's explore the Pathlib library

from pathlib import Path
from src.document_parsing.sample_data import Parsed_minerU_raw
from src.document_parsing.data_extraction import MinerU_Parser

minerU_testing = MinerU_Parser(data_file_path="C:\\Users\Hp\\Documents\\AI Projects docs\\RAG\\RAG_for_Anything.pdf")

#minerU_test_run = minerU_testing.run_minerU()
#minerU_output_file = minerU_testing.read_minerU_output()
#minerU_formatted_output = minerU_testing.format_minerU_output()
#print(minerU_formatted_output)

run_minerU = minerU_testing.run_minerU()
read_minerU = minerU_testing.read_minerU_output()
format_minerU = minerU_testing.format_minerU_output()

print(format_minerU)

