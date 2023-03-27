/* //<>//
 * Class qui gére tout ce qui a un rapport avec une population d'agents.
 */
class Population { 
  private ArrayList<Agent> agent_list; // Liste d'agents.
 
  public Population() {
    this.agent_list   = new ArrayList<Agent>();
  
    // Initialisation de MAXAGENT agents.
    this.initAgents(mouvement_emergence.MAXAGENT);
  }
  
  
  // getter :
  ArrayList<Agent> getAgent_list() { return this.agent_list; }
  
  
  /**
    * @role : procédure permettant d'initialiser un agent dans la 
    *         fenètre. 
    * @param nbAgent : le nombre d'agent à initialiser.
    */
  private void initAgents(int nbAgent) {
    for (int i = 0; i < nbAgent; i++) {
      this.agent_list.add(new Agent());
    }
  }
  
  /**
    * @role : procédure permettant d'afficher les agents sur l'écran.
    */
  public void drawAgent() {
    for (int i = 0; i < this.agent_list.size(); i++) {
      this.agent_list.get(i).drawAgent();
    }
  }
 
 /**
    * @role : procédure permettant d'ajouter un agent, sa taille et sa couleur
    *         dans la population.
    * @param agent : l'agent à ajouter.
    */
  public void add(Agent agent) {
    this.agent_list.add(agent);
  } 
  
  /**
    * @role : procédure permettant de supprimer un agent, sa taille et sa couleur
    *         dans les listes, donné par son index.
    * @param index  : l'index de l'agent voulu.
    */
  private void remove(int index) {
    this.agent_list.remove(index);
  }  

  /**
    * @role : fonction calculant la distance entre deux agents.
    * @param agent1 : le premier agent.
    * @param agent2 : le deuxième agent.
    * @return : un float contenant la distance entre les deux positions.
    */
  private float distance(Agent agent1, Agent agent2) {
    return sqrt(pow(agent2.getAgentPosition().x - agent1.getAgentPosition().x, 2) + pow(agent2.getAgentPosition().y - agent1.getAgentPosition().y, 2));
  }


  /**
    * @role : fonction calculant l'indice l'indice de l'agent le plus proche.
    * @param agent : l'agent dont on cherche son plus proche voisin.
    * @return : un entier contenant l'indice de l'agent le plus proche.
    *
    * @variance : Les mouvement ne sont pas toujours prévisibles car la fonction nearestIndex(...) peut changer ça valeur 
    *             de retour durant l'appel du programme car elle est appeller continuellement dans le draw() grace à la
    *             procédure updateAllAgents().
    */
  private int nearestIndex(Agent agent) {  
    int   nearestIndex = -1; // initialisé a "-1" car un indice est toujours positif, donc cela permet de connaître les cas d'erreurs.
    float minDistance  = width * height + 10; // valeur plus grande que la plus grande diagonal de l'écran.

    for (int i = 0; i < this.agent_list.size(); i++) {

      // on ne calcule pas la distance entre les deux même point.
      if (!agent.equals(this.agent_list.get(i))) {
        if (distance(agent, this.agent_list.get(i)) < minDistance) {

          nearestIndex = i;
          minDistance = distance(agent, this.agent_list.get(i));
        }
      }
    }

    return nearestIndex;
  }


  /**
    * @role : procédure déplacant un agent donné par son index.
    * @parma index : l'indice de l'agent en question.
    */
  private void updateAgent(int index) {
    Agent agent        = this.agent_list.get(index);
    PVector speed      = new PVector(0, 0);
    Agent nearestAgent = this.agent_list.get(this.nearestIndex(agent));  
  
    if ((this.distance(nearestAgent, agent) > mouvement_emergence.LIMITFAGOCYTOSE)  || (abs(nearestAgent.getAgentPosition().z - agent.getAgentPosition().z) >  mouvement_emergence.LIMITFAGOCYTOSE)) {
      if ((int)nearestAgent.getAgentPosition().x > (int)agent.getAgentPosition().x) speed.x =  1;
      if ((int)nearestAgent.getAgentPosition().x < (int)agent.getAgentPosition().x) speed.x = -1;
      if ((int)nearestAgent.getAgentPosition().y > (int)agent.getAgentPosition().y) speed.y =  1;
      if ((int)nearestAgent.getAgentPosition().y < (int)agent.getAgentPosition().y) speed.y = -1;
      if ((int)nearestAgent.getAgentPosition().z > (int)agent.getAgentPosition().z) speed.z =  1;
      if ((int)nearestAgent.getAgentPosition().z < (int)agent.getAgentPosition().z) speed.z = -1;
    } 
    else {
      phagocytose(agent, index);
    }

    agent.updatePos(speed);
  }
 
  
  /**
    * @role : procédure déplacant tout les agents de la liste d'agents.
    */
  public void updateAllAgents() {
    // on vérifie que la liste ne contiennent pas moins de 2 éléments, sinon erreur lors de l'appel a nearestIndex.
    if (this.agent_list.size() > 1) {
      for (int i = 0; i < this.agent_list.size(); i++) {
        this.updateAgent(i);
      }
    } 
}

