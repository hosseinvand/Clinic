HEROKU = True

if HEROKU:
    from .settings_heroku import *
else:
    from .settings_local import *