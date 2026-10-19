---
slug: programme-camp
titre: Programme de camp (picasso, programme général, programme détaillé)
signaux: [picasso, programme de camp, programme général, programme détaillé, grille horaire, dossier de camp, horaire du camp, journée type, point fixe, PF, responsable de jour, blocs de programme, camp d'été, camp d'automne, quota d'encadrement]
parametres:
  - {nom: date du camp, obligatoire: true}
  - {nom: forme de camp, obligatoire: false}
  - {nom: branches et nombre de programmes, obligatoire: false}
  - {nom: camp J+S ou non, obligatoire: false}
  - {nom: effectifs, obligatoire: false}
  - {nom: durée, obligatoire: false}
inclut: [activite-js, concept-de-securite]
derive_de: {slug: programme-camp, relu_le: 2026-10-18}
statut: valide
---
Lire tous les fichiers du dossier dans l'ordre.

Livrable principal : le programme de camp, c'est-à-dire le picasso (grille jour × heure) et les fiches de blocs qui le détaillent. Les autres livrables de camp sont en annexe (dernier fichier), sans développement. La fiche d'une activité (modèles de bloc AC et SC compris) se corrige avec `activite-js` ; le concept de sécurité avec `concept-de-securite`. Le « programme général » officiel est la vue d'ensemble ; le « programme détaillé » est le dossier qui le complète ; le picasso tient lieu de programme général (terrain).

## Non-négociables
Portées : `[tous]` camp annoncé J+S ou non ; `[js]` camp annoncé J+S, quelle que soit la date ; `[2027]` camp J+S dès 2027-01-01 ; `[après]` délais de clôture, après le camp. Camp non J+S : seuls les N `[tous]` (N1 à N12) s'appliquent ; N22 vaut aussi pour un camp non J+S annoncé dans la MiData (mainteneur).
N1. [tous] Le programme général indique : thème, responsable de camp, organisateur, coach, lieu et nom du gîte ou de la place, dates, genre de camp, jour-date-responsable de la journée, nom de chaque activité et de son responsable, heures d'arrivée et de départ (Sardine).
N2. [tous] Le responsable de camp transmet le programme général avec l'annonce au RG et au coach, qui donne un retour (Sardine).
N3. [tous] Pour tout camp dès trois jours, J+S ou non, l'annonce passe par la MiData. Deux échéances successives : le responsable de camp complète l'annonce et remet le programme général au RG et au coach 7 semaines avant le début ; le coach transmet l'annonce au MSdS 6 semaines avant (règlement de camp MSdS pour les 6 semaines du coach, liste des délais du cudesch pour les 7 semaines du responsable ; confirmé par la Sardine, J-49 / J-43, calendrier en ligne non ingéré). « Dès trois jours » : choix prudent retenu par le mainteneur. Le règlement s’applique dès trois jours, mais sa clause d’annonce et la Sardine écrivent « plus de 3 jours » ; le formulaire d’autorisation écrit « dès 3 jours ».
N4. [tous] Le dossier de camp est remis au RG et au coach au moins 3 semaines avant le début (règlement de camp MSdS, Sardine). La Sardine place le dossier à 4 semaines (J-28) et l'autorisation à 3 semaines (J-21) : retenir 4 semaines comme date prudente.
N5. [tous] Le dossier contient : programme général, thème et fil rouge, description des blocs, concept de sécurité du camp, règles du camp, arrangements d'équipe (tâches, responsables du jour), liste des participants ; pour une randonnée : temps de marche, cartes, concept de sécurité, programme de mauvais temps (Sardine).
N6. [tous] Chaque bloc est décrit par écrit : nom, jour-date-heure, lieu, fil rouge, responsables, contenu et déroulement chronométré, matériel, variante d'intempéries, concept de sécurité de l'activité si nécessaire (Sardine).
N7. [tous] Jeux, sport et activités du thème sont tous décrits, pas seulement les activités J+S (Sardine).
N8. [tous] Un concept de sécurité existe pour le camp et pour chaque activité à caractère dangereux, J+S ou non (règlement de camp MSdS, Sardine, check-list A de l'autorisation de camp : un concept pour le camp et pour chaque activité dangereuse).
N9. [tous] Les activités d'un domaine de sécurité (montagne, hiver, eau) sont lues et approuvées par un·e expert·e J+S du domaine, qui le confirme par sa signature ; le coach signe ensuite l'autorisation après avis de l'expert·e (règlement de camp MSdS, Sardine, autorisation de camp ; l'ordre des signatures vient du mainteneur).
N10. [tous] Le programme répond aux exigences de la branche et aux fondements du scoutisme ; camp interbranches : programme en grande partie propre à chaque branche (règlement de camp MSdS). Repères des livres de branche : « Selon la branche » (recommandations).
N11. [tous] Camp avec filles et garçons : maîtrise composée de femmes et d'hommes, réflexion sur hébergement, rôles, tâches, santé (règlement de camp MSdS, qui dit « camp mixte » ; dans le vocabulaire des équipes, « mixte » désigne un camp à plusieurs groupes d'âge : ne pas employer le mot ici). Check-list du cudesch pour les unités mixtes : encadrement mixte, tentes ou dortoirs séparés, tâches réparties sans stéréotype.
N12. [tous] Le camp ne peut avoir lieu qu'avec l'autorisation signée du RG et du coach, éventuellement avec compléments à valider avant le camp (règlement de camp MSdS, Sardine).
