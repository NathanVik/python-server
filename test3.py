#test for database access
from config import db

#db.users.insert_one({"name": "Nathan", "email": "nathan@email.com"})
#db.users.insert_one({"name": "admin", "email": "admin@email.com"})
#db.users.insert_one({"name": "Steve", "email": "steve@email.com"})


cursor = db.users.find({"name" : "Steve"})

for user in cursor:
    print(user)

