

from src.document_parsing.data_extraction import MinerU_Parser
from src.document_parsing.sample_data import combined_knowledge_units



"""
Utils Functions:

1- Knowledge units splitter
2- Context extractor for multi-modal content

"""


# Lets define the function to split the knowledge units into textual and non-textual units

def units_splitter(knowledge_units_list:list):
    """
    This function takes the list of the knowledge units created in the parsing process from minerU output, and 
    filter out the textual and non-textual knowledge units on the basis of their content type, into two different
    objects. 

    **Args:**
    knowledge_units_list (list): It is the list of the knowledge units - combined textual and non-textual units.

    **Returns:**
    textual_knowledge_units (list): It is the list of the textual knowledge units.
    multi-model_knowledge_units (list): It is the list of the non-textual knowledge units.

    **Raises:**

    Implementation workflow:
    
    1- Initiate the two lists to store respective type of units separately.
    2- Iterate over the units using for loop 
    3- If content type is in ["title","text"]: append the list for textual knowledge units
    4- If content type == "table": append the list for non-textual knowledge units
    5- Return the textual_knowledge_units, non_textual_knowledge_units
    
    """

    # lets initialize the minerU parser
    #### FREEZED FOR TESTING PURPOSE ####
    #init_minerU = MinerU_Parser(data_file_path=knowledge_units_list)
    #knowledge_units_list = init_minerU.format_minerU_output()

    complete_knowledge_units = knowledge_units_list

    # Let's initialize the lists for textual and non-textual units separately
    multi_model_units = []
    textual_units = []

    for unit in complete_knowledge_units:
        unit = dict(unit)

        # Let's fetch the textual units
        content_type = unit.get("content_type")
        if content_type in ["text","title"]:
            textual_units.append(unit)
        
        # Let's fetch the non-textual units
        elif content_type == "table":
            multi_model_units.append(unit)

    return print(multi_model_units)



units_splitter(knowledge_units_list=combined_knowledge_units)

#units_splitter(knowledge_units_list="C:\\Users\Hp\\Documents\\AI Projects docs\\RAG\\RAG_for_Anything.pdf")
