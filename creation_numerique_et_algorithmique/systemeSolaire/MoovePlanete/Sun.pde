class Sun extends Astre { 
  private Asteroid asteroide_tab[]; // array containing the asteroids.
  
  Sun(int size, float vitesseOrbit, float angleMoonSun, float vitesseRotation, float angleRotationSun, float angleInclinaisonRotation, String textureSun) {
    super(size, new PVector(width/2, height/2, -500), vitesseOrbit, angleMoonSun, vitesseRotation, angleRotationSun, angleInclinaisonRotation, 0, 9, textureSun); // 9 car neuf planètes dans le système solaire et 0 car le soleil n'est pas la lune d'un autre astre.
    this.asteroide_tab = new Asteroid[MoovePlanete.NBASTEROIDE];
  }
  
  /**
    * @role : procedure initializing the various asteroids.
    * @param distanceAsteroide : distance between the sun and the asteroid.
    */
  void initAsteroide(float distanceAsteroide) {
    for (int i = 0; i < MoovePlanete.NBASTEROIDE; i++) {
      this.asteroide_tab[i] = new Asteroid(distanceAsteroide, new PVector(width/2, height/2, -500)); 
    }
  }
  
  /**
    * @role : procedure displaying the various asteroids on the screen.
    */
  void diplayAsteroide() {
    for (Asteroid asteroide :  this.asteroide_tab) {
      asteroide.displayAsteroid();
    }
  }

  /**
    * @role : procedure displaying the sun in the center of the screen with its texture.
    */
  void showSun() { 
    pushMatrix();
      translate(this.getPositionSuperAstre().x, this.getPositionSuperAstre().y, this.getPositionSuperAstre().z);    // au milieu avec une profondeur de -500.
      rotateY(this.getAngleRotationAstre()); // rotation du soleil selon l'axe Y.
      shape(this.getAstreShape());        
    popMatrix();
    
    // addition of a point of light at the level of the sun.
    pointLight(255,255, 255, width/2, height/2, -300);
  
    if (this.getNbMoonInTab() > 0) this.showMoon(); 
  }
}
