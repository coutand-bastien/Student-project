import exception.QuadtreeException;

import java.io.File;
import java.io.IOException;
import java.util.Scanner;

public class UserInterface {
    final Scanner sc;

    public UserInterface() {
        this.sc = new Scanner(System.in);
    }

    /**
     * It allows the graphic display in the console.
     * It allows the execution of all the functions implemented in the project.
     *
     * @throws IOException       : transmits a possible error coming from toPNG or toTXT.
     * @throws QuadtreeException : transmits a possible error coming from compressPhi or compressDelta.
     */
    public void graphicInterface() throws QuadtreeException, IOException {
        boolean keepOnGoing = true; // (keep Going = true) -> the user wants to continue the program.
        String answerKeepOnGoing;   // user answer = 'y / n / Y / N'.

        int answerInt; // store the integer resulting from the user's choices.

        Quadtree quadtree   = null;
        String quadtreeName = "";

        // their uses, are made in case no operation is done and a toPNG or toTXT is done
        int opNumber = 0;
        String op    = "";

        String txtChoice1 =
                        "\nWelcome to the Bitmap compression program \n" +
                        "\nWhat do you want to do?" +
                        "\n1 - Load a PNG image in memory into a quadtree" +
                        "\n2 - Apply Delta compression for a given delta" +
                        "\n3 - Apply a Phi compression for a given phi" +
                        "\n4 - Save the quadtree in a PNG file" +
                        "\n5 - Save the textual representation of the quadtree in a TXT file" +
                        "\n6 - Give the comparative measurements of two PNG image files";

        String txtChoice2 =
                        "\nWhat do you want to do ?" +
                        "\n1 - Load an image from your computer" +
                        "\n2 - load an image from the predefined image folder";

        while (keepOnGoing) {
            answerKeepOnGoing = "";

            answerInt = this.secureInt(txtChoice1, 1, 6); // display the different possible choices and retrieve the user's choice.

            switch (answerInt) {
                case 1: // Load a PNG image in memory into a quadtree
                    int userChoice = this.secureInt(txtChoice2, 1, 2);
                    String pngPath = null;

                    if (userChoice == 1) {
                        pngPath = this.secureFile(false); // choice in the computer files.

                        if (pngPath == null)  // if there is no cancel or exit from the user
                            break;
                    }

                    String defaultPath = this.fileUserChoice();
                    quadtreeName       = (userChoice == 1) ? pngPath.substring(pngPath.lastIndexOf("/")+1, pngPath.lastIndexOf('.')) : defaultPath.substring(defaultPath.lastIndexOf("/")+1, defaultPath.lastIndexOf('.')); // prend le nom du fichier.png
                    quadtree           = new Quadtree((userChoice == 1) ? new ImagePNG(pngPath) :  new ImagePNG(defaultPath));

                    System.out.println(quadtree.toString());
                    break;


                case 2: // Apply Delta compression for a given delta
                    if (quadtree != null) {
                        int delta = this.secureInt("\nPlease choose a delta between 0..255", 0, 255);

                        double timeStart = System.currentTimeMillis();
                        quadtree.compressDelta(delta);
                        System.out.println("\nDELTA in seconds: " + (System.currentTimeMillis() - timeStart) / 1000.0 + "s");

                        opNumber = delta; op = "-delta"; // for toPNG and toTXT

                    }
                    else {
                        System.out.println("\nThe quadtree is empty, no image has been configured. Please enter 1");
                    }
                    break;


                case 3: // Apply a Phi compression for a given phi
                    if (quadtree != null) {
                        int phi = this.secureInt("Please choose a phi between 0..+inf", 0, 2147483647);

                        double timeStart = System.currentTimeMillis();
                        quadtree.compressPhi(phi); // 2147483647 max for int
                        System.out.println("\nPHI in seconds: " + (System.currentTimeMillis() - timeStart) / 1000.0 + "s");

                        opNumber = phi;op = "-phi"; // for toPNG and toTXT
                    }
                    else {
                        System.out.println("\nThe quadtree is empty, no image has been configured. Please enter 1");
                    }
                    break;


                case 4: // Save the quadtree in a PNG file
                    if (quadtree != null) {
                        String dirPath;

                        if (!(dirPath = this.secureFile(true)).equals("null/")) // if there is no cancel or exit from the user
                            quadtree.toPNG(dirPath, quadtreeName, op, opNumber);
                    }
                    else {
                        System.out.println("\nThe quadtree is empty, no image has been configured. Please enter 1");
                    }
                    break;


                case 5: // Save the textual representation of the quadtree in a TXT file
                    if (quadtree != null) {
                        String dirPath;

                        if (!(dirPath = this.secureFile(true)).equals("null/"))  // if there is no cancel or exit from the user
                            quadtree.toTxt(dirPath, quadtreeName, "", 0);
                    }
                    else {
                        System.out.println("\nThe quadtree is empty, no image has been configured. Please enter 1");
                    }
                    break;


                case 6: // Give the comparative measurements of two PNG image files
                    double     weight1, weight2;
                    boolean    isComputingEQM = true; // security variable
                    ImagePNG[] png_tab        = new ImagePNG[2];
                    String     msg            =
                                    "\nPlease choose which folder you want to choose an image from:" +
                                    "\n1 - PNG image from the image bank" +
                                    "\n2 - PNG image from your computer";

                    for (int i = 0; i < png_tab.length; i++) {
                        System.out.println("\nPlease choose the image N°"+ i);

                        if (this.secureInt(msg, 1, 3) == 1) {
                            png_tab[i] = new ImagePNG(this.fileUserChoice()); // PNG image from the image bank
                        } else {
                            String dirPath;

                            if (!(dirPath = this.secureFile(false)).equals("null/")) { // if there is no cancel or exit from the user
                                png_tab[i] = new ImagePNG(dirPath);
                            } else {
                                isComputingEQM = false;
                            }
                        }
                    }

                    if (isComputingEQM) {
                        weight1 = ((double)png_tab[0].width() * (double)png_tab[0].height() * 3.0) / (1024.0*1024.0);
                        System.out.println("\nThe minimum weight of image N°"+ 1 +" is: " + weight1  + "Mo"); // get the weight in Mo

                        weight2 = ((double)png_tab[1].width() * (double)png_tab[1].height() * 3.0) / (1024.0*1024.0);
                        System.out.println("\nThe minimum weight of image N°"+ 2 +" is: " + weight2  + "Mo"); // get the weight in Mo

                        System.out.println("\nThe images are similar to : " + ImagePNG.computeEQM(png_tab[0], png_tab[1]) + "%");
                        System.out.println("\nThe weight ratio of image 1 to image 2 is : " + ((weight1-weight2) / weight1) * 100 + "%");

                    }
                    break;
            }

            // To continue or not...
            while (!(answerKeepOnGoing.equals("y") || answerKeepOnGoing.equals("Y") || answerKeepOnGoing.equals("n") || answerKeepOnGoing.equals("N"))) {
                System.out.println("\nDo you want to do other things? (Y/N)");

                System.out.print("\nreply : ");
                answerKeepOnGoing = this.sc.next();

                if (!(answerKeepOnGoing.equals("y") || answerKeepOnGoing.equals("Y") || answerKeepOnGoing.equals("n") || answerKeepOnGoing.equals("N")))
                    System.out.println("\n" + Main.ANSI_RED + "\"Please enter Y or N! !" + Main.ANSI_RESET);

                if (answerKeepOnGoing.equals("n") || answerKeepOnGoing.equals("N"))
                    keepOnGoing = false;
            }
        }
    }



