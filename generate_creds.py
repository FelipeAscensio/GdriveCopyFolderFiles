#!/usr/bin/env python

from pydrive2.auth import GoogleAuth, RefreshError
from pydrive2.drive import GoogleDrive

gauth = GoogleAuth()

try:
    #gauth.LocalWebserverAuth()
    gauth.CommandLineAuth()
except RefreshError:
    current_directory = os.path.dirname(os.path.abspath(__file__))
    os.remove(current_directory + "\creds.json")
    print("Automatic token refreshal failed, please give your authentication code again by visiting this link \n\n" + gauth.GetAuthUrl())
    code = input("\n\nYour authentication code: ")
    gauth.Auth(code)
    gauth.SaveCredentialsFile("creds.json")

drive = GoogleDrive(gauth)