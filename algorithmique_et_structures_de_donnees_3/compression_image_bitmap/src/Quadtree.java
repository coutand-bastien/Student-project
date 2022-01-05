import exception.QuadtreeException;

import java.awt.*;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.TreeSet;

/**
 * The R-Quadtree represents a two-dimensional partition of space by breaking down the region into
 * four equal regions, then each region into four sub-regions (NW : 1, NE : 2, SE : 3, SW : 4), and so on, with each "terminal node"
 * called a leaf, comprising corresponding data. to a specific sub-region. Each node in the tree has
 * exactly: either four children or none (leaf).
 *
 *                                      North
 *                               .--------.--------.
 *                               |   NW   |   NE   |
 *                               |  (1)   |  (2)   |
 *                         West  '--------'--------'  East
 *                               |   SW   |    SE  |
 *                               |  (4)   |   (3)  |
 *                               '--------'--------'
 *                                      South
 *
 * A “region” quadtree with depth n can be used to represent an image of 2n × 2n pixels, where the
 * value of each pixel is a color in RGB mode. The parent node represents the entire image. If the
 * pixels in a given region are not all the same color, that region is subdivided.
 *
 *                                        R
 *                        _____________/__|__\_______________
 *                       /           /           \          \
 *                      1           2            3          4
 *                    / | \       / | \        / | \      / | \              W = White, B = Black
 *                   / | | \     / | | \      / | | \    / | | \
 *                  W W  W  W   B W  W  W   B  W  W  B  W  W W  W
 *
 *
 *  ((ffffff ffffff ffffff ffffff) (000000 ffffff ffffff ffffff) (000000 ffffff ffffff 000000) (ffffff ffffff ffffff ffffff))
 *
 * To save space, it is possible to reduce the tree by pruning (removal of leaves): if
 * all the leaves of the same node have the same color, so we can delete these four leaves; we
 * thus decreases the tree (saving memory space) and we make access to the color by one pixel faster
 * (time saving). This compression is lossless, i.e., the image is not degraded.
 *
 *                                        R
 *                        _____________/__|__\_______________
 *                       /           /           \          \
 *                      B           2            3           W              W = White, B = Black
 *                                / | \        / | \
 *                               / | | \      / | | \
 *                              B W  W  W   B  W  W  B
 *
 * (ffffff (000000 ffffff ffffff ffffff) (000000 ffffff ffffff 000000) ffffff)
 *
 *  HEIGHT = WHIDTH = 2^n, n >= 0
 */
public class Quadtree implements Comparable<Quadtree>{
    private ImagePNG png;
    private Color colorValue; // color of the node
    private Quadtree[] node; // 4 max, children
    private final Quadtree father; // father of the node

//---------------------------------------- Builders -------------------------------------------//
    // Starting constructor:
    public Quadtree(ImagePNG png) {
        this.png = png;
        this.colorValue = null;
        this.node = null;
        this.father = null;
        QuadtreeConst(png);
    }

    // node constructor.
    // A node has no color and 4 children.
    private Quadtree(Quadtree father) {
        this.colorValue = null;
        this.father = father;
    }

//---------------------------------------- Methods Builder -------------------------------------------//

    /**
     * It allows the construction of the quadtree thanks to a linear path of the pixels, 
     * starting from the highest point on the left (0, 0).
     * 
     * To achieve this, she looks to see if on her path she encounters a new pixel color. 
     * If so, it divides the image into 4 equivalent regions and traverses them as before. 
     * So on until you get to a leaf.
     * 
     * @param png : The image has been transformed into a quadtree.
     */
    private void QuadtreeConst(ImagePNG png) {
        if (png.width() == 1) // 1x1 px
            this.colorValue = png.getPixel(0, 0);
        else
            QuadtreeConst_rec(png, 0, 0, png.width());
    }

