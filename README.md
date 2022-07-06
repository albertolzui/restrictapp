# Restrictapp

Restrictapp is a travel restriction information resource application.

## Getting Started

Restrictapp was created with FastAPI and can be deployed on the local server using uvicorn or the free development server - Deta. A MongoDB Database was also setup with multiple collections for CRUD operations.

[FastAPI Documentation](https://fastapi.tiangolo.com/)

[Uvicorn Documentation](https://www.uvicorn.org/)

[Deta Documentation](https://docs.deta.sh/docs/micros/about/)

[Running a server manually with Uvicorn](https://fastapi.tiangolo.com/deployment/manually/)

[Deploying to Deta](https://fastapi.tiangolo.com/deployment/deta/)


###### The requirements.txt file

The requirements.txt file contains all essential modules, frameworks and libraries required to run Restrictapp

`pip install -r requirements.txt`



## How it works

Retrictapp gets information on travel restrictions available on country pairs (origin and destination) from other web resources (notably Kayak.com) through webscrapping with BeautifulSoup and saves the information block into a MongoDB collection from where a user's search prompts access to available text from the database and outputs it to the user. 

Restricapp also generates suggestions based on filter criterion selected by a user as well as the origin country. In this case the suggestions are also based on what is stored in the collection on the database.

With Restrictapp, users are able to create accounts and save trips. User accounts along with saved trips are stored in a separate collection on MongoDB.


## MongoDB Credentials are Stored in .env file

The MongoDB connection requires a username and access key, which are stored in a .env file and accessed on the python scripts as `USER` and `KEY`.

## The Code

Information on the classes, functions and API routes served are available as comments within each Python file, and more extensively in `testing.py`


## Languages

```
Python
JavaScript
HTML
CSS

```









