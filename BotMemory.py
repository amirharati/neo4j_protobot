"""
  A wrapper class to interface with neo4j graph database.
  The interface is acting as "memory".
"""

from neo4jrestclient.client import GraphDatabase
from neo4jrestclient import client


class BotMemory:
    """
        Simple wrapper class.
        allows to add to memory.
        perform simple inference.
    """
    def __init__(self, db_user, db_pass, host="http://localhost:7474"):
        # connect to the database.
        self.db = GraphDatabase(host,
                                username=db_user,
                                password=db_pass)

    def memorize_restaurant_facts(self, name, cuisine=None, location=None):
        """
           A method to memorize facts related to restaurants
        """
        n = self._add_node(name, "restaurant_name")
        if cuisine not None:
            c = self._add_node(cuisine, "cuisine")
            n.relationship.create("is_a", c)
        if location not None:
            l = self._add_node(location, "location")
            n.relationship.create("located", l)

    def memorize_user_facts(self, name, cuisine=None, location=None):
        """
           A method to memorize facts about user.
        """
        n = self._add_node(name, "user_name")
        if cuisine not None:
            c = self._add_node(cuisine, "cuisine")
            n.relationship.create("likes", c)
        if location not None:
            l = self._add_node(location, "location")
            n.relationship.create("located", l)

    def clear_memory(self):
        q = "MATCH (n:user_name) DELETE n"
        results = self.db.query(q, returns=(client.Node, str, client.Node))
        q = "MATCH (n:restaurant_name) DELETE n"
        results = self.db.query(q, returns=(client.Node, str, client.Node))
        q = "MATCH (n:cuisine) DELETE n"
        results = self.db.query(q, returns=(client.Node, str, client.Node))
        q = "MATCH (n:location) DELETE n"
        results = self.db.query(q, returns=(client.Node, str, client.Node))

    def _memorize(self, entity1, entity2, rel):
        e1 = self._add_node(entity1['name'], entity1['type'])
        e2 = self._add_node(entity2['name'], entity2['type'])
        # create a relationship
        # BUG: can create multiple links
        e1.relationships.create(rel, e2)

    def _add_node(self, node_name, node_type):
        """
            add a node if not existed.
            and return the node.
        """
        q = 'MATCH (r:' + node_type + ') WHERE r.name="' \
            + node_name + '" RETURN r'
        results = self.db.query(q, returns=(client.Node, str, client.Node))
        res = self.db.labels.create(node_type)

        if (len(results) == 0):
            r = self.db.nodes.create(name=node_name)
            res.add(r)
        else:
            r = results[0][0]
        return r



    #def reterive(self, ...):
    # need to be generic. For example in this case we want to incorprate
    # location and cusine for a user but generally not sure
