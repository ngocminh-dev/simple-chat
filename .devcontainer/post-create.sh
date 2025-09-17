#!/bin/bash

echo "Installing backend dependencies..."
pip install -r ./backend/requirements.txt

echo "Installing frontend dependencies..."
cd ./frontend
npm install