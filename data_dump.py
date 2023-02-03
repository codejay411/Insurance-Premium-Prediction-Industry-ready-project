import pymongo
import pandas as pd
import json

client = pymongo.MongoClient("mongodb+srv://codejay:codejay1234@cluster0.kgzne.mongodb.net/?retryWrites=true&w=majority")
db = client.test

DATA_FILE_PATH = (r"C:\jay\Data Science Project\Insurance-Premium-Prediction-Industry-ready-project\insurance.csv")
DATABASE_NAME = "Insurance"
COLLECTION_NAME = "Insurance_project"

if __name__ == "__main__":
    df = pd.read_csv(DATA_FILE_PATH)
    print(f"Rows and columns: {df.shape}")

    df.reset_index(drop=True, inplace=True)

    json_record = list(json.loads(df.T.to_json()).values())
    print(json_record[0])

    client[DATABASE_NAME][COLLECTION_NAME].insert_many(json_record)
    print("Data insertion in database complete.")