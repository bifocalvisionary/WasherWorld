##  Toolkit - Flask App Quickstart Template

### Introduction
This project serves as a template for creating MongoDB enabled webpages powered by flask. It contains a home page,
login page, bug report form, and about page. Each of these pages is MongoDB enabled.

If used properly, it should cut down on time spent rewriting essentially identical code.

With minor modifications, this general structure should serve as a good base for any project meant to be deployed

### Usage
There are some modifications that should be made to the provided template before development begins

1. In utils/databaseUtils, the address of the mongoDB client should be changed to a project specific database

2. In static/img, icon.png represents the favicon of the webapp, hackathon-logo should be the logo of whatever hackathon 
   the project is being created for, and base-background is the image used as the background for all pages

3. Utilities for uploading and retrieving images to and from a google cloud bucket are included in databaseUtils and a route
   for accessing these utilities is commented out in app.py
   
