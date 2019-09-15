from flask import Blueprint, jsonify
from EasyG import db

bp = Blueprint('graph', __name__, url_prefix='/graph')


def build_nodes(node):
    data = {"name": node['name'], "label": node['label']}
    return data


def build_edges(relationship):
    if relationship.start_node:
        print(relationship.start_node)
    if relationship.end_node:
        print(relationship.end_node)
    if relationship.type:
        print(relationship.type)
    data = {"source": relationship.start_node['name'],
            "target": relationship.end_node['name'],
            "relationship": relationship.type}
    return data


@bp.route('/', methods=['GET'])
def get_graph():
    gra = db.get_db()
    nodes = list(map(build_nodes, gra.nodes.match()))
    edges = list(map(build_edges, gra.relationships.match()))
    # edges=[]
    # # nodes = gra.nodes.match()
    # edges = gra.relationships.match()
    for o in edges:
        i = 11
        print(o)
    return jsonify(elements={"nodes": nodes, "edges": edges})
