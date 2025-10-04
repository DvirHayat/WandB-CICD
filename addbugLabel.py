import os
from ghapi.all import GhApi
owner,repo = os.getenv("GITHUB_REPOSITORY").split("/")
api = GhApi(owner=owner, repo=repo)
commeted = os.getenv("INPUT_COMMAND")
if commeted == "/bug":
    api.issues.add_labels(issue_number=int(os.getenv("GITHUB_ISSUE_NUMBER")), labels=["bug"])
elif commeted == "/feature":
    api.issues.add_labels(issue_number=int(os.getenv("GITHUB_ISSUE_NUMBER")), labels=["feature"])
elif commeted == "/resolved":
    api.issues.remove_label(issue_number=int(os.getenv("GITHUB_ISSUE_NUMBER")), name="bug")
