import os

# Must be set before importing app.database, which initializes the engine.
os.environ.setdefault("TESTING", "true")
