/*
 * @projet : l’objet de ce projet est d’implémenter un algorithme de tri par fusion multiple de monotonies. 
 *           Ces données seront stockées dans un chaînage qui sera ensuite partitionné en morceaux croissants puis ces morceaux seront 
 *           fusionnés en une nouvelle liste triée.
 *
 * @cadreDuProjet: projet dans le cadre de L'UE : algorithme et programmation 2019/2020, au sein de l'Université de Nantes.
 *
 * @MisAJour : 28/12/2019 à 17h34 par GARNIER Cyprien.
 *
 * @Createur : COUTAND Bastien (bastien.coutand@etu.univ-nantes.fr),
 *             GARNIER Cyprien (cyprien.garnier@etu.univ-nantes.fr).
 */

#include <iostream> 
#include <string>
#include <fstream>
#include <ctime> // time(), clock_t, clock(), CLOCKS_PER_SEC
#include <math.h> // partie entière (floor)

using namespace std;

// −−−−−−−−−−−−−−−− Types −−−−−−−−−−−−−−−−−−−−−−−−−−−−−
typedef string DATATYPE; // possibilité de changer le type, aucun changement dans le programme de la partie A,B,C et D.

typedef struct _datum {
    DATATYPE valeur; 
    _datum * suiv; // maillon suivant.
} dataType;

typedef dataType * p_data;

typedef struct _datallst{
    int capa; // capacité totale du tableau.
    int nbMono; // capacité effective du tableau.
    p_data * monotonies; // valeur du tableau.
} datalistes;


//−−−−−−−−−−−−−−−−−−− PARTIE A −−−−−−−−−−−−−−−−−−−−−−−−−−//
/**
 * @param uneval : la valeur à ajouter dans le chaînage.
 * @param chain : le chaînage où l'on souhaite y ajouter une valeur.
 * @role: ajoute devant le chaînage chain, un nouveau maillon avec la valeur uneval.
 **/
p_data ajoutDevant(DATATYPE uneval, p_data chain){
    p_data ptr = new dataType;
    ptr -> valeur = uneval;
    ptr -> suiv = chain;

    return ptr;
}

// −−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−

/**
 * @param chain : le chaînage à afficher.
 * @role: affiche tout un chaînage.
 **/
void aff(p_data chain){
    p_data stock = chain;
    
    cout << "-> ";

    while(stock != nullptr){
        cout << stock -> valeur << " -> ";
        stock = stock -> suiv; 
    }

    cout << "fin" << endl;
}
// −−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−
/**
 * @param sentinelle: stop l'ajout de chaînon si l'utilisateur saisit cette valeur.
 * @role: ajouter des data devant et retourne la tête.
 * @return : maillon de tête.
 **/
p_data saisieBorne(DATATYPE sentinelle){
    DATATYPE newValeur;
    p_data stock = new dataType;

    cout << "ajouter votre premiere valeur : ";
    cin >> newValeur;

    stock -> valeur = newValeur;
    stock -> suiv = nullptr;

    while(sentinelle != newValeur){
        cout << "ajouter votre une nouvelle valeur : ";
        cin >> newValeur;

        stock = ajoutDevant(newValeur, stock);
    }
    

    return stock;
}
// −−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−
/**
 * @param nb : le nombre de maillons a créé.
 * @role: fonction retournant un chaînage avec des valeurs rentrées par l'utilisateur, dans l'ordre de saisie
 *        (le premier à la fin du chaînage et le dernier au début du chaînage).
 * @preondition: nb >= 0. 
**/
p_data saisieNombre(int nb) { 
    p_data ptr = nullptr;
    string valeur;
        
    for(int i = 0; i < nb; i++) {
        cout << "saisir la valeur du " << nb-i << " maillon" << endl;
        cin >> valeur;
        ptr = ajoutDevant(valeur, ptr);
    }

    return ptr;
}

