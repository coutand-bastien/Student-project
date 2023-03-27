/**
 * @Created: 2019-12-26
 * @author COUTAND Bastien, GARNIER Cyprien
 * @version 1.1
 * @what implementation of produit, mise en étoile et transposer
 */
package Test;

import JFSM.*;

import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

public class Test {

    public Test() {

    }

    public void affAuto(Automate afn) {
        System.out.println(afn);
        afn.save("test.jff");
    }

    /**
     * test du premier automate du projet, le premier à l'origine du projet.
     */
    public void testOriginal() throws JFSMException {
        System.out.println("----------------------Test de l'original----------------------");
        System.out.println();

        Set<String> A = new HashSet<>();
        A.add("a");A.add("b");A.add("c");

        Set<Etat> Q = new HashSet<>();
        Q.add(new Etat("1"));Q.add(new Etat("2"));
        Q.add(new Etat("3"));Q.add(new Etat("4"));Q.add(new Etat("5"));

        Set<Transition> mu = new HashSet<>();
        mu.add(new Transition("1","a","2"));
        mu.add(new Transition("1","b","4"));
        mu.add(new Transition("2","b","3"));
        mu.add(new Transition("2","c","4"));
        mu.add(new Transition("3","a","2"));
        mu.add(new Transition("3","b","4"));
        mu.add(new Transition("4","a","5"));
        mu.add(new Transition("5","c","5"));


        Set<String> F = new HashSet<>();
        F.add("5");
        F.add("4");
        F.add("1");
        Automate afn = new AFD(A, Q, "1", F, mu);

        this.affAuto(afn);
    }

    public void testLoad() {
        System.out.println("----------------------Test load essaie.jff-----------------------");
        System.out.println();

        Automate afn2 = Automate.load("./Test/essai.jff");
        System.out.println(afn2.getClass().getName());
        System.out.println(afn2);
    }

    public void testTP4() throws JFSMException {
        System.out.println("----------------------Test TP4-----------------------");
        System.out.println();

        Set<String> A = new HashSet<>();
        A.add("ZO");
        A.add("GA");
        A.add("BU");
        A.add("MEU");

        Set<Etat> Q = new HashSet<>();
        Q.add(new Etat("1"));
        Q.add(new Etat("2"));
        Q.add(new Etat("3"));
        Q.add(new Etat("4"));
        Q.add(new Etat("5"));
        Q.add(new Etat("5"));
        Q.add(new Etat("6"));
        Q.add(new Etat("7"));
        Q.add(new Etat("8"));
        Q.add(new Etat("9"));

        Set<Transition> mu = new HashSet<>();
        mu.add(new Transition("1","ZO","1"));
        mu.add(new Transition("1","GA","4"));
        mu.add(new Transition("1","BU","5"));

        mu.add(new Transition("2","BU","5"));
        mu.add(new Transition("2","MEU","1"));
        mu.add(new Transition("2","ZO","6"));

        mu.add(new Transition("3","MEU","2"));
        mu.add(new Transition("3","ZO","6"));
        mu.add(new Transition("3","GA","3"));

        mu.add(new Transition("4","GA","7"));
        mu.add(new Transition("4","BU","8"));
        mu.add(new Transition("4","ZO","5"));

        mu.add(new Transition("5","BU","8"));
        mu.add(new Transition("5","ZO","9"));
        mu.add(new Transition("5","GA","6"));

        mu.add(new Transition("6","GA","6"));
        mu.add(new Transition("6","ZO","9"));

        mu.add(new Transition("7","MEU","7"));

        mu.add(new Transition("8","MEU","7"));

        mu.add(new Transition("9","BU","9"));
        mu.add(new Transition("9","MEU","8"));



        Set<String> F = new HashSet<>();
        F.add("7");
        F.add("8");
        F.add("9");

        Set<String> I = new HashSet<>();
        I.add("1");
        I.add("2");
        I.add("3");

        Automate afn = new AFN(A, Q, I, F, mu);

        List<String> l = new ArrayList<>();
        l.add("MEU");
        l.add("MEU");
        l.add("BU");
        l.add("ZO");
        l.add("BU");
        l.add("MEU");
        System.out.println();

        l.add("GA");
        l.add("BU");
        l.add("ZO");
        l.add("MEU");
        System.out.println();

        l.add("ZO");
        l.add("ZO");
        l.add("GA");
        l.add("ZO");
        l.add("GA");
        l.add("GA");
        l.add("ZO");
        System.out.println();

        l.add("BU");
        l.add("GA");
        l.add("ZO");
        l.add("MEU");
        System.out.println();

        afn.run(l);
        affAuto(afn);
    }

