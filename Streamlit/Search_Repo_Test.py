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


# token = ''
# client = Github()

client = Github('my_client_id', 'my_client_secret')

@st.cache_resource
def get_repos():
    modules_org = client.get_organization('ds-modules').get_repos()
    repo_list = []
    for i in modules_org:
        repo_list.append(i)
    print(len(repo_list))
    
    toremove = 0
    for i in range(len(repo_list)):
        if repo_list[i].full_name == 'ds-modules/Library-HTRC':
            toremove = i
    repo_list.pop(toremove)
    print(len(repo_list))

    return repo_list

repo_list = get_repos()

def search_github(keyword, query):
    '''
    keyword: what you want to search (query)
    query: https://docs.github.com/en/search-github/searching-on-github/searching-code#search-within-a-users-or-organizations-repositories
    '''
    rate_limit = client.get_rate_limit()
    rate = rate_limit.search
    if rate.remaining == 0:
        print(f'You have 0/{rate.limit} API calls remaining. Reset time: {rate.reset}')
        return
    else:
        print(f'You have {rate.remaining}/{rate.limit} API calls remaining')

    # to change query: add/remove parameters
    # useful extensions: md, ipynb, etc...
    # visit website linked in description
    print('Query: ' + keyword + ' ' + query)
    result = client.search_code(keyword + ' ' + query)

    max_size = 100
    print(f'Found {result.totalCount} file(s)')
    if result.totalCount > max_size:
        result = result[:max_size]

    for file in result:
        print(f'{file.download_url}')

    st.write(result)

    return result

@st.cache_data
def get_all_contents():
    # NOTICE: unless you want to go over your allowed API calls per hour, only run this once.
    total_modules_ipynb = 0
    ipynb_counts = []
    filepaths = []
    for i in range(len(repo_list)):
        rate_limit = client.get_rate_limit()
        rate = rate_limit.search
        if rate.remaining == 0:
            print('loading API...')
            time.sleep(20)
        else:
            print(f'You have {rate.remaining}/{rate.limit} API calls remaining')

        test_repo = client.get_repo(repo_list[i].full_name)
        print('Repo Name: ', test_repo,)
        print('Repo Link: ', f'github.com/{test_repo.full_name}')

        total_ipynb = 0
        test_contents = test_repo.get_contents("")
        file_contents = []

        while test_contents:
            file_content = test_contents.pop(0)
            if file_content.type == "dir":
                test_contents.extend(test_repo.get_contents(file_content.path))
            else:
                if 'ipynb' in file_content.path:
                    total_ipynb += 1
                file_contents.append(file_content)
        filepaths.append(file_contents)

        total_modules_ipynb += total_ipynb
        ipynb_counts.append(total_ipynb)
        print('Total .ipynb files in this repo: ', total_ipynb)
        print('Total .ipynb files in ds-modules: ', total_modules_ipynb)
        print('---')

import ast

# with open('163repos.txt', 'r') as f:
#     allrepos = [list(eval(line)) for line in f]

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

