

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
        ABS_PATH (Path): It is the absolute path that we need to use in order to convert the relative path of the table_image to the
        absolute path. For now, we do not have the output of minerU path and our input path same (Because minerU is not running command statement correctly)
        so, we are manually bringing the path of the minerU output manually. Otherwise, we would just have to import it using path.cwd().
        
        **Returns:**
        self.content_list (list): It is the list of the knowledge units that contains the information about part of the document.

        **Raises:**

        """
        # lets get the input of the function
        minerU_raw_output = Parsed_minerU_raw
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
        

content_list = format_minerU_output()
print(content_list)