    private void QuadtreeConst_rec(ImagePNG png, int x, int y, int childWith) {
            Color pixel00 = png.getPixel(x, y);
            int columns = x, row = y;
            int childWidthSin1 = childWith - 1;

            // scan the pixels linearly to see if they are all the same color.
            while (pixel00.equals(png.getPixel(columns, row)) && ((row != y + childWidthSin1) || (columns != x + childWidthSin1))) {
                if (columns == x + childWidthSin1) {
                    columns = x;
                    row++;
                } else {
                    columns++;
                }
            }

            // if compressed leaves or node ...
            // if all the pixels in the region are scanned then compression because no other color.
            if (pixel00.equals(png.getPixel(columns, row)) && row == y + childWidthSin1 && columns == x + childWidthSin1) {
                this.colorValue = png.getPixel(columns, row);
                this.node = null;
            }
            else { // ... otherwise there are at least 2 different pixel colors.
                int[][] matrix = {{0, 0}, {1, 0}, {1, 1}, {0, 1}};  // in the order of the regions: North-East (1), North-west (2), South-West (3), South-East (4)
                int widthDiv2 = childWith / 2;

                this.node = new Quadtree[4]; // create 4 children

                // with x and y the old coordinate of the highest point to the left of the region being looked at.
                // NE (i = 0) -> x, y
                // NW (i = 1) -> x + widthDiv2, y
                // SW (i = 2) -> x + widthDiv2, y + widthDiv2
                // SE (i = 3) -> x, y + widthDiv2

                for (int i = 0; i < this.node.length; i++) {
                    this.node[i] = new Quadtree(this);
                    this.node[i].QuadtreeConst_rec(png, x + widthDiv2 * matrix[i][0], y + widthDiv2 * matrix[i][1], widthDiv2);
                }
            }
    }

//---------------------------------------- getters/setters -------------------------------------------//
    public ImagePNG getPNG() {
        return png;
    }
    public Color getColorValue() {
        return colorValue;
    }

    public void setColorValue(Color colorValue) {
        this.colorValue = colorValue;
    }

//---------------------------------------- Methods Compress -------------------------------------------//

    /*----------------------------------------------------------------------------------------------------*
     * By allowing a certain level of loss, the tree can be reduced more sharply. We offer two            *
     * methods both based on the color difference: let F1,. . . , F4 the four leaves of the same node N.  *
     * We denote (Ri, Vi, Bi) the color of each leaf Fi. The average color (Rm, Vm, Bm) of these leafs    *
     * is then defined as follows:                                                                        *
     *                                                                                                    *
     * The colorimetric difference λi of the leaf Fi is its distance normalized to the mean color :       *
     *                         ___________________________________________                                *
     *                        / (Ri - Rm)² + (Vi - Vm)² + (Bi - Bm)²                                      *
     *              λi =  \  /  -----------------------------------                                       *
     *                     \/                   3                                                         *
     *                                                                                                    *
     * and the colorimetric difference Λ at node N is defined by: Λ = max i∈1..4 λi.                      *
     *----------------------------------------------------------------------------------------------------*/


    /**
     * calculation of the Λ (bigLambda).
     *
     * @assert node contains 4 threads which are leaves
     * @return an array with index 0: Λ, 1: Rm, 2: Gm, 3: Bm
     */
    private double[] bigLambda() {
        double[] lambda_tab = new double[4], rgbColor = this.mediumColor();
        double Rm = rgbColor[0], Gm = rgbColor[1], Bm = rgbColor[2], Ri, Gi, Bi;

        for (int i = 0; i < node.length; i++) {
            Ri = this.node[i].getColorValue().getRed();
            Gi = this.node[i].getColorValue().getGreen();
            Bi = this.node[i].getColorValue().getBlue();

            lambda_tab[i] = Math.sqrt(((Ri - Rm) * (Ri - Rm) + (Gi - Gm) * (Gi - Gm) + (Bi - Bm) * (Bi - Bm)) / 3.0);
        }

        return new double[] {
                Math.max(Math.max(lambda_tab[0], lambda_tab[1]), Math.max(lambda_tab[2], lambda_tab[3])),
                Rm,
                Gm,
                Bm,
        };
    }



    /**
     * @assert node != null
     * @return the average color of 4 leaves of the same node.
     */
    private double[] mediumColor() {
        double Rm = 0, Gm = 0, Bm = 0;

        for (Quadtree quadtree : node) {
            Rm += quadtree.getColorValue().getRed();
            Gm += quadtree.getColorValue().getGreen();
            Bm += quadtree.getColorValue().getBlue();
        }

        return new double[] {Rm/4.0, Gm/4.0, Bm/4.0};
    }



    /**
     * @return the number of leaves in a quadtree.
     */
    public int leafAccount() {
        int nbLeaf = 0;

        if (node == null) return 1;

        for (Quadtree quadtree : node) {
            nbLeaf += (quadtree.colorValue == null) ? quadtree.leafAccount() : 1;
        }


        return nbLeaf;
    }



