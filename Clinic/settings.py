HEROKU = False

if HEROKU:
    from .settings_heroku import *
else:
    from .settings_local import *