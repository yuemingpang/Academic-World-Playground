import mysql.connector
from mysql.connector import errorcode
import pandas as pd

class connectSQL:
  def __init__(self):
    self.user = 'root'
    self.password = 'password@CS411'
    self.host = '127.0.0.1'
    self.database = 'academicworld'

  def connect(self):
    try:
      cnx = mysql.connector.connect(user=self.user, password=self.password,
                                        host=self.host, database=self.database)

    except mysql.connector.Error as err:
      if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
      elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
      else:
        print(err)
    else:
      return cnx

  # create the index on university photo URL
  def index(self):
    cnx = self.connect()
    cursor = cnx.cursor()
    cursor.execute("DROP INDEX myindex ON academicworld.university")
    query = "CREATE INDEX myindex ON university(photo_url)"
    cursor.execute(query)
    cnx.commit()
    cursor.close()
    cnx.close()

  # create the view on university-faculty-keyword 
  def view(self):
    cnx = self.connect()
    cursor = cnx.cursor()
    cursor.execute("DROP VIEW IF EXISTS myview")
    query = "CREATE VIEW myview AS SELECT university.name AS school, faculty.id AS fid, keyword.name AS keyword FROM university, faculty, faculty_keyword, keyword WHERE university.id=faculty.university_id AND keyword.id=faculty_keyword.keyword_id AND faculty.id=faculty_keyword.faculty_id"
    cursor.execute(query)
    cnx.commit()
    cursor.close()
    cnx.close()

  #create the trigger when updating university URL 
  def trigger(self):
    cnx = self.connect()
    cursor = cnx.cursor()
    cursor.execute("DROP TRIGGER IF EXISTS mytrigger")
    data = ("https://www.freecodecamp.org/news/content/images/size/w2000/2020/08/Untitled-design-1-.png",)
    query = "CREATE TRIGGER mytrigger BEFORE UPDATE ON university FOR EACH ROW BEGIN IF NEW.photo_url = OLD.photo_url THEN SET NEW.photo_url = %s; END IF; END"
    cursor.execute(query, data)
    cnx.commit()
    cursor.close()
    cnx.close()
    
  #1 SQL top 5 universities by its # of faculty associated (contain not exact mactch) with input keywords
  def widgetOne(self, keyword):
    query = "SELECT school, COUNT(DISTINCT fid) AS count FROM myview WHERE keyword LIKE %s GROUP BY school ORDER BY count DESC LIMIT 5"
    data = ('%'+ str(keyword) +'%',)
    cnx = self.connect()
    df = pd.read_sql(query, con=cnx, params=data)
    cnx.close()
    return df

  #2 SQL top 5 faculty keywords in a University
  def widgetTwo(self, name):
    query = "SELECT keyword, COUNT(DISTINCT fid) AS count FROM myview WHERE school=%s GROUP BY keyword ORDER BY count DESC LIMIT 5"
    data = (name,)
    cnx = self.connect()
    df = pd.read_sql(query, con=cnx, params=data)
    cnx.close()
    return df

  #5 SQL update university photo URL
  def widgetUpdateFive(self, name, url):
    if url=='None':
      return 
    cnx = self.connect()
    cursor = cnx.cursor()
    query = "UPDATE university SET photo_url=%s WHERE university.name=%s"
    data = (url, name)
    cursor.execute(query, data)
    cnx.commit()
    cursor.close()
    cnx.close()
  #5 SQL display university photo
  def widgetFive(self, name):
    query = "SELECT photo_url FROM university WHERE university.name=%s"
    data = (name,)
    cnx = self.connect()
    df = pd.read_sql(query, con=cnx, params=data)
    cnx.close()
    return df['photo_url'].values[0]

  #6 SQL update faculty photo URL
  def widgetUpdateSix(self, name, url):
    if url=='None':
      return 
    cnx = self.connect()
    cursor = cnx.cursor()
    query = "UPDATE faculty SET photo_url=%s WHERE faculty.name=%s"
    data = (url, name)
    cursor.execute(query, data)
    cnx.commit()
    cursor.close()
    cnx.close()
  #6 SQL display faculty photo
  def widgetSix(self, name):
    query = "SELECT photo_url FROM faculty WHERE faculty.name=%s"
    data = (name,)
    cnx = self.connect()
    df = pd.read_sql(query, con=cnx, params=data)
    cnx.close()
    return df['photo_url'].values[0]
