Bienvenue sur notre projet Hadoop : ligne de transilien N

MS SIO 2019-2020 - CentraleSupélec

Membres de l'équipe : 
DESMARCHELIER Pierre,
LY Stéphane,
NGBANGO Soulémanou,
RHERMINI Acheq

# Installation : 

1) Installer l'outil Virtualbox : https://www.virtualbox.org/wiki/Downloads (alternativement, on peut également passer par une instance EC2)
2) Télécharger la version 2.6.5 de la sandbox HDP : https://www.cloudera.com/downloads/hortonworks-sandbox.html
3) Importer l'image de la machine virtuelle téléchargée dans Virtualbox et installer HDP
4) Se connecter à sa machine virtuelle en SSH
5) Lancer le docker engine avec la commande sudo dockerd
6) Lancer le docker hdp puis le docker proxy avec la commande docker start
7) Entrer dans le docker hdp avec la commande docker exec
8) Cloner ce repository dans /usr/hdp/current/KafkaBroker
9) ...

Note : afin de pouvoir se connecter à HDFS et faire les reqûetes avec Tableau, un plugin spécifique peut être nécessaire : https://www.cloudera.com/downloads/hdp.html
