#!/bin/bash

### File: setconda.sh

# To run this script from project root directory:
# RUN: . .vscode/setconda.sh

# SETMEUP_GIST_URL="https://gist.githubusercontent.com/sugatoray/64e6c4c4ab42ef42a76be4a658712c4d/raw/b37a70aea4d782d1a61b8129ce185844ec4691e0/setmeup.sh"
# cd .vscode && curl $SETMEUP_GIST_URL -o setmeup.sh && cd ..

alias getrepo="git rev-parse --show-toplevel"
alias getrepo-dirname="basename $(getrepo)"
alias topdir="getrepo || pwd"
alias setconda=". $(topdir)/.vscode/setconda.sh"
alias baseconda="conda activate base"
# run ymake <command> from repository root folder
alias ymake="make -C $(topdir)/.vscode" # this dynamically runs the command wrt .vscode folder
# run xmake <command> from repository root folder
alias xmake="make -f $(topdir)/.vscode/Makefile" # Duplicate of setmeup:xmake
alias setmeup=". $(topdir)/.vscode/setmeup.sh" 
alias loadvars=". $(topdir)/.vscode/loadvars.sh" # Duplicate of setmeup:loadvars
alias gotoroot="cd $(getrepo)"

PROJECT_NAME="vscode-markdown-extension-pack"
PROJECT_CONDA_ENV="fav_env"

setmeup && loadvars || true

PROJECT_NAME="$(getrepo-dirname || echo $PROJECT_NAME)"

# formatsetconda $PROJECT_NAME $PROJECT_CONDA_ENV || 
conda activate $PROJECT_CONDA_ENV

unset \
    PROJECT_NAME \
    PROJECT_CONDA_ENV
