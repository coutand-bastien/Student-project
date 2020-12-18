package source;

import exception.ListTaskServiceException;

import java.util.ArrayList;

public class Service {
	private String name;
	private int hourlyCost;
	private ArrayList<Task> taskList;
	
	public Service(String name, int hourlyCost) {
		this.name = name;
		this.hourlyCost = hourlyCost;
		this.taskList = new ArrayList<>();
	}

	public ArrayList<Task> getTaskList() { return this.taskList; }
	public int getHourlyCost() { return this.hourlyCost; }

	public String getName() { return this.name; }

	/**
     * @throws ListTaskServiceException : you can not add a task that already exists (the same task with the same employer).
	 * @role allows adding a task for a member with his instructions and sort the list if the list has at least 2 elements.
	 * @param nameTask : the name of the task to add.
	 * @param duration : the duration of the task at hand.
	 * @param numberOfPeopleWorking : the number of people required for this task.
	 * @param employer : the member who want to creat the task.
	 */
	public void taskAddiction(String nameTask, int duration, int numberOfPeopleWorking, Member employer, boolean volunteerTask) throws ListTaskServiceException {
		Task task = new Task(nameTask, duration, numberOfPeopleWorking, employer, volunteerTask);

		if(this.getTaskList().contains(task)) { throw new ListTaskServiceException("error: you try to add a task that already exists"); }

		this.getTaskList().add(task);
		if (this.getTaskList().size() > 1) { this.sortTaskList(); }
	}

	/**
	 * @throws ListTaskServiceException : you can not add a task that already exists (the same task with the same employer).
	 * @role Allows adding a task for a member with his instructions and sort the list if the list has at least 2 elements.
	 *       It use by the FileReader class when returning from task by an attachment file (example .txt, .csv)
	 * @param task : the task who want to add.
	 */
	public void taskAddiction(Task task) throws ListTaskServiceException {
		if(this.getTaskList().contains(task)) { throw new ListTaskServiceException("error: you try to add a task that already exists"); }

		this.getTaskList().add(task);
		if (this.getTaskList().size() > 1) { this.sortTaskList(); }
	}
	
	/**
	 * @throws ListTaskServiceException : You can not delete a non existent task or you can not delete a member if the list is empty.
	 * @role allows the deletion of a task belonging to a member.
	 * @param nameTask : the name of the task to delete.
	 * @param employer : the member who want to creat the task.
	 */
	public void taskDelete(String nameTask, Member employer) throws ListTaskServiceException {
		int cpt = 0;

		if (this.getTaskList().isEmpty()) { throw new ListTaskServiceException("error: the task list is empty"); }

		while (cpt < this.getTaskList().size() && !(this.getTaskList().get(cpt).getName().equals(nameTask) && this.getTaskList().get(cpt).getEmployer().equals(employer))) {
			cpt++;
		}

        // allows to cover the case of error where one does not find service with this task.
        if (cpt == this.getTaskList().size()) { throw new ListTaskServiceException("error: the task does not exist or was poorly written"); }

        // if we pass all the cases of error, it means that the task has been found.
        this.getTaskList().remove(cpt);

	}

	/**
	 * @throws ListTaskServiceException : if the task list is empty or if the task does not exist in the list.
	 * @role the function is to delete a task if it is present in the list.
	 * @param task : the task to be deleted.
	 */
	public void taskDelete(Task task) throws ListTaskServiceException {
		if (this.getTaskList().isEmpty()) { throw new ListTaskServiceException("error: the task list is empty"); }

		int index = this.getTaskList().indexOf(task);

		if (index == -1) { throw new ListTaskServiceException("error: you are trying to delete a task that does not exist"); }

		this.getTaskList().remove(index);
	}

	/**
	 * @throws ListTaskServiceException : if the list does not contain the task or if it's empty.
	 * @role returns the Object task if it is found in the list of a service.
	 * @param nameTask : the name of the task who search.
	 * @param employer : the name of the employer who search.
	 * @return Task.
	 */
	public Task searchTask(String nameTask, Member employer) throws ListTaskServiceException {
		int cpt = 0;

		if(this.getTaskList().isEmpty()) { throw new ListTaskServiceException("error: the task list is empty"); }

		while (cpt < this.getTaskList().size() && !(this.getTaskList().get(cpt).getName().equals(nameTask) && this.getTaskList().get(cpt).getEmployer().equals(employer))) {
			cpt++;
		}

		// allows to cover the case of error where one does not find service with this task.
		if (cpt == this.getTaskList().size()) {
			throw new ListTaskServiceException("error: the task does not exist or was poorly written");
		}

		// if we pass all the cases of error, it means that the task has been found.
		return this.getTaskList().get(cpt);
	}

	/**
	 * @role allows you to sort a task list with the bubble sort method.
	 * @link https://fr.wikipedia.org/wiki/Tri_%C3%A0_bulles.
	 */
	private void sortTaskList() {
		Task task;
		
		for (int i = 0; i < this.getTaskList().size(); i++) {
			for(int j = 1; j < (this.getTaskList().size() - i); j++) {
				String s1 = this.getTaskList().get(j-1).getName();
				String s2 = this.getTaskList().get(j).getName();
				
				/* This function (compareToIgnoreCase()) returns 0 if both strings are equal, a negative value if str1 is smaller than str2,
				or a positive value if str2 is smaller than str1. */
				if (s1.compareToIgnoreCase(s2) > 0){
					task = this.getTaskList().get(j-1);
					this.getTaskList().set(j-1, this.getTaskList().get(j));
					this.getTaskList().set(j, task);
				}
			}
		}
	}

	/**
	 * @role : redefinition of the contains method because that of the super-class
	 * 	       was not efficient enough for our class service.
	 * @param task : the task to find in a service.
	 * @return boolean.
	 */
	public boolean contains(Task task) {
		boolean find = false;
		int cpt = 0;

		while (cpt < this.getTaskList().size() && !find) {
			if(this.getTaskList().get(cpt).equals(task)) {
				find = true;
			}
			cpt++;
		}

		return find;
	}

	/**
	 * @throws ListTaskServiceException : if the service list is empty.
	 * @role function that displays all the task of a service.
	 */
	public void displayTask() throws ListTaskServiceException {
		if (this.getTaskList().isEmpty()) { throw new ListTaskServiceException("error: the list is empty"); }

		for(int i = 0; i < this.getTaskList().size(); i++) {
			System.out.println(this.getTaskList().get(i).toString());
		}
	}

	public String toString() {
		return "the service: " + this.getName() + " cost: " + this.getHourlyCost() + " tokens.";
	}
}

















