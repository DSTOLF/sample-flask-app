# Sample Flask App

This is a sample Flask App that's intended to be easily configured and extended, with a dynamic data model in [yaml format](./models.yaml).

The [model file](./models.yaml) is a list of tables and it's corresponding columns, defined with data types, data size and and additional `doc` attribute, which can configured with a Faker algorithm in the format of `<algorithm name>-<locale>`. Please check the Faker [documentation](https://faker.readthedocs.io/en/master/locales.html) for additional details about supported algorithms and locales.

Once you have the [model file](./models.yaml) customized to your specific needs, just run the migrations files and it will take care of creating the data model and populating it with fake data.

Note: if you have a Postgres database ready to use, first edit the [environment file](./.env.python) and
```
source .env.file
```

If you don't have a Postgres database ready and just want to run some quick test, just edit the [config file](./config.py), comment the Postgres connection string and uncomment the Sqlite connection string like this:
```
SQLALCHEMY_DATABASE_URI = ('sqlite:///teste.db')
# SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://{}:{}@{}:{}/{}".format(database_user,database_password,database_host,database_port,database_name)
```

When you are ready, you can either run your own [custom migration](./migrations_custom.py)
```
python3 migrations_custom.py
```

Or run a fully automated migration with [fake data](./migrations_faker.py) based on what you defined in `models.yaml`
```
python3 migrations_faker.py
```

Once you have the data generated, just run the app and visit the the Flask Admin web app on `http://127.0.0.1:5000/admin/` to easily view, edit and create data: 
```
source .env.file
python3 app.py
```