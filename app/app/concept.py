from py2neo.ogm import GraphObject, Property, RelatedTo
from flask import g


class Concept(GraphObject):
    name = Property()
    brief = Property()
    content = Property()

    relates = RelatedTo('Concept')

    @staticmethod
    def delete(id_: int):
        concept = Concept.get_node(id_)
        return g.db.delete(concept)

    @staticmethod
    def upsert(concept):
        g.db.push(concept)
        return concept

    def walk(self):
        pass

    @staticmethod
    def get_list():
        return list(Concept.match(g.db))

    @staticmethod
    def get_node(id_: int):
        return Concept.match(g.db, int(id_)).first()