// −−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−
/**
 * @param chain : le chaînage à retourner.
 * @role: inverse un chaînage. S'il est trié dans l'ordre croissant alors 
 *        il sera trié par ordre décroissant à la fin du chaînage.
 * @precondition: chain soit différent null.
 * @return : un chaînage inversé.
 **/
void retournement(p_data & chain) {
    p_data avant = nullptr, apres = chain -> suiv;
    
    while (apres != nullptr) {
        chain -> suiv = avant;
        // le précédent deviens le suivant.
        avant = chain;
        chain = apres;
        apres = chain -> suiv;
    }
 
    chain -> suiv = avant; // on change le dernier.
}

// −−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−
/**
 * @param chain1 : premier chaînage.
 * @param chain2 : second chaînage.
 * @role: fusionne deux chaînages terminés par nullptr dans l'ordre croissant.
 * @precondition: les chaînages sont triés par ordre croissant.
 * @postconditions: le chaînage est rempli et trié par ordre croissant.
 * @return: un chaînage trié par ordre croissant.
 **/
p_data fusion(p_data chain1, p_data chain2) {
    p_data chainFu = nullptr;

    // tant qu'il reste encore des maillons dans les deux chaînages.
    while (chain1 != nullptr && chain2 != nullptr) {

        if (chain1 -> valeur <= chain2 -> valeur) {
            chainFu = ajoutDevant(chain1 -> valeur, chainFu);
            chain1 = chain1 -> suiv;
        } 
        else {
            chainFu = ajoutDevant(chain2 -> valeur, chainFu);
            chain2 = chain2 -> suiv;
        }
    }

    // quand un des chaînages est arrivé à Null : on rajoute le reste des valeurs de l'autre chaînage à chainFu.
    // permet aussi de gérer le cas : si un des chaînages est null en paramètre de la fonction.
    while (chain2 != nullptr) {
       chainFu = ajoutDevant(chain2 -> valeur, chainFu);
       chain2 = chain2 -> suiv;
    }

    while (chain1 != nullptr) {
       chainFu = ajoutDevant(chain1 -> valeur, chainFu);
       chain1 = chain1 -> suiv;
    }

    // retournement du chaînage car il est dans l'ordre décroissant.
    retournement(chainFu);
    return chainFu;
}

// −−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−
/**
 * @param chain1 : premier chaînage.
 * @param chain2 : second chaînage.
 * @role: fusionne deux chaînages terminés par nullptr dans l'ordre croissant, de façon récursive.
 * @precondition: les chaînages sont triés par ordre croissant.
 * @postconditions: le chaînage est rempli et trié par ordre croissant.
 * @return : un chaînage trié par ordre croissant.
 **/
 p_data fusion_rec(p_data chain1, p_data chain2, p_data & chainFu) {

    // si on arrive au bout des deux chaînage.
    if (chain1 == nullptr && chain2 == nullptr) {
        retournement(chainFu); // on le trie par ordre croissant (car trié par ordre décroissant).
        return chainFu;
    } 
    else {
       // quand un des chaînages est arrivé à Null : on rajoute le reste des valeurs de l'autre chaînage à chainFu.
       // permet aussi de gérer le cas : si un des chaînages est null en paramètre de la fonction.
        if (chain1 == nullptr) {
            chainFu = ajoutDevant(chain2 -> valeur, chainFu);
            chain2 = chain2 -> suiv;
        } 
        else if (chain2 == nullptr) {
            chainFu = ajoutDevant(chain1 -> valeur, chainFu);
            chain1 = chain1 -> suiv;
        } 
        // cas normal, on affecte dans le nouveau chaînage en fonction de la valeur des maillons du chaînage 1 et 2.
        else if (chain1 -> valeur <= chain2 -> valeur) {
            chainFu = ajoutDevant(chain1 -> valeur, chainFu);
            chain1 = chain1 -> suiv;
        } 
        else {
            chainFu = ajoutDevant(chain2 -> valeur, chainFu);
            chain2 = chain2 -> suiv;
        }   

        return fusion_rec(chain1, chain2, chainFu);
    }
 }

