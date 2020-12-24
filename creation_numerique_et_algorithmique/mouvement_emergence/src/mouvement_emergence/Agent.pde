/*
 * Class qui gére tout ce qui a un rapport avec un agent.
 */
class Agent { 
  private PVector agentPosition; // position de l'agent.
  private float   agentSize;     // taille de l'agent.
  private Color   agentCol;      // couleur de l'agent.
  
  /**
    * Constructeur qui créer un agent avec une position aléatoire sur la fenètre, taille de STARTSIZE (10) pixels et une couleur 
    * aléatoire aussi.
    */
  public Agent() {
   this.agentPosition = new PVector(random(0, width), random(0, height), random(0,1000));
   this.agentSize     = mouvement_emergence.STARTSIZE;
   this.agentCol      = new Color();
  }
  
  /**
    * Constructeur qui créer un agent les variables passées en paramètre.
    */
  public Agent(PVector pos, float size, Color col) {
   this.agentPosition = pos;
   this.agentSize     = size;
   this.agentCol      = col;
  }
  
  // getters :
  PVector getAgentPosition() { return this.agentPosition; }
  Color   getAgentCol()      { return this.agentCol;      }
  float   getAgentSize()     { return this.agentSize;     }
  
  /**
    * @role : procédure permettant d'afficher un agent sur l'écran avec ça couleur.
    */
  public void drawAgent() {
      fill(this.getAgentCol().getHue(), this.getAgentCol().getSaturation(), this.getAgentCol().getBrightness(), this.getAgentCol().getTransparency());
      pushMatrix();
        translate(this.getAgentPosition().x, this.getAgentPosition().y, this.getAgentPosition().z);
        sphere(this.getAgentSize());
      popMatrix();
  }

  /**
    * @role : procédure permettant de déplacé un agent par addition avec un nouveau vector.
    * @param newPos : la nouvelle position de l'agent.
    */
  public void updatePos(PVector newPos) {
    this.getAgentPosition().add(newPos);
  }
}
