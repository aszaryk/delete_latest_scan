# Delete Builds from Applications and Sandboxes

Script to delete scans from application profiles and sandboxes, requiring a list of application ID's and sandbox ID's as input

Uses Python3

## Setup

Clone this repository:

    git clone https://github.com/aszaryk/delete_latest_scan

Install dependencies:

    cd delete_latest_scan
    pip3 install -r requirements.txt

(Optional) Save Veracode API credentials in `~/.veracode/credentials`

    [default]
    veracode_api_key_id = <YOUR_API_KEY_ID>
    veracode_api_key_secret = <YOUR_API_KEY_SECRET>

## Usage

Tested using Python3 

usage: delete_latest_build.py apps_sandboxes.txt

NOTE:

--apps_sandboxes.txt is a REQUIRED text file containing application and sandbox ID's: [app_id:sandbox_id]. See example file. 

--If no [sandbox_id] is provided, the utility will delete the most recent policy level scan from the app profile
