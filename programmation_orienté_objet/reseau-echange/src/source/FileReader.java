package source;

import exception.ListTaskServiceException;

import java.io.*;
import java.util.Objects;

public class FileReader {
    private File file;

    public FileReader() {
        this.file = new File("task.csv");
    }

    /**
     * @role test the existence of a file and create it if it does not exist.
     */
    private void existentFile() {
        if (!this.file.exists()) {
            try {
                this.file.createNewFile();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }

    /**
     * @role allows the writing of objects in the file specify.
     *       It is used to serialize objects in the class testClass
     * @param member : the beneficiary member.
     */
    public void writeTask(Member member) throws IOException {
        Task t1 = new Task("lire", 2, 34, member, true);
        Task t2 = new Task("ecrire", 4, 2, member, false);
        Task t3 = new Task("copier", 1, 1, member, true);

        FileOutputStream fis;
        ObjectOutputStream out = null;

        this.existentFile();

        try {
            fis = new FileOutputStream(this.file);
            out = new ObjectOutputStream(fis);

            out.writeObject(t1);
            out.writeObject(t2);
            out.writeObject(t3);

        } catch (IOException e) {
            e.printStackTrace();
        }
        finally {
            Objects.requireNonNull(out).close(); // removes the case of if in is null.
        }
    }

    /**
     * @role allows the reading of objects in the file specify.
     * @param service : the service who is affected to the task.
     */
    public void readTask(Service service) throws IOException {
        FileInputStream fis;
        ObjectInputStream in = null;

        this.existentFile();

        try {
            fis = new FileInputStream(this.file);
            in = new ObjectInputStream(fis);

            // available() : returns the number of bytes left to read in the file.
            while(fis.available() > 0) {
                service.taskAddiction((Task)in.readObject());
            }
            in.close(); // closing the flow
         }
        catch (IOException | ClassNotFoundException | ListTaskServiceException e) {
            e.printStackTrace();
        }
        finally {
            Objects.requireNonNull(in).close(); // removes the case of if in is null.
        }
    }
}
