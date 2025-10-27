# orbitai_matcher_backend_

Deployment notes
----------------

This project exposes a package-level WSGI app object so production WSGI
servers can import the application directly using the module path. Use the
following Procfile entry when deploying with Gunicorn or platforms that expect
`<module>:<app>` semantics:

```
web: gunicorn app:app
```

If you previously used `gunicorn runserver:app` change it as shown above, or
ensure `runserver.py` exposes a top-level `app` variable. We added a package
level `app` in `app/__init__.py` so `gunicorn app:app` works by default.