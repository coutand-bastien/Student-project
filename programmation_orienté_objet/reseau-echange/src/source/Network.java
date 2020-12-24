package source;

import exception.*;

import java.util.ArrayList;

public class Network {
	private ArrayList<Service> serviceList;
	private ArrayList<Member> memberList;
	private ArrayList<Admin> adminList;
	private ArrayList<RealiseTask> historicTask;
	private String name;
	
	public Network(String name) {
		this.serviceList = new ArrayList<>();
		this.memberList = new ArrayList<>();
		this.adminList = new ArrayList<>();
		this.historicTask = new ArrayList<>();
		this.name = name;
	}

	public String getName() { return this.name; }

	public ArrayList<Service> getServiceList() { return this.serviceList; }
	public ArrayList<Member> getMemberList() { return this.memberList; }
	public ArrayList<Admin> getAdminList() { return this.adminList; }
	public ArrayList<RealiseTask> getHistoricTask() { return this.historicTask; }

	/**
	 * @role adding a service in the network.
	 * @param service : the service added.
	 */
	public void addService(Service service) {
		this.getServiceList().add(service);
	}

	/**
	 * @throws ListServiceNetworkException : if the service of list is empty or if the service is a non-existent service.
	 * @role allows you to delete a service.
	 * @param service : the service to be deleted.
	 */
	public void removeService(Service service) throws ListServiceNetworkException {
		if(this.getServiceList().isEmpty()) { throw new ListServiceNetworkException("error: you try to look at an empty service list"); }
		if(!this.getServiceList().contains(service)) { throw new ListServiceNetworkException("error: you are trying to delete a non-existent service"); }
		this.getServiceList().remove(service);
	}

	/**
	 * @throws ListMemberNetworkException : returns an error if a member is added while it already exists.
	 * @throws ListAdminNetworkException : the error transfer by the isAdmin method in Network class.
	 * @role add a member and their Network Service.
	 * @param member : the member to add.
	 * @param admin : the administrator who wants to add the member.
	 */
	public void addMember(Member member, Admin admin) throws ListMemberNetworkException, ListAdminNetworkException {
		if (this.isAdmin(admin)) {
			if (this.getMemberList().contains(member)) { throw new ListMemberNetworkException("error: you try to bring in a member who already exists"); }
			this.getMemberList().add(member);
			this.getServiceList().addAll(member.getServiceList()); // We add all the services of the member in the Service list.
		}
	}

	/**
	 * @throws ListMemberNetworkException : if the member does not exist in the list and the membership list is empty.
	 * @throws ListServiceNetworkException : the error transfer by the removeAllService method in Network class.
	 * @throws ListAdminNetworkException : the error transfer by the isAdmin method in Network class.
	 * @role removes the member as well as the service on the network.
	 * @param member : the member to delete.
	 * @param admin : the administrator who wants to remove the member.
	 */
	public void removeMember(Member member, Admin admin) throws ListMemberNetworkException, ListServiceNetworkException, ListAdminNetworkException {
		if (this.isAdmin(admin)) {
			if (this.getMemberList().isEmpty()) { throw new ListMemberNetworkException("error: you try to look at an empty member list"); }
			if (!this.getMemberList().contains(member)) { throw new ListMemberNetworkException("error: you are trying to delete a non-existent member"); }
			this.removeAllService(member); // we remove the tasks of the member.
			this.getMemberList().remove(member); // we remove the member of the network.
		}
	}

