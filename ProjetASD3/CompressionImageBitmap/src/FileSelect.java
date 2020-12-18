import javax.swing.*;
import javax.swing.filechooser.FileNameExtensionFilter;

/**
 * Class that manages file selection.
 */
public class FileSelect {

    /**
     * It allows the selection in graphic form of a file or a folder according to the boolean
     * isDirectory. True = folder.
     *
     * @param isDirectory : true if the file to fetch is a folder.
     * @return a String corresponding to the path of the file to fetch.
     */
    public static String fileSelect(boolean isDirectory) {
        FileNameExtensionFilter filter = new FileNameExtensionFilter("PNG Images", "png");
        JFileChooser jfc = new JFileChooser();

        System.out.println("\nPlease choose a destination folder");

        jfc.setFileFilter(filter); // apply the choice of the type of images in .png
        jfc.setAcceptAllFileFilterUsed(false); // disable the choice of type * .all
        jfc.setFileSelectionMode((isDirectory) ? JFileChooser.DIRECTORIES_ONLY : JFileChooser.FILES_ONLY);

        // as long as the user has not chosen a file, the program will not give an answer
        if (jfc.showOpenDialog(null) == JFileChooser.APPROVE_OPTION)
            return jfc.getSelectedFile().toString();

        return null;
    }
}
