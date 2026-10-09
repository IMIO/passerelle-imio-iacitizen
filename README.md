# passerelle-imio-iacitizen

Application passerelle d'iA.Citizen. Elle n'ajoute **aucun connecteur** : elle pose une tâche
horaire (`hourly`) sur les connecteurs **Plone REST API** d'Entr'ouvert existants.

## Fonctionnement

Le cron horaire de passerelle (`passerelle-manage tenant_command cron --all-tenants hourly`,
lancé par uwsgi) appelle `hourly()` sur chaque connecteur qui la surcharge. Pour chaque connecteur
Plone REST API :

1. cherche une requête modèle dont le filtre porte `portal_type=imio.events.Event` ou
   `portal_type=imio.news.NewsItem` ; sinon ne fait rien ;
2. lit les catégories spécifiques de l'entité Smartweb (`imio.events.vocabulary.EventsLocalCategories`
   ou `imio.news.vocabulary.NewsLocalCategories`) ;
3. crée ou met à jour une requête par catégorie : slug `local-<libellé slugifié>`, filtre
   `category_and_topics=<libellé français>`, autres réglages repris de la requête modèle.

Rien n'est jamais supprimé. Si Entr'ouvert définit un jour `PloneRestApi.hourly`, la
synchronisation est désactivée et un avertissement est journalisé au démarrage.

Nécessite imio.smartweb.core >= 1.4.63 côté Smartweb pour que les catégories spécifiques soient
exposées par le `@…_request_forwarder`.

## Installation

Le paquet installe `/etc/passerelle/settings.d/50passerelle_imio_iacitizen.py`, qui active
l'application (`INSTALLED_APPS` / `TENANT_APPS`). Redémarrer passerelle.

## Lancement manuel

```
passerelle-manage tenant_command cron hourly --connector plone-restapi [--connector-slug evenements] -d <tenant>
```

Voir aussi `combo-plugin-imio-iacitizen`, qui affiche ces catégories sur la page « Mon compte ».
