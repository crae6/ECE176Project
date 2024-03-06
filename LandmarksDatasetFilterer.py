import csv
import requests
from pathlib import Path

# directory to save the images
data_dir = Path('data')
data_dir.mkdir(exist_ok=True)

# path to original CSV file
csv_file_path = 'train.csv'

def download_image(url, filepath):
    headers = {
        'User-Agent': 'ECE176LandmarkFilterer/1.0 (mpersiani@ucsd.edu)'  # replace with your name and email
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # HTTPError if the response status code is 4XX/5XX
        filepath.parent.mkdir(parents=True, exist_ok=True)  # ensure the directory exists
        with open(filepath, 'wb') as f:
            f.write(response.content)
        return True
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return False

desired_landmark_ids = ['47378', '141899', '59745', '70297', '166683', '55350', '163459', '64325', '156556', '174715', '43845', '168098', '152673']

# counter for each landmark ID
download_counter = {landmark_id: 0 for landmark_id in desired_landmark_ids}

with open(csv_file_path, mode='r') as file, open(downloaded_images_csv, mode='w', newline='') as out_file:
    csv_reader = csv.DictReader(file)
    fieldnames = ['id', 'filepath', 'landmark_id']
    csv_writer = csv.DictWriter(out_file, fieldnames=fieldnames)
    csv_writer.writeheader()
    
    for row in csv_reader:
        landmark_id = row['landmark_id']
        if landmark_id in desired_landmark_ids and download_counter[landmark_id] < 100:
            image_url = row['url']
            filename = image_url.split('/')[-1]  # get filename from URL
            # modify filepath to include a subdirectory for each landmark_id
            landmark_dir = data_dir / landmark_id
            filepath = landmark_dir / filename
            
            if download_image(image_url, filepath):
                download_counter[landmark_id] += 1
                csv_writer.writerow({'id': row['id'], 'filepath': str(filepath), 'landmark_id': landmark_id})
                print(f"Downloaded {download_counter[landmark_id]} images for landmark ID {landmark_id}")

print("Download process for specified landmarks completed.")
