static final int NBPLANETMAX = 9;   // maximum number of stars (the solar system has nine planets in total).
static final int NBASTEROIDE = 500; // maximum number of asteroids.

static boolean debug;      // flag allowing the activation of debugging (display of the axes of rotation).
static float valueOfSpeed; // multiple of the speed (default = 1).

boolean stopZoom, stopDezoom, stopDroite, stopGauche, stopAcc, stopDec; // flag allowing the prolonged key press.
boolean showOrbit, stop, haut, help, info, asteroide; // flag allowing the activation of different options.
float zoomHB, zoomDG; // zoom position.

PImage backgroundImage;

Sun sun;
Front front;

void settings() {
  size(1800, 1012, P3D);
}

void setup() {
  frameRate(20);
  noStroke();

  showOrbit = true;
  stop      = false;
  debug     = false;
  haut      = false;
  help      = false; 
  info      = false;

  stopAcc    = false;
  stopDec    = false;
  stopZoom   = false; 
  stopDezoom = false;
  stopDroite = false;
  stopGauche = false;
  
  asteroide = false;

  zoomHB       = 900; 
  zoomDG       = width/2; 
  valueOfSpeed = 1;
 //<>//
  sun   = new Sun(70, 0, 0, 0.2, 0, 0, "sunmap.jpg");
  front = new Front();
  
  sun.initAsteroide(700); // we create the asteroids only once, because they require a lot of computing power.

  backgroundImage = loadImage("stars4.png");
}

void draw() { 
  background(backgroundImage);
  
  if (help && !info) {
    camera(); // return the camera to the initial position.
    front.displayHelp();
  } 
  else if (!help && info) {
    camera(); // return the camera to the initial position.
    front.displayInfo();
  } 
  else if (!help && !info) {
   // change of camera depending on the flag (top).
    if (!haut) {
      camera(width/2, 0, zoomHB, zoomDG, height/2, -500, 0, 1, 0);
    } else {
      camera(width/2, -zoomHB, 0, width/2, height/2, -500, 0, 1, 0);
    }

    sun.showSun(); 
    if (asteroide) sun.diplayAsteroide();  // when the flag (asteroid) is true, then there is display of the asteroid belt.
    if (showOrbit) sun.drawOrbit();        // when the flag (showOrbit) is true, then there is display of the orbits.
    if (!stop)     sun.orbitAndRotation(); // when the flag (stop) is false, then there is a rotation of the planets. //<>//

    /////////////////////////////////////////
    //           APPUIE PROLONGE           //
    /////////////////////////////////////////

    if (stopZoom) zoomHB += 20;
    if (stopDezoom) zoomHB -= 20; 
    if (stopDroite) zoomDG -= 20; 
    if (stopGauche) zoomDG += 20; 
    if (stopAcc) valueOfSpeed += 0.1;
    if (stopDec) valueOfSpeed -= 0.1;
  } 
}

void keyPressed() {

                    /////////////////////////////////////////
                    //         AFFICHAGE PLANETE           //
                    /////////////////////////////////////////

  /*
   * Possibility of putting the same planet several times if the desire is felt.
   */
  PVector sunPos = new PVector(width/2, height/2, -500);
  if (key == 'a') sun.addMoon(20, sunPos, 1.F,     0, 0.00710, 0, 0,             100,  0, "mercurymap.jpg");            
  if (key == 'z') sun.addMoon(24, sunPos, 0.73294, 0, 0.00171, 0, radians(-2),   200,  0, "venusmap.jpg");      
  if (key == 'e') sun.addMoon(28, sunPos, 0.62327, 0, 0.41666, 0, radians(23.5), 350,  1, "earthmap.jpg");  
  if (key == 'r') sun.addMoon(26, sunPos, 0.50460, 0, 0.40816, 0, radians(25),   550,  0, "marsmap.jpg");       
  if (key == 't') sun.addMoon(54, sunPos, 0.27354, 0, 1.F,     0, radians(3),    1000, 0, "jupitermap.jpg");           
  if (key == 'y') sun.addMoon(44, sunPos, 0.20217, 0, 0.86956, 0, radians(27),   1300, 0, "saturnmap.jpg");    
  if (key == 'u') sun.addMoon(36, sunPos, 0.14252, 0, 0.58823, 0, radians(98),   1600, 0, "uranusmap.jpg");    
  if (key == 'i') sun.addMoon(22, sunPos, 0.11364, 0, 0.62500, 0, radians(27),   2000, 0, "neptunemap.jpg");   
  if (key == 'o') sun.addMoon(15, sunPos, 0.09879, 0, 0.06535, 0, radians(17),   2700, 0, "plutonmap.jpg"); 
  if (key == 'p') asteroide = !asteroide; // affiche ou non la ceinture astéroïde.
  
                     /////////////////////////////////////////
                     //         OPTIONS CAMERA              //
                     /////////////////////////////////////////

  // key to see from above.
  if (key == 'b') haut = !haut;

  // key to zoom.
  if (keyCode == DOWN) stopZoom = true; 

  // key to zoom out.
  if (keyCode == UP) stopDezoom = true;   
  
  // key to "zoom" on the right.
  if (keyCode == RIGHT) stopDroite = true; 

  // key to "zoom" to the left.
  if (keyCode == LEFT) stopGauche = true;   

                      /////////////////////////////////////////
                      //         OPTIONS INTERRACTIVES       //
                      /////////////////////////////////////////

  // a touch to accelerate the planets.
  if (key == 'c') stopAcc = true;

  // a key to accelerate the planets, it also makes it possible to turn the planets in the opposite direction when the acceleration becomes negative.
  if (key == 'v') stopDec = true;

  // a key to delete the last planet added around the sun.
  if (key == 'q') sun.delMoon();

  // display the lines representing the orbits of the planets on the screen.
  if (key == 'x') showOrbit = !showOrbit;

  // stop the movement of the stars.
  if (key == 's') stop = !stop; 

  // display the axes of rotation of the planets on themselves.
  if (key == 'd') debug = !debug;
  
  // display the help page to see the keys.
  if (key == 'h') help = true;
  
  // display information about the planets.
  if (key == 'n') info = true;

  // restart.
  if (key == 'w') setup();
}

/*
 *Detect when a key is released. * Useful for long press of a key on the keyboard.
 */
void keyReleased() {
  if (keyCode == DOWN)  stopZoom   = false; 
  if (keyCode == UP)    stopDezoom = false;  
  if (keyCode == RIGHT) stopDroite = false; 
  if (keyCode == LEFT)  stopGauche = false; 

  if (key == 'c') stopAcc = false;
  if (key == 'v') stopDec = false;
  
  if (key == 'h') help = false;
  if (key == 'n') info = false;
}
