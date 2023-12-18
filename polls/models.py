import os, datetime
from neo4j import GraphDatabase
from decouple import config


class Neo4jCRUDOperations:
    def __init__(self):
        None
    
    def connect(self):
        print(config('LOCAL_BOLT_URI'))
        print(config('LOCAL_NEO4J_USERNAME'))
        print(config('LOCAL_NEO4J_PASSWORD'))
        self._driver = GraphDatabase.driver(config('LOCAL_BOLT_URI')
                                            , auth=(config('LOCAL_NEO4J_USERNAME')
                                            , config('LOCAL_NEO4J_PASSWORD')))

    def close(self):
        if self._driver is not None:
            self._driver.close()

    def get_question_by_id(self, id):
        with self._driver.session() as session:
            result = session.read_transaction(self._get_question_by_id, id)
            if result:
                return result[0]['q']
            else:
                return None
    
    def get_choice_by_id(self, id):
        with self._driver.session() as session:
            result = session.read_transaction(self._get_choice_by_id, id)
            if result:
                return result[0]['c']
            else:
                return None
    
    def get_latest_questions(self, num):
        with self._driver.session() as session:
            results = session.read_transaction(self._get_latest_questions, num)
            if results:
                list = []
                for result in results:
                    list.append(result['q'])
                return list
            else:
                return None
    
    def get_latest_choices(self, num):
        with self._driver.session() as session:
            results = session.read_transaction(self._get_latest_choices, num)
            if results:
                list = []
                for result in results:
                    list.append(result['c'])
                return list
            else:
                return None
    
    def create_question(self, text):
        with self._driver.session() as session:
            last_questions = session.read_transaction(self._get_latest_questions, 1)
            id = 1
            if last_questions:
                id = int(last_questions[0]['q']['id']) + 1
            result = session.write_transaction(self._create_question, id, text)
            if result:
                return result[0]['q']
            return None
    
    def add_choice_to_question(self, question_id, text):
        with self._driver.session() as session:
            last_choices = session.read_transaction(self._get_latest_choices, 1)
            id = 1
            if last_choices:
                id = last_choices[0]['c']['id'] + 1
            result = session.write_transaction(self._add_choice_to_question, question_id, id, text)
            if result:
                return result[0]['c']
            return None

    def get_choices_by_question_id(self, question_id):
        with self._driver.session() as session:
            results = session.read_transaction(self._get_choices_by_question_id, question_id)
            if results:
                list = []
                for result in results:
                    list.append(result['c'])
                return list
            else:
                return None
    
    def add_votes_to_choice(self, id, votes):
        with self._driver.session() as session:
            results = session.write_transaction(self._add_votes_to_choice, id, votes)
            if results:
                return results[0]['c']
            return None
    
    @staticmethod
    def _get_question_by_id(tx, id):
        result = tx.run("MATCH (q:Question {id: $id}) RETURN q", id=id)
        return result.data()
    
    @staticmethod
    def _get_choice_by_id(tx, id):
        result = tx.run("MATCH (c:Choice {id: $id}) RETURN c", id=id)
        return result.data()


    @staticmethod
    def _get_latest_questions(tx, num):
        result = tx.run("MATCH (q:Question) RETURN q ORDER BY q.id DESC LIMIT $num" , num=num)
        return result.data()
    
    @staticmethod
    def _get_latest_choices(tx, num):
        result = tx.run("MATCH (c:Choice) RETURN c ORDER BY c.id DESC LIMIT $num" , num=num)
        return result.data()
    
    @staticmethod
    def _create_question(tx, id, text):
        pub_date = datetime.datetime.now()  
        result = tx.run("CREATE (q:Question {id: $id, text: $text, pub_date:$pub_date}) RETURN q" , id=id, text=text, pub_date=pub_date)
        return result.data()

    @staticmethod
    def _add_choice_to_question(tx, question_id, id, text):
        pub_date = datetime.datetime.now()  
        result = tx.run("MATCH (q:Question {id: $question_id}) CREATE (q)-[:HAS_CHOICE]->(c:Choice {id: $id,text:$text,pub_date:$pub_date,votes:0}) RETURN c", question_id=question_id, id=id, text=text, pub_date=pub_date)
        return result.data()
    
    @staticmethod
    def _get_choices_by_question_id(tx, id):
        result = tx.run("MATCH (c:Choice)<-[:HAS_CHOICE]-(q:Question {id:$id}) RETURN c" , id=id)
        return result.data()
    


    #DEBUG THIS - code doesn't increment but cypher command underneath works with variables
    @staticmethod
    def _add_votes_to_choice(tx, id, votes):
        cypher_query = "MATCH (c:Choice) WHERE c.id = $id SET c.votes = c.votes + $votes RETURN c"
        result = tx.run(cypher_query, {"id": int(id), "votes": int(votes)})
        return result.data()


'''
    def delete_node(self, label, properties):
        with self._driver.session() as session:
            session.write_transaction(self._delete_node, label, properties)

    @staticmethod
    def _delete_node(tx, label, properties):
        query = f"MATCH (n:{label} $properties) DELETE n"
        tx.run(query, properties=properties)

'''