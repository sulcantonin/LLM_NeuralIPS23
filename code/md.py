import re
from rapidfuzz import fuzz

def remove_section(text, sect):
    start = re.search(sect, text, flags=re.DOTALL)
    if start == None: # not found
        
        return text
    start = start.end()
    
    end = re.search(r'\n#', text[start:], flags=re.DOTALL)
    
    if end == None: # last # wasn't found 
        end = len(text)
    else:
        end = end.start() + start
    return text[:start-len(sect)] + text[end:]

def split_by_sections(text):
    return re.split('#+ .*',text)

def split_by_paragraphs(text):
    return re.split('\n',text)

def clean_string_before_qa(text : str) -> str:
    # text = re.sub(r'{.*}','',text) # removing this {sort=...}
    # text = re.sub(r'\\','',text) # removing escape caraceters
    # text = re.sub(r'\n','',text) # removing newlines
    return text

# print(data_)
def replace_eqn(x : str) -> str:
    eqns = set(re.findall(r'\$.*?\$',x))
    eqn_dict = {eqn : f'EQN{str(i).zfill(3)}' for i, eqn in enumerate(eqns)}
    for eqn in eqn_dict:
        x = x.replace(eqn, eqn_dict[eqn])
    return x, eqn_dict

def replace_eqn_back(x, eqn_dict):
    eqn_dict_rev = {eqn_dict[k] : k for k in eqn_dict}
    for placeholder in eqn_dict_rev:
        x = x.replace(placeholder,eqn_dict_rev[placeholder])
    return x

def clean_colons(text):
    '''
    issue from from pypandoc transformation of arxiv (latex) to markdown
    
    when text is converted with pypandoc, figures and special tags are replaced with :: tag
    This is redunant and should be removed, this just removes the ::+ tag from the text
    '''
    text = re.sub('::+.*(\n|$)','',text)
    return text

def clean_image(text):
    ''''
    issue from from pypandoc transformation of arxiv (latex) to markdown
    
    this kind of placegholds for images are also about to be removed
    ![image](fig0.eps){width="100mm"}
    print(clean_image("""giwhrngw\neginir\n![image](fig0.eps){width="100mm"}ewgkhwn\nwpeighn"""))
    '''
    
    return re.sub('!\[image\]\(.*\)\{.*\}','',text)

def clean_wiki_markdown(text):
    '''
    issue from wiki (html) to markdown
    '''
    text = re.sub(r"```.*```",'', text, flags = re.DOTALL)
    text = re.sub(r"\[.*?\]\{.*?\}",'',text, flags = re.DOTALL)
    return text