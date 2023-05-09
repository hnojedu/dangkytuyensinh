from python_docx_replace import docx_replace
import docx

def generate(replace_dict, filedir):

    doc = docx.Document(filedir)
    docx_replace(doc, **replace_dict)
    
    doc.save(filedir)
