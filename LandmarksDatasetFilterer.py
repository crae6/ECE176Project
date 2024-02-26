import csv
import requests
from pathlib import Path

# Define the directory where you want to save the images
data_dir = Path('data')
data_dir.mkdir(exist_ok=True)

# Path to your original CSV file
csv_file_path = 'train.csv'

# New CSV file to track downloads
downloaded_images_csv = data_dir / 'downloaded_images.csv'

def download_image(url, filepath):
    headers = {
        'User-Agent': 'ECE176LandmarkFilterer/1.0 (carae@ucsd.edu)'  # Replace with your app name and email
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raises an HTTPError if the response status code is 4XX/5XX
        with open(filepath, 'wb') as f:
            f.write(response.content)
        return True
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return False

desired_landmark_ids = ['47378', '141899', '59745', '70297', '166683', '55350', '163459', '64325', '156556', '174715', '43845', '168098', '152673']  # Add more IDs as needed

with open(csv_file_path, mode='r') as file, open(downloaded_images_csv, mode='w', newline='') as out_file:
    csv_reader = csv.DictReader(file)
    fieldnames = ['id', 'filepath', 'landmark_id']
    csv_writer = csv.DictWriter(out_file, fieldnames=fieldnames)
    csv_writer.writeheader()
    
    for row in csv_reader:
        landmark_id = row['landmark_id']
        
        # Check if the current landmark ID is in the list of desired IDs
        if landmark_id in desired_landmark_ids:
            image_url = row['url']
            filename = image_url.split('/')[-1]  # Extract filename from URL
            filepath = data_dir / f"{landmark_id}_{filename}"
            
            # Download and save image
            if download_image(image_url, filepath):
                # Write to new CSV if download was successful
                csv_writer.writerow({'id': row['id'], 'filepath': str(filepath), 'landmark_id': landmark_id})

print("Download process for specified landmarks completed.")