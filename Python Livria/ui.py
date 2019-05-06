# Librairies 
import numpy as np 
import pandas as pd
pd.set_option('display.max_columns', 40) # Permet d'affichier plus de colonne des dataframes
import ipywidgets as wg
from IPython.core.display import Image, display
# On importe les librairies pour diviser le set en un set d'entraînement et un set de test, et entraîner notre modèle
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score
from sklearn.multiclass import OneVsRestClassifier

# Fichiers
ratings = pd.read_csv('data/ratings.csv')
books = pd.read_csv('data/books.csv')
tags = pd.read_csv('data/tags.csv')
btags = pd.read_csv('data/book_tags.csv')

# Données pour la prédiction des thèmes
dataCrit = pd.read_csv('data/df_entree.csv', sep='\t')
dataTheme = pd.read_csv('data/df_sortie.csv', sep='\t')

# On supprime la colonne inutile :
del dataTheme['Unnamed: 0']
del dataCrit['Unnamed: 0']

# Idem pour les livres on garde que ce dont on a besoin
books = books.drop(['goodreads_book_id','best_book_id', 'work_id','books_count','isbn','isbn13','title','language_code','work_ratings_count','work_text_reviews_count','ratings_count','ratings_1','ratings_2','ratings_3','ratings_4','ratings_5','image_url'], axis=1)

# On définit les critères d'entrée et les thèmes de sortie
themes_name = dataTheme.columns
criteres_name = dataCrit.columns

personnalite = ['Calme', # personnalité
       'Intellectuel',
       'Aventurier',
       'Agite',
       'Sociable',
       'Introverti',
       'Altruiste',
       'Creatif',
       'Reserve',
       'Amusant',
       'Ambitieux',
       'Autoritaire',
       'Jaloux',
       'Consciencieux',
       'Curieux',
       'Geek',
       'Sportif',
       'Pantouflard',
       'Esprit']
passe_temps =   ['Sport','Dessin','Rien faire','Jeux videos','Cuisine','Theatre','Meditation']
attentes =['Voyage','FacileLire','Reflechir','Connaissance','Personnage','Tout','Style']

s_sexe = wg.RadioButtons(options=['Homme', 'Femme'], description='Renseignez votre sexe')#,style=style)
s_pers = wg.SelectMultiple(options=personnalite, description='Sélectionnez les items qui vous définissent le mieux',disabled=False)#, style=style) 
s_passe_t = wg.SelectMultiple(options=passe_temps, description='Quels sont vos passe-temps ?', disabled=False)#, style=style)
s_attentes = wg.SelectMultiple(options=attentes, description="Qu'est ce qui vous plaît dans un livre ?")#, style=style, disabled=False)

# On créer un set regroupant critères d'entrées et thèmes à prédire
df_entier = pd.concat([dataCrit,dataTheme], axis=1)
# On crée les set de test et d'entrainement
train, test = train_test_split(df_entier, test_size=0.30, shuffle=True)
# On nettoie les set pour ne garder que les valeurs d'entrée ou de sortie
x_train = train.drop(themes_name, axis=1)
y_train = train.drop(criteres_name, axis=1)
x_test = test.drop(themes_name, axis=1)
y_test = test.drop(criteres_name, axis=1)

# On utilise un pipeline pour utiliser la régression logistique sur ce problème de classification multitache
LogReg_pipeline = Pipeline([
                ('clf', OneVsRestClassifier(LogisticRegression(solver='sag'), n_jobs=-1)),
            ])

# FONCTIONS

# Pour la sélection des critères  
def display_quest():    
    display(s_sexe, s_pers, s_passe_t, s_attentes)
    
    
# Fonction pour afficher les livres
def show_books(books):    
    print('                   Liste des livres qui pourraient vous plaire\n               ===================================================\n')
    for row in books.itertuples():
        print('{} de {} ({}).     Note moyenne: {}/5'.format(str(row[4]),str(row[2]),int(row[3]),str(row[5])))
        display(Image(url= str(row[6]), width=100, height=100))       
        
        


# On instancie une classe qu'on nomme Livria. Cela va nous permettre de travailler sur des variables sans nous soucier de la réexécution de ce script.


class Livria:    

    def __init__(self):
        self.car_input = pd.DataFrame([np.zeros((34), dtype=int)], columns=criteres_name)
        self.themes_output = pd.DataFrame([np.zeros((14), dtype=int)], columns=themes_name)
    
        # Fonction pour enregistrer les critères sélectionnés        
    def enr_crits (self, s_sexe, s_pers, s_pt, s_attentes):
        # On enregistre les valeurs :
        if ('Homme' == s_sexe):
            self.car_input['Sexe'] = 1
        else:
            self.car_input['Sexe'] = 0

        for c in personnalite:
            if (c in s_pers):
                self.car_input[c] = 1
            else:
                self.car_input[c] = 0
        for p in passe_temps:
            if (p in s_pt):
                self.car_input[p] = 1
            else:
                self.car_input[p] = 0
        for att in attentes:
            if (att in s_attentes):
                self.car_input[att] = 1
            else:
                self.car_input[att] = 0
            # On return les valeurs renseignées
        self.car_input=self.car_input.sort_index(axis=1)
        
    def predict (self):
        themes = list(dataTheme.columns.values)
        for theme in themes :
            print('**Calculs des prédictions pour {}...**'.format(theme))

            # Training logistic regression model on train data
            LogReg_pipeline.fit(x_train, train[theme])

            # calculating test accuracy
            prediction = LogReg_pipeline.predict(self.car_input)
            self.themes_output[theme]=prediction
            print(prediction)