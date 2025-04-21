# Hospital Scan Report Portal

A Streamlit application for managing hospital scan reports.

## Features

- Register new scan reports with patient information
- Upload and store scan images
- View all scan reports in a searchable table
- Search for reports by patient name
- Export reports as CSV

## Deployment Options

This application is designed to be deployable to various cloud platforms:

### Streamlit Cloud

1. Create a Streamlit account at [streamlit.io](https://streamlit.io)
2. Connect your GitHub repository
3. Deploy the app directly from the repository

### Heroku

1. Create a Heroku account and install the Heroku CLI
2. Initialize a git repository and commit all files
3. Create a new Heroku app: `heroku create your-app-name`
4. Add a PostgreSQL database: `heroku addons:create heroku-postgresql:hobby-dev`
5. Deploy to Heroku: `git push heroku main`

### Railway

1. Create a Railway account at [railway.app](https://railway.app)
2. Create a new project from GitHub
3. Add a PostgreSQL database service
4. Configure the environment variables in the Railway dashboard
5. Deploy the application

## Environment Variables

Create a `.env` file based on the `.env.example` template and set the following variables:

- `DATABASE_URL`: Connection string for your database
- `STORAGE_MODE`: Set to "local" or "s3" for file storage
- Additional variables based on your chosen storage provider

## Local Development

1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the environment:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Run the app: `streamlit run app.py`

## Database Migration

When deploying to a cloud platform, you may need to migrate your data from SQLite to PostgreSQL. Use the following steps:

1. Export your SQLite data: `sqlite3 scan_reports.db .dump > database_dump.sql`
2. Convert the SQL syntax to be PostgreSQL compatible
3. Import to PostgreSQL: `psql -d your_postgres_db -f converted_dump.sql`

Alternatively, use the built-in pandas integration to export/import your data.