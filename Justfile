#!/bin/bash

# What is a justfile?
# - source: https://github.com/casey/just
# - cheatsheet: https://cheatography.com/linux-china/cheat-sheets/justfile/


########################## Extesion Specific Parameters #############################

VSCE_PUBLISHER := "sugatoray"
VSCE_NAME := "vscode-remotework-extension-pack"
PYTHON := "python3"

########################## DONOT CHANGE PARAMETERS BELOW ###############################

VSCE_EXTENSION_URL := "https://marketplace.visualstudio.com/items?itemName={{VSCE_PUBLISHER}}.{{VSCE_NAME}}"
VSCE_MANAGEMENT_URL := "https://marketplace.visualstudio.com/manage/publishers/{{VSCE_PUBLISHER}}"
VSCE_TOKEN_URL := "https://dev.azure.com/{{VSCE_PUBLISHER}}/_usersSettings/tokens"

####################### PARAMETERS ###########################

help:
	@echo "\n Makefile Commands' Help\n"
	# Commands:
	#
	# vsix-move         :	Move the .vsix artifact(s) under .artifacts folder.
	# vsix-clear        :	Clear the .vsix files from .artifacts folder.
	#
	# pkg-build         :	Build the extension (creates a.vsix file).
	# pkg-publish       :	Publish the extension.
	# pkg-release       :	Build and Publish the extension.
	#
	# vsce-open         :	Opens the VS Code Extension Management page for a Publisher.
	# vsce-token        :	Opens the Azure DevOps Page to Manage the Personal Access Token for VSCE-
	# vsce-metadata     :	Fetches extension metadata
	# vsce-extn         :	Opens the Marketplace Extension Page in Browser
	#
	# py-clear          :	Clear off various python artifacts (files/folders)
	# py-genreadme      :	Generate README.md from package.json
	# 
	@echo "\n ...: How To Manage Relevant Environment Variables :... \n"
	# 1. Update export VAR="value" lines in ~/.secrets/manage_secrets.sh file.
	# 2. Add the following line to your ~/.bashrc or ~/.zshrc file:
	#    . ~/.secrets/manage_secrets.sh
	# 3. Open a new shell (bash, zsh, etc.)
	# 

############################## ..: COMMANDS :.. ################################

vsix-move:
	@echo "\n Moving .vsix files to .artifacts folder... ⏳\n"
	mv *.vsix ./.artifacts/

vsix-clear:
	@echo "\n Moving .vsix files to .artifacts folder... ⏳\n"
	rm ./.artifacts/*.vsix

pkg-build:
	@echo "\n🔥⚙️ Packaging... ⏳\n"
	vsce package

pkg-publish:
	@echo "\n📘📄 Publishing... ⏳\n"
	# Publish to VS Code Marketplace: using vsce
	vsce publish -p ${VSCE_PAT}
	# Publish to open-vsx.org: using ovsx
	ovsx publish -p ${OVSX_PAT}

pkg-release: pkg-build vsix-move pkg-publish vsix-move vsix-clear
	@echo "\n✨ Releasing... ⏳\n"

vsce-open:
	@echo "\n✨ Open VS Code Extension Manager in Browser... ⏳\n"
	{{PYTHON}} -c "import webbrowser; webbrowser.open('{{VSCE_MANAGEMENT_URL}}')"

vsce-token:
	@echo "\n✨ Open VS Code Extension Token Manager in Browser... ⏳\n"
	{{PYTHON}} -c "import webbrowser; webbrowser.open('{{VSCE_TOKEN_URL}}')"

vsce-metadata:
	@echo "\n✨ Show VS Code Extension Metadata... ⏳\n"
	vsce show {{VSCE_PUBLISHER}}.{{VSCE_NAME}}  

vsce-extn:
	@echo "\n✨ Open VS Code Extension Marketplace in Browser... ⏳\n"
	{{PYTHON}} -c "import webbrowser; webbrowser.open('{{VSCE_MANAGEMENT_URL}}')"

## Clear repository of python artifacts

# .PHONY: py-clear
py-clear: # Clear off various python artifacts (files/folders)
	@echo "\n✨ Clear artifact files... ⏳\n"
	@echo "\n🟢 Clear .ipynb_checkpoints files"
	@# same as:
	@# find **/.ipynb_checkpoints type -f -delete
	@# source:
	@# - https://askubuntu.com/a/842170/853549
	rm -rf ./.ipynb_checkpoints ./**/.ipynb_checkpoints
	
	@echo "\n🟢 Clear __pycache__ folders"
	@# same as:
	@# find **/__pycache__ -delete
	rm -rf ./__pycache__ \
		./**/__pycache__ \
		./**/**/__pycache__

# .PHONY: py-genreadme
py-genreadme:
	@echo "\n✨ Generate README.md from package.json... ⏳\n"
	{{PYTHON}} ./composer/compose.py
#########################################################

# .PHONY: test-envar
test-envar:
	@echo "\nTesting Environment Variables... \n"
	echo "${HOME}"

# behold a recipe
test-fun:
  echo "hi" > tmp.txt
  cat tmp.txt
  rm tmp.txt
