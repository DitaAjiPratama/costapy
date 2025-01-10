python3 -m venv .venv                   # Create .venv

.venv/bin/pip3 install --upgrade pip    # Upgrade pip

.venv/bin/pip3 install bottle           # Micro Framework
.venv/bin/pip3 install gunicorn         # WSGI Server Backend
.venv/bin/pip3 install beaker           # Session & caching library
.venv/bin/pip3 install mako             # Template library

.venv/bin/pip3 install mysql-connector  # Database connector
.venv/bin/pip3 install bcrypt           # Password hash
.venv/bin/pip3 install pyjwt[crypto]    # JWT
.venv/bin/pip3 install requests         # For HTTP Request (Recaptcha need a POST HTTP requests)
