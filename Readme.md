# Gmail Email Processing App

This application fetches emails from Gmail using the Gmail API, stores them in a SQLite database, and processes them based on predefined rules.

## Installation

1. Clone the repository:
```
git clone https://github.com/your_username/email-processing-app.git
cd email-processing-ap
```

2. Install the required Python packages using pip:

```
pip install -r requirements.txt
```

3. Create credentials.json:

* Visit the Google Cloud Console: https://console.cloud.google.com/
* Create a new project or select an existing one.
* Navigate to "APIs & Services" > "Credentials".
* Click on "Create credentials" and select "OAuth client ID".
* Choose the application type (desktop app or web application).
* Set the authorized redirect URIs (e.g., http://localhost:8080/oauth2callback).
* After creating the OAuth client ID, download the credentials.json file.
* Place the downloaded credentials.json file in the project directory.

4. Create rules.json:

Define rules for processing emails in a JSON file (rules.json).
See the example provided in the project directory.

## Usage

1. Run the main script to fetch emails and store them in the database:

```
python auth.py
```

2. Run the script to process emails based on rules:

```
python process_emails.py
```

The application will fetch emails from Gmail, store them in the SQLite database, and process them according to the defined rules.

```
Make sure to replace `your_username` with your actual GitHub username in the clone URL provided in step 1. Also, ensure that you provide appropriate instructions for creating and populating the `rules.json` file based on the provided example.
```
