/**
 *
 * Copyright (C) 2017 Emmanuel DESMONTILS
 *
 * This library is free software; you can redistribute it and/or modify
 * it under the terms of the GNU Lesser General Public License as
 * published by the Free Software Foundation; either version 2.1 of the
 * License, or (at your option) any later version.
 *
 * This library is distributed in the hope that it will be useful, but
 * WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public
 * License along with this library; if not, write to the Free Software
 * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307
 * USA
 *
 *
 *
 * E-mail:
 * Emmanuel.Desmontils@univ-nantes.fr
 *
 *
 **/


/**
 * Automate.java
 *
 * @Created: 2019-12-26
 * @author COUTAND Bastien, GARNIER Cyprien
 * @version 1.1
 * @what implementation of produit, mise en étoile et transposer
 */

package JFSM;

import java.util.*;

import org.xml.sax.*;
import org.xml.sax.helpers.DefaultHandler;
import org.xml.sax.helpers.XMLReaderFactory;
import javax.xml.parsers.SAXParserFactory;
import javax.xml.parsers.ParserConfigurationException;
import javax.xml.parsers.SAXParser;

import java.io.FileOutputStream;
import java.io.FileWriter;
import java.io.File;

public class Automate implements Cloneable {
    public Map<String,Etat> Q;
    public Set<String> F, I;
    public Set<String> A;
    public Stack<Transition> histo;
    public Set<Transition> mu;
    protected String current;

    /**
     * Constructeur de l'automate {A,Q,I,F,mu}
     * @param A l'alphabet de l'automate (toute chaîne de caratères non vide et différente de \u03b5)
     * @param Q l'ensemble des états de l'automate
     * @param I l'ensemble des états initiaux de l'automate
     * @param F l'ensemble des états finaux de l'automate
     * @param mu la fonction de transition de l'automate
     * @exception JFSMException Exception si un état qui n'existe pas est ajouté comme état initial ou final
     */
    public Automate(Set<String> A, Set<Etat> Q, Set<String> I, Set<String> F, Set<Transition> mu) throws JFSMException {
        // Ajout de l'alphabet
        assert A.size()>0 : "A ne peut pas être vide" ;
        for(String a : A) {
            if ((a.equals(""))||(a.equals("\u03b5"))) throw new JFSMException("Un symbole ne peut pas être vide ou \u03b5");
        }
        this.A = A;
        this.mu = new HashSet<>();

        // Ajout des états
        assert Q.size()>0 : "Q ne peut pas être vide" ;
        this.Q = new HashMap<>();

        for (Etat e : Q)
            if (this.Q.containsKey(e.name)) System.out.println("Etat dupliqué ! Seule une version sera conservée.");
            else this.Q.put(e.name,e);

        // Création de l'historique (chemin)
        this.histo = new Stack<>();

        // Ajout des transitions
        this.mu.addAll(mu);

        // On collecte les états initiaux, on les positionne comme tel. S'il n'existe pas, il est oublié.
        // assert I.size()>0 : "I ne peut pas être vide" ;
        this.I = new HashSet<>();
        for (String i : I) setInitial(i);

        // On collecte les états finaux, on les positionne comme tel. S'il n'existe pas, il est oublié.
        this.F = new HashSet<>();
        for(String f : F) setFinal(f);
    }

    public Object clone() {
        Automate o = null;
        try {
            o = (Automate)super.clone();
            // o.Q = (Map<String,Etat>) ((HashMap<String,Etat>)Q).clone() ;
            o.Q = new HashMap<>();
            for(Etat e : this.Q.values()) {
                o.addEtat((Etat)e.clone());
            }
            o.F = (Set<String>)  ((HashSet<String>)F).clone();
            o.I = (Set<String>)  ((HashSet<String>)I).clone();
            o.A = (Set<String>)  ((HashSet<String>)A).clone();
            o.histo = (Stack<Transition>) ((Stack<Transition>)histo).clone();
            //o.mu = (Set<Transition>) ((HashSet<Transition>)mu).clone();
            o.mu = new HashSet<>();
            for(Transition t : this.mu) {
                o.addTransition((Transition)t.clone());
            }
        } catch(CloneNotSupportedException cnse) {
            cnse.printStackTrace(System.err);
        }
        return o;
    }

