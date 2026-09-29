def get_db():
    print("Create DB session")

    yield "DB session"

    print("Close DB session")
