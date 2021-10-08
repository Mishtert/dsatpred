#!/usr/bin/env python
# coding: utf-8

# In[ ]:


def clean_text_rem_stopwords(text):
    import re
    """Basic cleaning of texts."""
    #convert to lower case
    text = text.lower()

    # remove html markup
    text = re.sub("(<.*?>)", "", text)

    # remove non-ascii and digits
    text = re.sub("(\\W|\\d)", " ", text)

    #remove whitespace
    text = text.strip()
    
    # remove stopwords
    text = ' '.join(word for word in text.split() 
                    if word not in stop_words)
    return text

def clean_text_stopwords_intact(text):
    import re
    """Basic cleaning of texts."""
    #convert to lower case
    text = text.lower()

    # remove html markup
    text = re.sub("(<.*?>)", "", text)

    # remove non-ascii and digits
    text = re.sub("(\\W|\\d)", " ", text)

    #remove whitespace
    text = text.strip()
    return text

# def remove_spaces(df,col):
#     df[col] = df[col].apply(lambda x: x.strip())
#     df[col] = df[col].apply(lambda x: x.lstrip())
#     df[col] = df[col].apply(lambda x: x.rstrip())
#     return df[col]

def remove_spaces(text):
    text = text.strip()
    text = text.lstrip()
    text = text.rstrip()
    return text

def clean_header(df):
    df.columns = df.columns.str.strip().str.lower().str.replace(
        '(', '_').str.replace(')', '').str.replace(' ', '')
    
    
def replace_text(text):
    text = text.replace(old,new)
    return text
    