// −−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−
/**
 * @param chain : chaînage.
 * @role: compte le nombre de monotonies croissantes dans un chaînage.
 * @return : le nombre de monotonies.
 **/
int nbCroissances(p_data chain){
    p_data stockChain = chain;
    p_data stockChainPrecedent = chain;
    int result = 1;

    while (stockChain -> suiv != nullptr){
        if((stockChainPrecedent -> valeur) > (stockChain -> valeur)){
            result++;
        }

        stockChainPrecedent = stockChain ;
        stockChain = stockChain -> suiv;  
    }  

    return result;      
}

// −−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−
/**
 * @param chain : premier chaînage.
 * @param mono : première monotonie croissante
 * @role: place dans le chaînage mono la première monotonie croissante de chain et l’en retire.
 * @precondition: chain doit comporter au moins une monotonie.
 * @postcondition: chain aura une monotonie en moins et mono aura une monotonie.
 **/
void extraireCroissances(p_data & chain, p_data & mono) {
    p_data stockChain;
    bool conditionEnd;

    conditionEnd = false;

    mono = chain;
    stockChain = chain;
    
    //parcourt le chainage jusqu'au dernier maillon ou s'arréte si conditionEnd est vrai.
    while (!conditionEnd && (stockChain -> suiv != nullptr)) {
        //la variable de stockage prend la valeur du maillon suivant.
        stockChain = stockChain -> suiv;

        //si la valeur du maillon stocké est inferieur au maillon précedent, stop la boucle.
        if ((stockChain -> valeur) < (chain -> valeur)){
            conditionEnd = true;
            chain -> suiv = nullptr;
            chain = stockChain;
        }
        else {
            chain = chain ->suiv;
        }
    }
    //si le chainage a été parcouru en entier et que la condition d'arret est encore false, cela veut dire que le chainage est une et même monotonie.
    if (!conditionEnd) {
        chain = nullptr;
    }
}


// −−−−−−−−−−−−−−−−−−− PARTIE B −−−−−−−−−−−−−−−−−−−−−−−−−− //
/**
 * @param nb : nombre de maillons à créer.
 * @role: créer et renvoie une structure de type datalistes.
 * @return un datalistes.
 **/
datalistes iniT(int nb) {
    datalistes dataTab;
    dataTab.nbMono = 0;
    dataTab.capa = nb;
    dataTab.monotonies = new p_data[nb];
    return dataTab;
}

// −−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−
/**
 * @param chain : chaînage à insérer.
 * @param mono : le tableau de monotonies croissantes.
 * @role: ajoute dans le tableau, le chaînage chain.
 * @precondition: nbmono < capa.
 * @postcondition: le tableau aura une valeur de plus.
 **/
void ajouterFin(p_data chain, datalistes & mono) {
    if (mono.nbMono < mono.capa) {
        // applique la valeur à mono.nbMono puis incrémente.
        mono.monotonies[mono.nbMono++] = chain;
    }
}

// −−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−
/**
 * @param mono : tableau de monotonies croissantes.
 * @role: affiche les valeurs stockées dans le tableau.
 * @precondition: mono.nbMono > 0.
 **/
void affT(datalistes mono) {
    for (int i = 0; i < mono.nbMono; i++) {
        cout << i+1 << " case : "; aff(mono.monotonies[i]);
    }
}
// −−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−
/**
 * @param mono : le tableau de monotonies croissantes.
 * @role: supprime du tableau mono le dernier chaînage (la dernière case).
 * @precondition: mono != null.
 * @postcondition: 
 * @return renvoie le dernier chaînage encore stocké
 **/
