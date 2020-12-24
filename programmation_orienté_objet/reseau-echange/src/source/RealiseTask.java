package source;

import java.text.DateFormat;
import java.text.SimpleDateFormat;
import java.util.Date;

/**
 * the class corresponds to the task that was performed and paid for, so those stored in the network history.
 */
public class RealiseTask {
    private static final DateFormat dateFormat = new SimpleDateFormat("yyyy.MM.dd G 'at' HH:mm:ss z");
    private Task taskRealize;
    private final String date;

    public RealiseTask(Task taskRealize) {
        this.taskRealize = taskRealize;
        Date nowDate = new Date();
        this.date = dateFormat.format(nowDate);
    }

    public Task getTaskRealize() { return this.taskRealize; }
    public String getDate() { return this.date; }

    public String toString() {
        return this.getTaskRealize() + " --- " + this.getDate();
    }
}
