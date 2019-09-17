from py2neo import Graph, Node, Relationship
from py2neo.ogm import GraphObject

from flask import g


def get_db():
    if 'db' not in g:
        g.db = Graph('http://182.254.156.112:7474', username='neo4j', password='root1234')
    return g.db


def push_node(node):
    if isinstance(node, GraphObject):
        return get_db().push(node)


def get_node(node):
    if isinstance(node, GraphObject):
        return node.match(get_db()).first()


def del_node():
    pass


def update_edges():
    pass


def walk():
    pass