    public void testAutomateNormal() throws JFSMException {
        System.out.println("----------------------Test Automate Normal-----------------------");
        System.out.println();

        Set<String> A = new HashSet<>();
        A.add("a");
        A.add("b");
        A.add("c");

        Set<Etat> Q = new HashSet<>();
        Q.add(new Etat("0"));
        Q.add(new Etat("1"));
        Q.add(new Etat("2"));

        Set<String> I = new HashSet<>();
        I.add("0");

        Set<String> F = new HashSet<>();
        F.add("2");

        Set<Transition> mu = new HashSet<>();
        mu.add(new Transition("0","a","1"));
        mu.add(new Transition("1","c","1"));
        mu.add(new Transition("1","b","2"));

        Automate afn = new AFN(A, Q, I, F, mu);

        System.out.println("Automate avant transformation\n");
        this.affAuto(afn);
        System.out.println();
        this.affAuto(afn.normaliser());
    }

    public void testAutomateNonNormal1() throws JFSMException {
        System.out.println("----------------------Test Automate non normal-----------------------");
        System.out.println("car l'état initial est la fin de deux transitions, et l'état final possède deux transitions sortantes");
        System.out.println();

        Set<String> A = new HashSet<>();
        A.add("a");
        A.add("b");
        A.add("c");

        Set<Etat> Q = new HashSet<>();
        Q.add(new Etat("0"));
        Q.add(new Etat("1"));
        Q.add(new Etat("2"));

        Set<String> I = new HashSet<>();
        I.add("0");

        Set<String> F = new HashSet<>();
        F.add("2");

        Set<Transition> mu = new HashSet<>();
        mu.add(new Transition("0","b","0"));
        mu.add(new Transition("0","a","1"));
        mu.add(new Transition("1","b","0"));
        mu.add(new Transition("1","c","1"));
        mu.add(new Transition("1","b","2"));
        mu.add(new Transition("2","c","1"));
        mu.add(new Transition("2","c","2"));

        Automate afn = new AFN(A, Q, I, F, mu);

        System.out.println("Automate avant transformation\n");
        this.affAuto(afn);
        System.out.println();
        this.affAuto(afn.normaliser());
    }

    public void testAutomateNonNormal2() throws JFSMException {
        System.out.println("----------------------Test Automate non normal-----------------------");
        System.out.println("automate non-normal car il possède deux états initiaux.");
        System.out.println();

        Set<String> A = new HashSet<>();
        A.add("a");
        A.add("b");
        A.add("c");

        Set<Etat> Q = new HashSet<>();
        Q.add(new Etat("0"));
        Q.add(new Etat("1"));
        Q.add(new Etat("2"));

        Set<String> I = new HashSet<>();
        I.add("0");
        I.add("1");

        Set<String> F = new HashSet<>();
        F.add("2");

        Set<Transition> mu = new HashSet<>();
        mu.add(new Transition("0", "a", "1"));
        mu.add(new Transition("1", "c", "2"));
        mu.add(new Transition("0", "c", "2"));

        Automate afn = new AFN(A, Q, I, F, mu);

        System.out.println("Automate avant transformation\n");
        this.affAuto(afn);
        System.out.println();
        this.affAuto(afn.normaliser());
    }

    public void testAutomateStandard() throws JFSMException {
        System.out.println("----------------------Test Automate standard-----------------------");
        System.out.println();

        Set<String> A = new HashSet<>();
        A.add("a");
        A.add("b");
        A.add("c");

        Set<Etat> Q = new HashSet<>();
        Q.add(new Etat("0"));
        Q.add(new Etat("1"));
        Q.add(new Etat("2"));

        Set<String> I = new HashSet<>();
        I.add("0");

        Set<String> F = new HashSet<>();
        F.add("2");

        Set<Transition> mu = new HashSet<>();
        mu.add(new Transition("0","a","1"));
        mu.add(new Transition("1","c","1"));
        mu.add(new Transition("1","b","2"));

        Automate afn = new AFN(A, Q, I, F, mu);

        System.out.println("Automate avant transformation\n");
        this.affAuto(afn);
        System.out.println();
        this.affAuto(afn.standardiser());
    }

