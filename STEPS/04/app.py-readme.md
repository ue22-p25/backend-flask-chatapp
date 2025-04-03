## Step 04: serve a basic frontend

In this move we add in the mix the first seed of the app frontend

### new files

a HTML template, and a CSS file, see below

### new endpoint

And we also add a dedicated endpoint `/front/users` that will serve this page; the way it is intended to work is:

1. you direct your browser to `http://localhost:5001/front/users`
1. which will call the `/api/users` endpoint
1. which in turn will retrieve all users from the DB
1. and pass that list to the new **Jinja2 template** (the .j2 file)
1. that will create one custom HTML element per user
1. and return the full HTML page - with all users - back to the browser

### new imports

We need:

- `render_template` to render the Jinja2 template;
- `requests` to call the `/api/users` endpoint

### keeping the app modular

Step #3 deserves a few more words; to retrieve all user details, we have a choice between:

- asking the database directly
- or forwarding the request to the `/api/users` endpoint

We have gone for the latter option, as it is more in line with the micro-services philosophy  
The idea is that even though our current deployment runs in a single Flask app,
we want to be able to **deploy it in more distributed way**, with the services for
- the database
- the `/front/`
- and the `/api/` endpoints

all running in different containers/computers

Also note that this way of doing things is SSR (Server-Side rendering); relying
on the API to implement this endpointmakes it more likely for us move to CSR
(Client-Side rendering) in the future if need be.
