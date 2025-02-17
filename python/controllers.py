from python.model import SynopData, DecodedCSVData, session
import os

def extract_timestamp(filename):
    """Extracts the timestamp from filenames."""
    try:
        if filename.endswith('.csv'):
            # Extract timestamp from CSV filename (e.g., "2025021100.csv")
            return filename.split('.')[0]
        elif filename.endswith('syn.txt'):
            # Extract timestamp from Synop filename (e.g., "2025021100syn.txt")
            return filename.replace('syn.txt', '')
        else:
            raise ValueError(f"Unsupported file format for filename: {filename}")
    except Exception as e:
        raise ValueError(f"Error extracting timestamp from filename: {filename}. Details: {e}")

def store_synop_data(filepath):
    """Stores decoded Synop data in the SynopData table with timestamp, avoiding duplicates."""
    filename = os.path.basename(filepath)
    timestamp = extract_timestamp(filename)

    # Check if the file already exists in the database
    existing_record = session.query(SynopData).filter_by(filename=filename, timestamp=timestamp).first()
    
    if existing_record:
        print(f"Synop data '{filename}' already exists in the database. Skipping insert.")
        return  # Skip inserting duplicate data

    with open(filepath, 'rb') as file:
        synop_record = SynopData(
            filename=filename,
            file_content=file.read(),
            timestamp=timestamp
        )
        session.add(synop_record)
        session.commit()
        print(f"Synop data from '{filename}' stored successfully with timestamp '{timestamp}'.")


def store_csv_data(filepath):
    """Stores decoded CSV data in the DecodedCSVData table with timestamp, avoiding duplicates."""
    filename = os.path.basename(filepath)
    timestamp = extract_timestamp(filename)

    # Check if the file already exists in the database
    existing_record = session.query(DecodedCSVData).filter_by(filename=filename, timestamp=timestamp).first()
    
    if existing_record:
        print(f"CSV data '{filename}' already exists in the database. Skipping insert.")
        return  # Skip inserting duplicate data

    with open(filepath, 'rb') as file:
        csv_record = DecodedCSVData(
            filename=filename,
            file_content=file.read(),
            timestamp=timestamp
        )
        session.add(csv_record)
        session.commit()
        print(f"CSV data from '{filename}' stored successfully with timestamp '{timestamp}'.")

# def store_contours_data(filepath):
#     """Stores metadata of contours data in the ContoursData table."""
#     import shutil

#     filename = os.path.basename(filepath)
#     timestamp = extract_timestamp(filename)
#     destination_folder = "contours_files"  # Folder to store contours files
#     os.makedirs(destination_folder, exist_ok=True)
    
#     # Copy file to destination folder
#     destination_path = os.path.join(destination_folder, filename)
#     shutil.copy(filepath, destination_path)

#     # Save metadata in database
#     contours_record = ContoursData(
#         filename=filename,
#         file_path=destination_path,
#         timestamp=timestamp
#     )
#     session.add(contours_record)
#     session.commit()
#     print(f"Contours data from '{filename}' stored successfully with timestamp '{timestamp}'.")