title = st.text_input('What are you looking for?', '')
truth = []
raw_contents = []
if title:
    st.write('Note: Currently only searching 163/170 public repos. Fix coming soon.')
    # for i in range(len(allrepos)):
    #     for j in range(len(allrepos[i])):
    #         check = allrepos[i][j][0]
    #         if type(check) == str:
    #             if title in check.lower():
    #                 contentfile = eval(filepaths[i])[j]
    #                 # for x in range(len(raw_contents)):
    #                 #     if len(raw_contents) == 0:
    #                 #         continue
    #                 #     elif similar(raw_contents[x], check.lower()) > .8:
    #                 #         raw_contents_created = repo_list[x].created_at
    #                 #         contentfile_created = repo_list[i].created_at
    #                 #         if raw_contents_created < contentfile_created:
    #                 #             truth.pop(i)
    #                 print(repo_list[i])
    #                 truth.append([i, j])
    #                 raw_contents.append(check.lower())

    for i in range(len(first35_repos)):
        for j in range(len(first35_repos[i])):
            check = first35_repos[i][j][0]
            if type(check) == str:
                if title in check.lower():
                    contentfile = eval(filepaths[i])[j]
                    # for x in range(len(raw_contents)):
                    #     if len(raw_contents) == 0:
                    #         continue
                    #     elif similar(raw_contents[x], check.lower()) > .8:
                    #         raw_contents_created = repo_list[x].created_at
                    #         contentfile_created = repo_list[i].created_at
                    #         if raw_contents_created < contentfile_created:
                    #             truth.pop(i)
                    truth.append([i, j])
                    raw_contents.append(check.lower())

    for i in range(len(second35_repos)):
        for j in range(len(second35_repos[i])):
            check = second35_repos[i][j][0]
            if type(check) == str:
                if title in check.lower():
                    contentfile = eval(filepaths[35 + i])[j]
                    # for x in range(len(raw_contents)):
                    #     if len(raw_contents) == 0:
                    #         continue
                    #     elif similar(raw_contents[x], check.lower()) > .8:
                    #         raw_contents_created = repo_list[x].created_at
                    #         contentfile_created = repo_list[i].created_at
                    #         if raw_contents_created < contentfile_created:
                    #             truth.pop(i)
                    truth.append([35 + i, j])
                    raw_contents.append(check.lower())

    for i in range(len(third35_repos)):
        for j in range(len(third35_repos[i])):
            check = third35_repos[i][j][0]
            if type(check) == str:
                if title in check.lower():
                    contentfile = eval(filepaths[70 + i])[j]
                    # for x in range(len(raw_contents)):
                    #     if len(raw_contents) == 0:
                    #         continue
                    #     elif similar(raw_contents[x], check.lower()) > .8:
                    #         raw_contents_created = repo_list[x].created_at
                    #         contentfile_created = repo_list[i].created_at
                    #         if raw_contents_created < contentfile_created:
                    #             truth.pop(i)
                    truth.append([70 + i, j])
                    raw_contents.append(check.lower())
                    
    for i in range(len(fourth35_repos)):
        for j in range(len(fourth35_repos[i])):
            check = fourth35_repos[i][j][0]
            if type(check) == str:
                if title in check.lower():
                    contentfile = eval(filepaths[105 + i])[j]
                    # for x in range(len(raw_contents)):
                    #     if len(raw_contents) == 0:
                    #         continue
                    #     elif similar(raw_contents[x], check.lower()) > .8:
                    #         raw_contents_created = repo_list[x].created_at
                    #         contentfile_created = repo_list[i].created_at
                    #         if raw_contents_created < contentfile_created:
                    #             truth.pop(i)
                    truth.append([105 + i, j])
                    raw_contents.append(check.lower())
        
    for i in range(len(fifth23_repos)):
        for j in range(len(fifth23_repos[i])):
            check = fifth23_repos[i][j][0]
            if type(check) == str:
                if title in check.lower():
                    print(140+i,j)
                    contentfile = eval(filepaths[140 + i])[j]
                    # for x in range(len(raw_contents)):
                    #     if len(raw_contents) == 0:
                    #         continue
                    #     elif similar(raw_contents[x], check.lower()) > .8:
                    #         raw_contents_created = repo_list[x].created_at
                    #         contentfile_created = repo_list[i].created_at
                    #         if raw_contents_created < contentfile_created:
                    #             truth.pop(i)
                    truth.append([140 + i, j])
                    raw_contents.append(check.lower())

    print(truth)
    for i in range(len(truth)):
        repo = truth[i][0]
        file = truth[i][1]
        contentfile = eval(filepaths[repo])[file]
        path = re.findall('=.*', contentfile)[0][2:-2]
        st.write(repo_list[repo].get_contents(path = path).html_url)
    if len(truth) == 0:
        st.write('None Found')
    else:
        st.write('Complete')