    /**
     * It allows non-graphic display in the console.
     * It performs all compressions (PHI and DELTA), saves them in a .png and a .txt.
     * In addition it compares them with the image without modification
     *
     * @param args : the list of arguments passed as a parameter of the call to the project via the terminal.
     * @throws IOException       :  transmits a possible error coming from toPNG or toTXT.
     * @throws QuadtreeException : transmits a possible error coming from compressPhi or compressDelta.
     */
    public void nonInteractif(String[] args) throws IOException, QuadtreeException {
        if (Integer.parseInt(args[1]) >= 0 && Integer.parseInt(args[1]) <= 255) {
            if (Integer.parseInt(args[2]) > 0) {
                ImagePNG imagePNG  = new ImagePNG(args[0]);
                Quadtree quadtree1 = new Quadtree(imagePNG), quadtree2 = new Quadtree(imagePNG);
                String   dirPath, fileName;
                double   weight1, weight2;

                System.out.println(quadtree1.toString());
                fileName = args[0].substring(args[0].lastIndexOf("/") + 1, args[0].lastIndexOf('.'));
                weight1 = ((double)imagePNG.width() * (double)imagePNG.height() * 3.0); // H * W * 3 (because 3 bytes per pixel).

                // compressDelta...
                if (!(dirPath = this.secureFile(true)).equals("null/")) {  // if there is no cancel or exit from the user
                    quadtree1.compressDelta(Integer.parseInt(args[1]));
                    weight2 = ((double)quadtree1.leafAccount() * 3.0); // the number of leafs gives the number of pixels.

                    quadtree1.toPNG(dirPath, fileName, "-delta", Integer.parseInt(args[1]));
                    quadtree1.toTxt(dirPath, fileName, "-delta", Integer.parseInt(args[1]));
                    System.out.println("\nThe weight ratio of image 2 to image 1 is : " + (weight2/weight1) * 100 + "%");
                    System.out.println("Comparison between the png image and the image compressed with the delta method : " + ImagePNG.computeEQM(imagePNG, quadtree1.getPNG()) + "%");
                }

                // compressPhi...
                if (!(dirPath = this.secureFile(true)).equals("null/")) {  // if there is no cancel or exit from the user
                    quadtree2.compressPhi(Integer.parseInt(args[2]));
                    weight2 = ((double)quadtree2.leafAccount() * 3.0); // the number of leafs gives the number of pixels.

                    quadtree2.toPNG(dirPath, fileName, "-phi", Integer.parseInt(args[2]));
                    quadtree2.toTxt(dirPath, fileName, "-phi", Integer.parseInt(args[2]));
                    System.out.println("\nThe weight ratio of image 2 to image 1 is : " + (weight2/weight1) * 100 + "%");
                    System.out.println("Comparison between the png image and the image compressed with the phi method : " + ImagePNG.computeEQM(imagePNG, quadtree2.getPNG()) + "%");
                }
            }
            else {
                System.out.println("parameter error : 0 <phi");
            }
        }
        else {
            System.out.println("parameter error: 0 <= delta <= 255");
        }
    }


