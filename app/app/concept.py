from py2neo.ogm import GraphObject, Property, RelatedTo, Label, GraphObjectMatcher, NodeMatcher
from flask import g


class Concept(GraphObject):
    name = Property()
    brief = Property()
    content = Property()
    label = Property()

    relates = RelatedTo('Concept')

    @classmethod
    def delete(self, id_: int):
        concept = Concept.get_node(id_)
        return g.db.delete(concept)

    @classmethod
    def upsert(self, concept):
        g.db.push(concept)
        return concept

    @classmethod
    def get_list(self, label):
        return list(Concept.match(g.db).where(label=label))

    @classmethod
    def get_node(self, id_: int):
        return Concept.match(g.db, int(id_)).first()
