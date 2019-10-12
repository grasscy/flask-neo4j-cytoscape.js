from py2neo import Graph
from app import Ccp

##连接neo4j数据库，输入地址、用户名、密码
graph = Graph('http://182.254.156.112:7474', username='neo4j', password='root1234')

c = Ccp.create(graph)
