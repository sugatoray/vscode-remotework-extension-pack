#!/bin/bash

## Quick Refs
##? To soft-reset (revert back) last git commit:
##^ git reset --soft HEAD~1
##? For soft-resetting last 3 git commits:
##^ git reset --soft HEAD~3

## Git Commands as Aliases
alias getrepo="git rev-parse --show-toplevel 2>/dev/null"
alias getrepo-dirname="basename $(getrepo)"
alias getrepo-dirpath="echo $(getrepo)"
alias getrepo-parentdir="dirname $(getrepo)"
alias getrepo-remote="git remote get-url origin"
# getrepo-remote | cut -d ":" -f2 | cut -d "." -f1
alias getrepo-name="getrepo-remote | cut -d ':' -f2 | cut -d '.' -f1"
alias getrepo-owner="getrepo-name | cut -d '/' -f1"
alias getrepo-root="getrepo-name | cut -d '/' -f2"

## Setconda Commands
alias topdir="getrepo || pwd"
alias setconda=". $(topdir)/.vscode/setconda.sh"
alias baseconda="conda activate base"
# run ymake <command> from repository root folder
alias ymake="make -C $(topdir)/.vscode" # this dynamically runs the command wrt .vscode folder
# run xmake <command> from repository root folder
alias xmake="make -f $(topdir)/.vscode/Makefile"
alias setmeup=". $(topdir)/.vscode/setmeup.sh"
alias loadvars=". $(topdir)/.vscode/loadvars.sh"
alias gotoroot="cd $(getrepo)"

## Commands for Conda Enviornment
alias conda-envname="conda env list | grep \* | cut -d '*' -f1 | tr -d ' '"
alias conda-envpath="conda env list | grep \* | cut -d '*' -f2 | tr -d ' '"

## Commands for python and pip
#
# define command: python
# - this will map to the current pip environment's python
# - code logic: https://stackoverflow.com/a/27369375/8474894
alias python="${$(which pip)/pip/python}"
# define command for upgrading pip
alias pipup="python -m pip install --upgrade pip"

# Commands for venv
VENV_DIR=".venv"
alias makevenv="setconda && python -m venv ${VENV_DIR} --prompt venv --copies"
alias venvup="source $(topdir)/${VENV_DIR}/bin/activate && setmeup"
alias venvdown="deactivate && setmeup"
alias setvenv="setconda && makevenv && venvup"
alias clearvenv="venvdown && rm -rf $(topdir)/.venv"
alias resetvenv="clearvenv && setvenv"


## Docs Generating Commands
alias genpdocs="pdoc -d google -h localhost -n -p 5555 --math --show-source"

unset \
    VENV_DIR
