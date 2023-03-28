from neo4j import GraphDatabase
import pandas as pd

class connectNeo4j:
  def __init__(self):
    self.URI = "bolt://localhost:7687"
    self.AUTH = ("neo4j", "password@CS411")

  #4 Neo4j top 5 publication by citation#
  def widgetFour(self, year):
    driver = GraphDatabase.driver(self.URI, auth=self.AUTH)
    with driver.session(database="academicworld") as session:
      record = session.execute_read(self.helper, year=year)
    df = pd.DataFrame(record)
    session.close()
    driver.close()
    df.rename(columns={0: 'title', 1: 'citation#'}, inplace=True)
    return df
    
  @staticmethod
  def helper(tx, year):
    query = "MATCH (p:PUBLICATION {year: $year}) RETURN p.title, p.numCitations ORDER BY p.numCitations DESC LIMIT 5"
    result = tx.run(query, year=year)
    output = list(result)
    return output
  