    public String toString() {
        StringBuilder s = new StringBuilder("{ A={ ");
        for(String a : A ) s.append(a).append(" ");
        s.append("} Q={ ");
        for(Etat q : Q.values() ) s.append(q).append(" ");
        s.append("} I={ ");
        for(String q : I ) s.append(q).append(" ");
        s.append("} F={ ");
        for(String q : F ) s.append(q).append(" ");
        s.append("} \n   mu={ \n");
        for(Transition t : mu ) s.append("\t").append(t).append("\n");
        s.append("   }\n}");

        return s.toString();
    }

    /**
     * Ajoute une transition à mu.
     * @param t transition à ajouter
     */
    public void addTransition(Transition t) {
        mu.add(t);
    }

    /**
     * Ajoute un état à Q.
     * @param e L'état
     */
    public void addEtat(Etat e){
        if (!Q.containsKey(e.name))
            Q.put(e.name,e);
    }

    /**
     * Retrouve un état par son nom.
     * @param n Le nom de l'état
     * @return l'état retrouvé, null sinon
     */
    public Etat getEtat(String n) {
        return Q.getOrDefault(n, null);
    }

    /**
     * Fixe le vocabulaire de l'automate.
     * @param A la vocabulaire
     */
    public void setA(Set<String> A){
        this.A = A;
    }

    /**
     * Indique qu'un état (par son nom) est un état initial.
     * @param e Le nom de l'état
     * @exception JFSMException Si l'état est absent
     */
    public void setInitial(String e) throws JFSMException {
        if (Q.containsKey(e)) {
            I.add(e);
        } else throw new JFSMException("Etat absent:"+e);
    }

    /**
     * Indique qu'un état est un état initial.
     * @param e L'état
     * @exception JFSMException Si l'état est absent
     */
    public void setInitial(Etat e) throws JFSMException {
        setInitial(e.name);
    }

    /**
     * Indique qu'un état (par son nom) est un état final.
     * @param e Le nom de l'état
     * @exception JFSMException Si l'état est absent
     */
    public void setFinal(String e) throws JFSMException {
        if (Q.containsKey(e)) {
            F.add(e);
        } else throw new JFSMException("Etat absent:"+e);
    }

    /**
     * Indique qu'un état est un état final.
     * @param e L'état
     * @exception JFSMException Si l'état est absent
     */
    public void setFinal(Etat e) throws JFSMException {
        setFinal(e.name);
    }

    /**
     * Détermine si un état (par son nom) est un état initial.
     * @param e Le nom de l'état
     * @return vrai si initial, faux sinon
     */
    public boolean isInitial(String e){
        assert Q.containsKey(e) : "isInitial : l'état doit être un état de l'automate." ;
        return I.contains(e);
    }

    /**
     * Détermine si un état est un état initial.
     * @param e L'état
     * @return vrai si initial, faux sinon
     */
    public boolean isInitial(Etat e){
        return isInitial(e.name);
    }

    /**
     * Détermine si un état (par son nom) est un état final.
     * @param e Le nom de l'état
     * @return vrai si final, faux sinon
     */
    public boolean isFinal(String e){
        assert Q.containsKey(e) : "isFinal : l'état doit être un état de l'automate." ;
        return F.contains(e);
    }

    /**
     * Détermine si un état est un état final.
     * @param e L'état
     * @return vrai si final, faux sinon
     */
    public boolean isFinal(Etat e){
        return isFinal(e.name);
    }

    /**
     * Initialise l'exécution de l'automate.
     */
    public void init() {
        histo.clear();
    }

    /**
     * Indique si l'automate est dans un état final.
     * @return vrai si final, faux sinon
     */
    public boolean accepte(){return isFinal(current);}

    /**
     * Indique si l'automate est epsilon-libre.
     * @return vrai si e-libre, faux sinon
     */
    public boolean epsilonLibre(){
        boolean ok = true ;
        for(Transition t : mu) {
            if (t instanceof EpsilonTransition) {
                ok = false;
                break;
            }
        }
        return ok;
    }

