
import numpy as np
import datetime
import os
import csv
import markdown2
import tabulate
import typing
import matplotlib.pyplot as plt
import pypandoc
from operator import itemgetter


try:
    with open("DumpFile.txt", encoding="utf8") as fh:
        res=fh.read()
except:
        print("Le fichier n'existe pas %s", os.path.abspath('fichieratraiter.txt'))
ress=res.split('\n')
tab_dest=np.array([])
tableau_evenements=np.array([])
fic=open("test.csv", "w")#test est le fichier d'arrivée des extractions
evenement = "DATE ; SOURCE ; PORT ; DESTINATION ; FLAG ; SEQ ; ACK ; WIN ; OPTIONS ; LENGTH" #intitulé de mes colonnes
fic.write(evenement + "\n") #écriture de mes titres dans le tableur
characters = ":" #définir une variable avec le caractère ":" (qui nous sera utile pour la suite)

ipslistmesocuilels = {

}

bigdata = []


for event in ress:
    if event.startswith('11:42'): #évenement qui commence par "11:42" (ils commencent tous par 11:42)
        #déclaration variables et remise à zéro
        seq = ""
        heure1 = ""
        nomip = ""
        port = ""
        flag = ""
        ack = ""
        win = ""
        options = ""
        length = ""
        #Pour la date de l'évenement (première colonne)
        texte=event.split(" ")
        heure1=texte[0]
        #Pour la source (2ème colonne)
        texte=event.split(" ")
        nomip1=texte[2].split(".")
        # print(nomip1)
        if len(nomip1) == 2:
            nomip=nomip1[0]
        if len(nomip1) == 3:
            nomip=nomip1[0]+ "." +nomip1[1]
        if len(nomip1) == 4:
            nomip=nomip1[0]+ "." +nomip1[1]+ "." +nomip1[2]
        if len(nomip1) == 5:
            nomip=nomip1[0]+ "." +nomip1[1]+ "." +nomip1[2]+ "." +nomip1[3]
        if len(nomip1) == 6:
            nomip=nomip1[0]+ "." +nomip1[1]+ "." +nomip1[2]+ "."+nomip1[3]+"."+ nomip1[4]
        # print("nomip :",nomip)
        flag2=0
        for item in tab_dest:
            if item == nomip:
                flag2=1
    
        if flag2==0:
            tab_dest = np.append(tab_dest,nomip)
        # print("tableau", tab_dest)
        #port
        if len(texte) > 1:
            port1=texte[2].split(".")
            port=port1[-1]
        #Pour la destination (3ème colonne)
        texte=event.split(" ")
        nomip2=texte[4]
        # Flag
        texte=event.split("[") #On coupe à partir du crochet
        if len(texte) > 1: #s'il y a plus de une partie à partir du crochet
            flag1=texte[1].split("]") #on prend après le premier crochet et on coupe au deuxième crochet
            flag=flag1[0]#pourquoi 0 ? Car on prend la partie de gauche du deuxième crochet (ce qu'on recherche)
        #seq
        texte=event.split(",")#on coupe à la virgule
        if len(texte) > 1: #s'il y a plus de 1 partie à partir du crochet
            if texte[1].startswith(" seq"): #Si le texte [1] commence par " seq"
                seq1=texte[1].split(" ") #on coupe à l'espace et on prend le texte juste après
                seq=seq1[2] #On a 2 parties entre le split ',' et ce que je recherche
        #ack
        if len(texte) > 2: #
            if texte[2].startswith(" ack"): #Si le texte [2] commence par "ack"
                ack1=texte[2].split(" ") #on coupe à l'espace et on prend le texte juste après
                ack=ack1[2] #On a 2 parties entre le split ',' et ce que je recherche
            #si la partie "seq" est absente :
            if texte[1].startswith(" ack"): #Si le texte [1] commence par " ack"
                ack1=texte[1].split(" ") #on coupe à l'espace et on prend le texte juste après
                ack=ack1[2] #On a 2 parties entre le split ',' et ce que je recherche
        #win
        if len(texte) > 3: #si le nombre de partie est supérieur à 3
            #si "ack" est présent
            if texte[3].startswith(" win"): #Si le texte [3] commence par " win"
                win1=texte[3].split(" ") #on coupe à l'espace et on prend le texte juste après
                win=win1[2] #On prend le texte après l'espace (la partie qu'on retrouvera dans le tableau)
            #si "ack" n'est pas présent
            if texte[2].startswith(" win"): #Si le texte [2] commence par " win"
                win1=texte[2].split(" ") #on coupe à l'espace et on prend le texte juste après
                win=win1[2]#On prend le texte après l'espace (la partie qu'on retrouvera dans le tableau
        #options
        texte=event.split("[") #On coupe à partir du crochet
        if len(texte) > 2: #
            options1=texte[2].split("]") #On part du premier "[" et on a texte [2] pour arriver à ce qu'on souhaite récupérer
            options=options1[0]#pourquoi 0 ? Car on prend la partie à gauche du deuxième crochet "]"
    
        #length (avec option)
        texte=event.split("]")
        if len(texte) > 2: #vérifier le nombre de partie (split au crochet)
                length1=texte[2].split(" ") #on part du premier "[" et ce qu'on recherche est bien dans texte [2]. On split à l'espace pour avoir que le nombre
                length=length1[2] #On veut bien le "2" pour avoir que le nombre (il y a une partie avant l'espace + une autre après).
        #length (sans option)
        texte=event.split(",")
        if len(texte) > 3:
            if texte[3].startswith(" length"): #Si ça commence par " length" et on recherche dans le texte [3]
                length1=texte[3].split(" ") #on coupe à l'espace
                length=length1[2] ##On veut bien le "2" pour avoir que le nombre (texte [1] avant l'espace c'est le mot "length").
                length = length.replace(characters,"")#remplacement du "characters" en " " (pour éviter que le tableur écrit sous forme de date)
        if event.startswith("11:42:55.536521") : #dès que le programme arrive à la dernière ligne du fichier texte
            prog=0 #il ne fait plus de tour, il s'arrete
        evenement=heure1+";"+nomip+ ";" +port+ ";" + nomip2+ ";"+flag+ ";" +seq+ ";" +ack+ ";" +win+ ";" +options+ ";" +length
        data = [heure1, nomip, port, nomip2, flag, seq, ack, win, options, length]
        # if nomip in bigdata.keys():
        #     bigdata[nomip] += 1
        # else:
        #     bigdata[nomip] = 1
        bigdata += [data]
        if nomip in ipslistmesocuilels.keys():
            ipslistmesocuilels[nomip] += 1
        else:
            ipslistmesocuilels[nomip] = 1
        # fic.write(evenement + "\n") #on écrire "evenement" dans le csv et \n pour revenir à la ligne (pour ne pas écrire sur la même ligne)
