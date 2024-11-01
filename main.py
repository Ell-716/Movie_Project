import argparse
import os
from storage.storage_json import StorageJson
from storage.storage_csv import StorageCsv
from movie_app import MovieApp
from colorama import init, Fore

init(autoreset=True)


def main():
    """Parse command-line argument for storage file and initialize MovieApp
    with the appropriate storage class."""

    parser = argparse.ArgumentParser()
    parser.add_argument('file', nargs='?')
    args = parser.parse_args()

    # Assign file_path based on input or default
    if args.file:
        file_path = args.file
    else:
        file_path = os.path.join("data", "data.json")
        print(Fore.RED + f"No valid filename provided. Proceeding with default file '{file_path}'.")

    # Determine the storage type by file extension
    if file_path.endswith('.csv'):
        storage = StorageCsv(file_path)
    elif file_path.endswith('.json'):
        storage = StorageJson(file_path)
    else:
        print(Fore.RED + f"Unsupported file type for '{file_path}'. Defaulting to JSON format.")
        file_path = os.path.join("data", "data.json")
        storage = StorageJson(file_path)

    if not os.path.exists(storage.file_path):
        print(Fore.RED + f"File '{storage.file_path}' does not exist. "
              f"A new file will be created.")

        with open(file_path, 'w') as file:
            if file_path.endswith('.json'):
                file.write('{}')
            elif file_path.endswith('.csv'):
                file.write("Title,Year,Rating,Poster,Note,imdbID\n")
            print(f"New file '{file_path}' has been created.")

    movie_app = MovieApp(storage)
    movie_app.run()


if __name__ == "__main__":
    main()
