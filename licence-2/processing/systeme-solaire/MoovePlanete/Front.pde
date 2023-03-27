class Front {
  private PFont  police;
  private PImage toucheClavierA, toucheClavierZ, toucheClavierE, toucheClavierR, toucheClavierT, 
                 toucheClavierY, toucheClavierU, toucheClavierI, toucheClavierO, toucheClavierB,
                 toucheClavierC, toucheClavierV, toucheClavierQ, toucheClavierX, toucheClavierS, 
                 toucheClavierD, toucheClavierH, toucheClavierN, toucheClavierW, toucheClavierP;
                 
  private PImage toucheClavierDOWN, toucheClavierUP, toucheClavierRIGHT, toucheClavierLEFT;
  
  Front() {
    this.police = loadFont("Monospaced.bolditalic-48.vlw");
    textFont(police);
    
    this.toucheClavierA = loadImage("toucheA.png");
    this.toucheClavierZ = loadImage("toucheZ.png");
    this.toucheClavierE = loadImage("toucheE.png");
    this.toucheClavierR = loadImage("toucheR.png");
    this.toucheClavierT = loadImage("toucheT.png");
    this.toucheClavierY = loadImage("toucheY.png");
    this.toucheClavierU = loadImage("toucheU.png");
    this.toucheClavierI = loadImage("toucheI.png");
    this.toucheClavierO = loadImage("toucheO.png");
    this.toucheClavierP = loadImage("toucheP.png");
    
    this.toucheClavierB     = loadImage("toucheB.png");
    this.toucheClavierDOWN  = loadImage("toucheDOWN.png");
    this.toucheClavierUP    = loadImage("toucheUP.png");
    this.toucheClavierRIGHT = loadImage("toucheRIGHT.png");
    this.toucheClavierLEFT  = loadImage("toucheLEFT.png");
    
    this.toucheClavierC = loadImage("toucheC.png");
    this.toucheClavierV = loadImage("toucheV.png");
    this.toucheClavierQ = loadImage("toucheQ.png");
    this.toucheClavierX = loadImage("toucheX.png");
    this.toucheClavierS = loadImage("toucheS.png");
    this.toucheClavierD = loadImage("toucheD.png");
    this.toucheClavierH = loadImage("toucheH.png");
    this.toucheClavierN = loadImage("toucheN.png");
    this.toucheClavierW = loadImage("toucheW.png");
  }
  
  /**
    * @role : procedure displaying the aids for the different interactions.
    */
  void displayHelp() {
    stroke(255);
    strokeWeight(2);
    fill(255);
    
    // title :
    textSize(38);
    text("Welcome to the help page", 580, 50, 0);  
    line(570, 65, 1140, 65); // underline the title.
    
    // footer :
    textSize(23);
    text("* : hold down", 80, 900);
    
    textSize(19);
    text("Program created by Bastien Coutand & Thomas Georges", 10, 992, 0);
    text("19/04/2020, V.1.0.0", 1560, 992, 0);
    
    // body :    
    textSize(33);
    text("Display of planets :", 50, 200, 0);
    
      textSize(25);
      image(toucheClavierA, 60, 230); 
      text("Mercure", 120, 260, 0);
      
      image(toucheClavierZ, 60, 290); 
      text("Vénus", 120, 320, 0);
      
      image(toucheClavierE, 60, 350); 
      text("Terre", 120, 380, 0);
      
      image(toucheClavierR, 60, 410); 
      text("Mars", 120, 440, 0);
      
      image(toucheClavierT, 60, 470); 
      text("Jupiter", 120, 500, 0);
      
      image(toucheClavierY, 60, 530); 
      text("Saturne", 120, 560, 0);
      
      image(toucheClavierU, 60, 590); 
      text("Uranus", 120, 620, 0);
      
      image(toucheClavierI, 60, 650); 
      text("Neptune", 120, 680, 0);
      
      image(toucheClavierO, 60, 710); 
      text("Pluton", 120, 740, 0);
      
      image(toucheClavierP, 60, 770); 
      text("Asteroid belt", 120, 800, 0);
    
    textSize(33);
    text("Camera options :", 600, 200, 0);
       
       textSize(25);
       image(toucheClavierB, 610, 230); 
       text("Seen from above", 670, 260, 0);
      
       image(toucheClavierUP, 610, 290); 
       text("Zoom *", 670, 320, 0);
      
       image(toucheClavierDOWN, 610, 350); 
       text("Dézoom *", 670, 380, 0);
       
       image(toucheClavierRIGHT, 610, 410); 
       text("Right *", 670, 440, 0);
      
       image(toucheClavierLEFT, 610, 470); 
       text("Left *", 670, 500, 0);
    
    textSize(33);
    text("Other options :", 1150, 200, 0);       
       
       textSize(25);
       image(toucheClavierC, 1160, 230); 
       text("Accelerate the movement of planets *", 1220, 260, 0);
      
       image(toucheClavierV, 1160, 290); 
       text("Decelerates the movement of planets *", 1220, 320, 0);
       
       image(toucheClavierQ, 1160, 350); 
       text("Delete the last planet added", 1220, 380, 0);
      
       image(toucheClavierX, 1160, 410); 
       text("Remove orbits", 1220, 440, 0);
      
       image(toucheClavierS, 1160, 470); 
       text("Stop rotation", 1220, 500, 0);
      
       image(toucheClavierD, 1160, 530); 
       text("Debug", 1220, 560, 0);
     
       image(toucheClavierH, 1160, 590); 
       text("Help or planets display *", 1220, 620, 0);
       
       image(toucheClavierN, 1160, 650); 
       text("Displays info on planets *", 1220, 680, 0);
      
       image(toucheClavierW, 1160, 710); 
       text("Restart", 1220, 740, 0);      
  }
  
  /**
    * @role : procedure displaying the characteristics of the different planets.
    */
  void displayInfo() {
    stroke(255);
    strokeWeight(2);
    fill(255);
    
    // title :
    textSize(38);
    text("Characteristic of the planets", 580, 50, 0);  
    line(570, 65, 1230, 65); // underline the title  
    
    // footer :    
    textSize(19);
    text("Source : http://www.astronoo.com/fr/articles/caracteristiques-des-planetes.html", 50, 862);
    text("Program created by Bastien Coutand & Thomas Georges", 10, 992, 0);
    text("19/04/2020, V.1.0.0", 1560, 992, 0);
    
    // body :    
    textSize(20);
    text("Astre", 50, 320, 0);
      text("Mercure", 50, 400, 0);
      text("Vénus", 50, 450, 0);
      text("Terre", 50, 500, 0);
      text("Mars", 50, 550, 0);
      text("Jupiter", 50, 600, 0);
      text("saturne", 50, 650, 0);
      text("Uranus", 50, 700, 0);
      text("Neptune", 50, 750, 0);
      text("Pluton", 50, 800, 0);
    
    text("Diameter(km)", 210, 320, 0);
      text("  4 880", 210, 400, 0);
      text(" 12 104", 210, 450, 0);
      text(" 12 756", 210, 500, 0);
      text("  6 805", 210, 550, 0);
      text("142 984", 210, 600, 0);
      text("120 536", 210, 650, 0);
      text(" 51 312", 210, 700, 0);
      text(" 49 922", 210, 750, 0);
      text("  2 300", 210, 800, 0);
    
    text("Orbit tilt(°)", 380, 320);
      text("7.004870", 380, 400, 0);
      text("3.390000", 380, 450, 0);
      text("0", 380, 500, 0);
      text("1.850610", 380, 550, 0);
      text("1.305300", 380, 600, 0);
      text("2.484460", 380, 650, 0);
      text("0.772556", 380, 700, 0);
      text("1.769170", 380, 750, 0);
      text("17.141750", 380, 800, 0);
    
    text("Orbital speed(km/s)", 655, 320);
      text("48.92", 655, 400, 0);
      text("35.02", 655, 450, 0);
      text("29.78", 655, 500, 0);
      text("24.07 ", 655, 550, 0);
      text("13.05", 655, 600, 0);
      text("9.64", 655, 650, 0);
      text("6.81", 655, 700, 0);
      text("5.43", 655, 750, 0);
      text("4.72", 655, 800, 0);
    
    text("Mass(kg)", 940, 320);
      text("0.3302e24", 940, 400, 0);
      text("4.8685e24", 940, 450, 0);
      text("5.9736e24", 940, 500, 0);
      text("0.6418e24", 940, 550, 0);
      text("1898.6e24", 940, 600, 0);
      text("568.46e24", 940, 650, 0);
      text("86.810e24", 940, 700, 0);
      text("102.43e24", 940, 750, 0);
      text("1.3140e22", 940, 800, 0);
    
    text("Revolution(an)", 1080, 320);
      text("0.241", 1080, 400, 0);
      text("0.615", 1080, 450, 0);
      text("1", 1080, 500, 0);
      text("1,881", 1080, 550, 0);
      text("11.862", 1080, 600, 0);
      text("29.452", 1080, 650, 0);
      text("84.323", 1080, 700, 0);
      text("164.882", 1080, 750, 0);
      text("248.078", 1080, 800, 0);
      
    text("Axis tilt(°)", 1280, 320);
      text("0.03", 1280, 400, 0);
      text("177.36", 1280, 450, 0);
      text("23.43", 1280, 500, 0);
      text("25.19", 1280, 550, 0);
      text("3.12", 1280, 600, 0);
      text("26.73", 1280, 650, 0);
      text("97.77", 1280, 700, 0);
      text("29.58", 1280, 750, 0);
      text("17.14", 1280, 800, 0);
    
    text("Rotation time(J)", 1530, 320);
      text("58,646", 1530, 400, 0);
      text("243,019", 1530, 450, 0);
      text("23H56", 1530, 500, 0);
      text("24H37", 1530, 550, 0);
      text("9H50", 1530, 600, 0);
      text("10H14", 1530, 650, 0);
      text("10H49", 1530, 700, 0);
      text("15H40", 1530, 750, 0);
      text("6,387", 1530, 800, 0);    
  }
}
