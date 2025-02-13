# 🚀 NetFlow - Recherche d'adresses mail professionnelles

NetFlow est un outil de recherche d'adresses e-mail professionnelles avec des filtres avancés.

**NetFlow** est un outil puissant conçu pour faciliter la prospection B2B en automatisant la recherche d'adresses e-mail professionnelles. Grâce à ses **filtres avancés**, il permet de cibler précisément les prospects en fonction de **critères spécifiques** (secteur, poste, localisation, etc.).

---

## 📖 Sommaire
- [🎯 Objectif](#-objectif)
- [⚙️ Installation](#-installation)
- [📜 Manuel d'utilisation](#-manuel-dutilisation)
- [📈 Résultats](#-résultats)

---

## 🎯 Objectif

✅ **Optimisé pour le démarchage B2B** : Trouvez rapidement des contacts pertinents.  
✅ **Filtres avancés** : Affinez vos recherches selon des critères précis (poste, localisation, mots-clés).

---

## ⚙️ Installation

### 📌 Prérequis
- **Navigateur Firefox** (obligatoire)

### 📥 Étapes d’installation
1. **Cloner le dépôt GitHub** :
   ```bash
   git clone https://github.com/DarkoSancho/NetFlow.git
   cd NetFlow
   ```
2. **Lancer NetFlow.exe** 🚀

---

## 📜 Manuel d'utilisation

### 🚀 Lancement

Au lancement de `NetFlow.exe`, la fenêtre suivante s'affiche :

![image](https://github.com/user-attachments/assets/b8e08908-7471-4940-b64f-62a07d2b07d6)

### 🔍 Options de recherche

#### ✉️ Sélection du domaine e-mail
- Renseigner un domaine d'adresse mail précis (ex: `gmail.com`, `yahoo.fr`).
- Le domaine spécial `[All]` permet d'extraire plusieurs types d'adresses mail.
- Si la case n'est pas cochée, l'extraction des adresses e-mail ne sera pas effectuée.

#### 🌍 Alias de pays
- Indiquez le pays cible de la recherche.
- ⚠️ Seul l'alias du pays (ex: `fr`, `us`, `uk`) est accepté, et non le nom complet.

#### 👩‍🏭 Intitulé du poste
- Entrez le poste recherché (ex: `Développeur`, `Avocat`).

#### ❤️ Mots-clés à inclure
- Ajoutez des mots-clés obligatoires (ex: `ville`, `entreprise`, `secteur`).

#### 💔 Mots-clés à exclure
- Excluez des mots-clés indésirables (ex: `ville`, `entreprise`, `secteur`).

#### 🎓 Niveau d'étude
- Choisissez un niveau d’étude : `Bachelor`, `Master` ou `Doctorat`.

#### 📄 Nombre de pages
- Définissez le nombre de pages à visiter par recherche.

### ⚠️ Règles obligatoires
- 🌶️ Champs obligatoirement cochés
- ⚠️ Il faut cocher au moins une case parmi : `Job title`, `Keyword to include/exclude` et `Level of study` pour assurer le bon fonctionnement du programme.

### 📝 Notes
- Pour renseigner plusieurs mots-clés, les séparer par des virgules `[mot1, mot2, mot3]`.

---

## 📈 Résultats

✅ **Temps d’exécution** : ~20 secondes (avec un captcha à remplir).  
✅ **Un fichier `results.csv` est généré**, contenant les informations suivantes :
- Nom
- Adresse e-mail
- Poste (ou Localisation)
- Entreprise actuelle
- Lien LinkedIn
- Description sommaire (si disponible)

---

## 🔥 Contact & Contribution
📌 **Développé par** : DarkoSancho

🚀 Profitez de NetFlow pour simplifier votre prospection B2B ! 🎯
