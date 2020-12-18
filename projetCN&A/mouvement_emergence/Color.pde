/*
 * Class qui gére tout ce qui a un rapport avec les couleurs, car le type color
 * n'est pas un objet de base, donc on ne peut pas le mettre dans des ArrayList.
 */
class Color {
  private int hue, saturation, brightness, transparency; // mode HSB (hue pour les couleurs).

  /**
    * Constructeur d'une couleur aléatoire entre différent seuil de saturation, 
    * luminosité et couleur, la transparence est fixé.
    */
  public Color() {
    this.hue          = (int)random(0, 360);
    this.saturation   = (int)random(50, 100);
    this.brightness   = (int)random(60, 100);
    this.transparency = 100; // aucune transparence.
  }
  
  /**
    * Constructeur d'une couleur donnée en paramètre, la transparence est fixé.
    */
  public Color(int hue, int saturation, int brightness) {
    this.hue          = hue;
    this.saturation   = saturation;
    this.brightness   = brightness;
    this.transparency = 100;  // aucune transparence.
  }
  
  // getters :
  public int getHue()          { return this.hue;          }
  public int getSaturation()   { return this.saturation;   }
  public int getBrightness()   { return this.brightness;   }
  public int getTransparency() { return this.transparency; }
}
