from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication
from azure.devops.v5_0.git.models import GitQueryCommitsCriteria
from azure.devops.v5_0.git.models import GitVersionDescriptor
import os
import matplotlib.pyplot as plt
import csv

# Fill in with your personal access token and org URL
personal_access_token = 'Enter Pat'
organization_url = 'https://dev.azure.com/mseng'

reenter_org_url = input("Enter your org url, or press Enter: ")
if reenter_org_url != '':
    organization_url = reenter_org_url

reenter_PAT = input("Enter your PAT, or press Enter: ")
if reenter_PAT != '':
    personal_access_token = reenter_PAT

# Create a connection to the org
credentials = BasicAuthentication('', personal_access_token)
connection = Connection(base_url=organization_url, creds=credentials)

git_client = connection.get_client('azure.devops.released.git.git_client.GitClient')
repo_id = 'fb240610-b309-4925-8502-65ff76312c40'
search_criteria = GitQueryCommitsCriteria()
search_criteria.author = "pranpati@microsoft.com"
search_criteria.item_version = GitVersionDescriptor()
search_criteria.item_version.version = 'master'

commits = git_client.get_commits(repo_id, search_criteria, 'AzureDevOps', None, 1000)
commits_ids = [c.commit_id for c in commits]

file_types = {}
files_count = {}

for i in range(len(commits_ids)):
    changes = git_client.get_changes( commits_ids[i], repo_id, 'AzureDevOps')
    for j in range(len(changes.changes)):
        if 'isFolder' in changes.changes[j]['item']:
            continue
        type_of_change = changes.changes[j]['changeType']
        filename, file_extension = os.path.splitext(changes.changes[j]['item']['path'])
        if type_of_change not in file_types:
            file_types[type_of_change] = {}
        if file_extension in file_types[type_of_change]:
            file_types[type_of_change][file_extension] = file_types[type_of_change][file_extension] + 1
            files_count[file_extension] = files_count[file_extension] + 1
        else:
            file_types[type_of_change][file_extension] = 1
            files_count[file_extension] = 1

with open('count_by_file_types.csv', 'w') as output:
    writer = csv.writer(output)
    for key, value in files_count.items():
        writer.writerow([key, value])

# Plots top 8 file types
# file_types = sorted(file_types.items(), key=lambda x: x[1])
# file_types.reverse()
# if len(file_types) > 8:
#     file_types = file_types[0:7]
# file_types, count = zip(*file_types)
#
# plt.bar(file_types, count)
# plt.show()

# plt.pie(count, labels=file_types)
# plt.axis('equal')
# plt.show()