    /**
     * Maximum authorized degradation in the form of an integer ∆ ∈ 0..255: the
     * leaves F1, ..., F4 of the same node N are deleted Λ ≤ ∆.
     *
     * @param delta :∆ ∈ 0..255, representing the maximum of the color accept in the quadtree.
     * @assert ∆ ∈ 0..255 and node != null
     * @throws QuadtreeException : if the quadtree has only one leaf.
     */
    public void compressDelta(int delta) throws QuadtreeException {
        if (this.node == null) throw new QuadtreeException("We cannot apply a PHI compression on a tree with only 1 leaf !!!");

        this.compressDelta_rec(delta);
        System.out.println(this.toString());
    }

    private void compressDelta_rec(int delta) {
        for (Quadtree quadtree : node) {
            if (quadtree.node != null) {
                quadtree.compressDelta_rec(delta);
            }
        }

        if (node[0].colorValue != null && node[1].colorValue != null && node[2].colorValue != null && node[3].colorValue != null) {
            double[] val = this.bigLambda(); // calculate the colorimetric difference.

            if (val[0] <= delta) {
                this.node = null;
                this.colorValue = new Color((int)val[1], (int)val[2], (int)val[3]);
            }
        }
    }



    /**
     * The degradation can be defined according to a desired maximum weight, which can be
     * translate by an integer Φ > 0 representing the maximum number of leaves allowed in the tree.
     * The leaves are then pruned in ascending order of Λ.
     *
     * @assert Φ > 0 and node != null
     * @param phi : Φ > 0, representing the maximum number of leaves allowed in the tree.
     * @throws QuadtreeException : if the quadtree has only one leaf.
     */
    public void compressPhi(int phi) throws QuadtreeException {
        if (this.node == null) throw new QuadtreeException("We cannot apply a PHI compression on a tree with only 1 leaf !!!");

        this.compressPhi_rec(phi);
        System.out.println(this.toString());
    }

    private void compressPhi_rec(int phi) {
        int nbLeafs = this.leafAccount();
        TreeSet<Quadtree> node_treeSet = new  TreeSet<>();
        this.constTreeSet_rec(node_treeSet); // Create a tree comprising all the nodes with 4 leaves.

        while (phi < nbLeafs && !node_treeSet.isEmpty()) {
            nbLeafs -= 3; // -4 leaves + 1 node = -3

            Quadtree elemSup   = node_treeSet.first();
            double [] rgbColor = elemSup.mediumColor(); //get the average colors of the 4 leafs.

            elemSup.setColorValue(new Color((int)rgbColor[0], (int)rgbColor[1], (int)rgbColor[2]));
            elemSup.node = null; // prune the 4 threads
            node_treeSet.pollFirst(); // remove the smallest element, which have the smallest Λ.

            // if the father of the prune node also has 4 children which are leaves, then we add it in the TreeSet.
            if (elemSup.father.node[0].colorValue != null && elemSup.father.node[1].colorValue != null && elemSup.father.node[2].colorValue != null && elemSup.father.node[3].colorValue != null) {
                node_treeSet.add(elemSup.father);
            }
        }
    }

    private void constTreeSet_rec(TreeSet<Quadtree> node_treeSet) {
        for (Quadtree quadtree : node) {
            if (quadtree.node != null)
                quadtree.constTreeSet_rec(node_treeSet);
        }

        // if the father has 4 leaves:
        if (node[0].colorValue != null && node[1].colorValue != null && node[2].colorValue != null && node[3].colorValue != null) {
            node_treeSet.add(this); 
        }
    }



    /**
     * The purpose of the function is to reproduce a PNG image, from an R-quadtree.
     *
     * It makes a prefix path of the tree, to the leaf of this one. If this leaf
     * corresponds to a size of 1x1 pixels then the color of the leaf is added to
     * the image at coordinates (x, y). Otherwise, it is a previously compressed node,
     * so you have to fill an entire region of size childWidth, with the color of the leaf.
     *
     * @param dirPath : the path of the folder where the image will be stored.
     * @param fileName : the name of the image.
     * @param fileOp : the type of operation to perform on the image (delta for Delta
     *                 compression, phi for PHI compression and nothing for a lossless
     *                 image due to compression).
     * @param number : delta or phi or 0 for nothing.
     * @throws IOException : transmits a possible error coming from the method save to the class ImagePNG.
     */
    public void toPNG(String dirPath, String fileName, String fileOp, int number) throws IOException {
        ImagePNG newPng = this.png.clone();
        this.toPNG_rec(newPng, 0, 0, newPng.width());
        newPng.save(dirPath + fileName + fileOp + number + ".png");
        this.png = new ImagePNG(dirPath + fileName + fileOp + number + ".png");
    }

