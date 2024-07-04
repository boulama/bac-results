# Extracteur et Analyseur des Résultats du Baccalauréat 2024 du Niger

## Motivation

Le site officiel du Baccalauréat 2024 du Niger (https://www.officebacniger.com/) ne présente les résultats que jury par jury. Cet outil extrait et agrège les données de tous les jurys, offrant une vue d'ensemble complète des résultats du Baccalauréat 2024.

## Fonctionnalités

- Extraction des données de résultats de tous les jurys
- Agrégation des statistiques de l'ensemble des jurys
- Visualisations des résultats globaux
- Sauvegarde des données extraites pour une analyse ultérieure

## Prérequis

- Python 3.6 ou supérieur
- Bibliothèques Python : requests, beautifulsoup4, matplotlib, tqdm, python-dotenv

## Configuration

1. Clonez cette repo sur votre machine locale.
2. Installez les dépendances :
   ```
   pip install -r requirements.txt
   ```
3. Créez un fichier `.env` à la racine du projet avec les informations suivantes :
   ```
   COOKIE=votre_cookie_ici
   TOKEN=votre_token_ici
   ```

Pour obtenir le cookie et le token ([tuto video](assets/tutorial.mp4)):
1. Naviguez sur le site https://www.officebacniger.com/
2. Ouvrez les outils de développement de Chrome (F12)
3. Allez dans l'onglet "Network"
4. Effectuez une recherche de resultats (selectionnez un jury et le groupe, cliquez sur "voir les statistiques")
5. Trouvez une requête vers le site et copiez le cookie et le token depuis les en-têtes de la requête

<center><img src="assets/cookie-and-token.jpg" width="500"></center>

## Utilisation

Exécutez le script :
```
python extract.py
```

Le script va :
1. Extraire les données de tous les jurys
2. Traiter et agréger les statistiques
3. Sauvegarder les résultats dans `stats_final.json` et `tallies.json`
4. Afficher un graphique circulaire des résultats globaux

## Structure du Code

- `BacStatsFetcher` : Gère les requêtes HTTP vers le site officiel
- `DataExtractor` : Parse le HTML et extrait les données pertinentes
- `StatisticsProcessor` : Traite et agrège les statistiques
- `DataVisualizer` : Crée les visualisations des données

## Note

Cet outil est conçu à des fins éducatives et analytiques. Veuillez respecter les conditions d'utilisation du site officiel et éviter les requêtes excessives sur une courte période.

## Contribution

Les contributions pour améliorer l'outil ou étendre ses fonctionnalités sont les bienvenues. Veuillez soumettre une demande de pull ou ouvrir une issue pour discuter des modifications proposées.
