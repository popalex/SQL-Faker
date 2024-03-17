import logging
import random

import pandas as pd
import pymssql
import sqlalchemy
from dotenv import dotenv_values
from mimesis import Address, Datetime, Person
from mimesis.enums import Gender
from sqlalchemy import create_engine

# Load environment variables
config = dotenv_values(".env")

# # Configure logging to both console and file
logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
rootLogger = logging.getLogger()
rootLogger.setLevel(logging.INFO)

# fileHandler = logging.FileHandler("{0}/{1}.log".format(logPath, fileName))
# fileHandler.setFormatter(logFormatter)
# rootLogger.addHandler(fileHandler)

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
rootLogger.addHandler(consoleHandler)


def create_rows_mimesis(num=1):
    gender = random.choice([Gender.FEMALE, Gender.MALE])
    output = [{"first_name": person.first_name(gender),
               "last_name": person.last_name(gender),
               "address": address.address(),
            #    "name": person.name(),
               "email": person.email(),
               "city": address.city(),
               "state": address.state(),
               "date_time": datetime.datetime(),
               "randomdata": random.randint(1000, 2000)
               } for x in range(num)]
    return output


try:
    # Create SQLAlchemy engine
    engine = create_engine(config["CONNECTION_STRING"])

    # Connect to the database
    with engine.connect() as conn:
        # Log engine info
        logging.info(f"Connected to database: {engine}")

        # Initialize mimesis objects
        person = Person('en')
        address = Address()
        datetime = Datetime()

        num_rows = int(config["ROWS"])
        rows_per_batch=int(config["INSERT_LIMIT"])
        logging.info(f"Generating {num_rows} rows")

        # Check if num_rows is greater than 1000 (INSERT_LIMIT)
        if num_rows > rows_per_batch:
            # Insert data in batches of 1000 rows
            for i in range(0, num_rows, rows_per_batch):
                batch_df = pd.DataFrame(create_rows_mimesis(min(1000, num_rows - i)))
                batch_df.to_sql(config["TABLE_NAME"], engine, method='multi', index=False, if_exists='append')
                logging.info(f"Inserted {min(1000, num_rows - i)} rows into table: {config['TABLE_NAME']}")
        else:
            # Create DataFrame with mimesis-generated data
            df = pd.DataFrame(create_rows_mimesis(num_rows))
            # Write DataFrame to SQL database
            df.to_sql(config["TABLE_NAME"], engine, method='multi', index=False, if_exists='replace')
            logging.info(f"Inserted {num_rows} rows into table: {config['TABLE_NAME']}")

        conn.commit()
    
except Exception as e:
    # Log exception if any error occurs
    logging.error(f"An error occurred: {str(e)}")
    
# Log connection closure
logging.info("Database connection closed.")