  /**
    * @role : procédure permettant le phagocytage de deux agents : 
    *         "Deux agents situés à une distance inférieure à une limite fixe (LIMITFAGOCYTOSE) 
    *         sont transformés en un seul agent. La somme des aires des 2 agents donne l’aire de 
    *         l’agent résultant. La position de l’agent résultant sera celle d’un des agents."
    * @param agent : l'agent à phagocyter avec son plus proche voisin.
    * @param index : l'indice de l'agent à phagocyter avec son plus proche voisin.
    */
  private void phagocytose(Agent agent, int index) {
    int nearestInd = this.nearestIndex(agent);

    /*
      L'air d'un disque avec son diamètre est : (PI*D²)/4, avec D : le diamètre, PI ~ 3.14, on en déduit : 
              airTotal    = airDisque1 + airDisque2
              (PI*DT²)/4  = (PI*D1²)/4 + (PI*D2²)/4
              (PI*DT²)/4  = PI*(D1² + D2²)/4
                      DT² = D1² + D2²
                       DT = sqrt(D1² + D2²)
     */

    // on stocke les valeurs de taille et de couleur avant suppression dans la liste.
    float newSize = sqrt(pow(this.agent_list.get(index).getAgentSize(), 2) + pow(this.agent_list.get(nearestInd).getAgentSize(), 2));
    
    // interpolation des couleurs :
    int hue        = lerpColor(this.agent_list.get(index).getAgentCol().getHue(),        this.agent_list.get(nearestInd).getAgentCol().getHue(),        random(0,1));
    int saturation = lerpColor(this.agent_list.get(index).getAgentCol().getSaturation(), this.agent_list.get(nearestInd).getAgentCol().getSaturation(), random(0,1));
    int brightness = lerpColor(this.agent_list.get(index).getAgentCol().getBrightness(), this.agent_list.get(nearestInd).getAgentCol().getBrightness(), random(0,1));
    
    if (index > this.nearestIndex(agent)) {
      this.remove(index);
      this.remove(nearestInd);
    } else {
      this.remove(nearestInd);
      this.remove(index);
    }  
    
    this.agent_list.add(new Agent(new PVector(agent.getAgentPosition().x, agent.getAgentPosition().y, agent.getAgentPosition().z), newSize, new Color(hue, saturation, brightness)));
  }

  
   /**
    * @role : procédure de debuggage du programme. Elle affiche les variables 
    *         (taille et agent le plus proche) et traces des lignes vers l'agents 
    *         le plus proches d'un autres.
    *
    * @color fill(0)            : en noir   --> l'index de l'agent.
    * @color fill(245, 45, 234) : en violet --> l'index de l'agent le plus proche.
    */
  public void debug() {
    textSize(10);   

    for (int i = 0; i < this.agent_list.size(); i++) {
      fill(0);
      text(i, this.agent_list.get(i).getAgentPosition().x + 10, this.agent_list.get(i).getAgentPosition().y);

      fill(245, 45, 234);
      text(this.nearestIndex(this.agent_list.get(i)), this.agent_list.get(i).getAgentPosition().x + 10, this.agent_list.get(i).getAgentPosition().y + 10);

      fill(0);
      stroke(5);
      line(this.agent_list.get(i).getAgentPosition().x, this.agent_list.get(i).getAgentPosition().y, this.agent_list.get(this.nearestIndex(this.agent_list.get(i))).getAgentPosition().x, this.agent_list.get(this.nearestIndex(this.agent_list.get(i))).getAgentPosition().y);
      noStroke();
    }
  }
}