    /**
     * Supprime les états qui ne sont pas utiles (accessible et co-accessible)
     * @return un automate équivalent utile (tous les états sont utiles)
     */
    public Automate emonder() {
        System.out.println("emonder() : méthode non implémentée");
        Automate afn = (Automate) this.clone();

        // A compléter

        return afn;
    }

    /**
     * Détermine si l'automate est utile
     * @return booléen
     */
    public boolean estUtile() {
        System.out.println("estUtile() : méthode non implémentée");
        boolean ok = false;

        // A compléter

        return ok;
    }

    /**
     * @role Permet de transformer l'automate en un automate standard.
     * @return un automate équivalent standard.
     * @throws JFSMException : si l'état n'est pas absent.
     */
    public Automate standardiser() throws JFSMException {
        System.out.println("standardiser() : ");
        Automate auto = (Automate) this.clone();

        System.out.println("automate est standard ? " + this.estStandard());

        if (!this.estStandard()) {
            Set<Transition> nouvelleTransition = new HashSet<>();

            // on garde tout les états initiaux dans une variable avant suppression.
            Set<String> etatsInitiaux = this.I;

            // suppresion de tous les états initiaux dans I.
            auto.I.removeAll(this.I);

            // création du nouvel état initial et ajout dans Q et I de l'automate.
            Etat newEtatInitial = new Etat("etatInitial");
            auto.addEtat(newEtatInitial);
            auto.setInitial(newEtatInitial);

            // pour tout les états initiaux avant leur suppression...
            for (String etatInitSup : etatsInitiaux) {
                // ... pour toutes leurs transitions...
                for (Transition transition : auto.mu) {
                    // on regarde si la source de la transition est égal à un ancien état initial, gère les doublons.
                    if (transition.source.equals(etatInitSup) && !auto.mu.contains(new Transition("étatInitial", transition.symbol, transition.source))) {
                        // si oui, on le replace par le nouvel état initial.
                        nouvelleTransition.add(new Transition("étatInitial", transition.symbol, transition.source));
                    }
                }
            }

            auto.mu.addAll(nouvelleTransition);
        }

        return auto;
    }

    /**
     * @role Détermine si l'automate est standard donc si aucune cible de transition n'est
     *       initial.
     * @return booléen.
     */
    public boolean estStandard() {
        Iterator<Transition> it;
        boolean trouver = false; // variable permettant de stocker si une cible de transition est initial.

            if (this.I.size() == 1) {
                it = this.mu.iterator();

            while (it.hasNext() && !trouver) {
                // le programme regarde si la cible de la transition est initial.
                if (this.isInitial(it.next().cible)) {
                    trouver = true;
                }
            }

            // retourne l'inverse de trouver car le but est de ne pas trouver la cible de la transition qui est initial.
            return !trouver;
        }

        return false;
    }


    /**
     * @role Permet de transformer l'automate en un automate normalisé, donc standard aussi.
     * @return un automate équivalent normalisé
     */
    public Automate normaliser() throws JFSMException {
        System.out.println("normaliser() : ");
        Automate auto = (Automate) this.clone();

        System.out.println("automate est normale ? " + this.estNormalise());

        if(!estStandard()) { auto = auto.standardiser(); }

        if(!auto.estNormalise()) {
            Set<Transition> nouvelleTransition = new HashSet<>();

            // on garde tout les états finaux dans une variable avant suppression.
            Set<String> etatsFinaux  = this.F;

            // suppresion de tous les états finaux dans F.
            auto.F.removeAll(auto.F);

            // création du nouvel état final et ajout dans Q et F de l'automate.
            Etat newEtatFinal = new Etat("etatFinal");
            auto.addEtat(newEtatFinal);
            auto.setFinal(newEtatFinal);

            // pour tout les états finaux avant leur suppression...
            for (String etatFinSup : etatsFinaux) {
                // ... pour toutes leurs transitions...
                for (Transition transition : auto.mu) {
                    // on regarde si la cible de la transition est égal à un ancien état final.
                    if (transition.cible.equals(etatFinSup)) {
                        // si oui, on le replace par le nouvel état final.
                        nouvelleTransition.add(new Transition(transition.source, transition.symbol, "etatFinal"));
                    }
                }
            }

            auto.mu.addAll(nouvelleTransition);
        }
        return auto;
    }

