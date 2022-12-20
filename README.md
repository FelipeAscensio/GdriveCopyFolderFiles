# COPY FOLDERS/FILE GOOGLE DRIVE

## Folder to folder copying of files on google drive. Supports subfolders and files

## 1º Step - Clone This Repository
Install dependencies: pip install pip install -r /[your-path]/gdrive-folder-copier/requirements.txt

## 2º Step - For use this service, you need:

    - Activated Google Drive API on GCP Console: https://developers.google.com/drive/api/guides/about-sdk?hl=pt_BR
    - Create a OAuth credentials for "Desktop" on CGP Console: https://console.cloud.google.com/apis/credentials
    - Download credentials .json, rename to: client_secrets.json. And save in same service folder.

## 3º Step - Validate credentials

Run this script "generate_creds.py". Its return an url for verification your credentials. Copy for browser, and authorized with your user.
After authorization, paste the code generate for you bash. Done! Your credentials is validated and generate a new file "creds.json"

## 4º Step - Apache (WebService)
For run this service i used Apache webservice. So all files need permissions for user Apache.

Run this command for your folder: chown -R  www-data:www-data gdrive-folder-copier

Attention! Every time you generate a new "creds.json", you need apply command above.

You also define cgi path in your apache.conf, example: ScriptAlias /cgi-bin/ /[your-path]/gdrive-folder-copier/

In this repo have a .conf apache to be used. "gdrive.conf"

## 5º Step - Access Your Service

This service is accessed for browser, port 80 for default: http://[your-host]:80/



