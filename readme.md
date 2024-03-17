# SQL-Faker : Data Generator

This Python script generates mock data using the Mimesis library and inserts it into a SQL database. It's particularly useful for populating databases with sample data for testing or development purposes.

## Requirements

- Python 3.x
- pandas
- pymssql
- sqlalchemy
- mimesis
- dotenv

## Installation

1. Clone this repository.
2. Install the required dependencies using `pip install -r requirements.txt`.
3. Set up a `.env` file following the provided `.env.example`.

## Configuration

Before running the script, make sure to configure the `.env` file with appropriate values for your database connection.

- `CONNECTION_STRING`: Connection string for your SQL database.
- `ROWS`: Number of rows of mock data to generate.
- `INSERT_LIMIT`: Maximum number of rows to insert in a single transaction.
- `TABLE_NAME`: Name of the table in your database to insert the data.

## Usage

Run the script using the command:

```bash
python main.py
```

The script will generate mock data according to the configuration specified in the `.env` file and insert it into the specified table in your SQL database.

## Logging

The script logs its activity to both the console

## License

This project is licensed under the MIT License - see the `LICENSE` file for details.