    /**
     * @role Détermine si l'automate est normalisé, donc si aucune cible de transition n'est
     *       initial et aucune source de transition n'est .
     * @return booléen
     */
    public boolean estNormalise() {
        Iterator<Transition> it;
        boolean trouver = false;  // variable permettant de stocker si une source de transition est final.

        if (this.estStandard()) {
            if (this.F.size() == 1) {

                it = this.mu.iterator();

                while (it.hasNext() && !trouver) {
                    // le programme regarde si la source de la transition est final.
                   if(this.isFinal(it.next().source)) { trouver = true; }
                }
            }
        } else {
            return false;
        }

        // retourne l'inverse de trouver car le but est de ne pas trouver la source de la transition qui est final.
        return !trouver;
    }


    /**
     * Construit un automate reconnaissant le produit du langage de l'automate avec celui de "a" : L(this)xL(a)
     * @param auto2 un Automate
     * @return un automate reconnaissant le produit
     */
    public Automate produit(Automate auto2) throws JFSMException {
        System.out.println("produit() :");

        // si les automates sont égaux, alors il s'agit de la mise en étoile.
        if (auto2.equals(this)) { return this.etoile(); }

        Set<String> F = new HashSet<>(auto2.F); //on met au départ l'état final de l'automate a renvoyer avec les états finaux de l'automate deux.

        // on ajoute la langage du premier et du deuxième automate.
        Set<String> A = new HashSet<>(); // aucun problèmes de doublons car la collection SET n'accepte pas les doublons.
        A.addAll(this.A);
        A.addAll(auto2.A);

        //---------------- ETATS ----------------------//

        // on ajoute tout les états du premier et du deuxième automate ...
        Map<String,Etat> QMap = new HashMap<>();
        QMap.putAll(this.Q);
        QMap.putAll(auto2.Q);

        // ... et on supprime tout les états initiaux du deuxième automate de Q, puis on ajoute les états finaux dans F.
        for (String etatInitialAut2 : auto2.I) {
            Etat etatI = new Etat(etatInitialAut2);
            // les états sont ajouté dans la collection d'état avec leurs nom comme clé, donc on les supprime avec leur clé, qui est aussi leur nom.
            QMap.remove(etatI.getName());

            //---------------- DEBUT ETATS FINAUX----------------------//

            // on regarde si les états initiaux du deuxième automate, ne sont pas aussi finaux.
            if (auto2.F.contains(etatInitialAut2)) {
                F.addAll(this.F);
                F.removeAll(auto2.I); // on supprime touts les états initiaux du deuxième automate dans les états finaux.
            }

            //---------------- FIN ETATS FINAUX----------------------//
        }

        Set<Etat> Q = new HashSet<>();

        // transformation du QMap en une collection Set.
        Set<Map.Entry<String, Etat>> QSet = QMap.entrySet();

        // on récupère juste les valeurs des Etats dans un Set pour être en accord avec le constructeur d'Automate.
        for (Map.Entry<String, Etat> stringEtatEntry : QSet) {
            Q.add(stringEtatEntry.getValue());
        }

        //---------------- TRANSITION ----------------------//

        Set<Transition> mu = new HashSet<>(this.mu);

        // toutes les transitions du deuxième automate sauf celles qui partent d'un état initial de celui-ci.
        for (Transition trans : auto2.mu) {
            if (!auto2.I.contains(trans.source)) {
                mu.add(trans);
            }
        }

        // toutes les transitions qui partent d'un état initial du deuxième automate, partent des états finaux du premier automate.
        for (String etatI : auto2.I) {
            for (Transition trans : auto2.mu) {
                if (trans.source.equals(etatI)) {
                    for (String etatF : this.F) {
                        mu.add(new Transition(etatF, trans.symbol, trans.cible));
                    }
                }
            }
        }

        return new Automate(A, Q, this.I, F, mu);
    }

