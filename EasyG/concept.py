from py2neo.ogm import GraphObject, Property, RelatedTo
from EasyG import db


class Concept(GraphObject):
    name = Property()
    relates = RelatedTo('Concept')

    def add(self):
        return db.push_node(self)

    def delete(self):
        return db.del_node(self)

    def update(self):
        return db.push_node(self);

    def walk(self):
        return db.walk(self)


#
# from py2neo import Graph, Node, Relationship
#
# ##连接neo4j数据库，输入地址、用户名、密码
graph = Graph('http://182.254.156.112:7474', username='neo4j', password='root1234')
# # tx = graph.begin()
# # c1 = Concept()
# # c1.name = 'hw'
# # tx.create(c1)
# #
# # tx.commit()
# rs = Concept.match(graph).first()
# print(rs)


from EasyG.concept import Concept

c1 = Concept()
db.push_node(c1)
