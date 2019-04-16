# -*- coding: utf-8 -*-
"""
Éditeur de Spyder

Ceci est un script temporaire.
"""
# Librairies
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
# Plot data
import matplotlib.pyplot as plt

# Lecture du fichier 'df_sortie.csv' contenant les thèmes choisis  et vectorisés des réponses du questionnaire.
dataNotes = pd.read_csv('./data/ratings.csv')

# On montre les premières lignes de dataTheme
print(dataNotes.head())

print('Les dimensions de dataNotes sont de : ' + str(dataNotes.shape))

n_users = dataNotes['user_id'].nunique()
n_items = dataNotes['book_id'].nunique()
print ("Nombre d'utilisateurs = " + str(n_users) + ' | Nombre de livres = ' + str(n_items))

train_data_notes, test_data_notes = train_test_split(dataNotes, test_size=0.25)
train_data_notes_matrix = np.zeros((n_users,n_items))
