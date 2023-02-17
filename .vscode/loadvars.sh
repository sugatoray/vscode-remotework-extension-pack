#!/bin/bash

## Env-Variable-Loader Commands
if [ -e "$(topdir)/.env" ]; then export $(cat "$(topdir)/.env"); fi; \
if [ -e "$(topdir)/.vscode/.env" ]; then export $(cat "$(topdir)/.vscode/.env"); fi; \
if [ -e "$(topdir)/.vscode/.env.shared" ]; then export $(cat "$(topdir)/.vscode/.env.shared"); fi; \
if [ -e "$(topdir)/.secrets/.env.shared" ]; then export $(cat "$(topdir)/.secrets/.env.shared"); fi; \
if [ -e "$(topdir)/.secrets/.env.secret" ]; then export $(cat "$(topdir)/.secrets/.env.secret"); fi;
