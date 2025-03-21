import os
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import EncryptedType

# In a production environment, store your encryption key securely (e.g., in an environment variable)
SECRET_KEY = os.getenv("DATABASE_ENCRYPTION_KEY", "mysecretkey1234567")

Base = declarative_base()

class Data(Base):
    """
    Data model with encrypted 'content' field.
    The content is stored encrypted in the database.
    """
    __tablename__ = 'data'
    id = Column(Integer, primary_key=True)
    content = Column(EncryptedType(String, SECRET_KEY), nullable=False)

# Create the SQLite engine (or change the URL to match your SQL database)
engine = create_engine("sqlite:///data.db", echo=True)

# Create all tables (if they don't already exist)
Base.metadata.create_all(engine)

# Create a configured "Session" class
Session = sessionmaker(bind=engine)

def add_data(content: str) -> int:
    """
    Adds a new data record with encrypted content.
    
    @param content: The string data to be stored (will be encrypted).
    @return: The ID of the newly added record.
    """
    session = Session()
    data_entry = Data(content=content)
    session.add(data_entry)
    session.commit()
    session.close()
    return data_entry.id

def get_data(data_id: int) -> Data:
    """
    Retrieves a data record by its ID.
    
    @param data_id: The ID of the data record.
    @return: The retrieved Data object or None if not found.
    """
    session = Session()
    data_entry = session.query(Data).filter(Data.id == data_id).first()
    session.close()
    return data_entry

def update_data(data_id: int, new_content: str) -> Data:
    """
    Updates the encrypted content of a data record.
    
    @param data_id: The ID of the data record.
    @param new_content: The new content to be encrypted and stored.
    @return: The updated Data object or None if not found.
    """
    session = Session()
    data_entry = session.query(Data).filter(Data.id == data_id).first()
    if data_entry:
        data_entry.content = new_content
        session.commit()
    session.close()
    return data_entry

def delete_data(data_id: int) -> bool:
    """
    Deletes a data record by its ID.
    
    @param data_id: The ID of the data record.
    @return: True if deletion was successful, False otherwise.
    """
    session = Session()
    data_entry = session.query(Data).filter(Data.id == data_id).first()
    if data_entry:
        session.delete(data_entry)
        session.commit()
        session.close()
        return True
    session.close()
    return False

# Example usage (for testing purposes)
if __name__ == "__main__":
    # Add a record
    new_id = add_data("Sensitive information")
    print(f"Data added with ID: {new_id}")

    # Retrieve the record
    record = get_data(new_id)
    print("Retrieved record:", record.id, record.content)

    # Update the record
    updated = update_data(new_id, "Updated sensitive information")
    print("Updated record content:", updated.content)

    # Delete the record
    if delete_data(new_id):
        print(f"Record {new_id} deleted successfully.")
    else:
        print(f"Failed to delete record {new_id}.")