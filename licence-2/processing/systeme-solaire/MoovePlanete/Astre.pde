class Astre { //<>//
  private int size;                // the radius of the star.
  private float distanceMoonAstre; // distance between a moon and its star.
  private String nameAstre;        // name of the star.
  
  private float angleMoonAstre; // starting angle between the moon and its planet (0 by default), then incremented to rotate.
  private float vitesseOrbit;   // increment added to the angle to produce a feeling of rotation.

  private float angleRotationAstre; // starting angle of rotation of the planet on itself (0 by default).
  private float vitesseRotation;    // increment added to the angle to produce a feeling of rotation.

  private float angleInclinaisonRotation; // angle of the inclination of the rotation vector relative to the Y axis.

  private PVector positionAstre;      // the position of the star.
  private PVector positionSuperAstre; // position of the attracting star.

  private PImage  textureAstre; // the image of the star.
  private PShape  astreShape;   // form of the star.

  private Astre moon_tab[];
  private int nbMoonInTab;

  Astre(int size, PVector positionSuperAstre, float vitesseOrbit, float angleMoonAstre, float vitesseRotation, float angleRotationAstre, float angleInclinaisonRotation, float distanceMoonAstre, int nbMoon, String textureAstre) {
    this.size               = size;  
    this.distanceMoonAstre  = distanceMoonAstre;

    this.angleMoonAstre     = angleMoonAstre;
    this.vitesseOrbit       = vitesseOrbit;

    this.angleRotationAstre = angleRotationAstre;
    this.vitesseRotation    = vitesseRotation;

    this.angleInclinaisonRotation = angleInclinaisonRotation;

    this.positionAstre      = new PVector();
    this.positionSuperAstre = positionSuperAstre;

    this.nameAstre   = textureAstre;
    this.moon_tab    = new Astre[nbMoon];
    this.nbMoonInTab = 0;

    this.textureAstre = loadImage(textureAstre);
    this.astreShape   = createShape(SPHERE, this.size);
    this.astreShape.setTexture(this.textureAstre);
  }

  // getters :
  PVector getPositionAstre()      { return this.positionAstre;      }
  PVector getPositionSuperAstre() { return this.positionSuperAstre; }
  float   getAngleRotationAstre() { return this.angleRotationAstre; }
  PShape  getAstreShape()         { return this.astreShape;         }
  int     getNbMoonInTab()        { return this.nbMoonInTab;        }
  int     getSize()               { return this.size;               }
  Astre[] getMoon_tab()           { return this.moon_tab;           }


  /**
    * @role: displays the stars on the screen, with its texture, assigning them a new position
    *        for each call.
    */
  private void showAstre() {  
    // use the trigonometric to make a circle if not rotate (easier to use).
    this.positionAstre = new PVector(this.positionSuperAstre.x + sin(this.angleMoonAstre) * this.distanceMoonAstre, this.positionSuperAstre.y, this.positionSuperAstre.z + cos(this.angleMoonAstre) * this.distanceMoonAstre);   

    // update the position of the star of attraction (superAster) for its moons.
    for (int i = 0; i < this.nbMoonInTab; i++) {
      if (this.moon_tab[i] != null) this.moon_tab[this.nbMoonInTab-1].positionSuperAstre = this.positionAstre;
    }     

    pushMatrix();       
    translate(this.positionAstre.x, this.positionAstre.y, this.positionAstre.z); 

    // display of the star's axis of rotation.
    if (MoovePlanete.debug) {
      stroke(255, 0, 0);
      line(0, 0, 0, sin(this.angleInclinaisonRotation) * 100,  cos(this.angleInclinaisonRotation) * 100, 0);
      line(0, 0, 0, sin(this.angleInclinaisonRotation) * -100, cos(this.angleInclinaisonRotation) * -100, 0);
      noStroke();
    }     

    rotate(this.angleRotationAstre, sin(this.angleInclinaisonRotation), cos(this.angleInclinaisonRotation), 0); // inclinaison et rotation sur l'axe de rotation de la planète.
    shape(this.astreShape);
    popMatrix();

    // display of the different rings of Saturn.
    if (this.nameAstre.equals("saturnmap.jpg")) { 
      drawRing(1, 60); 
      drawRing(2, 65); 
      drawRing(5, 70);
    }

    if (nbMoonInTab > 0) this.showMoon();
  }

  /**
    * @role: displays all the moons of the stars on the screen, assigning them a new position
    *        for each call, thanks to the showAstre function.
    */
  void showMoon() {
    for (int i = 0; i < this.nbMoonInTab; i++) {
      if (this.moon_tab[i] != null) {         
        this.moon_tab[i].showAstre();
      }
    }
  }

  /**
    * @role: increases the angle of rotation of the star on itself and between the attracting star and that moon, thanks to the speed of the
    *        orbit divided by a number so that it is not too fast.
    *        Produces a movement effect.
    */
  void orbitAndRotation() {
    this.angleMoonAstre     += this.vitesseOrbit/50    * MoovePlanete.valueOfSpeed;
    this.angleRotationAstre += this.vitesseRotation/50 * MoovePlanete.valueOfSpeed;

    // we change the orbit of all the moons on the planet too.
    for (int i = 0; i < this.nbMoonInTab; i++) {
      if (this.moon_tab[i] != null) this.moon_tab[i].orbitAndRotation();
    }
  }

 /**
   * @role: displays the orbits on the screen using dots to 
   *        draw for each degree of a trigonometric circle.
   */
  void drawOrbit() {
    stroke(255);
    strokeWeight(2);

    // we draw points at each degree, for each position on the planet. (forms a circle)
    for (int i = 0; i < this.nbMoonInTab; i++) {      
      if (this.moon_tab[i] != null) {
        
        for (int j = 0; j < 360; j++) {            
          // use the trigonometric to make a circle if not rotate (easier to use).
          float distanceMoonAstre = this.moon_tab[i].distanceMoonAstre;
          point(width/2 + sin(j) * distanceMoonAstre, height/2, -500 + cos(j) * distanceMoonAstre);
        }
      }
    }

    noStroke();
  }

  /**
    * @role : displays the rings of a planet on the screen using dots to
    *         draw for each degree a trigonometric circle.
    * @param ringSize     : the size of a ring.
    * @parma ringDistance : the distance of a ring with the star having them.
    */
  void drawRing(float ringSize, float ringDistance) {
    stroke(240, 195, 0);
    strokeWeight(ringSize);

    for (int i = 0; i < 360; i++) {
      point(this.positionAstre.x + sin(i) * ringDistance, height/2, this.positionAstre.z + cos(i) * ringDistance);
    }
    noStroke();
  }

  /**
    * @role : procedure for adding a moon to a star thanks to its constructor.
    * @param sizeMoon                 : size of the star.
    * @param positionSuperAstre       : position of the attracting star.
    * @param vOrbit                   : speed of the star on the orbit.
    * @param angleMoonAstre           : starting angle of the star between the attracting star and itself.
    * @param vRotation                : rotation speed on itself.
    * @param angleRotationAstre       : starting angle of the star when it turns on itself.
    * @param angleInclinaisonRotation : rotation angle on itself with respect to the Y axis.
    * @param distanceMoonAstre        : distance between the star and its attracting star.
    * @param nbMoon                   : moon number of the star.
    * @param moonName                 : name of the star.
    */
  void addMoon(int sizeMoon, PVector positionSuperAstre, float vOrbit, float angleMoonAstre, float vRotation, float angleRotationAstre, float angleInclinaisonRotation, float distanceMoonAstre, int nbMoon, String moonName) {
    if (this.nbMoonInTab < this.moon_tab.length) {
      this.moon_tab[this.nbMoonInTab] = new Astre(sizeMoon, positionSuperAstre, vOrbit, angleMoonAstre, vRotation, angleRotationAstre, angleInclinaisonRotation, distanceMoonAstre, nbMoon, moonName); 

      if (nbMoon > 0) {
        // calculation of the coordinates of the attracting star of the new moon.
        PVector superMoon = new PVector(positionSuperAstre.x + sin(angleMoonAstre) * distanceMoonAstre, positionSuperAstre.y, positionSuperAstre.z + cos(angleMoonAstre) * distanceMoonAstre);
        
        // a box to add if other moon stars (super stars) have sub-moons.
        switch(moonName) {
          case "earthmap.jpg" : this.moon_tab[this.nbMoonInTab].addMoon(10, superMoon, 0.21347, 0, 0.00251, 0, radians(7), 50, 0, "moonmap.jpg");
          break;
        }    
      }

      this.nbMoonInTab++;
    }
  }
  
  /**
    * @role : procedure for deleting the last planet added.
    */
  void delMoon() { 
    this.nbMoonInTab--;
  }
}
