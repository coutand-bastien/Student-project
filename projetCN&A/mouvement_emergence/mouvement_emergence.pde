import peasy.*;

/*
 * @nameProject : Emergence et agents autonomes.
 *
 * @project : Le but de ce projet est de pouvoir créer des agents autonomes qui vont se phagocyter pour pouvoir évoluer (grossir). 
 *
 * @partOfTheProject : Ce projet fait parti d'un distanciel au sein de l'Université de Nantes.
 *
 * @lastUpdate : 08 avril par Bastien COUTAND.
 *
 * @Creator : COUTAND Bastien (bastien.coutand@etu.univ-nantes.fr).
 */
public static final int   MAXAGENT        = 1000; // nombre maximal d'agents créées.
public static final float STARTSIZE       = 10.F; // taille d'un agent au départ.
public static final int   LIMITFAGOCYTOSE = 2;    // seuil limite avant phagocytose.

private boolean debug, loop;

Population population;

PeasyCam cam;

void settings() {
  size(800, 800, P3D);
}

void setup() {
 
  frameRate(20);
  colorMode(HSB, 360, 100, 100, 100);
  noStroke();
  
  population = new Population();
  debug      = false;
  loop       = false;
  
  cam = new PeasyCam(this, 1000);
  cam.lookAt(width/2, height/2, 1000);
}

void draw() {
  background(360); // blanc en HSB.
  
  population.drawAgent();
  
  // si loop == true alors les agents ne se déplace plus.
  if (!loop) population.updateAllAgents();
    
  // si debug == true alors l'affichage est modifié.
  if (debug) population.debug();
}

void mouseClicked() {
  // ajout d'un agent à la position de la souris, de taille : taille de la liste et de couleurs aléatoire.
  population.add(new Agent(new PVector(mouseX, mouseY, random(0, 1000)), population.getAgent_list().size(), new Color()));
}

void keyPressed() {
  // lettre pour debuger (d)
  if (key == 'd') debug = !debug; 

  // lettre pour restart (r)
  if (key == 'r') setup(); 
  
  // lettre pour stopper le programme (e)
  if (key == 'e') loop = !loop; 
}
