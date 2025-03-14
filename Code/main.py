import tkinter as tk
import threading
import time
import re
import sys
import csv
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from unidecode import unidecode
from tkinter import messagebox
from tkinter import ttk


regions_villes = {
    "Auvergne-Rhône-Alpes": [
        "Saint-Étienne",
        "Grenoble",
        "Villeurbanne",
        "Clermont-Ferrand",
        "Lyon"
    ],
    "Bourgogne-Franche-Comté": [
        "Auxerre",
        "Chalon-sur-Saône",
        "Belfort",
        "Besançon",
        "Dijon"
    ],
    "Bretagne": [
        "Vannes",
        "Lorient",
        "Quimper",
        "Brest",
        "Rennes"
    ],
    "Centre-Val de Loire": [
        "Châteauroux",
        "Blois",
        "Bourges",
        "Orléans",
        "Tours"
    ],
    "Corse": [
        "Calvi",
        "Corte",
        "Porto-Vecchio",
        "Bastia",
        "Ajaccio"
    ],
    "Grand Est": [
        "Nancy",
        "Mulhouse",
        "Metz",
        "Reims",
        "Strasbourg"
    ],
    "Hauts-de-France": [
        "Dunkerque",
        "Tourcoing",
        "Roubaix",
        "Amiens",
        "Lille"
    ],
    "Île-de-France": [
        "Saint-Denis",
        "Montreuil",
        "Argenteuil",
        "Boulogne-Billancourt",
        "Paris"
    ],
    "Normandie": [
        "Saint-Lô",
        "Dieppe",
        "Évreux",
        "Cherbourg-en-Cotentin",
        "Caen",
        "Rouen",
        "Le Havre"
    ],
    "Nouvelle-Aquitaine": [
        "La Rochelle",
        "Pau",
        "Poitiers",
        "Limoges",
        "Bordeaux"
    ],
    "Occitanie": [
        "Béziers",
        "Perpignan",
        "Nîmes",
        "Montpellier",
        "Toulouse"
    ],
    "Pays de la Loire": [
        "La Roche-sur-Yon",
        "Saint-Nazaire",
        "Le Mans",
        "Angers",
        "Nantes"
    ],
    "Provence-Alpes-Côte d'Azur": [
        "Avignon",
        "Aix-en-Provence",
        "Toulon",
        "Nice",
        "Marseille"
    ]
}


regions = ["None"]+list(regions_villes.keys())

def CreateRech(email,country, j_title, w_include, w_exclude, Education, area):
    """ Crée la recherche en fonction des filtres (None si pas de filtre)"""
    if all(param is None for param in [country, j_title, w_include, w_exclude, Education]):
        root = tk.Tk()
        root.withdraw()  # Cache la fenêtre principale
        messagebox.showerror("Erreur", "No results for your search or the search is to wide")
        sys.exit(1)
    Res = "https://www.google.com/search?q="

    if any(param is not None for param in [j_title, w_include, area]):
        if j_title is not None:
            separated_words_j = j_title.split(',')            
            for i in range(0,len(separated_words_j)):
                Res+= 'intitle:'
                Res+=f'"{separated_words_j[i]}" '
        if w_include is not None:
            separated_words_i = w_include.split(',')
            for i in range(0,len(separated_words_i)):
                Res+=f'"{separated_words_i[i]}"'
        if area is not None:
                if area in regions_villes.keys():
                    for elem in regions_villes[area]:
                        Res +=f'"{elem}" OR '
                else:
                    messagebox.showerror("Erreur", "Name of the area is unvalid")
                    sys.exit(1)
                if Res.endswith(" OR "):  
                    Res = Res[:-4]              
        Res+=' '
    if w_exclude is not None:
        Res+='-intitle'
        separated_words_e = w_exclude.split(',')
        for i in range(0,len(separated_words_e)):
            Res+=f'"{separated_words_e[i]}"'
        Res +=' '


    if email is not None:
        if unidecode(email).lower() =="all":
            emails = [
                "laposte.net",
                "sfr.fr",
                "orange.fr",
                "wanadoo.fr",
                "yahoo.fr",
                "hotmail.fr",
                "hotmail.fr",
                "hotmail.com",
                "outlook.com",
                "gmail.com"
            ]
            Res +='('
            for i in range (0,len(emails)-1):
                Res+=f'"@{emails[i]}" OR '
            Res +=f'"{emails[len(emails)-1]}") '
        else:
            Res +=f'"@{email}"'

    Res += f' -intitle:"profiles" '  #' -intitle:"profiles" -inurl:"dir/"email"@{Email}.com"'

    if country is not None:
        Res += f'(site:{country}.linkedin.com/in/ OR site:{country}.linkedin.com/pub/)'
    else:
        Res += '(site:linkedin.com/in/ OR site:linkedin.com/pub/)'

    if Education is not None:
        Education = unidecode(Education).lower()
        if Education =="bachelor":
            Res += '&as_oq=bachelor+degree+licence'
        if Education == "master":
            Res+='&as_oq=masters+mba+master+diplome+msc+magister+magisteres+maitrise'
        if Education =="doctoral":
            Res+='&as_oq=dr+Ph.D.+PhD+D.Phil+DPhil+doctor+Doctorado+Doktor+Doctorat+Doutorado+DrSc+Tohtori+Doctorate+Doctora+Duktorah+Dottorato+Daktaras+Doutoramento+Doktorgrad'

    # if Firm is not None:
    #     Res += f'+"Entreprise+actuelle+%2A+{Firm}+%2A+'

    return Res