    public void testAutomateNonStandard1() throws JFSMException {
        System.out.println("----------------------Test Automate non standard-----------------------");
        System.out.println("car il possède deux états initiaux.");
        System.out.println();

        Set<String> A = new HashSet<>();
        A.add("a");
        A.add("b");
        A.add("c");

        Set<Etat> Q = new HashSet<>();
        Q.add(new Etat("0"));
        Q.add(new Etat("1"));
        Q.add(new Etat("2"));

        Set<String> I = new HashSet<>();
        I.add("0");
        I.add("1");

        Set<String> F = new HashSet<>();
        F.add("2");

        Set<Transition> mu = new HashSet<>();
        mu.add(new Transition("0", "a", "1"));
        mu.add(new Transition("1", "c", "2"));
        mu.add(new Transition("0", "c", "2"));

        Automate afn = new AFN(A, Q, I, F, mu);

        System.out.println("Automate avant transformation\n");
        this.affAuto(afn);
        System.out.println();
        this.affAuto(afn.standardiser());
    }

    public void testAutomateNonStandard2() throws JFSMException {
        System.out.println("----------------------Test Automate non standard-----------------------");
        System.out.println("car l'état initial est la fin de deux transitions.");
        System.out.println();

        Set<String> A = new HashSet<>();
        A.add("a");
        A.add("b");
        A.add("c");

        Set<Etat> Q = new HashSet<>();
        Q.add(new Etat("0"));
        Q.add(new Etat("1"));
        Q.add(new Etat("2"));

        Set<String> I = new HashSet<>();
        I.add("0");

        Set<String> F = new HashSet<>();
        F.add("2");

        Set<Transition> mu = new HashSet<>();
        mu.add(new Transition("0","a","0"));
        mu.add(new Transition("0","b","1"));
        mu.add(new Transition("1","c","0"));
        mu.add(new Transition("1","c","2"));
        mu.add(new Transition("2","a","2"));

        Automate afn = new AFN(A, Q, I, F, mu);

        System.out.println("Automate avant transformation\n");
        this.affAuto(afn);
        System.out.println();
        this.affAuto(afn.standardiser());
    }

    public void testAutomateTranspose() throws JFSMException {
        System.out.println("----------------------Test Automate transposé-----------------------");
        System.out.println();

        Set<String> A = new HashSet<>();
        A.add("a");
        A.add("b");
        A.add("c");

        Set<Etat> Q = new HashSet<>();
        Q.add(new Etat("0"));
        Q.add(new Etat("1"));
        Q.add(new Etat("2"));
        Q.add(new Etat("3"));
        Q.add(new Etat("4"));

        Set<String> I = new HashSet<>();
        I.add("0");

        Set<String> F = new HashSet<>();
        F.add("2");
        F.add("3");
        F.add("4");

        Set<Transition> mu = new HashSet<>();
        mu.add(new Transition("0","a","0"));
        mu.add(new Transition("0","b","1"));
        mu.add(new Transition("0","b","4"));
        mu.add(new Transition("1","c","0"));
        mu.add(new Transition("1","c","2"));

        mu.add(new Transition("1","a","3"));
        mu.add(new Transition("2","a","2"));
        mu.add(new Transition("3","c","2"));
        mu.add(new Transition("4","c","1"));
        mu.add(new Transition("4","a","3"));

        Automate afn = new AFN(A, Q, I, F, mu);

        System.out.println("Automate avant transformation\n");
        this.affAuto(afn);
        System.out.println();
        this.affAuto(afn.transpose());
    }