    private void toPNG_rec(ImagePNG newPNG, int x, int y, int childWith) {
        // if we hit a leaf in the quadtree...
        if (this.colorValue != null) {
            // if it's a compressed node...
            // because a leaf has a size of childWith = 1, because it's 1x1 px.
            if (childWith > 1) {
                int columns = x, row = y;
                int childWidthSin1 = childWith - 1;

                while ((row != y + childWidthSin1) || (columns != x + childWidthSin1)) {
                    newPNG.setPixel(columns, row, this.colorValue);

                    if (columns == x + childWidthSin1) {
                        columns = x;
                        row++;
                    } else {
                        columns++;
                    }
                }

                newPNG.setPixel(columns, row, this.colorValue);
            }
            else { // else it's a single leaf (1x1 px)...
                newPNG.setPixel(x, y, this.colorValue);
            }
        }
        else {
            if (this.node != null) {
                int[][] matrix = {{0, 0}, {1, 0}, {1, 1}, {0, 1}}; // in the order of the regions: North-East (1), North-west (2), South-West (3), South-East (4)
                int widthDiv2 = childWith / 2;

                // with x and y the old coordinate of the highest point to the left of the region being looked at.
                // NE (i = 0) -> x, y
                // NW (i = 1) -> x + widthDiv2, y
                // SW (i = 2) -> x + widthDiv2, y + widthDiv2
                // SE (i = 3) -> x, y + widthDiv2

                for (int i = 0; i < node.length; i++) {
                    this.node[i].toPNG_rec(newPNG, x + widthDiv2 * matrix[i][0], y + widthDiv2 * matrix[i][1], widthDiv2);
                }
            }
        }
    }



    /**
     * The purpose of the function is to produce a TXT file, containing the quadtree in textual form. The colors are in hexadecimal.
     * example: ((ffffff ffffff ffffff ffffff) (000000 ffffff ffffff ffffff) (000000 ffffff ffffff 000000)
     *
     * @param dirPath : the path of the folder where the image will be stored.
     * @param fileName : the name of the image.
     * @param fileOp : the type of operation to perform on the image (delta for Delta
     *                 compression, phi for PHI compression and nothing for a lossless
     *                 image due to compression).
     * @param number : delta or phi or 0 for nothing.
     * @throws IOException : transmits a possible error coming from the method save to the class ImagePNG.
     */
    public void toTxt(String dirPath, String fileName, String fileOp, int number) throws IOException {
        PrintWriter writer = new PrintWriter(dirPath + fileName + fileOp + number +".txt");
        writer.println(this.toString());
        writer.close();
    }



    /**
     * @node != null
     * @return Textual representation of the quadtree in parenthesized form,
     *         where each color is represented by its hexadecimal code.
     */
    public String toString () {
        if (node == null)
            return ImagePNG.colorToHex(this.colorValue);
        else
            return "(" + node[0].toString() + " " + node[1].toString() + " " + node[2].toString() + " " + node[3].toString() + ")";
    }



    /**
     * Overload the CompareTo method, so that it can handle duplicate quadtree.
     * For this, we compare the colorimetric difference of each node having 4 leaves.
     * And we sort them according to their natural orders. If they are equal, then we c
     * heck that the quadtree to add does not already exist in the TreeSet. Otherwise it
     * is ALWAYS added to the LEFT OF THE TREESET.
     *
     * @assert node contains 4 threads which are leaves
     * @param q : the new quadtree to watch.
     * @return an integer, 1: right, -1: left, 0: equal.
     */
    @Override
    public int compareTo(Quadtree q) {
        double DeltaThis = this.bigLambda()[0];
        double DelataO   = q.bigLambda()[0];
        return (DeltaThis > DelataO) ? 1 :  (this == q) ? 0 : -1;
    }
}