def show_loading_window():
    """ Affiche une fenêtre indiquant que l'exécution est en cours """
    loading_window = tk.Toplevel(root)
    loading_window.title("Execution in progress...")
    loading_window.geometry("300x80")
    loading_window.resizable(False, False)

    tk.Label(loading_window, text="Execution in progress...", font=("Arial", 12)).pack(pady=20)
    
    root.update()  # Met à jour l'interface pour afficher immédiatement
    return loading_window




def isemail(text):
    """ Nettoie le texte et extrait les emails """
    clean_text = re.sub(r'<.*?>', '', text)  
    email_regex = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    emails = re.findall(email_regex, clean_text)  # Recherche des emails
    if len(emails)==0:
        return "Unknown"
    else:
        email = emails[0]
        n = len(email)-email[::-1].find(".")
        end = email[n:len(email)]
        if  len(end)>2 and end !="com" :
            email = email[0:n-1]
            email = email.replace(" ","").strip()
        return email 


def getfirm(under_text):
    """ Récupère la dernière <span> pour l'entreprise """
    spans = under_text.find_all("span")  # Trouver tous les <span>
    return spans[-1].text.strip() if spans else "Unknown"

def remove_html_tags(text):
    """Supprime toutes les balises HTML d'un texte."""
    clean_text = re.sub(r'<[^>]+>', '', text)  
    return clean_text.strip() 

