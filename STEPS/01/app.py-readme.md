## use a SQL database

Let's start with empowering our Flask app with a SQL database.

This is only boilerplate code, but it's central to the rest of the steps.

### globals

- We import SQLAlchemy, that provides a full SQL toolkit and Object Relational Mapper (ORM) for Python.
- We configure Flask to use the DB located at `sqlite:///chat.db`
- We create a new database object, and its `session` attribute, that will allow us to interact with said DB
