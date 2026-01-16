import os
import requests
import zipfile
import io

def download_movielens():
    url = "https://files.grouplens.org/datasets/movielens/ml-latest-small.zip"
    save_dir = "data"

    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    print("Downloading MovieLens dataset...")
    r = requests.get(url)
    z = zipfile.ZipFile(io.BytesIO(r.content))
    z.extractall(save_dir)
    print("Data extracted to /data")

if __name__ == "__main__":
    download_movielens()