    /**
     * The function is used to secure an "int" type entry and
     * to make it correspond to the desired size: it is between Minimum and Maximum.
     *
     * @param msg: the message with the list of digits, desired numbers.
     * @param borneMin: the minimum number that the value must not exceed.
     * @param borneMax: the maximum number that the value must not exceed.
     * @return an integer between [lower limit, maximum limit].
     */
    private int secureInt (String msg, int borneMin, int borneMax) {
        return this.secureInt_rec (msg, borneMin, borneMax, -1);
    }

    private int secureInt_rec (String msg, int borneMin, int borneMax, int reponse) {
        boolean isInt = false;

        System.out.println(msg);
        System.out.print("\nanswer : ");

        try {
            reponse = this.sc.nextInt();

            if (reponse >= borneMin && reponse <= borneMax) {
                isInt = true;
            } else {
                System.out.println("\n" + Main.ANSI_RED + "Please enter a number between " + borneMin + " and " + borneMax + " !" + Main.ANSI_RESET + "\n");
            }
        }
        catch (Exception e) {
            System.out.println("\n" + Main.ANSI_RED + "Please enter an integer !" + Main.ANSI_RESET);
        }

        this.sc.nextLine();

        return isInt ? reponse : this.secureInt_rec(msg, borneMin, borneMax, reponse);
    }


    /**
     * The function allows to call to call the methods of the FileSeclect class
     * which allows to choose a file or a folder, according to the boolean in parameter,
     * thanks to a graphical interface.
     *
     * @param isDirectory : true if the file to fetch is a folder.
     * @return a String corresponding to the path of the file to fetch.
     */
    private String secureFile(boolean isDirectory) {
        return isDirectory ? FileSelect.fileSelect(true) + "/" :  FileSelect.fileSelect(false);
    }


    /**
     * The function allows you to display all the files in a folder as a
     * numbered list.
     *
     * @param msg : The list containing all the file names numbered from 1 to number of file.
     * @return It returns an integer, which is the maximum of this list (its size).
     */
    private int diplayDirectory(StringBuilder msg) {
        File[] file_tab = new File("./img/pngs").listFiles();
        int lenght = 0;

        if (file_tab != null) {
            lenght = file_tab.length;

            for (int i = 0; i < lenght; i++) {
                msg.append("\n").append(i).append(" - ").append(file_tab[i].getName());
            }
        } else {
            System.out.println("No files in folder !");
        }

        return lenght;
    }


    /**
     * It allows user-machine interface, it displays a list of files
     * coming from a folder, it retrieves the user's choice, and returns it.
     *
     * @return a String, which is the path of the user file choice.
     */
    private String fileUserChoice() {
        StringBuilder msg        = new StringBuilder("\nThe files to choose from are :");
        File[]         file_tab  = new File("./img/pngs").listFiles();
        int           maxBorn    = this.diplayDirectory(msg);
        int           userChoice = this.secureInt(msg.toString(), 0, maxBorn-1);

        assert file_tab != null;
        return "./img/pngs/" + file_tab[userChoice].getName();
    }
}