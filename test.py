from python.model import SynopData,DecodedCSVData, session
import os

def retrieve_small_file(file_id, output_dir='retrieved_files'):
    """Retrieves a small file from the database and saves it to the output directory."""
    os.makedirs(output_dir, exist_ok=True)
    file_data = session.query(DecodedCSVData).filter_by(timestamp=file_id).first()
    if file_data:
        output_path = os.path.join(output_dir, file_data.filename)
        with open(output_path, 'wb') as file:
            file.write(file_data.file_content)
        print(f"Small file '{file_data.filename}' retrieved and saved to '{output_path}'.")
    else:
        print(f"No small file found with ID: {file_id}.")

retrieve_small_file(file_id='2025021103')