# print("tableau final", tab_dest)
# plt.plot(range(len(tab_dest)), tab_dest)
#plt.ylabel('some numbers')
# plt.show()
# fic.close()

# print(ipslistmesocuilels)

sorted_data = sorted(ipslistmesocuilels.items(), key = itemgetter(1), reverse=True)

# print(sorted_data)

susreqiesys = []

# a = 0
# for i in range(2):
#     # print(sorted_data[i])
#     a+=1
# print(a)
# print(bigdata)

# print(sorted_data[1][0])
# print(sorted_data[0][0])

# # a = 0
for el in bigdata:
    if el[1] == sorted_data[0][0] or el[1] == sorted_data[1][0]:
        # print(el)
        susreqiesys += [el]
        evenement=el[0]+";"+el[1]+ ";" +el[2]+ ";" + el[3]+ ";"+el[4]+ ";" +el[5]+ ";" +el[6]+ ";" +el[7]+ ";" +el[8]+ ";" +el[9]
        fic.write(evenement + "\n")
#         # a+=1
# # print(a)
import time
time.sleep(1)
#CSV TO MARKDOWN
try:
    csv_data = np.genfromtxt("test.csv", delimiter=';', dtype=None, names=True, encoding=None)
except IndexError as e:
    print(f"Error loading CSV data: {e}")
    csv_data = None

if csv_data is not None:
    # Convert CSV to Markdown
    markdown_table = tabulate.tabulate(csv_data, headers=["DATE", "SOURCE", "PORT", "DESTINATION", "FLAG", "SEQ", "ACK", "WIN", "LENGTH"], tablefmt="pipe")

    # Convert Markdown to HTML using markdown2
    html_content = markdown2.markdown(markdown_table)

    # Save HTML content to file
    with open("test.html", "w", encoding="utf-8") as html_file:
        html_file.write(html_content)

    # Plotting
    tab_dest = np.unique(csv_data["SOURCE"])  # Assuming SOURCE is the column containing IP addresses
    print("tableau final", tab_dest)
    plt.plot(range(len(tab_dest)), tab_dest)
    plt.show()
    fic.close()
else:
    print("CSV data is not available.")
