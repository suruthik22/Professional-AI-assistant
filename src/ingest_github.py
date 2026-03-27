import requests
import json
import base64
import os 
import re

USERNAME="suruthik22"

headers={"Authorization":f"token {os.getenv('GITHUB_TOKEN')}"}

def clean_text(text):
    text = re.sub(r"!\[.*?\]\(.*?\)", "", text)
    text = re.sub(r"\[.*?\]\(.*?\)", "", text)
    text = re.sub(r"#", "", text)
    return text.strip()

def fetch_github():
    repos_url=f"https://api.github.com/users/{USERNAME}/repos"
    repos=requests.get(repos_url, headers=headers).json()
    print(repos)
    all_data=[]

    for repo in repos:
        repo_name=repo["name"]

        branch=repo.get("default_branch","main")
        
        readme_url=f"https://api.github.com/repos/{USERNAME}/{repo_name}/readme?ref={branch}"
        response = requests.get(readme_url, headers=headers)
        
        content = ""

        if response.status_code==200:
            data=response.json()

            #Decode base64 content
            if "content" in data:
                raw=base64.b64decode(data["content"]).decode("utf-8", errors="ignore")
                content=clean_text(raw)
        else:
            print(f"{repo_name} -> {response.status_code}")
           
        all_data.append({
            "type":"project",
            "Project name":repo_name,
            "Project description":repo.get("description",""),
            "Project content":content[:5000] #limit size
        })

    with open("data/raw/github.json","w", encoding="utf-8") as f:
        json.dump(all_data, f, indent=2)

if __name__=="__main__":
    fetch_github()