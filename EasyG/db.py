from py2neo import Graph, Node, Relationship
from flask import g


def get_db():
    if 'db' not in g:
        g.db = Graph('http://182.254.156.112:7474', username='neo4j', password='root1234')
    return g.db