	/**
	 * @throws ListMemberNetworkException :  the error transfer by the removeMember method in Network class
	 * @throws ListServiceNetworkException :  the error transfer by the removeMember method in Network class.
	 * @throws ListAdminNetworkException : the error transfer by the removeMember and isAdmin method in Network class and if the admin is already existed.
	 * @role add a admin in the two list, because an admin is also an member, and their Network Service.
	 * @param newAdmin : the admin to add.
	 * @param member : the member before the change of class (null if there is already an Admin).
	 * @param admin : the administrator who wants to add the admin.
	 */
	public void addAdmin(Member member, Admin newAdmin, Admin admin) throws ListAdminNetworkException, ListMemberNetworkException, ListServiceNetworkException {
		if (this.isAdmin(admin)) {
			if (this.getAdminList().contains(newAdmin)) { throw new ListAdminNetworkException("error: you try to bring in a admin who already exists"); }

			// if the parameter newAdmin is already present in the member list.
			if (this.getMemberList().contains(newAdmin)) {
				this.removeMember(member, admin); // delete the old one in the Member type member list ...
			}

			// otherwise it is not present in any list so we add it everywhere.
			this.getAdminList().add(newAdmin);
			this.getMemberList().add(newAdmin); // ... and add the new one in the Admin type's member list.
			this.getServiceList().addAll(newAdmin.getServiceList()); // We add all the services of the admin in the Service list.
		}
	}

	/**
	 * @throws ListAdminNetworkException : the error transfer by the removeMember and isAdmin method in Network class.
	 * 									   Or if admin list is empty, if the admin is non-existent in the admin list or if
	 * 									   there is only one admin in the network.
	 * @role removes the admin in the adminlist.
	 * @param delAdmin : the admin to delete.
	 * @param admin : the administrator who wants to remove the admin.
	 */
	public void removeAdmin(Member delAdmin, Admin admin) throws ListAdminNetworkException {
		if (this.isAdmin(admin)) {
			if (this.getAdminList().isEmpty()) { throw new ListAdminNetworkException("error: you try to look at an empty admin list"); }
			if (!this.getAdminList().contains(delAdmin)) { throw new ListAdminNetworkException("error: you are trying to delete a non-existent admin"); }
			if (this.getAdminList().size() < 1) { throw new ListAdminNetworkException("If you delete the last admin, the network will no longer have an administrator"); }
			this.getAdminList().remove(delAdmin); // we remove the admin of the network.
		}
	}

	/**
	 * @throws ListServiceNetworkException : if the service list is empty.
	 * @role function that displays all the services of a network.
	 * @return String with all the service.
	 */
	public String displayServiceList() throws ListServiceNetworkException {
		if (this.getServiceList().isEmpty()) { throw new ListServiceNetworkException("error: you try to look at an empty service list"); }

		StringBuilder serviceList = new StringBuilder();
		for (int i = 0; i < this.getServiceList().size(); i++) {
			serviceList.append("\n - ").append(this.getServiceList().get(i).getName());
		}
        return serviceList.toString();
	}

	/**
	 * @throws ListMemberNetworkException : if the member list is empty.
	 * @role function that displays all the member of a network.
	 * @return String with all the members.
	 */
	public String displayMemberList() throws ListMemberNetworkException {
		if (this.getMemberList().isEmpty()) { throw new ListMemberNetworkException("error: you try to look at an empty member list"); }

		StringBuilder memberList = new StringBuilder();
		for (int i = 0; i < this.getMemberList().size(); i++) {
			memberList.append("\n - ").append(this.getMemberList().get(i).getName());
		}
		return memberList.toString();
	}

	/**
	 * @throws ListAdminNetworkException : if the admin list is empty.
	 * @role function that displays all the admin of a network.
	 * @return String with all the admin.
	 */
	public String displayAdminList() throws ListAdminNetworkException {
		if (this.getAdminList().isEmpty()) { throw new ListAdminNetworkException("error: you try to look at an empty admin list"); }

		StringBuilder adminList = new StringBuilder();
		for (int i = 0; i < this.getAdminList().size(); i++) {
			adminList.append("\n - ").append(this.getAdminList().get(i).getName());
		}
        return adminList.toString();
	}

	/**
	 * @throws ListHistoricNetworkException : if the historic list is empty.
	 * @role function that displays all the historic of a network.
	 * @return String with all the historic.
	 */
	public String displayHistoricList() throws ListHistoricNetworkException {
		if (this.getHistoricTask().isEmpty()) { throw new ListHistoricNetworkException("error: you try to look at an empty historic list"); }

		StringBuilder historicList = new StringBuilder();
		for (int i = 0; i < this.getHistoricTask().size(); i++) {
			historicList.append("\n - ").append(this.getHistoricTask().get(i).toString());
		}
		return historicList.toString();
	}

