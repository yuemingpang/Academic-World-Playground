from pymongo import MongoClient
import pandas as pd

class connectMongo:
  def __init__(self):
    self.path = "mongodb://127.0.0.1:27017"

  #3 MongoDB top 5 publications keywords by score (citation*score)
  def widgetThree(self, input='database system'):
    query = [
      {"$unwind": "$keywords"},
      {"$match": {"keywords.name": input}},
      {"$project": {"_id": 0, "title": 1, "score": {"$multiply": ["$numCitations", "$keywords.score"]}}},
      {"$sort": {"score":-1}},
      {"$limit": 5}
    ]
    client = MongoClient(self.path)
    database = client['academicworld']
    collection = database['publications']
    data = collection.aggregate(query)
    df = pd.DataFrame(data)
    client.close()
    return df


  