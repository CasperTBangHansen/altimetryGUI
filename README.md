# Requirements
A static webapp on azure which has to be linked to a copy of this repository. Furthermore a PostgreSQL database has to be setup with the [PostGIS](https://postgis.net/) extensions.

## Environment variables
The environment variables are needed to make a connection to a PostgreSQL database.

| Environment variable                                  | Explanation                                                 |
|--------------------------------------|-------------------------------------------------------------|
| ALTIMETRY_USERNAME                   | Username for the database                                   |
| ALTIMETRY_PASSWORD                   | Password for the database                                   |
| ALTIMETRY_HOST                       | Hostname of the database                                    |
| ALTIMETRY_DATABASE_PORT              | Port of the database                                        |
| ALTIMETRY_DATABASE                   | Database name                                               |
| ALTIMETRY_DATABASE_CONNECTION_ENGINE | Engine to use for the connection (likely 'psycopg2')          |
| ALTIMETRY_DATABASE_TYPE              | Type of database (likely 'postgresql')                        |
| ALTIMETRY_CREATE_TABLES              | If the connection should create the tables ('true'/'false') |
| SALT                                 | For salting the password (Make sure it is compatiable with the bcrypt python package) |

# Suggestion
The following environment variables are optional but they are nice to have set the first time the database is setup. This is to make an admin account that can login and make new products/resolutions through the API.

| Environment variable                                  | Explanation                                                 |
|--------------------------------------|-------------------------------------------------------------|
| DEFAULT_USERNAME                   | Username for the API                                   |
| DEFAULT_PASSWORD                   | Password for the API of the default username                                   |
## Databases
If the tables in the database is not setup before running step 4 in the pipeline it is strongly recommended to set the environment variable ```ALTIMETRY_CREATE_TABLES='true'```.

# Pipeline
Make sure you have set the CI/CD pipeline correctly up for Azure Static Web Apps.