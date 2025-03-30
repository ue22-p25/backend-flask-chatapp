## step 01: use a SQL database

A lot is going on here:

### globals

- We import SQLAlchemy, that provides a full SQL toolkit and Object Relational Mapper (ORM) for Python.
- We configure Flask to use the DB located at `sqlite:///chat.db`
- We create a new database object, and its `session` attribute, that will allow us to interact with said DB

### endpoints

- We create a new endpoint `/db/alive` that will return a 200 OK response if the DB is alive
- Also we create a new endpoint `/api/version` that will return the version of
  the code (we will increment the global `VERSION` variable as we go along the
  steps)

### to try it out

```
http ://localhost:5000/db/alive
http ://localhost:5000/api/version
```
