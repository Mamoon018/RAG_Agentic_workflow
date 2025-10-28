

## Let's explore the Pathlib library

from pathlib import Path
from src.document_parsing.sample_data import Parsed_minerU_raw
from src.document_parsing.data_extraction import MinerU_Parser

minerU_testing = MinerU_Parser(data_file_path="C:\\Users\Hp\\Documents\\AI Projects docs\\RAG\\RAG_for_Anything.pdf")

#minerU_test_run = minerU_testing.run_minerU()
#minerU_output_file = minerU_testing.read_minerU_output()
#minerU_formatted_output = minerU_testing.format_minerU_output()
#print(minerU_formatted_output)




def format_minerU_output():

        """
        It takes the JSON output of the minerU, and fetches the information elements required to create the knowledge units. 

        **Args:**
        self.content_of_json (markdown): It is the parsed output in the JSON format.
        
        **Returns:**
        self.content_list (list): It is the list of the knowledge units that contains the information about part of the document.

        **Raises:**

        """
        # lets get the input of the function
        minerU_raw_output = Parsed_minerU_raw

        PDF_INFO = minerU_raw_output.get("pdf_info","")
        content_list = []

        # Lets get all the knowledge units in the content list
        for page in PDF_INFO:
            page_no = page.get("page_idx","")
            discarded_block = page.get("discarded_blocks","")
            para_blocks = page.get("para_blocks","")
            for para_dict_details in para_blocks:
                para_lines = para_dict_details.get("lines","")
                for lines_dict_details in para_lines:
                    spans_details = lines_dict_details.get("spans","")
                    for span_dict_details in spans_details:
                        content_of_block_line = span_dict_details.get("content","")
                        content_type_of_block = span_dict_details.get("type","")
                knowledge_unit = {"page_no.":page_no, "raw_content":content_of_block_line, "content type": content_type_of_block}
                content_list.append(knowledge_unit)


        # Let's fetch the complete information related to the metadata of the tables




        return content_list
        

content_list = format_minerU_output()
print(content_list)