
Django + Neo4J Driver

This app's functionality was taken from the "polls' tutorial at the official site:

https://docs.djangoproject.com/en/4.2/intro/tutorial01/

However, it was adapted to use _only_ the Neo4J Driver (and not other derivative libraries like neomodel):

https://neo4j.com/docs/api/python-driver/current/index.html

The graph-edge model is a straightforward modelling of the relational tables of the original tutorial.

This was a development-only POC and NOT for production.


# django setup
django-admin startproject mysite
# create an app
python manage.py startapp polls

python -m venv .venv
# virtual start
.venv\scripts\activate

# install reqiurements
pip3 install -r requirements.txt

python manage.py runserver
# (http://localhost:8000/polls/)

# You cannot install anything beyond the neo4j python driver in Python 12+. Use ChatGPT for instructions #

# Useful Cipher
# test connecion
MATCH (n) RETURN count(n) as node_count
# get whole graph
MATCH (n) RETURN n
# erase whole graph
MATCH (n) DETACH DELETE n