def getresults(url, max_pages):
    """Récupère les résultats de l'url sur max_pages pages"""
    options = webdriver.FirefoxOptions()
    #options.add_argument("--headless")  # Exécute sans ouvrir une fenêtre
    driver = webdriver.Firefox(options=options)



    # Accéder à Google
    driver.get(url)
    time.sleep(2)

    try:
        wait = WebDriverWait(driver, 60)
        accept_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[text()='Tout accepter']")))       
        accept_button.click()

    except Exception :
        root = tk.Tk()
        root.withdraw()  # Cache la fenêtre principale
        messagebox.showerror("Erreur", "Not fast enough on the captcha :'(")
        driver.quit()
        sys.exit(1)



    #driver.minimize_window()  # Réduit la fenêtre
    #driver.execute_script("document.body.style.zoom='0.1'")  

    data_collected = {}
    page_number = 1


    while page_number <= max_pages:
        time.sleep(0.5)  # Attendre que la page se charge
        soup = BeautifulSoup(driver.page_source, "html.parser")
        results = soup.find_all("div", class_="MjjYud")  

        for result in results:
            h3_element = result.find("h3", class_="LC20lb MBeuO DKV0Md")
            name = h3_element.text if h3_element else "Unknown"
            inurl_element = result.find(class_="VwiC3b yXK7lf p4wth r025kc hJNv6b Hdw6tb")
            under_text = result.find(class_="YrbPuc")
            div_link= result.find(class_="yuRUbf")
            if div_link:
                link = div_link.find("a")
                if link and link.has_attr("href"):
                    extracted_url=link["href"]
                else:
                    extracted_url = "Unknonw"
            else:
                extracted_url = "Unknonw"
            if inurl_element:
                inurl_text = str(inurl_element)  
                email = isemail(inurl_text)
                other = remove_html_tags(inurl_text)  
            else:
                email = "Unknown"
                other = "Nothing else"
            
            firm = getfirm(under_text) if under_text else "Unknown"
            
            data_collected[name] = {
                "identity": name.split(" - ")[0] if " - " in name else "Unknown",
                "email": email,
                "poste": name.split(" - ")[1] if " - " in name else "Unknown",
                "entreprise": firm,
                "link": extracted_url,
                "other": other
            }

        try:
            next_button = driver.find_element(By.LINK_TEXT, "Suivant")
            next_button.click()
            page_number += 1
        except Exception:
            root = tk.Tk()
            root.withdraw()  # Cache la fenêtre principale
            messagebox.showinfo("Infos", f"Not enough results for the number of pages but we continue")
            break

    # # Afficher les résultats
    # for name, info in data_collected.items():
    #     print(f"Nom: {info['identity']}")
    #     print(f"Email: {info['email']}")
    #     print(f"Poste: {info['poste']}")
    #     print(f"Entreprise: {info['entreprise']}")
    #     print(f"Link: {info['link']}")
    #     print(f"Other: {info['other']}")
    #     print("-" * 50)

    driver.quit()
    data_collected = {name: info for name, info in data_collected.items() if info["identity"] != "Unknown"} #Enlever les unknown
    return (data_collected)



def clean(text):
    """Nettoie le texte en supprimant les caractères spéciaux et les espaces inutiles"""
    if text is None:
        return "Unknown"
    text = text.replace("\n", " ").replace("\r", " ")  # Supprimer les retours à la ligne
    text = text.replace("\t", " ")  # Supprimer les tabulations
    text = text.strip()  # Supprimer les espaces inutiles
    return text