    /** 
	* Construit un automate reconnaissant le langage de l'automate à l'étoile : L(this)*
	* @return un automate reconnaissant la mise à l'étoile
	* @throws JFSMException
	*/
	public Automate etoile() throws JFSMException  {
		System.out.println("etoile() :");
		
		Automate afn = (Automate) this.clone();
		
		//verifie si l'automate est bien standard.
        if(!afn.estStandard()) { afn = afn.standardiser(); }

        //Si i l'état initial de l'automate L n'est pas final, le rend aussi final.
        for(String etatInitial : this.I) {
            if (!this.F.contains(etatInitial)) {
                afn.F.addAll(this.I);
            }
        }

        //toutes les transition qui partent d'un état initial, partent des états finaux.
        for(String etatI : this.I){
            for(Transition trans : this.mu){
                if(trans.source.equals(etatI)){
                    for(String etatF : this.F){
                        afn.mu.add(new Transition(etatF,trans.symbol,trans.cible));
                    }
                }
            }
        }
        return afn;
	}

    /**
     * Construit un automate reconnaissant l'union du langage de l'automate avec celui de "a" : L(this) U L(a)
     * @param a un Automate
     * @return un automate reconnaissant l'union
     */
    public Automate union(Automate a) {
        System.out.println("union() : méthode non implémentée");
        return a;
    }

    /**
     * Construit un automate reconnaissant l'intersection du langage de l'automate avec celui de "a"
     * @param a un Automate
     * @return un automate reconnaissant l'intersection
     */
    public Automate intersection(Automate a) {
        System.out.println("intersection() : méthode non implémentée");
        return a;
    }

    /**
     * Construit un automate reconnaissant le complémentaire du langage
     * @return un automate reconnaissant le complémentaire
     */
    public Automate complementaire() {
        System.out.println("complémentaire() : méthode non implémentée");
        return this;
    }

    /**
     * Construit un automate complet
     * @return l'automate complet
     */
    public Automate complet() {
        System.out.println("complet() : méthode non implémentée");
        return this;
    }

    /**
     * Teste si un automate est complet
     * @return booléen
     */
    public boolean estComplet() {
        System.out.println("estComplet() : méthode non implémentée");
        return true;
    }

    /**
	 * Construit un automate reconnaissant le langage transposé
	 * 
	 * @return l'automate complet
	 * @throws JFSMException
	 */
	public Automate transpose() throws JFSMException {
		System.out.println("transpose() : ");
		Automate transpose = (Automate) this.clone();
		
		//change les états finaux en états initiaux et les états initiaux en états finaux?
		Set<String> stock;
		stock = transpose.F;
		transpose.F = transpose.I;
		transpose.I = stock;
		
		//vide toutes les transitions de l'automate transposé.
		transpose.mu.clear();
        
        //récupére les transition de l'automate puis les ajouts dans l'automate transposé en les inversant.
		for(Transition trans : this.mu){
			transpose.mu.add(new Transition(trans.cible, trans.symbol, trans.source));
		}
		
		
		return transpose;
	}
    /**
     * Détermine des transitions possibles que peut emprunter l'automate en fonction de l'état courant et du symbole courant
     * @param symbol le symbole
     * @exception JFSMException Exception levée si la méthode n'est pas implémentée
     * @return la liste des transitions possibles
     */
    public Queue<Transition> next(String symbol) throws JFSMException  {
        throw new JFSMException("Méthode next non implémentée");
    }

    /**
     * Exécute l'automate sur un mot (une liste de symboles)
     * @param l la liste de symboles
     * @return un booléen indiquant sur le mot est reconnu
     * @exception JFSMException Exception levée si la méthode n'est pas implémentée
     */
    public boolean run(List<String> l) throws JFSMException  {
        throw new JFSMException("Méthode run non implémentée");
    }

