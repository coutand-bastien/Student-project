class Asteroid { 
  private PVector positionSuperAstre; // position of the attracting star.
  private PVector asteroidePos;       // position of the asteroid.

  private float vitesseOrbit; // speed of the asteroid.
  private float distance;     // distance between the sun and the asteroid.
  private float angle;        // angle of departure of the asteroid.

  Asteroid(float distance, PVector positionSuperAstre) {
    this.positionSuperAstre = positionSuperAstre;
    this.asteroidePos       = new PVector();

    this.angle        = random(0, 2*PI); // angle between 0 and 2PI.
    this.distance     = random(distance, distance + 100); // random distance between distance and distance + 100 to create a width effect.
    this.vitesseOrbit = random(0.01, 0.8); // speed between 0.01 and 0.8.
  }

  /**
    * @role : displays asteroids on the screen, assigning them a new position 
    *         for each call.
    */
  void displayAsteroid() {
    this.asteroidePos = new PVector(this.positionSuperAstre.x + sin(this.angle) * this.distance, this.positionSuperAstre.y, this.positionSuperAstre.z + cos(this.angle) * this.distance);   
    
    pushMatrix();
      translate(this.asteroidePos.x, this.asteroidePos.y, this.asteroidePos.z);
      fill(211, 211, 211); // grey.
      sphere(5);
    popMatrix();   
    
    this.orbit();
  }

  /**
    * @role : increase the angle thanks to the speed of the 
    *         orbit divide by a number so that it is not too fast. 
    *         Produces a movement effect.
    */
  private void orbit() {
    this.angle += this.vitesseOrbit/50 * MoovePlanete.valueOfSpeed;
  }
}