def save_to_csv(results, filename="results.csv"):
    """Enregistre les résultats dans un fichier CSV proprement formaté"""
    if not results:
        root = tk.Tk()
        root.withdraw()  # Cache la fenêtre principale
        messagebox.showerror("Erreur", "No results for your search")
        sys.exit(1)
        return

    # Chemin vers le répertoire courant (où le script est exécuté)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(current_dir, filename)

    headers = ["Identity", "Email", "Post", "Current Firm", "Link", "Full Name (Page Title)", "Other"]

    with open(filepath, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(headers)

        for name, info in results.items():
            writer.writerow([
                info.get("identity"),
                info.get("email"),
                info.get("poste"),
                info.get("entreprise"),
                info.get("link"),
                clean(name),
                clean(info.get("other")),
            ])

    # Ouvrir le fichier avec l'application par défaut
    if sys.platform == "win32":
        os.startfile(filepath)
    else:
        opener = "open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, filepath])

    root = tk.Tk()
    root.withdraw()  # Cache la fenêtre principale
    messagebox.showinfo("Succès", f"Fichier '{filename}' enregistré avec succès à l'emplacement:{filepath} !")


def get_user_input():
    """ Récupère les valeurs sélectionnées par l'utilisateur dans l'interface graphique """
    selected_options = {}

    for key, var in check_vars.items():
        if var.get():  # Si la checkbox est cochée
            value = entry_vars[key].get().strip()
            selected_options[key] = value if value else None  
        else:
            selected_options[key] = None  

    # Gestion du champ Education et Area
    for key in ["area", "Education"]:
        value = entry_vars[key].get().strip()
        if value.lower() == "none":
            selected_options[key] = None  # Convertit "None" en None
        else:
            selected_options[key] = value

    # Vérification du champ Nb_pages
    nb_pages = entry_vars["Nb_pages"].get().strip()
    if nb_pages.isdigit() and int(nb_pages) > 0:
        selected_options["Nb_pages"] = int(nb_pages)
    else:
        messagebox.showerror("Erreur", "Please enter a positive integer for the number of pages.")
        return  

    # Vérification du champ Country
    if selected_options.get("country") and len(selected_options["country"]) > 2:
        messagebox.showerror("Error", "The country alias is requested (e.g. fr, us, uk).")
        return

    root.quit()
    root.destroy()

    # Affichage des valeurs récupérées pour débogage
    print("Selected options:", selected_options)

    search_url = CreateRech(
        selected_options.get("email"), selected_options.get("country"), selected_options.get("j_title"),
        selected_options.get("w_include"), selected_options.get("w_exclude"), selected_options.get("Education"), selected_options.get("area")
    )

    print("\n URL Générée :", search_url)

    results = getresults(search_url, selected_options.get("Nb_pages", 1))
    
    if results:
        save_to_csv(results)
    else:
        messagebox.showerror("Erreur", "No data retrieved from search.")



# **Interface Graphique avec Tkinter**
root = tk.Tk()
root.title("Research options")
root.geometry("700x500")

bg_color = "#f5f5f5"  # Couleur de fond 
title_color = "#333333"  # Couleur du texte
highlight_color = "#0078D7" 

root.configure(bg=bg_color)  

title = tk.Label(root, text="Research options", 
                 font=("Arial", 18, "bold"), fg=title_color, bg=bg_color)
title.pack(pady=15)

subtitle_frame = tk.Frame(root, bg="white", padx=15, pady=5, relief="ridge", bd=2)
subtitle_frame.pack(pady=5, fill="x", padx=20)

subtitle = tk.Label(subtitle_frame, text="Fill in the options in the language of the selected country", font=("Arial", 12, "bold"), fg=highlight_color, bg="white")
subtitle.pack()



options = {
    "email": "Email domain selection(e.g : gmail.com, yahoo.fr, etc.)",
    "country": "Country Alias (e.g : fr, us, ca...)",
    "j_title": "Job title OR The most specific (e.g. [Courtier, Assurances])",
    "w_include": "Keyword to include",
    "w_exclude": "Keyword to exclude",
    "Education": "Level of study ( in Bachelor, Master, Doctoral)",
    "area": "Area of researches "
}

check_vars = {}
entry_vars = {}

for key, desc in options.items():
    frame = tk.Frame(root)
    
    if key == "area":
        tk.Label(frame, text=desc, font=("Arial", 10)).pack(side="left")  # Ajout d'un label descriptif
        entry_vars[key] = tk.StringVar()
        dropdown = ttk.Combobox(frame, textvariable=entry_vars[key], values=regions, state="readonly")
        dropdown.pack(side="right")
        dropdown.current(0)  # Sélectionne "None" par défaut
    elif key == "Education":        
        tk.Label(frame, text=desc, font=("Arial", 10)).pack(side="left")  # Ajout d'un label descriptif
        entry_vars[key] = tk.StringVar()
        dropdown = ttk.Combobox(frame, textvariable=entry_vars[key], values=["None","Bachelor","Master","Doctoral"], state="readonly")
        dropdown.pack(side="right")
        dropdown.current(0)  # Sélectionne "None" par défaut
    else:
        # Checkbox + champ texte standard
        check_vars[key] = tk.BooleanVar()
        checkbox = tk.Checkbutton(frame, text=desc, variable=check_vars[key])
        checkbox.pack(side="left")
        entry_vars[key] = tk.StringVar()
        entry = tk.Entry(frame, textvariable=entry_vars[key], width=25)
        entry.pack(side="right")

    frame.pack(fill="x", padx=10, pady=5)


# Champ pour le nombre de pages
frame_pages = tk.Frame(root)
frame_pages.pack(fill="x", padx=10, pady=5)

tk.Label(frame_pages, text="Number of pages (10 results/page) :").pack(side="left")
entry_vars["Nb_pages"] = tk.StringVar()
entry_pages = tk.Entry(frame_pages, textvariable=entry_vars["Nb_pages"], width=5)
entry_pages.pack(side="right")
validate_button = tk.Button(root, text="Confirm", command=get_user_input, 
                            font=("Arial", 12, "bold"), 
                            bg=highlight_color, fg="white",
                            relief="raised", padx=15, pady=5)
validate_button.pack(pady=20)

root.mainloop()