import socket
import hashlib
import os
import json
import re
import shutil
import string
import secrets
import pickle
import time

if "tmp" not in os.listdir(os.path.dirname(__file__)):
    os.system("mkdir tmp")

if "tmp" not in os.listdir(os.path.dirname(__file__)):
    os.system("mkdir project")


def clean_cli():
    if os.name == 'nt':
        os.system("cls")
    else:
        os.system("clear")

clean_cli()

connected = False

token = ""

while True:
    ADRESSE = '88.185.169.23'
    PORT = 19999

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    if connected == True:
        print("Connecter en tant que: " + str(username) + "\nToken: " + str(token))

    print("""
      /$$$$$$             /$$$$$$$                       /$$      /$$$$$$  /$$ /$$                       /$$    
     /$$__  $$           | $$__  $$                     | $$     /$$__  $$| $$|__/                      | $$    
    | $$  \ $$ /$$    /$$| $$  \ $$ /$$$$$$   /$$$$$$  /$$$$$$  | $$  \__/| $$ /$$  /$$$$$$  /$$$$$$$  /$$$$$$  
    | $$  | $$|  $$  /$$/| $$$$$$$/|____  $$ /$$__  $$|_  $$_/  | $$      | $$| $$ /$$__  $$| $$__  $$|_  $$_/  
    | $$  | $$ \  $$/$$/ | $$____/  /$$$$$$$| $$  \__/  | $$    | $$      | $$| $$| $$$$$$$$| $$  \ $$  | $$    
    | $$  | $$  \  $$$/  | $$      /$$__  $$| $$        | $$ /$$| $$    $$| $$| $$| $$_____/| $$  | $$  | $$ /$$
    |  $$$$$$/   \  $/   | $$     |  $$$$$$$| $$        |  $$$$/|  $$$$$$/| $$| $$|  $$$$$$$| $$  | $$  |  $$$$/
     \______/     \_/    |__/      \_______/|__/         \___/   \______/ |__/|__/ \_______/|__/  |__/   \___/  


                            (1): Login                (2): Nouveau Projet
                            (3): List des projet      (4): Rejoindre un projet
                            (5): Utiliser un projet   (6): Maj
                            (7): Quitter          
    """)

    choix = input("> ")

    if choix == "1":
        if connected != True:
            username = input("\nUsername: ")
            password = input("Password: ")
            clean_cli()

            action = "login"

            hashcrypt = hashlib.md5()

            hashcrypt.update(password.encode('utf-8'))

            password_hasher = hashcrypt.hexdigest()
            
            s.connect((ADRESSE, PORT))

            request = f"{action}:{username}:{password_hasher}"
            s.sendall(request.encode('utf-8'))

            data = s.recv(1024)
            
            received_data = data.decode('utf-8')
            
            data = received_data.split(':')

            if data[0] == "Logged":
                connected = True
                token = str(data[1])

            s.close()
        else:
            clean_cli()
            print("Vous étes déja connecter retour au menu dans 5 secondes !")
            time.sleep(5)
            clean_cli()


    elif choix == "2":
        if connected == True:
            project_name = input("\nNom du projet: ")
            clean_cli()
            project_name_filtered = re.sub(r'[^a-zA-Z0-9]', '', project_name)

            if project_name_filtered != "":
                os.system('mkdir "project/'+str(project_name_filtered)+'"')
                alphabet = string.ascii_letters + string.digits
                tokenfile = ''.join(secrets.choice(alphabet) for i in range(64)) 

                data = {
                    "name": str(project_name_filtered),
                    "token": str(tokenfile),
                }

                json_object = json.dumps(data, indent=2)
                    
                with open("./project/"+str(project_name_filtered)+"/.config.json", "w") as file:
                    file.write(json_object)

                s.connect((ADRESSE, PORT))

                action = "newproject"

                request = f"{action}:{token}:{project_name}:{tokenfile}"

                s.sendall(request.encode('utf-8'))
                s.close()
            else:
                print("Le nom du projet est invalide retour au menu dans 5 secondes !")
                time.sleep(5)
                clean_cli()
        else:
            clean_cli()
            print("Vous devez vous connecter pour créer un projet retour au menu dans 5 secondes !")
            time.sleep(5)
            clean_cli()

    elif choix == "3":
        if connected == True:
            clean_cli()
            s.connect((ADRESSE, PORT))

            action = "listproject"

            request = f"{action}:{token}"

            s.sendall(request.encode('utf-8'))

            data = s.recv(1024)
            
            received_data = data.decode('utf-8')
            
            if received_data != "":
                print(received_data)
            else:
                print("*" * 50)
                print("                Aucun projet !")
                print("*" * 50)

            s.close()
        else:
            clean_cli()
            print("Vous devez vous connecter pour obtenir la liste de vos projets retour au menu dans 5 secondes !")
            time.sleep(5)
            clean_cli()

    elif choix == "4":
        if connected == True:
            token_invitation = input("Entrer le token d'invitation du projet: ")
            s.connect((ADRESSE, PORT))

            action = "joinproject"

            request = f"{action}:{token}:{token_invitation}"

            s.sendall(request.encode('utf-8'))

            data = s.recv(1024)
            
            received_data = data.decode('utf-8')
            
            print(received_data)

            s.close()
            clean_cli()
        else:
            clean_cli()
            print("Vous devez vous connecter pour rejoindre un projet retour au menu dans 5 secondes !")
            time.sleep(5)
            clean_cli()
        
    elif choix == "5":
        clean_cli()
        s.connect((ADRESSE, PORT))

        action = "listproject"

        request = f"{action}:{token}"
        s.sendall(request.encode('utf-8'))

        data_recu = s.recv(1024)
        
        received_data = data_recu.decode('utf-8')
                
        if received_data != "":
            print(received_data)
            project_id = input("Projet a selectionné(by id): ")

            s.close()
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((ADRESSE, PORT))

            clean_cli()
            
            action = "editproject"

            request = f"{action}:{token}:{project_id}"
            s.sendall(request.encode('utf-8'))

            data_recu = s.recv(1024)

            try:
                received_list = pickle.loads(data_recu)
            except pickle.UnpicklingError:
                print("Error deserializing data!")

            for element in received_list:
                project_id = element[0]
                project_name = element[1]
                project_token = element[2]

            s.close()

            while True:
                clean_cli()
                print("Project id: " + str(project_id) + "\nProject name: " + str(project_name) + "\nProject token: " + str(project_token))

                print("""      
            (1): Mettre a jour        (2): Supprimer
            (3): Télécharger          (4): Créer un lien d'invitation
            (5): Retour au menu
                
            """)

                option = input("> ")

                if option == "1":
                    action = "majclientproject"
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.connect((ADRESSE, PORT))

                    for project in os.listdir("./project"):
                        with open("./project/"+project+"/.config.json", "r") as file:
                            data = json.load(file)
                        if (data['token'] == str(project_token)):
                            Project_Path = "./project/"+str(project)
                            archived = shutil.make_archive('./tmp/'+str(project), 'zip', './project/'+str(project))
                            reponse = f"{action}:{token}:{str(element[2])}"
                            s.sendall(reponse.encode('utf-8'))
                            with open(archived, 'rb') as f:
                                print(f"Envoi du fichier '{archived}'...")
                                while True:
                                    donnees = f.read(1024)
                                    if not donnees:
                                        break
                                    s.sendall(donnees)
                                print("Fichier envoyer avec succés")
                                time.sleep(5)
                            if os.name == 'nt':
                                os.system('RMDIR /S /Q ' + str(archived))                            
                            else:
                                os.system("rm -fr " + str(archived))
                            clean_cli()
                    break

                if option == "2":
                    action = "delproject"
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.connect((ADRESSE, PORT))
                    request = f"{action}:{token}:{project_id}"
                    s.sendall(request.encode('utf-8'))
                    for project in os.listdir("./project"):
                        with open("./project/"+project+"/.config.json", "r") as file:
                            data = json.load(file)
                        if (data['token'] == str(element[2])):
                            if os.name == 'nt':
                                Project_Path = "project\\" + str(project)
                            else:
                                Project_Path = "./project/"+str(project)
                    try:
                        if os.name == 'nt':
                            os.system('RMDIR /S /Q ' + Project_Path)
                            time.sleep(10)                  
                        else:
                            os.system("rm -fr " + Project_Path)
                        clean_cli()
                    except:
                        pass
                    break


                if option == "3":
                    action = "dwldproject"
                    socks = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    socks.connect((ADRESSE, PORT))
                    request = f"{action}:{token}:{element[2]}"
                    socks.sendall(request.encode('utf-8'))

                    with open('./tmp/'+str(element[1])+'.zip', 'wb') as f:
                        print("Réception du fichier en cours...")

                        while True:
                            
                            donnees = socks.recv(1024)

                            if not donnees:
                                break
                            f.write(donnees)
                        
                    shutil.unpack_archive('./tmp/'+str(element[1])+'.zip', "./project/"+str(element[1]), "zip") 
                    print("Télécharger est mise a jour avec succés !")
                    if os.name == 'nt':
                        os.system('del tmp\\'+str(element[1])+'.zip')                            
                    else:
                        os.system("rm -fr ./tmp/"+str(element[1])+'.zip')
                    time.sleep(2)

                if option == "4":
                    action = "geninvitetokenproject"
                    socks = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    socks.connect((ADRESSE, PORT))
                    request = f"{action}:{token}:{element[2]}"
                    socks.sendall(request.encode('utf-8'))

                    donnees = socks.recv(1024)
                    received_data = donnees.decode('utf-8')
                    print("Token d'invitation au projet: " + received_data)
                    time.sleep(5)

        else:
            print("*" * 50)
            print("                Aucun projet !")
            print("*" * 50)
            print("\nRetour au menu principale dans 5 secondes !")
            time.sleep(5)
            clean_cli()        

    elif choix == "7":
        clean_cli()
        quit()

    else:
        clean_cli()