    public void testAutomateProduit() throws JFSMException {
        System.out.println("----------------------Test Automate pour produit-----------------------");
        System.out.println();

        Set<String> A = new HashSet<>();
        A.add("a");
        A.add("b");
        A.add("c");

        Set<Etat> Q = new HashSet<>();
        Q.add(new Etat("1"));
        Q.add(new Etat("2"));
        Q.add(new Etat("3"));
        Q.add(new Etat("4"));
        Q.add(new Etat("5"));
        Q.add(new Etat("6"));

        Set<String> I = new HashSet<>();
        I.add("1");

        Set<String> F = new HashSet<>();
        F.add("6");

        Set<Transition> mu = new HashSet<>();
        mu.add(new Transition("1","a","2"));
        mu.add(new Transition("1","b","4"));
        mu.add(new Transition("2","c","2"));
        mu.add(new Transition("2","b","3"));
        mu.add(new Transition("2","a","5"));
        mu.add(new Transition("3","a","6"));
        mu.add(new Transition("3","b","4"));
        mu.add(new Transition("4","c","5"));
        mu.add(new Transition("5","a","5"));
        mu.add(new Transition("5","a","6"));

        Automate afn = new AFN(A, Q, I, F, mu);

        Set<String> A2 = new HashSet<>();
        A2.add("a");
        A2.add("b");

        Set<Etat> Q2 = new HashSet<>();
        Q2.add(new Etat("A"));
        Q2.add(new Etat("B"));
        Q2.add(new Etat("C"));
        Q2.add(new Etat("D"));
        Q2.add(new Etat("E"));

        Set<String> I2 = new HashSet<>();
        I2.add("A");

        Set<String> F2 = new HashSet<>();
        F2.add("E");

        Set<Transition> mu2 = new HashSet<>();
        mu2.add(new Transition("A","b","C"));
        mu2.add(new Transition("A","a","B"));
        mu2.add(new Transition("B","a","B"));
        mu2.add(new Transition("B","b","D"));
        mu2.add(new Transition("C","b","C"));
        mu2.add(new Transition("C","a","B"));
        mu2.add(new Transition("D","a","B"));
        mu2.add(new Transition("D","b","E"));
        mu2.add(new Transition("E","b","C"));
        mu2.add(new Transition("E","a","B"));

        Automate afn2 = new AFN(A2, Q2, I2, F2, mu2);

        this.affAuto(afn.produit(afn2));
    }

    public void testAutomateEtoile() throws JFSMException {
        System.out.println("----------------------Test Automate mis en étoile-----------------------");
        System.out.println();

        Set<String> A = new HashSet<>();
        A.add("a");
        A.add("b");
        A.add("c");

        Set<Etat> Q = new HashSet<>();
        Q.add(new Etat("0"));
        Q.add(new Etat("1"));
        Q.add(new Etat("2"));
        Q.add(new Etat("3"));
        Q.add(new Etat("4"));

        Set<String> I = new HashSet<>();
        I.add("0");

        Set<String> F = new HashSet<>();
        F.add("2");
        F.add("4");

        Set<Transition> mu = new HashSet<>();
        mu.add(new Transition("0","a","1"));
        mu.add(new Transition("1","c","1"));
        mu.add(new Transition("1","c","3"));
        mu.add(new Transition("1","b","2"));
        mu.add(new Transition("2","c","4"));
        mu.add(new Transition("3","a","4"));
        mu.add(new Transition("3","b","2"));
        mu.add(new Transition("4","c","4"));

        Automate afn = new AFN(A, Q, I, F, mu);

        System.out.println("Automate avant transformation\n");
        this.affAuto(afn);
        System.out.println();
        this.affAuto(afn.etoile());
    }

    public void testAutomateNonEtoile() throws JFSMException {
        System.out.println("----------------------Test Automate mis en étoile faux-----------------------");
        System.out.println("automate qui ne peut pas ètre mis à l'étoile car il n'est pas standard.");
        System.out.println();

        Set<String> A = new HashSet<>();
        A.add("a");
        A.add("b");
        A.add("c");

        Set<Etat> Q = new HashSet<>();
        Q.add(new Etat("0"));
        Q.add(new Etat("1"));
        Q.add(new Etat("2"));
        Q.add(new Etat("3"));
        Q.add(new Etat("4"));

        Set<String> I = new HashSet<>();
        I.add("2");
        I.add("3");
        I.add("4");

        Set<String> F = new HashSet<>();
        F.add("0");

        Set<Transition> mu = new HashSet<>();
        mu.add(new Transition("0","a","0"));
        mu.add(new Transition("0","c","1"));
        mu.add(new Transition("1","b","0"));
        mu.add(new Transition("1","c","3"));
        mu.add(new Transition("2","a","2"));
        mu.add(new Transition("2","c","4"));
        mu.add(new Transition("2","c","1"));
        mu.add(new Transition("3","b","0"));;
        mu.add(new Transition("4","a","3"));
        mu.add(new Transition("4","a","1"));

        Automate afn = new AFN(A, Q, I, F, mu);

        System.out.println("Automate avant transformation\n");
        this.affAuto(afn);
        System.out.println();
        this.affAuto(afn.etoile());
    }
}
