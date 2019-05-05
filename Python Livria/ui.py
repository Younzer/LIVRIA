# Librairies 
import numpy as np 
import pandas as pd
import ipywidgets as wg
from IPython.core.display import Image, display

# Fichiers
ratings = pd.read_csv('data/ratings.csv')
books = pd.read_csv('data/books.csv')
tags = pd.read_csv('data/tags.csv')
btags = pd.read_csv('data/book_tags.csv')
# Données pour les thèmes
dataCrit = pd.read_csv('data/df_entree.csv', sep='\t')
dataTheme = pd.read_csv('data/df_sortie.csv', sep='\t')
# On supprime la colonne inutile :
del dataTheme['Unnamed: 0']
del dataCrit['Unnamed: 0']

books = books.drop(['goodreads_book_id','best_book_id', 'work_id','books_count','isbn','isbn13','title','language_code','work_ratings_count','work_text_reviews_count','ratings_count','ratings_1','ratings_2','ratings_3','ratings_4','ratings_5','image_url'], axis=1)

def show_books(books):    
    print('                   Liste des livres qui pourraient vous plaire\n               ===================================================\n')
    for row in books.itertuples():
        print('{} de {} ({}).     Note moyenne: {}/5'.format(str(row[4]),str(row[2]),int(row[3]),str(row[5])))
        display(Image(url= str(row[6]), width=100, height=100))

        
# On définit les critères d'entrée et les thèmes de sortie
themes = dataTheme.columns
criteres = dataCrit.columns

cars = ['Calme', # personnalité
       'Intellectuel',
       'Aventurier',
       'Agite',
       'Sociable',
       'Introverti',
       'Altruiste',
       'Creatif',
       'Reserve',
       'Amusant',
       'Autoritaire',
       'Jaloux',
       'Consciencieux',
       'Curieux',
       'Geek',
       'Sportif',
       'Pantouflard',
       'Esprit']
pts=   ['Esprit','Sport','Dessin','Rien faire','Jeux videos','Cuisine','Theatre','Meditation']
atts=['Voyage','FacileLire','Reflechir','Connaissance','Personnage','Tout','Style']

# On importe les librairies pour diviser le set en un set d'entraînement et un set de test, et entraîner notre modèle
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score
from sklearn.multiclass import OneVsRestClassifier
# On créer un set regroupant critères d'entrées et thèmes à prédire
df_entier = pd.concat([dataCrit,dataTheme], axis=1)
# On crée les set de test et d'entrainement
train, test = train_test_split(df_entier, test_size=0.30, shuffle=True)
# On nettoie les set pour ne garder que les valeurs d'entrée ou de sortie
x_train = train.drop(themes, axis=1)
y_train = train.drop(criteres, axis=1)
x_test = test.drop(themes, axis=1)
y_test = test.drop(criteres, axis=1)

# On utilise un pipeline pour utiliser la régression logistique sur ce problème de classification multitache
LogReg_pipeline = Pipeline([
                ('clf', OneVsRestClassifier(LogisticRegression(solver='sag'), n_jobs=-1)),
            ])

criteres_entree = pd.DataFrame([np.zeros((34), dtype=int)], columns=criteres)
themes_predits = pd.DataFrame([np.zeros((14), dtype=int)], columns=themes)

themes = list(dataTheme.columns.values)
def predict (entree):
    for theme in themes :
        print('**Calculs des prédictions pour {}...**'.format(theme))

        # Training logistic regression model on train data
        LogReg_pipeline.fit(x_train, train[theme])

        # calculating test accuracy
        prediction = LogReg_pipeline.predict(entree)
        themes_predits[theme]=prediction
        print(prediction)
        
        

# On crée les élements interractifs :



    

    


