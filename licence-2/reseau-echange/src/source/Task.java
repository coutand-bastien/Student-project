package source;

import exception.PriceTaskInvalidTaskException;

import java.io.Serializable;

public class Task implements Serializable {
	private String nameTask;
	private int duration, numberOfPeopleWorking;
	private Member employer;
	private boolean isVolunteerTask;
	private boolean isAchievable;
	
	public Task(String nameTask, int duration, int numberOfPeopleWorking, Member beneficiaryMember, boolean volunteerTask) {
		this.nameTask = nameTask;
		this.duration = duration;
		this.numberOfPeopleWorking = numberOfPeopleWorking;
		this.employer = beneficiaryMember;
        this.isVolunteerTask = volunteerTask;
        this.isAchievable = false;
	}

	public Task(Task task) {
        this.nameTask = task.getName();
        this.duration = task.getDuration();
        this.numberOfPeopleWorking = task.getNumberOfPeopleWorking();
        this.employer = task.getEmployer();
        this.isVolunteerTask = task.isVolunteerTask();
        this.isAchievable = false;
    }

	/* getters and setters */
	public String getName() { return nameTask; }
	
	public int getDuration() { return duration; }
	public int getNumberOfPeopleWorking() { return numberOfPeopleWorking; }
	public Member getEmployer() { return employer; }
	
	public boolean getIsAchievable() { return this.isAchievable; }
	public void setIsAchievable(boolean isAchievable) { this.isAchievable = isAchievable; }

	public boolean isVolunteerTask() { return isVolunteerTask; }

	/**
	 * @role : redefinition of the equals method because that of the super-class
	 *         was not efficient enough for our class task.
	 * @param task : the task to compare.
	 * @return boolean if the task is the same.
	 */
	public boolean equals(Task task) {
		return ((this.getNumberOfPeopleWorking() == task.getNumberOfPeopleWorking()) &&
				(this.getName().equalsIgnoreCase(task.getName())) &&
				(this.getIsAchievable() == task.getIsAchievable()) &&
				(this.getEmployer().equals(task.getEmployer())) &&
				(this.getDuration() == task.getDuration()) &&
				(this.isVolunteerTask() == task.isVolunteerTask()));
	}

	/**
	 * @throws PriceTaskInvalidTaskException : if the task has not in the service list or if the task list is empty.
	 * @role allows the calculation of the price of the operation(task).
	 * @param service : the service concerned by the task.
	 * @param task : the task concerned by the service.
	 * @return returns a positive integer.
	 */
	public int operationPrice(Service service, Task task) throws PriceTaskInvalidTaskException {
		int cpt = 0;

		if (service.getTaskList().isEmpty()) { throw new PriceTaskInvalidTaskException("error: the task list is empty"); }

		while (cpt < service.getTaskList().size() && !(service.getTaskList().get(cpt).equals(task))) { cpt++; }

		if (service.getTaskList().get(cpt).equals(task)) {
			return task.isVolunteerTask() ? 0 : service.getHourlyCost() * task.getDuration() * task.getNumberOfPeopleWorking();
		} else {
			throw new PriceTaskInvalidTaskException("error: you try to pay for a task that does not fit to the service");
		}
	}

	/**
	 * @throws PriceTaskInvalidTaskException : the error transfer by the operationPrice method in task class.
	 * @role a task can be performed if there are enough people in the network with the desired
	 * 		 skill and if the beneficiary has the necessary amount of money.
	 * @param nbPeople : the number of people in the network with the skill of the task.
	 * @param member : the employer.
	 * @param service : the service where we look for people with the skills.
	 * @return an boolean.
	 */
	public boolean isRealized(int nbPeople, Member member, Service service) throws PriceTaskInvalidTaskException {
		return nbPeople >= this.getNumberOfPeopleWorking() && member.getToken() >= this.operationPrice(service, this);
	}

	public String toString() {
		return "The task " + this.getName() + " is done for " + this.getEmployer().getName() + " by " + this.getNumberOfPeopleWorking() + " number/s of people/s, it takes " + this.getDuration() + " hour, it is : " + this.getIsAchievable();
	}
}
