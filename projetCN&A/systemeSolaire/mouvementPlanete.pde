Sun sun;  
float j; 
float posX; 
float posY; 
boolean sunExist; 
boolean planetExist; 
boolean stroke; 
boolean cam; 
PImage b; 
void setup(){
  size(1800,1012, P3D); 
  frameRate(8); 
  sunExist = false; 
  j = 0; 
  stroke = true; 
  b = loadImage("stars4.jpg");
}

void  draw(){
  background(b); 
  
  if(stroke == false){
    noStroke(); 
  }else{
    stroke(5); 
  }
  
  if(sunExist == true){
    if(cam){
    camera(mouseY*4, height/2, mouseX*4, width/2, height/2, mouseX, 1, 1, 1); 
    }
    sun.showSun();
    //pointLight(255, 255, 255, mouseX, mouseY, 0);
    sun.orbitPlanet(); 
   
    if(stroke == true){
      translate(posX, posY); 
      ellipse(0, 0, 525, 525);  //Mercure
      ellipse(262, 0, 6,6); 
      
      ellipse(0, 0, 650, 650);  //Venus
      ellipse(325, 0, 6,6);
      
      
      ellipse(0, 0, 775, 775);  //Terre
      ellipse(388, 0, 8,8);
      
      ellipse(0, 0, 900, 900);  //Mars
      ellipse(450, 0, 6,6);
      
      ellipse(0, 0, 1025, 1025);  //Jupiter
      ellipse(512, 0, 40, 40);
      
      ellipse(0, 0, 1150, 1150);  //Saturne
      ellipse(574, 0, 34, 34);
      
      ellipse(0, 0, 1275, 1275);  //Uranus
      ellipse(636, 0, 15, 15);
      
      ellipse(0, 0, 1400, 1400);  //Neptune
      ellipse(700, 0, 14, 14); 
      
      ellipse(0, 0, 1525, 1525);  //Pluton
      ellipse(764, 0, 10,10);
      
      line(-sun.local().x, 0, width, 0); 
      line(0, -sun.local().y, 0, height);  
    }
  }
  
}

void keyPressed(){
  
  if(key == 97){
    sun.deletePlanet(); 
    if(j>=0){
      j--; 
    }
  }
  
  if(key == 98){
    stroke = !stroke; 
  }
  
  if(key == 99){
    cam = !cam; 
  }
}
/*
void mousePressed(){
  camera(mouseX*2, mouseY*2, 200, width/2, height/2, 0, 0, 1, 1); 
  
}*/

void mouseClicked(){
  if(sunExist == false){
    
    sun = new Sun(200, 0.001, mouseX, mouseY);
    posX = mouseX; 
    posY = mouseY; 
    sunExist = true; 
    
  }else if(j <= 9){
    
    if(mouseX >= posX + 225  && mouseX <= posX + 292){
      planetExist = true; 
      PlanetOfSun newPlanet = new PlanetOfSun(2, 0.087,mouseX, mouseY, sun.local(), "mercurymap.jpg", false); 
      sun.addPlanet(newPlanet); 
      j++; 
    }
    
    if(mouseX >= posX + 294  && mouseX <= posX + 358){
      planetExist = true; 
      PlanetOfSun newPlanet = new PlanetOfSun(4, 0.063,mouseX, mouseY, sun.local(), "venusmap.jpg", false); 
      sun.addPlanet(newPlanet); 
      j++; 
    }
    
    if(mouseX >= posX + 360  && mouseX <= posX + 420){
      planetExist = true; 
      PlanetOfSun newPlanet = new PlanetOfSun(4, 0.052,mouseX, mouseY, sun.local(), "earthmap.jpg", true); 
      sun.addPlanet(newPlanet); 
      j++; 
    }
    
    if(mouseX >= posX + 422  && mouseX <= posX + 478){
      planetExist = true; 
      PlanetOfSun newPlanet = new PlanetOfSun(3, 0.043,mouseX, mouseY, sun.local(), "mars_1k_color.jpg", false); 
      sun.addPlanet(newPlanet); 
      j++; 
    }
    
    if(mouseX >= posX + 480  && mouseX <= posX + 542){
      planetExist = true; 
      PlanetOfSun newPlanet = new PlanetOfSun(40, 0.024,mouseX, mouseY, sun.local(),"jupitermap.jpg", false); 
      sun.addPlanet(newPlanet); 
      j++; 
    }
    
    if(mouseX >= posX + 544  && mouseX <= posX + 606){
      planetExist = true; 
      PlanetOfSun newPlanet = new PlanetOfSun(34, 0.018,mouseX, mouseY, sun.local(), "saturnmap.jpg", false); 
      sun.addPlanet(newPlanet); 
      j++; 
    }
    
    if(mouseX >= posX + 608  && mouseX <= posX + 668){
      planetExist = true; 
      PlanetOfSun newPlanet = new PlanetOfSun(15, 0.013,mouseX, mouseY, sun.local(), "uranusmap.jpg", false); 
      sun.addPlanet(newPlanet); 
      j++; 
    }
    
    if(mouseX >= posX + 670  && mouseX <= posX + 730){
      planetExist = true; 
      PlanetOfSun newPlanet = new PlanetOfSun(14, 0.01,mouseX, mouseY, sun.local(), "neptunemap", false); 
      sun.addPlanet(newPlanet); 
      j++; 
    }
    
    if(mouseX >= posX + 732  && mouseX <= posX + 800){
      planetExist = true; 
      PlanetOfSun newPlanet = new PlanetOfSun(1, 0.009,mouseX, mouseY, sun.local(), "plutomap1k.jpg", false); 
      sun.addPlanet(newPlanet); 
      j++; 
    }
  }
}
