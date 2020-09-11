use admin
db.createUser(
  {
      user: "admin",
      pwd: "password", 
      roles: [ { role: "userAdminAnyDatabase", db: "admin" }, "readWriteAnyDatabase" ]
  }
)

use dev
db.createUser(
  {
      user: "dev",
      pwd: "dev", 
      roles: [ { role: "readWrite", db: "dev" } ]
  }
)


