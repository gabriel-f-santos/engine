# Makefile for Python project

# venv settings
export VIRTUALENV := $(PWD)/.venv
export PATH       := $(VIRTUALENV)/bin:$(PATH)
SHELL = /bin/bash

# Variables
VENV_DIR := .venv
PYTHON := python3.11

BLACK := $(VENV_DIR)/bin/black
FLAKE8 := $(VENV_DIR)/bin/flake8

# Directories
SRC_DIR := src
TEST_DIR := tests

# Targets and Rules
.PHONY: install test format lint

install: venv
	@echo "Installing project dependencies..."
	pip install -r requirements.txt

clean: 
	@echo "Cleaning..."
	rm -r .venv

venv:
	@echo "Creating virtual environment..."
	$(PYTHON) -m venv $(VIRTUALENV)
	pip install --upgrade pip
	@echo "Activate virtual environment..."
	source $(VIRTUALENV)/bin/activate

test:
	@echo "Running tests..."
	$(PYTHON) -m unittest

format:
	@echo "Formatting code with Black..."
	black $(PWD) --line-length=80 --target-version=py311

lint:
	@echo "Linting code with Flake8..."
	$(FLAKE8) $(PWD) --max-line-length=80 --exclude .venv,dependencies,migrations

# Default target
.DEFAULT_GOAL := test