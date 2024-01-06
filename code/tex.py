import re
import pypandoc

label_expr = re.compile(r'\\label{(.*?)}',)
label_expr_full = re.compile(r'\\label{.*?}',)
ref_expr = re.compile(r'\\ref{(.*?)}',)
ref_expr_full = re.compile(r'\\ref{.*?}',)
cite_expr_full = re.compile(r'\\cite{.*?}',)
begin_expr = re.compile(r'\\begin{(.*?)}', flags = re.DOTALL)
caption_expr = re.compile(r'\\caption{(.*?)}', flags = re.DOTALL)

tag_expr      = lambda tag : re.compile(r'\\begin{' + re.escape(tag) + r'}(.*?)\\end{' + re.escape(tag) + r'}', flags = re.DOTALL)
tag_expr_full = lambda tag : re.compile(r'\\begin{' + re.escape(tag) + r'}.*?\\end{' + re.escape(tag) + r'}', flags = re.DOTALL)


def get_begin_end(latex_document : str) -> dict:
    ''' returns a content between begin and end, where keys are labels'''

    begin_tags = set(re.findall(begin_expr,latex_document))
    if 'document' in begin_tags:
        begin_tags.remove('document')

    label_dict = {}

    for tag in begin_tags:
        # find all tags e.g. \begin{equation} ... \end{equation}
        tag_ = re.findall(tag_expr(tag), latex_document)
        tag_full_ = re.findall(tag_expr_full(tag), latex_document)
        
        # iteratre through every occurence of e.g. \begin{equation} ... \end{equation}
        for x_ in tag_full_:
            
            label = re.findall(label_expr,x_)
            if len(label) > 0:
                # storing the item in the label dict
                label_dict[label[0]] = x_
    return label_dict


def get_tag_data(text, tag):
    '''
        gets everything between \begin{tag} EVERYTHING \end{tag}
    '''
    tag = re.compile(r'\\begin{' + tag + r'}(.*)\\end{' + tag + r'}',flags = re.DOTALL)
    res = re.findall(tag, text)
    if len(res) > 0:
        return res[0]
    else:
        None

def get_tag_content(text, tag):
    '''
    gets everything between \tag{EVERYTHING}
    '''
    tag = re.compile(r'\\' + tag + r'{(.*?)}',flags = re.DOTALL)
    res = re.findall(tag, text)
    if len(res) > 0:
        return res[0]
    else:
        None

def get_section(text, tag):
    '''
        gets everything inside this section until it gets to another \section tag
    '''
    section_tag = r'\\section{(.*?)}'
    matches = [m for m in re.finditer(section_tag, text, flags = re.DOTALL)]
    matches_tag_idx = [i 
                       for i,m in enumerate(matches) 
                       if fuzz.token_set_ratio(tag.lower(), m.groups()[0].lower()) == 100]
    if len(matches_tag_idx) == 0:
        return None
    if len(matches) <= matches_tag_idx[0] + 1:
        return None
    
    start = matches[matches_tag_idx[0]  ].start()
    stop =  matches[matches_tag_idx[0]+1].start()
    
    return text[start:stop]

def get_figure_captions(label_dict : dict) -> dict:
    ''' goes through dict, if tag is figure, taking only its caption'''
    readable = {}

    for k in label_dict:
        entry = label_dict[k]
        tag = re.findall(begin_expr,entry)
        # if it is figure, just exporting the caption
        if tag[0] == 'figure':
            plain = pypandoc.convert_text(entry, 'plain', format='latex')
            if len(plain) == 0:
                entry = ''
            else:
                entry = f"(figure caption: {plain})"
        # else:
        #    readable_ = pypandoc.convert_text(entry, 'markdown', format='latex')

        readable[k] = entry
    return readable


def insert_tag_content_to_ref(latex_document : str, label_dict : dict) -> str:
    ''' 
    this function takes string in @latex_document and replaces all occurences of keys in @label_dict 
    with their content
    '''
    matches = list(re.finditer(ref_expr_full,latex_document))
    # !!! this is really important
    matches.reverse()
    for m in matches:
        # getting the name of the reference
        ref = re.findall(ref_expr,m.group(0))
        assert len(ref) == 1
        ref = ref[0]
        if ref in label_dict:
            # replacing the occurence of the reference with @label_dict_markdown[ref]
            latex_document = latex_document[:m.start()] + '\n\n' + label_dict[ref] + '\n\n' + latex_document[m.end():]
        else:
            
            print(f'A problem with reference {ref}')
    return latex_document

'''
# OBSOLETE
def replace_backslash_in_eq(data : str):
    eq = re.findall(r'\$.*?\$',data, flags = re.DOTALL)
    for eq_ in eq:
        eq_esc = re.sub(r'\\',r'\\\\',eq_)
        data = data.replace(eq_, eq_esc)
    return data
'''