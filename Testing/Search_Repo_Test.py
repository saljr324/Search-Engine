import time
import numpy as np
from github import Github
import streamlit as st
import pickle


token = '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'
client = Github(token)

# modules_org = client.get_organization('ds-modules').get_repos()
# repo_list = []
# for i in modules_org:
#     repo_list.append(i)

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

#search_github('Ari Edmundson', 'extension:ipynb org:ds-modules')

# remove = 0 
# for i in range(len(repo_list)):
#     if repo_list[i].full_name == 'ds-modules/Library-HTRC':
#         remove = i
# repo_list.pop(remove)


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

#title = st.text_input('What are you looking for?', '')
f = open("contents.txt", "r")
notebook_contents = [line[1:-1].split(',') for line in f]
print(len(notebook_contents[1]))

