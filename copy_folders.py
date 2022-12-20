#!/usr/bin/env python

from pydrive2.auth import GoogleAuth, RefreshError
from pydrive2.drive import GoogleDrive
import os
import sys

import cgi
import cgitb
import os

print("Content-Type: text/html\n\r\n")
#print()


OUTDIR="/www/http/gdrive-folder-copier/"
# Ativa o rastreamento de erros
cgitb.enable(display=0)
#cgitb.enable(display=0, logdir=OUTDIR)

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

#source_id = input("Folder to copy from: ")
#parent_id = input("Folder to copy to: ")
#prefix = input("Prefix to put if any: ")

form = cgi.FieldStorage()

source_id = form.getvalue("arg1")
parent_id = form.getvalue("arg2")
prefix = form.getvalue("arg3")

copy_parent_folder = True #None #set this to True if you want to copy the source folder into the destination folder

def copy_file(service, source_id, parent_folder_id, prefix_for_files):
    source = drive.CreateFile({'id': source_id})
    source.FetchMetadata('title')
    print('title: %s, id: %s' % (source['title'], source['id']))
    
    #dest_title = prefix_for_files + source['title']
    dest_title = source['title']
    copied_file = {'title': dest_title, 'parents': [{'id': parent_folder_id}]}
    f = service.files().copy(fileId=source_id, supportsAllDrives=True, body=copied_file).execute()

    print('title: %s, id: %s' % (f['title'], f['id']))

def copy_folder(folder, parent_id, prefix_for_folder):
    print('title: %s, id: %s' % (folder['title'], folder['id']))
    #dest_file = prefix_for_folder + folder['title']
    dest_file = folder['title']
    folder1 = drive.CreateFile({'mimeType': 'application/vnd.google-apps.folder', 'title': dest_file , 'parents': [{'id': parent_id}]})
    folder1.Upload()
    print('title: %s, id: %s' % (folder1['title'], folder1['id']))
    return folder1['id']


subfolders = {}

def copy_from_folder(folder_id, parent_folder_id, prefix_for_files):
    file_list = drive.ListFile({'corpora': "allDrives", 'q': "'%s' in parents and trashed = false" % (folder_id) }).GetList()

    for file1 in file_list:
        if file1['mimeType'] == 'application/vnd.google-apps.folder':
            copied_folder = copy_folder(file1, parent_folder_id, prefix_for_files)
            original_folder = file1['id']
            copy_from_folder(original_folder, copied_folder, prefix_for_files)
        else:
            copy_file(drive.auth.service, file1['id'], parent_folder_id, prefix_for_files)

def create_parent_folder(id, source_folder_id, prefix_for_folder):
    folder_source = drive.CreateFile({'id': source_folder_id})
    folder_source.FetchMetadata('title')
    print('title: %s, id: %s' % (folder_source['title'], folder_source['id']))

    #dest_title =  prefix_for_folder + folder_source['title'] 
    if prefix != None:
        dest_title = prefix_for_folder
        copied_folder = drive.CreateFile({'mimeType': 'application/vnd.google-apps.folder', 'title': dest_title, 'parents': [{'id': id}]})
        copied_folder.Upload()
        return copied_folder['id']
    else:
        dest_title = folder_source['title']
        copied_folder = drive.CreateFile({'mimeType': 'application/vnd.google-apps.folder', 'title': dest_title, 'parents': [{'id': id}]})
        copied_folder.Upload()
        return copied_folder['id']


if copy_parent_folder:
    parent_id = create_parent_folder(parent_id, source_id, prefix)
    

# Exibe os resultados na página HTML
print(" </head>")
print("<body>")
print("<h4>Resultado</h4>")
print(f"<p>{(copy_from_folder(source_id, parent_id, prefix))}</p>")
print("</body>")
print("</html>")

#copy_from_folder(source_id, parent_id, prefix)
