from models import SourceScrapingWeb
from .. import db

# Supposons que vous ayez extrait les données suivantes de l'image :
data = [
    {
        'url': 'http://example.com',
        'typeContenu': 'text/html',
        'autoScraping': True,
        'frequence': 'daily'
    },
    {
        'url': 'http://example.com',
        'typeContenu': 'text/html',
        'autoScraping': True,
        'frequence': 'daily'
    }
]

# Pour chaque dictionnaire dans les données :
for item in data:
    # Créez une nouvelle instance de SourceScrapingWeb avec les données
    source = SourceScrapingWeb(
        url=item['url'],
        typeContenu=item['typeContenu'],
        autoScraping=item['autoScraping'],
        frequence=item['frequence']
    )
    # Ajoutez la nouvelle source à la session
    db.session.add(source)

# Validez la session pour enregistrer les modifications dans la base de données
db.session.commit()
