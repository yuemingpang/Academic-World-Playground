### **Title:** Academic World Playground 

**Purpose:**  
The application is designed on top of 3 databases (SQL, MongoDB, Neo4j) related to academic records. It allows querying and updating the records through a dashboard. The target users are studnets who want to get familiar with academic world and see the photos of universities and faculties.  

**Objectives:**
- 1)be able to explore the statistics of input keywords;
- 2)be able to explore the statistics of certain publications;  
- 3)be able to view and update photos of universities and faculties;
- 4)utilize certain database techniques.  

**Demo:** https://mediaspace.illinois.edu/media/t/1_qrp43pv1

**Installation:** Just bare clone the app using: ```git clone --bare https://github.com/CS411DSO-SP23/YuemingPang.git``` 

**Usage:**  
Make sure all 3 databases are ready and connection information is correct. 
Then in your terminal, direct to the "app" folder and run: ```python3 app.py```. The address will be shown in your terminal. Copy the address and open it in your browser. Now you can interact with the dashboard.  

**Design:**  
The application contains 4 parts: SQL connection class, MongoDB connection class, Neo4j connection class, and the main dashboard app (layout and callbacks). There are totally 6 widgets in the dashboard:
  - 1)query top 5 universities by user input keyword. This is ranked by the number of faculty that relates to the keyword in each university.(Obj#1)  
  - 2)query top 5 keywords in a university specified by user. This is ranked by the number of faculty that relates to each keyword in that university.(Obj#1)  
  - 3)query top 5 publications by user input keyword. This is ranked by a score that is calulated by numCitations*keyword.score.(Obj#2)  
  - 4)query top 5 most cited publications published in specific year. This is ranked by numCitations. User will select the year when the publications were published.(Obj#2)  
  - 5)display or update the photo of an input university. Here we have 2 inputs which are the university name and the new photo URL.(Obj#3)  
  - 6)display or update the photo of an input faculty. Here we have 2 inputs which are the faculty name and the new photo URL.(Obj#3)  

**Implementation:**
  - SQL connection class: Pandas and mysql.connector are used. Define functions that can execute query 1), 2), 5), 6). Convert output into pandas dataframe and return.
  - MongoDB connection class: Pandas and pymongo are used. Define functions that can execute query 3). Convert output into pandas dataframe and return.
  - Neo4j connection class: Pandas and neo4j are used. Define functions that can execute query 4). Convert output into pandas dataframe and return.
  - Mainn dashboard app: Dash Plotly is used. Create 6 html widgets corresponding to the 6 components. To update the results according to user input, 6 callbacks function are defined. 3 objects of the connection classes are initialized to establish database connections. The callbacks will use these objects to call the corresponding query fucntions defined in the connection class.  

**Database Techniques:**
  - 1)Indexing: create index on the photo_url of university table to support query 5).This function is defined in the SQL connection class.(Obj#4)  
  - 2)View: create a view of university.name-faculty.id-keyword.name to support query 1) and 2). This function is defined in the SQL connection class.(Obj#4)  
  - 3)Trigger: create a trigger for updating the photo_url of university table to support query 5). This function is defined in the SQL connection class.(Obj#4)  

Extra-Credit Capabilities: N/A  

**Contributions:** Yueming Pang (about 40 hours)  
