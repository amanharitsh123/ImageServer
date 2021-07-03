import os
from neo4j import GraphDatabase

class Neo4jConnection:
    
    def __init__(self, uri, user, pwd):
        self.__uri = uri
        self.__user = user
        self.__pwd = pwd
        self.__driver = None
        try:
            self.__driver = GraphDatabase.driver(self.__uri, auth=(self.__user, self.__pwd))
        except Exception as e:
            print("Failed to create the driver:", e)
        
    def close(self):
        if self.__driver is not None:
            self.__driver.close()
        
    def query(self, query, db=None):
        assert self.__driver is not None, "Driver not initialized!"
        session = None
        response = None
        try: 
            session = self.__driver.session(database=db) if db is not None else self.__driver.session() 
            response = list(session.run(query))
        except Exception as e:
            print("Query failed:", e)
        finally: 
            if session is not None:
                session.close()
        return response

class DB:
    def __init__(self):
        self.uri = "bolt://"+os.environ['NEO_HOST']+":7687"
        self.username = os.environ['NEO_USER']
        self.password = os.environ['NEO_PASS']
        self.checkNode = "MATCH (j:Person {name:'%s'}) return j;"
        self.makeNode = "CREATE (j:Person {name: '%s'});"
        self.addFriend = "MATCH (p1: Person), (p2: Person) WHERE p1.name = '%s' AND p2.name = '%s' CREATE (p1)-[rel:IS_FRIENDS_WITH]->(p2);"
        self.checkFriend = "MATCH (j:Person {name:'%s'})-[rel:IS_FRIENDS_WITH]-(m:Person {name: '%s'}) return j;"
        self.conn = Neo4jConnection(uri=self.uri, user=self.username, pwd=self.password)
        self.db = "neo4j"
    
    def ifFriend(self, person1, person2):
        res = self.conn.query(self.checkFriend%(person1, person2), db=self.db)
        return len(res)!=0
    
    def ifNode(self, name):
        res = self.conn.query(self.checkNode%(name), db=self.db)
        if not res:
            self.conn.query(self.makeNode%name)
            print("Node created successfully")
            return
        print("Node already exist")
    
    def makeFriend(self, person1, person2):
        self.ifNode(person1)
        self.ifNode(person2)
        if self.ifFriend(person1, person2):
            print("Already friends")
            return
        res = self.conn.query(self.addFriend%(person1, person2), db=self.db)
        print("Added friend Sucessfully")


# Test Code
obj = DB()
obj.ifFriend("a", "c")
obj.makeFriend("a", "c")
obj.ifFriend("a", "c")