	/**
	 * @throws ListTaskServiceException : the error transfer by the taskDelete method in Service class.
	 * @role : Adding a task done in the task history. There is no removeRealiseTask
	 *         method because a historic all the changes even the unintended one.
	 * @param task : the realise task to add in the historic of the network.
	 * @param service : the service where the task is.
	 */
	public void addRealiseTaskInHistoric(Service service, Task task) throws ListTaskServiceException {
		RealiseTask realiseTask = new RealiseTask(task);
		this.getHistoricTask().add(realiseTask);
		service.taskDelete(task.getName(), task.getEmployer());
	}

	/**
	 * @throws ListServiceNetworkException : the error transfer by the removeService method in Service class.
	 * @role function to delete all the service of a member in the service list of the network, once this one remove from the network.
	 * @param employer : the deleted member of the network.
	 */
	public void removeAllService(Member employer) throws ListServiceNetworkException {
		for (Service serv : employer.getServiceList()) {
			if (this.getServiceList().contains(serv)) {
				this.removeService(serv);
			}
		}
	}

	/**
	 * @throws ListServiceMemberException : if the service list is empty.
	 * @role the function looks in the network member list if there are members with the required skill.
	 * @param skill : the search skill. The skill is the name of the task to be performed (facilitates the search),
	 *                example the task "cut grass" is a name of a task but also the name of skill.
	 * @return an ArrayList of member with this skill.
	 */
	public ArrayList<Member> personWithThisSkill(String skill) throws ListServiceMemberException {
		ArrayList<Member> memberList = new ArrayList<>();

		if (this.getMemberList().isEmpty()) { throw new ListServiceMemberException("error: the member list is empty"); }

		for (int i = 0; i < this.getMemberList().size(); i++) {
			for (int j = 0; j < this.getMemberList().get(i).getSkillList().size(); j++) {
				if (this.getMemberList().get(i).getSkillList().get(j).equalsIgnoreCase(skill)) {
					memberList.add(this.getMemberList().get(i));
				}
			}
		}
		return memberList;
	}

	/**
	 * @throws ListServiceMemberException : the error transfer by the personWithThisSkill method in Network class.
	 * @throws PriceTaskInvalidTaskException : the error transfer by the isRealized in Task class.
	 * @role function that checks whether a task is achievable.
	 * @param task : the task to check.
	 * @param skill : the skills sought.
	 * @param member : the employer of the task.
	 * @param service : the service of the task.
	 * @return boolean.
	 */
	public boolean taskIsRealized(Task task, String skill, Member member, Service service) throws ListServiceMemberException, PriceTaskInvalidTaskException {
		return task.isRealized(this.personWithThisSkill(skill).size(), member, service);
	}

	/**
	 * @throws ListAdminNetworkException : if the member is not in the admin List of the network.
	 * @role function that looks at whether a member is an admin or not.
	 * @param member : the member who want to check.
	 * @return boolean if the member is an admin.
	 */
	public boolean isAdmin(Member member) throws ListAdminNetworkException {
		if (!(member instanceof Admin)) { throw new ListAdminNetworkException("error : the admin is not in the adminList of the network"); }

		for (Admin admin : member.getNetwork().getAdminList()) {
			if (admin.getIdMember() == member.getIdMember() && admin.getMdp() == ((Admin)member).getMdp()) {
				return true;
			}
		}

		return false;
	}
	
	public String toString() {
		String str = "";

		try {
			// the conditions make it possible to avoid the cases of error for a list display without anything in it.
			if(!(this.getServiceList().isEmpty())) { str += "* The network " + this.getName() + " has the services: " + this.displayServiceList(); }
			if(!(this.getMemberList().isEmpty())) { str += "\n* ,the members : " + this.displayMemberList(); }
			if(!(this.getAdminList().isEmpty())) { str += "\n* and has the admin :" + this.displayAdminList(); }
		} catch (ListServiceNetworkException | ListMemberNetworkException | ListAdminNetworkException e) {
			e.printStackTrace();
		}

		return str;
	}
}