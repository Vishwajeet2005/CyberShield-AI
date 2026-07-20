#!/bin/sh
git filter-branch -f --env-filter '
if [ "$GIT_AUTHOR_EMAIL" = "cybershield@hackathon.ai" ]; then
    export GIT_AUTHOR_EMAIL="vishwajeetborade@gmail.com"
    export GIT_AUTHOR_NAME="Vishwajeet2005"
    export GIT_COMMITTER_EMAIL="vishwajeetborade@gmail.com"
    export GIT_COMMITTER_NAME="Vishwajeet2005"
fi
' -- --all
