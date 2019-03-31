# WebServiceMashup
A web based query system that uses REST, MongoDB as backend and Python & Flask for web deployment

Given dataset: 
Web Service API data from ProgrammableWeb.com 

Goals:
Project for designing the data structure for the database, parsing the text files and loading the data to a NoSQL database. 
Using this database as the backend, develop a web-based query systemthat allows the following query:

1.Returns the names of APIs based on different criteria, including updated year, protocols, category, rating (such as higher than, equal to, or lower than a given rating), and tags.
2.Returns the names of Mashups based on different criteria, including updatedyear, used APIs, and tags. 
3.Given a set of keywords,returns the names of APIs if all the keywords can be found in thetitle, summary, and the description of the APIs.
4.Given a set ofkeywords, returns the names of Mashups if all the keywords can be found in the title, summary, and the description of the Mashups

To run the code:

1. Start MongoDB.exe & make sure that mongodb is up and running.
2. Run the api.py file.
3. Click on http://127.0.0.1:5000/ from the output console.
4. Follow the instruction on the web interface
