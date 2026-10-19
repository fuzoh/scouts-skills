---
source: msds-hering-camps
version: '2026-10-17'
title: E. Administration des participant·e·s
url: https://hering.scout.ch/fr/lx06gdyius5ahjkpliddmx3o
sha256: 6594f0e89755c3d076f055875a4f59126d914de2461b415efdb3df7f5be6d310
---

<!-- #section-title -->
# E. Administration des participant·e·s

<!-- #qlvnoixi8gkhbilz5247ka05 -->
## Les participant·e·s s'inscrivent eux·elles-mêmes au camp

Lors de la création du camp, l’option « Inscription possible » dans l'onglet *Inscription* doit être sélectionnée. De plus, pour les camps J+S, le paramétrage "Obligatoire" pour la question "Numéro AVS" dans l'onglet *Données pour l'inscription* doit être choisi.

Avec ce paramétrage, les participant·e·s ou leur tuteur·trice·s légaux·ales (TL) peuvent s’inscrire au camp directement dans la [MiData](https://db.scout.ch/fr) avec leur login. Les participant·e·s/TL ne peuvent voir que les camps créés dans un groupe auquel ils·elles appartiennent (par exemple niveau correspondant). L’inscription se fait de la façon suivante :

1. Les participant·e·s/TL se connectent à la MiData et cliquent sur « Activités ». L’aperçu des « Evènements prévus prochainement » apparaît.
2. Les participant·e·s/TL peuvent s’inscrire au camp directement avec le bouton « S’inscrire ».
3. En cliquant sur le nom du camp, les participant·e·s/TL peuvent voir plus d’informations sur le camp.
4. Les participant·e·s/TL remplissent l’inscription (lors de la création du camp, des champs supplémentaires peuvent être enregistrés) et cliquent sur « Inscription ». Il est utile de laisser les participant·e·s/TL remplir les données obligatoires nécessaires au·à la coach pour la BDNS pour que l'importation qui suivra soit plus simple.

- Nom
- Prénom
- Date de naissance
- N°AVS ou PEID

<!-- #lce3mo2o2dujelwxucpthefb -->
## La maîtrise inscrit ou désinscrit les participant·e·s

Si les participant·e·s/TL ne s’inscrivent pas au camp directement dans la MiData, le·la responsable de camp peut alors enregistrer la liste des participant·e·s. Le·la responsable de camp, le·la RG et le·la coach ont accès à la liste des participant·e·s dans la  [MiData](https://db.scout.ch/fr). Ils peuvent y ajouter ou effacer des participant·e·s directement. Cela se fait de la même façon que d’[ajouter des membres de la maîtrise](https://hering.scout.ch/fr/mzv9wh016tndwiqo4xtl8ri7#m1btn4t00ox08mvnsxk0xabh).

Les données des participant·e·s requises pour l’inscription à la REGA et pour le·la coach sont à compléter par le·la responsable de camp. Le numéro AVS n'est à renseigner que si c'est la première fois qu'un·e participant·e participe à une offre J+S dans le groupe. Le paramètre devrait être enregistré comme *optionnel* dans les *données pour l'inscription* du camp.

<!-- #g8f29vlo6upf4zhmmtxrfsf4 -->
## Exporter la liste des participant·e·s à partir de la MiData

Si les participant·e·s sont enregistrés dans la [MiData](https://db.scout.ch/fr), la liste des participant·e·s peut être exportée sous forme de fichier csv pour la [BDNS](https://www.nds.baspo.admin.ch/#/startpage/dashboard) à partir de la MiData. A cet effet, le·la coach procède de la façon suivante :

1. Chercher le camp
2. Cliquer sur « Participants »
3. Cliquer sur « Exporter »
4. Choisir « CSV », « BDNS-camp ». Exporter un fichier csv, qui peut être utilisé pour le téléchargement dans la BDNS.

**Attention avec l’encoding**

C’est important pour l’affichage correct des caractères spéciaux.
Par défaut, la MiData exporte les fichiers csv avec l’encodage UTF-8 (un système de codage de caractères en informatique). Lors de l’import du fichier csv dans la BDNS, on peut choisir ce format pour garantir l’affichage correct des caractères spéciaux.
Si une liste doit être retravaillée dans excel avant d’être importée dans la BDNS, on peut l’exporter sous « Exports » → « Excel » → « BDNS-Camp ». Après l’avoir retravaillé, le fichier est exporté comme fichier csv et importé dans la BDNS avec l’encodage UTF-8.

**Instructions concernant les champs obligatoires**

Certains champs doivent être remplis afin de pouvoir charger le fichier. Lorsqu’une personne participe pour la première fois à une offre J+S au sein d’un groupe, elle doit obligatoirement renseigner son numéro AVS ou PIED lors de son inscription. Le chapitre sur [l'inscription](https://hering.scout.ch/fr/lx06gdyius5ahjkpliddmx3o#lce3mo2o2dujelwxucpthefb) contient une vue d’ensemble. Si des données manquent, il faut demander au·à la responsable de camp de les compléter. Idéalement, les données obligatoires auront déjà été collectées lors de [l’inscription](https://hering.scout.ch/fr/lx06gdyius5ahjkpliddmx3o#lce3mo2o2dujelwxucpthefb).

<!-- #uqjiwckwniqnbu6pvd5x6m9i -->
## Upload de la liste des participant·e·s dans la BDNS

Le fichier csv est importé dans la [BDNS](https://www.nds.baspo.admin.ch/#/startpage/dashboard) par le·la coach. Ceci peut être fait sous l’onglet « Participant·e·s ». Les processus sont détaillés pas à pas (photos incluses) dans les [instructions JS](https://rise.articulate.com/share/HpdR7xgTs3Hro1ALMcCZRVH_ugjXQ2ga#/).

Si le paramétrage et l’inscription des participant·e·s ont été faits de manière correcte, la procédure d’importation devrait se passer sans problème. Deux cas de figure sont possibles dans ce cas :

- Bernard est sur la liste avec son numéro AVS : il peut être importé. Si l’on observe une ou des différence(s) entre MiData et la BDNS au niveau de son nom, de son prénom et/ou de sa date de naissance, il faut modifier les données enregistrées dans son profil personnel sur MiData en conséquence.
- Donna est sur la liste sans son numéro AVS et la BDNS indique « Trouvé dans la BDNS » : elle peut être importée.

Les cas de figure possibles générant des erreurs sont les suivants :

- Nadine est sur la liste sans numéro AVS et la BDNS indique « Pas trouvé dans la BDNS » : elle ne peut pas être importée. Il faut annuler l’importation, aller sur « Ajouter un participant » et chercher Nadine dans la liste. Nadine est dans la liste, il faut comparer ses nom, prénom et date de naissance et corriger les erreurs sur MiData. L’importation peut ensuite être recommencée.
- Simon est sur la liste sans numéro AVS et la BDNS indique « Pas trouvé dans la BDNS » : il ne peut pas être importé. Il faut annuler l’importation, aller sur « Ajouter un participant » et chercher Simon dans la liste. Simon n’est dans la liste, il faut donc se procurer son numéro AVS et l’ajouter à ses données d’inscription sur MiData. L’importation peut ensuite être recommencée.

Si l’importation ne fonctionne pas pour tou·te·s les participant·e·s, nous recommandons d’annuler l’importation, de trouver la source de l’erreur, de corriger les données dans le fichier d’exportation, de transmettre la liste aux personnes concernées pouvant modifier les données sur MiData et de recommencer l’importation. Cela permet d’assainir les données sur MiData et d’éviter des erreurs futures.
