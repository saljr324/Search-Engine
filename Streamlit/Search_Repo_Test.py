import time
import numpy as np
import pandas as pd
from github import Github
import streamlit as st
import pickle
import json
import re
from difflib import SequenceMatcher
import os


client = Github('cec181f6847eb6472425', '1ab6e2c3b3ed83f4b25ecd390cd5ef65c629b591')

@st.cache_resource
def get_repos():
    modules_org = client.get_organization('ds-modules').get_repos()
    repo_list = []
    for i in modules_org:
        repo_list.append(i)
    
    toremove = 0
    for i in range(len(repo_list)):
        if repo_list[i].full_name == 'ds-modules/Library-HTRC':
            toremove = i
    repo_list.pop(toremove)

    return repo_list

repo_list = get_repos()

import ast

with open('Streamlit/first35.txt', 'r') as f:
    first35_repos = [list(ast.literal_eval(line)) for line in f]

with open('Streamlit/second35.txt', 'r') as f:
    second35_repos = [list(ast.literal_eval(line)) for line in f]

with open('Streamlit/third35.txt', 'r') as f:
    third35_repos = [list(ast.literal_eval(line)) for line in f]

with open('Streamlit/fourth35.txt', 'r') as f:
    fourth35_repos = [list(ast.literal_eval(line)) for line in f]

with open('Streamlit/fifth23.txt', 'r') as f:
    fifth23_repos = [list(ast.literal_eval(line)) for line in f]

with open('Streamlit/filepaths.txt', 'r') as f:
    filepaths = [line for line in f]



def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

try:
    st.title('Jupyter Notebook Search Engine')
    st.caption('For use on github.com/ds-modules. Note: Searching only 163/170 public repos. Fix coming soon.')
    st.subheader('What topic are you looking for?')
    title = st.text_input('Keywords:', '').lower()
    title = ' ' + title
    truth = []
    raw_contents = []
    unique_repos = []


    for i in range(len(first35_repos)):
        for j in range(len(first35_repos[i])):
            check = first35_repos[i][j][0]
            if type(check) == str:
                if title in check.lower():
                    contentfile = eval(filepaths[i])[j]
                    truth.append([i, j])
                    if i not in unique_repos:
                        unique_repos.append(i)
                    raw_contents.append(check.lower())

    for i in range(len(second35_repos)):
        for j in range(len(second35_repos[i])):
            check = second35_repos[i][j][0]
            if type(check) == str:
                if title in check.lower():
                    contentfile = eval(filepaths[35 + i])[j]
                    truth.append([35 + i, j])
                    if 35 + i not in unique_repos:
                        unique_repos.append(35 + i)
                    raw_contents.append(check.lower())

    for i in range(len(third35_repos)):
        for j in range(len(third35_repos[i])):
            check = third35_repos[i][j][0]
            if type(check) == str:
                if title in check.lower():
                    contentfile = eval(filepaths[70 + i])[j]
                    truth.append([70 + i, j])
                    if 70 + i not in unique_repos:
                        unique_repos.append(70 + i)
                    raw_contents.append(check.lower())

    for i in range(len(fourth35_repos)):
        for j in range(len(fourth35_repos[i])):
            check = fourth35_repos[i][j][0]
            if type(check) == str:
                if title in check.lower():
                    contentfile = eval(filepaths[105 + i])[j]
                    truth.append([105 + i, j])
                    if 105 + i not in unique_repos:
                        unique_repos.append(105 + i)
                    raw_contents.append(check.lower())

    for i in range(len(fifth23_repos)):
        for j in range(len(fifth23_repos[i])):
            check = fifth23_repos[i][j][0]
            if type(check) == str:
                if title in check.lower():
                    contentfile = eval(filepaths[140 + i])[j]
                    truth.append([140 + i, j])
                    if 140 + i not in unique_repos:
                        unique_repos.append(140 + i)
                    raw_contents.append(check.lower())

    repo_names = [repo_list[i] for i in unique_repos]
    repo_tabs = [re.findall(r'\/(.+)', i.full_name)[0] for i in repo_names] 
    truth.reverse()
    repo_tabs.reverse()
    if len(truth) == 0:
            st.write('None Found')
    else:
        tabs = st.tabs(repo_tabs)
        current_repo = repo_tabs[0]
        count = 0

        for i in range(len(truth)):
            repo = truth[i][0]
            file = truth[i][1]
            contentfile = eval(filepaths[repo])[file]
            path = re.findall('=.*', contentfile)[0][2:-2]

            url = repo_list[repo].get_contents(path = path).html_url
            clean_url = re.findall(r'(?:/)(.*?)(?:.)', url)
            repo = re.search(r'ds-modules/(.*?)/', url).group(1)
            if repo != current_repo:
                count += 1
                current_repo = repo_tabs[count]
            with tabs[count]:
                st.write(url)
        st.write('Complete')
except IndexError:
    st.write(' ')
