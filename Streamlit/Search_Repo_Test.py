import numpy as np
import pandas as pd
from github import Github
import streamlit as st
import json
import re


client = Github('cec181f6847eb6472425', '1ab6e2c3b3ed83f4b25ecd390cd5ef65c629b591')

def search_github(keyword, query):
    '''
    keyword: what you want to search (query)
    query: https://docs.github.com/en/search-github/searching-on-github/searching-code#search-within-a-users-or-organizations-repositories
    '''
    contentFiles = []
    result = client.search_code(keyword + ' ' + query)
 
    for file in result:
        contentFiles.append(file)
    
    return contentFiles

st.title('Jupyter Notebook Search Engine')
st.caption('For use on github.com/ds-modules')
st.subheader('What topic are you looking for?')
title = st.text_input('Keyword(s):', placeholder = 'Enter keyword(s) seperated by comma')

if title:
    contentFiles = search_github(title, 'org:ds-modules extension:ipynb')
    if len(contentFiles) == 0:
        st.write('None Found')
    else:
        html_url_0
        repo_tabs = []
        html_urls = []
        for i in range(len(contentFiles)):
            html_url = contentFiles[i].html_url
            repo = re.search(r'ds-modules/(.*?)/', html_url).group(1)
            html_urls.append(html_url)
            if repo not in repo_tabs:
                repo_tabs.append(repo)
        
        st.write(f'Found {len(contentFiles)} Notebooks in {len(repo_tabs)} repositories')
        tabs = st.tabs(repo_tabs)
        current_repo = re.search(r'ds-modules/(.*?)/', html_url_0).group(1)
        for i in range(len(contentFiles)):
            repo = re.search(r'ds-modules/(.*?)/', html_urls[i]).group(1)
            index = repo_tabs.index(repo)
            with tabs[index]:
                st.write(html_urls[i])
        st.write('Complete')
