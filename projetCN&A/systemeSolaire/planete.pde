class Planet{
  //PVector pos; 
  float radius; 
  float angle;
  float distance; 
  
  Planet(float r) {
   radius   = r; 
  }
  
 /* void spawnMoons(int total, int level) {
    planets = new Planet[total]; 
    for(int i = 0; i < planets.length; i++){
      planets[i] = new Planet(radius/(level*2), random(50,150), random(-0.1,10)); 
      if(level < 3){
        planets[i].spawnMoons(int(random(0,4)), level+1); 
      }
    }
  }*/
  
}

/***************************************************************************************************/

class Sun extends Planet{
  float radius; 
  float distance; 
  PlanetOfSun[] planets; 
  float orbitSpeed; 
  int indice; 
  PVector localisation; 
  float angle; 
  
  PImage texturePlanet;
  PShape globe;
  
  Sun(float r, float o, float positionX, float positionY) {
   super(r);
   planets = new PlanetOfSun[10];
   orbitSpeed = o; 
   indice  = 0; 
   localisation = new PVector(positionX,positionY); 
   angle = 0; 
   
   noStroke(); 
   this.texturePlanet = loadImage("sunmap.jpg");
   this.globe         = createShape(SPHERE, r);
   this.globe.setTexture(texturePlanet);
  }
   
  void addPlanet(PlanetOfSun planet){
     if(indice < 10){
      planets[indice] = planet; 
      indice ++; 
     }
   }
  
  void deletePlanet(){
    if(indice > 0){
      planets[indice - 1] = null; 
      indice --; 
    }  
}
  
  void showSun(){
    pushMatrix(); 
    
      translate(localisation.x,localisation.y); 
      rotate(angle);
      shape(this.globe); 
      
        pushMatrix(); 
          showPlanet();
        popMatrix(); 
        
     popMatrix(); 
     
    angle += orbitSpeed; 
  }
  
  void showPlanet(){
    if(planets != null){
      for(int i = 0; i < planets.length; i++){
        if(planets[i] != null){
          pushMatrix(); 
          rotate(planets[i].orbit());
          planets[i].show(); 
          translate(-(planets[i].localisation().x-localisation.x), -(planets[i].localisation().y - localisation.y));
          popMatrix(); 
        }
      }
    } 
  }
  
  void orbitPlanet(){ 
    if(planets != null){
      for(int i = 0; i < planets.length; i++){
        if(planets[i] != null){
          planets[i].orbit(); 
        }
      }
    }
  }
  
  float getRadius(){
    return this.radius; 
  }
  
  PVector local(){
    return localisation; 
  }
  
  int getIndice(){
  return this.indice; 
  } 
}

/***************************************************************************************************/

class PlanetOfSun extends Planet {
  float radius; 
  float angle;
  float distance; 
  float orbitSpeed; 
  PVector localisationPl;
  PVector localisationSun; 
  
  PImage texturePlanet;
  PShape globe;
  
  boolean moon; 
  
  PImage moonTexture; 
  PShape moonShape; 
  
  PlanetOfSun (float r, float o, float positionX, float positionY, PVector local, String name, boolean moonExist) {
   super(r);
   orbitSpeed     = o; 
   angle          = 0;
   localisationPl = new PVector(positionX, positionY); 
   localisationSun = new PVector(local.x, local.y); 
   moon            = moonExist; 
   noStroke(); 
   this.texturePlanet = loadImage(name);
   this.globe         = createShape(SPHERE, r);
   this.globe.setTexture(texturePlanet);
   
   this.moonTexture   = loadImage("mercurymap.jpg"); 
   this.moonShape     = createShape(SPHERE, 1); 
   this.moonShape.setTexture(moonTexture); 
  }
  
  float orbit() {
    return angle += orbitSpeed; 
  }
  
  void show(){ 
    translate(localisationPl.x - localisationSun.x, localisationPl.y - localisationSun.y);
    pushMatrix();
      rotate(50*angle); 
      shape(this.globe);
      orbit(); 
      if(moon){
        spawnMoons(angle); 
      }
    popMatrix(); 
     
  }
  
  void spawnMoons(float angle){
    pushMatrix(); 
      translate(200, 0); 
      rotate(-angle*4);
      shape(this.moonShape); 
      
    popMatrix(); 
  }
  
  PVector localisation(){
    return localisationPl; 
  }
  
   
}