p_data suppressionFin(datalistes & mono) {
    mono.nbMono--;
    return mono.monotonies[mono.nbMono];
}
// −−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−
/**
 * @param mono : le tableau de monotonies croissantes.
 * @role: ajoute bout à bout de tous les chaînages de mono dans un nouveau chaînage et 
 *        les suppriment du tableau mono.
 * @precondition: mono.nbMono > 0.
 * @postcondition: le nouveau chaînage sera valué par des monotonies croissantes.
 * @return un chaînage composé de tous les chaînage de mono.
 **/
p_data suppressionTotale(datalistes & mono) {
    p_data nouvelChain = mono.monotonies[0];
    p_data ptr = nouvelChain;

    // parcourt tout le tableau.
    for (int i = 1; i < mono.nbMono; i++) {
       // parcourt la monotonie jusqu'à l'avant-dernier maillon. 
       while (ptr -> suiv != nullptr) {
           ptr = ptr -> suiv;
       }
       // et y ajoute la prochaine monotonie.
       ptr -> suiv = mono.monotonies[i];
    }

    mono.nbMono = 0; // vide le tableau.

    return nouvelChain;
}
   

// −−−−−−−−−−−−−−−−−−− PARTIE D −−−−−−−−−−−−−−−−−−−−−−−−−− //
/**
 * @param chain : premier maillon du chaînage.
 * @role: rentrer dans un tableau les monotonies croissantes du chaînage contenu 
 *        dans chain.
 * @return un tableau avec tout les chaînages croissant.
 **/
datalistes separation(p_data & chain){
    datalistes dataTab;
    p_data mono;  
    int nbMono;

    nbMono = nbCroissances(chain);
    dataTab = iniT(100);
    dataTab.nbMono = nbMono;

    for(int i = 0; i < nbMono; i++){
        extraireCroissances(chain,mono);
        dataTab.monotonies[i] = mono;
    }

    return dataTab;
}


// −−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−
/**
 * @param tabmono : le tableau à trier.
 * @role: effectue une fusion multiple des monotonies stockées dans le tableau, pour ne conserver à la fin 
 *        qu’un seul chaînage trié dans la première case.
 * @precondition: nbMono > 1.   
 * @postcondition: le tableau ne contiendra qu'une case et la chaîne sera trié.
 **/
void trier(datalistes & tabmono) {
    // parcourt de l'avant-dernière case jusqu'à la première.
    for (int i = tabmono.nbMono - 2; i >= 0; i--) {
        tabmono.monotonies[i] = fusion(tabmono.monotonies[i], tabmono.monotonies[i+1]);
    }
    
    tabmono.nbMono = 1;
}

// −−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−
/**
 * @param chain : la chain à trier.
 * @role: trie un chaînage en utilisant une fusion multiple.
 * @precondition: chain doit avoir au moins deux maillons.
 * @postcondition: le nouveau chaînage sera trié.
 **/
void trier(p_data & chain) {
    datalistes fusion;
    //sépare le chaînage en monotonies croissantes.
    fusion = separation(chain);
    //fusionne les monotonies et les conserve un seul chainage trié dans la première case.
    trier(fusion);
    chain = fusion.monotonies[0];
}

// −−−−−−−−−−−−−−−−−−− PARTIE E −−−−−−−−−−−−−−−−−−−−−−−−−− //
/**
 * @param nb : nombre de mots à lire dans le fichier.
 * @role: lit nb mots d'un fichier.
 * @precondition: nb > 0.
 * @return un chaînage composé des mots lues.
 **/
p_data lecture(int nb, string nomFichier) {
    p_data chain = new dataType;
    p_data ptr = chain;

    ifstream monFlux(nomFichier);  // ouverture d'un fichier en lecture.

    if(monFlux) {

        // stocke les mots dans le chaînage.
        for (int i = 0; i < nb; i++) {
            monFlux >> ptr -> valeur;

            ptr -> suiv = new dataType;
            ptr = ptr -> suiv;       
        }  
        ptr -> suiv = nullptr;
    } 
    else {
        cout << "ERREUR: Impossible d'ouvrir le fichier" << endl;
    }

    monFlux.close(); // fermeture du flux.
    return chain;
}

