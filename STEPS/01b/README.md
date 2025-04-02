## step 01b: first endpoint

### endpoints

- We create a new endpoint `/db/alive` that will return a 200 OK response if the DB is alive

This triggers the minimal SQL code, just to make sure we can reach the DB; think of it as a "Hello world" for the DB

### to try it out

in all the rest we assume you run the Flask server on port 5001  

```bash
http ://localhost:5000/db/alive
```

### Note for windows users

It seems that the `http` command, when run on "Git Bash" for Windows, triggers an error:

> Request body (from stdin, –raw or a file) and request data (key=value) cannot be mixed. Pass –ignore-stdin to let key/value take priority

In that case, take the message at face value, and add the `-I` (shorthand for `--ignore-stdin`) option to the command:

```bash
http -I ://localhost:5000/db/alive
```

**Tip**: to continue using the same sentence (i.e. without the `-I`), you might be able to trick bash and define an alias

```bash
alias http='\http -I'
```
