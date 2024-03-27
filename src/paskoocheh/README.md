# Paskoocheh

Paskoocheh is an open source platform which provides the internet users a set of tools to stay
anonymous or more secure while browsing the internet. The ultimate goal of this platform is
to increase transparency, encourage online privacy and facilitate access to the data.

## Running Django Locally

### 1 Backend

*Note 2018-01-08: this is probably very outdated, since it was written for Paskoocheh 2.0.*

#### 1.2 Setup
The backend engine is built on top of  [Django](https://www.djangoproject.com/) which we recommend to run it inside a
virtual environment. In order to install the dependencies, use <code>pip</code> command and read all the dependencies
from <code>requirements.txt</code> file:
```bash
pip install -r requirements.txt
```
#### 1.3 Structure
There are three main applications inside the project directory (listed below). In addition to the applications, logs
folder keeps application specific logs, `paskoocheh/middleware.py` holds middleware for translations and finally
locale keeps the translation files.

##### 1.3.1 tools
tools is the application which is responsible for each software packages (tool) presented on the website. It incorporates
many information including basic software info, frequently asked questions, download links, latest versions and etc.

##### 1.3.2 authentication
Authentication is responsible for user accounts. It helps the user to register/login/logout to the system as well as
receiving notification when a tool is updated.

##### 1.3.3 paskoocheh
Paskoocheh is the main application responsible for loading the whole project, defining url routes and project specific
settings.

### 2 Web frontend

The Paskoocheh 3.0 web frontend is implemented as a Django application (webfrontend). Requests that don’t match other parts of the site (e.g `/admin`, `/static`, `/media`, `/markdownx`, etc.) are passed to webfrontend.  For more details, read `webfrontend/README.markdown`.

### 3 Database

The primary Paskoocheh database is PostgreSQL.

#### 3.1 PostgreSQL
Apply the database schema and create a django app admin user
```bash
python manage.py migrate
python manage.py createsuperuser
```

### 4 Configuration
Configuration of sensitive secrets inside the app should be handled through environment variables

Save the following into a file named `environment`
```bash
export BUILD_ENV=<development|production>
export DATABASE_HOST=<host>
export DATABASE_USER=<username>
export DATABASE_PASSWORD=<password>
export DJANGO_SECRET_KEY=<secret key>
```

then run `source environment` to set the variables

### 5 Serving the application

#### 5.1 Local Development
Create and source an `env.sh` based on `env-sample.sh` (or an `env.fish` based on `env-sample.fish`). See the comments in the sample files for more details.

It’s also worth setting up a Python virtual environment to ensure your Python version (2.7) and packages match the production environment.

From the `server` directory:

```bash
python manage.py migrate
python manage.py runsslserver 0.0.0.0:8443
```

Note that you need to use the [runsslserver](https://github.com/teddziuba/django-sslserver) command. This is because cookies are set with the [`secure`](https://en.wikipedia.org/wiki/Secure_cookies) flag (which prevents access over HTTP), and the built-in `runserver` command doesn’t support HTTPS.


To run the app with `BUILD_ENV=production`, you also need to run the following command whenever a static asset changes:

```bash
python manage.py collectstatic --noinput
```

Note: As of 2017-07-13, only a few tools in the development fixtures have versions with associated screenshots:

- Betternet
- Open VPN for Android
- Psiphon
- Ghostery

In Paskoocheh v2, screenshots are associated with tools, not tool versions. In Paskoocheh v3, screenshots can be associated with tool versions, and the web front-end will only display tool version screenshots (not the existing tool screenshots). Most of the tools in the test data don’t have tool version screenshots yet – the above were updated for development purposes.
