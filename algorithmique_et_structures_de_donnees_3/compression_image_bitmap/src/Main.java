/*
 * @nameProject : Compress bitmap images
 *
 * @project : The objective of the project is to achieve lossy compression of a
 *            bitmap image saved in PNG format and to observe the effects on its
 *            quality and weight.
 *
 * @partOfTheProject : project as part of courses at the University of Nantes.
 *
 * @lastUpdate : 05 december 2020.
 *
 * @Creator : COUTAND Bastien (bastien.coutand@etu.univ-nantes.fr),
 *            MAHBOUBI Saad   (saad.mahboubi@etu.univ-nantes.fr)
 */
public class Main {

    // colors for the terminal.
    public static final String ANSI_RED   = "\u001B[31m";
    public static final String ANSI_RESET = "\u001B[0m";

    public static void main(String[] args) {
        UserInterface userInterface = new UserInterface();

        try {
            if (args.length == 0)
                userInterface.graphicInterface();
            else if (args.length == 3)
                userInterface.nonInteractif(args);
            else
                System.out.println("You have to put a PNG image, a delta and a phi");
        }
        catch (Exception e) {
            System.out.println("\n" + ANSI_RED + e.toString() + ANSI_RESET);
            e.printStackTrace();
        }

        System.out.println("\nByeBye");
    }
}
