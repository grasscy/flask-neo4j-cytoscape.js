from flask import Blueprint, jsonify, request
from app.app.concept import Concept

bp = Blueprint('graph', __name__, url_prefix='/graph')


def build_nodes(concept: Concept):
    data = {'id': concept.__primaryvalue__, 'name': concept.name, 'brief': concept.brief, 'content': concept.content}
    return {'data': data}


def build_edges(concept):
    ret = []
    for ccp in concept.relates:
        data = {
            'source': concept.__primaryvalue__,
            'target': ccp.__primaryvalue__,
            'relationship': ''
        }
        ret.append({
            'data': data
        })
    return ret


@bp.route('/', methods=['GET'])
def get_list():
    concepts = Concept.get_list()
    nodes = []
    edges = []

    for concept in concepts:
        nodes.append(build_nodes(concept))
        edges += build_edges(concept)

    return jsonify(elements={"nodes": nodes, "edges": edges})


@bp.route('/concepts/<id_>', methods=['GET'])
def get_concepts(id_):
    return jsonify(Concept.get_node(id_))


@bp.route('/concepts', methods=['POST'])
def add_concept():
    data = request.json
    c = Concept()
    c.name = data['name']
    c.brief = data['brief']
    c.content = data['content']
    if data['source_id']:
        from_ = Concept.get_node(data['source_id'])
        from_.relates.add(c)
        return jsonify(build_nodes(Concept.upsert(from_)))
    return jsonify(build_nodes(Concept.upsert(c)))


@bp.route('/concepts/<id_>', methods=['PUT'])
def update_concept(id_):
    data = request.json
    c = Concept.get_node(id_)
    c.name = data['name']
    c.brief = data['brief']
    c.content = data['content']
    return jsonify(build_nodes(Concept.upsert(c)))


@bp.route('/concepts/<id_>', methods=['DELETE'])
def del_concept(id_):
    return jsonify(Concept.delete(id_))


@bp.route('/relations', methods=['POST'])
def add_relations():
    from_ = Concept.get_node(request.args.get('source_id'))
    to = Concept.get_node(request.args.get('target_id'))
    from_.relates.add(to)
    return jsonify(build_nodes(Concept.upsert(from_)))


@bp.route('/relations', methods=['DELETE'])
def del_relations():
    from_ = Concept.get_node(request.args.get('source_id'))
    to = Concept.get_node(request.args.get('target_id'))
    from_.relates.remove(to)
    return jsonify(build_nodes(Concept.upsert(from_)))
