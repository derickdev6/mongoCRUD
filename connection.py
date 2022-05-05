import pymongo


def main():
    try:
        # Connecting to server
        CONNECTION_STRING = "mongodb://localhost:27017"
        client = pymongo.MongoClient(CONNECTION_STRING)

        # Selecting db
        mydb = client['SismosAntioquia']

        # Selecting collection
        col = mydb['Sismos']

        records = list(col.find())
        # print("Printing each row")
        # for row in records:
        #     print("Name: ", row[0])
        #     print("Title: ", row[1])
        #     print("\n")
        print(f"Items = {len(records)}")
        for row in records:
            print(row)

    except Exception as e:
        print("Database not created and Failed to Connect")
    finally:
        print("Program ended successfully")


if __name__ == '__main__':
    main()
