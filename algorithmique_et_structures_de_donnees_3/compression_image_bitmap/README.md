# Compression d'images bitmap

## But du projet 

### (sujet dans le dossier ./doc)

Le projet avait pour but l'implémentation différents algorithmes de compression (avec et sans perte) d’une image bitmap enregistrée au format PNG et d’observer les effets sur sa qualité et son poids.

Pour gagner de la place, il est possible de réduire l’arbre par élagage (élimination de feuilles) : si toutes les feuilles d’un même nœud ont la même couleur, on peut alors supprimer ces quatre feuilles ; on fait ainsi diminuer l’arbre (gain d’espace mémoire) et on rend l’accès à la couleur d’un pixel plus rapide (gain de temps). Cette compression se fait sans perte, i.e., l’image n’est pas dégradée.

En autorisant un certain niveau de perte, on peut réduire l’arbre plus fortement. Nous proposons deux méthodes s’appuyant toutes deux sur l’écart colorimétrique : soient F1, ... , F4 les quatre feuilles d’un même nœud N. On note (Ri , Vi , Bi ) la couleur de chaque feuille Fi .

On considère deux méthodes de compression, l’une basée sur une qualité minimale, l’autre sur un poids maximal :

1. On peut définir une dégradation maximale autorisée sous la forme d’un entier ∆ ∈ 0..192 : les feuilles F1, ... , F4 d’un même nœud N sont supprimées si et seulement si Λ ≤ ∆.

2. On peut également définir la dégradation en fonction d’un poids maximum souhaité, ce qui peut se traduire par un entier Φ > 0 représentant le nombre maximum de feuilles autorisées dans l’arbre. Les feuilles sont alors élaguées par ordre croissant de Λ. Voir Figure 4 par exemple.

<br/>

## Execution

Exécution en mode Interactif : <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;` chmod a+x exec.sh && ./exec.sh `


Exécution en mode Non-Interactif : <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;` chmod a+x exec.sh && ./exec.sh image.png delta phi `

avec :
* image.png : une image au format PNG.
* delta : un nombre entre [0 , 255].
* phi   : un nombre > 0.


<br/>

## Cadre du projet 

Projet réalisé dans le cadre de l'unité d'enseignement algorithme et programmation 3 en 2020/2021, au sein de l'Université de Nantes.
 
<br/>

## Auteurs

COUTAND Bastien (bastien.coutand@etu.univ-nantes.fr), <br>
MAHBOUBI Saad   (saad.mahboubi@etu.univ-nantes.fr)

<br/>

## Dernière mise à jour
 
05/12/2020 à 20h07 par COUTAND Bastien.
 