/**
 * @role: calcule et affiche le temps de calcul de la fonction trié pour un nombre 
 *        croissant de mots (multiplié par 4 à chaque tour de boucle) au début d’un fichier texte.
 **/
void etude(char *text) {
    clock_t monChrono;
    const int Nvals = 50; // nombre d'essaies de la fonction trier.
    int nbMot;
    p_data texte;

    // Affichage des en-têtes de colonne (séparés par des tabulations).
    cout << "temps \t" << "nombre de mots a trier \t" << endl;

    for (int i = 0; i < Nvals; i++) {
        // choix du nombre de mots croissant.
        nbMot = i * 4;
        texte = lecture(nbMot, text);

        monChrono = clock(); // démarrage du Chronomètre.
           
            trier(texte); // exécution de la fonction étudiée.

        monChrono = clock() - monChrono; // arrêt du Chronomètre.

        // Affichage des informations (séparées par des tabulations).
        cout << (long)floor(double(monChrono)) << "\t" << nbMot << "\t"  << endl;
        //aff(texte); // possibilité d'affiché le texte, pas beaucoup de visibilité dans la console.
    }

    cout << "Remarque : temps donnés en 1/" << CLOCKS_PER_SEC << " secondes " << endl;
}

//−−−−−−−−−−−−−−−−−−− MAIN −−−−−−−−−−−−−−−−−−−−−−−−−− //
int main(int argc, char *argv[]) {
//--------------- Variables ----------------//
  
    p_data pointeur1 = nullptr; // pointeur utilisé pour la création du 1er maillon.
    p_data pointeur2 = nullptr; // pointeur utilisé pour les procédures aujoutdevant et ajouterFin.
    p_data pointeur3 = nullptr; // pointeur utilisé pour les fonctions fusion, fusion_rec, extraireCroissance et les procédures aff et saisieNombre.
    p_data pointeur4 = nullptr; // pointeur utilisé pour la procédure suppressionTotale.
    p_data pointeur5 = nullptr; // pointeur utilisé pour la fonction extraireCroissance.
    p_data pointeur6 = nullptr; // pointeur utilisé pour la fonction separartion.
    p_data pointeur7 = nullptr; // pointeur utilisé pour la procédure trier.
    p_data chainFu = nullptr; // pointeur de stockage de la valeur de la fonction fusion_rec.
    
    int nb; // nombre de maillon à créer.
    DATATYPE sentinelle; //valeur de tête du chaînage.
    
    datalistes dataChaine; // tableau utilisé par les procédures suppressionTotale et suppressionFin.
    datalistes dataChaine2; // tableau utilisé par lafonction séparation.

//--------------- Tests ----------------//
    
    // premier maillon
    pointeur1 = new dataType;
    pointeur1 -> valeur =  "450927186";
    pointeur1 -> suiv = nullptr;
    cout << "valeur : " << (*pointeur1).valeur << endl;

     
    //------------- test fonction ajoutDevant et aff ----------------//
    cout << " \n------------- test fonction ajoutDevant et aff ----------------" << endl;
    pointeur2 = ajoutDevant("504849460", pointeur1);
    cout << "valeur : " << (*pointeur2).valeur << endl;

    aff(pointeur2);
    
    
    //------------- test fonction saisieNombre ----------------//
    cout << " \n------------- test fonction saisieNombre ----------------" << endl;
    cout << "saisir le nombre de maillon voulu" << endl;
    cin >> nb;
    pointeur3 = saisieNombre(nb);

    aff(pointeur3);

     
    //------------- test fonction saisieBorne ----------------//
    cout << "\n ------------- test fonction saisieBorne ----------------" << endl;
    cout << "saisissez votre valeur de tete ";
    cin >> sentinelle;
    p_data test = saisieBorne(sentinelle);
    aff(test);

    
    //------------- test fonction fusion ----------------//
    cout << " \n------------- test fonction fusion ----------------" << endl;
    pointeur4 = ajoutDevant("999999999", pointeur4);
    pointeur4 = ajoutDevant("22", pointeur4);

    cout << "pointeur 4 :"; aff(pointeur4);

    cout << "le trie par fusion normal donne : "; aff(fusion(pointeur3, pointeur4));


    //------------- test fonction fusion_rec ----------------//
    cout << " \n------------- test fonction fusion_rec ----------------" << endl;
    cout << "le trie par fusion recursif donne : "; aff(fusion_rec(pointeur3, pointeur4, chainFu));


    //------------- test fonction nbCroissances ----------------//
    cout << " \n------------- test fonction nbCroissance ----------------" << endl;
    cout << "nombre de monotonie croissante : " << nbCroissances(test) << endl;
    

    //------------- test procedure extraireCroissances -------------//
    cout << " \n------------- test procedure extraireCroissances ----------------" << endl;
    pointeur5 = ajoutDevant("254", pointeur5);
    pointeur5 = ajoutDevant("3", pointeur5);
    
    cout << "chain : ";  aff(pointeur3); cout << endl;
    cout << "mono : ";   aff(pointeur5); cout << endl;
    
    extraireCroissances(pointeur3, pointeur5);
    
    cout << "chain : ";  aff(pointeur3); cout << endl;
    cout << "mono : ";   aff(pointeur5); cout << endl;
    
    
    //------------- test fonction iniT ----------------//
    dataChaine = iniT(5);
    

    //------------- test procedure affT et fonction ajouterFin ----------------//
    cout << " \n------------- test procedure affT et fonction ajouterFin ----------------" << endl;
    ajouterFin(pointeur4, dataChaine);
    ajouterFin(pointeur2, dataChaine);

    cout << "l\'affichage du tableau donne : " << endl; 
    affT(dataChaine); cout << endl;

    suppressionFin(dataChaine);

    affT(dataChaine);
    

    //------------- test fonction separtion ----------------//
    cout << " \n------------- test fonction separation ----------------" << endl;
    cout << "saisir le nombre de maillon voulu" << endl;
    cin >> nb;
    pointeur6 = saisieNombre(nb);
    cout <<"chainge avant separation : ";
    aff(pointeur6);
    dataChaine2 = separation(pointeur6);
    cout <<"chainage apres separation : ";
    aff(pointeur6);
    affT(dataChaine2);


    //------------- test suppressionTotale ----------------//
    cout << " \n------------- test fonction suppressionTotale ----------------" << endl;
    affT(dataChaine);
    pointeur4 = suppressionTotale(dataChaine);
    cout << "le nouveau pointeur4 vaut : "; aff(pointeur4);


    //------------- test trier 1er version ----------------//
    cout << " \n------------- test trier 1er version ----------------" << endl;
    ajouterFin(pointeur4, dataChaine);
    ajouterFin(pointeur2, dataChaine);
    
    affT(dataChaine);
    trier(dataChaine);
    cout << "le nouveau tableau est : " << endl; 
    affT(dataChaine);
    

    //------------- test trier 2eme version ----------------//
    cout << " \n------------- test trier 2eme version ----------------" << endl;
    cout << "saisir le nombre de maillon voulu" << endl;
    cin >> nb;
    pointeur7 = saisieNombre(nb);
    cout << "chainage avant fusion multiple :" << endl;
    aff(pointeur7);
    trier(pointeur7);
    cout << "chainage apres fusion multiple :" << endl;
    aff(pointeur7);


    //--------------- Etude ----------------//
    cout << " \n------------- etude de la fonction trier ----------------" << endl;
    etude(argv[0]);


    //--------------- Desallocation ----------------//
    delete pointeur1;
    delete pointeur2;
    delete pointeur3;
    delete pointeur4;
    delete pointeur5;
    delete pointeur6;
    delete pointeur7;
    delete chainFu;

    return 0;
}