    /**
     * Enregistre un automate sous le format XML "JFLAP 4".
     * @param file le nom du fichier
     */
    public void save(String file) {
        try{
            File ff=new File(file);
            ff.createNewFile();
            FileWriter ffw=new FileWriter(ff);
            ffw.write("<?xml version='1.0' encoding='UTF-8' standalone='no'?><!--Created with JFSM.--><structure>\n");
            ffw.write("\t<type>fa</type>\n");
            ffw.write("\t<automaton>\n");
            for(Etat e : Q.values()) {
                ffw.write("\t\t<state id='"+e.no+"' name='"+e.name+"'>\n\t\t\t<x>0</x>\n\t\t\t<y>0</y>\n");
                if (isInitial(e.name)) ffw.write("\t\t\t<initial/>\n");
                if (isFinal(e.name)) ffw.write("\t\t\t<final/>\n");
                ffw.write("\t\t</state>\n");
            }
            for(Transition t : mu){
                ffw.write("\t\t<transition>\n");
                Etat from = getEtat(t.source);
                ffw.write("\t\t\t<from>"+from.no+"</from>\n");
                Etat to = getEtat(t.cible);
                ffw.write("\t\t\t<to>"+to.no+"</to>\n");
                if (!(t instanceof EpsilonTransition)) ffw.write("\t\t\t<read>"+t.symbol+"</read>\n");
                else ffw.write("\t\t\t<read/>\n");
                ffw.write("\t\t</transition>\n");
            }
            ffw.write("\t</automaton>\n");
            ffw.write("</structure>\n");
            ffw.close();
        } catch (Exception e) {}
    }

    /**
     * Charge un automate construit avec JFLAP au format XML "JFLAP 4".
     * @param file le nom du fichier
     * @return un automate
     */
    static public Automate load(String file) {
        JFLAPHandler handler = new JFLAPHandler();
        try {
            XMLReader saxParser = XMLReaderFactory.createXMLReader();
            saxParser.setContentHandler(handler);
            saxParser.setErrorHandler(handler);
            saxParser.parse( file );
        } catch (Exception e) {
            System.out.println("Exception capturée : ");
            e.printStackTrace(System.out);
            return null;
        }
        try {
            if (AFD.testDeterminisme(handler.res) )
                return new AFD(handler.res) ;
            else return new AFN(handler.res) ;
        } catch (JFSMException e) {return null;}
    }

}

class JFLAPHandler extends DefaultHandler {
    String cdc ;
    public Set<Etat> Q;
    public Set<String> F, I;
    public Set<String> A;
    public Set<Transition> mu;
    private Etat e;
    private Transition t;
    private String from, to, read, state_name, state_id;
    private boolean final_state, initial_state;
    public Automate res ;

    public JFLAPHandler() {super();}

    public void characters(char[] caracteres, int debut, int longueur) {
        cdc = new String(caracteres,debut,longueur);
    }

    public void startDocument() {
        cdc="";
        A = new HashSet<>();
        I = new HashSet<>();
        F = new HashSet<>();
        Q = new HashSet<>();
        mu = new HashSet<>();
        res = null;
    }

    public void endDocument() {
        try{
            res = new Automate(A,Q,I,F,mu);
        } catch (JFSMException e) {
            System.out.println("Erreur:"+e);
        }
    }

    public void startElement(String namespaceURI, String sName, String name, Attributes attrs) {
        switch (name) {
            case "state":
                state_name = attrs.getValue("name");
                state_id = attrs.getValue("id");
                final_state = false;
                initial_state = false;
                break;
            case "initial":
                initial_state = true;
                break;
            case "final":
                final_state = true;
                break;
        }
        cdc="";
    }

    public void endElement(String uri, String localName, String name) {
        switch (name) {
            case "state":
                e = new Etat(state_id);
                Q.add(e);
                if (initial_state) I.add(state_id);
                if (final_state) F.add(state_id);
                break;
            case "transition":
                try {
                    if (!read.equals("")) {
                        A.add(read);
                        Transition t = new Transition(from, read, to);
                        mu.add(t);
                    } else {
                        EpsilonTransition t = new EpsilonTransition(from, to);
                        mu.add(t);
                    }
                } catch (JFSMException e) {
                    System.out.println("Erreur:" + e);
                }
                break;
            case "type":

                break;
            case "from":
                from = cdc;
                break;
            case "to":
                to = cdc;
                break;
            case "read":
                read = cdc;
                break;
        }
    }
}



