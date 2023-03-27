package source;

import exception.ListServiceMemberException;
import exception.ListSkillMemberException;

import java.io.Serializable;
import java.util.ArrayList;

public class Member implements Serializable {
	private static int NBINSTANCE = 0;
	private String name;
	private int token;
	private int idMember;
	private SocialClass socialClass; // normal, demi, zero.
	private ArrayList<Service> serviceList;
	private ArrayList<String> skillList; // you can not unlearn a skill.
	private Network network;
	
	public Member(String name, int token, SocialClass socialClass) {
		NBINSTANCE++;
		this.name = name;
		this.token = token;
		this.serviceList = new ArrayList<>();
		this.skillList = new ArrayList<>();
		this.socialClass = socialClass;
		this.idMember = NBINSTANCE;
		this.network = null;
	}
	
	public String getName() { return this.name; }
	public void setName(String nom) { this.name = nom; }

	public SocialClass getSocialClass() { return this.socialClass; }

	public ArrayList<String> getSkillList() { return this.skillList; }
	public void setSkillList(ArrayList<String> skillList) { this.skillList = skillList; }

	public ArrayList<Service> getServiceList() { return this.serviceList; }
	public void setServiceList(ArrayList<Service> serviceList) { this.serviceList = serviceList; }

	public int getToken() { return this.token; }

	public Network getNetwork() { return this.network; }
	public void setNetwork(Network network) { this.network = network; }

	public int getIdMember() { return this.idMember; }
	public void setIdMember(int id) { this.idMember = id; }
    
	public void addToken(int token) { this.token += token; }
	public void removeToken(int token) { this.token -= token; }

	public String displaySkill() {
		StringBuilder result = new StringBuilder();

		for (int i = 0; i < getSkillList().size(); i++) {
			result.append("\n- ").append(getSkillList().get(i)).append(" ");
		}

		return result.toString();
	}

	public String displayService() {
		StringBuilder result = new StringBuilder();

		for (int i = 0; i < getServiceList().size(); i++) {
			result.append("\n- ").append(getServiceList().get(i)).append(" ");
		}

		return result.toString();
	}
	
	/**
	 * @throws ListSkillMemberException : can only have the same skill once
	 * @role add source.Service in the tab of service
	 * @param skill : the skill to be add
	 */
	public void addSkill(String skill) throws ListSkillMemberException {
		if(!this.skillList.contains(skill)) {
			this.skillList.add(skill);
		} else {
			throw new ListSkillMemberException("error: you have returned a service that already exists");
		}
	}
	
	/**
	 * @throws ListServiceMemberException : you can only propose the same service once
	 * @role add source.Service in the tab of service
	 * @param service : the service to be add 
	 */
	public void addService(Service service) throws ListServiceMemberException {
		if(!this.serviceList.contains(service)) {
			this.serviceList.add(service);
		} else {
			throw new ListServiceMemberException("error: you have returned a service that already exists");
		}
	}
	
	/**
	 * @throws ListServiceMemberException : must exist to be able to remove it.
	 * @role remove service
	 * @param serviceList : the service to be remove.
	 */
	public void removeService(Service serviceList) throws ListServiceMemberException {
		if (this.serviceList.contains(serviceList)) { //Look if the service is present in the table if yes on the deletes.
			this.serviceList.remove(serviceList);
		}else {
			throw new ListServiceMemberException("error: the service you want to delete does not exist");
		}
	}
	
	/**
	 * @throws ListServiceMemberException : if the list is Empty and if the list does not have the task.
	 * @role search the service corresponding to a task in the services proposed by a member.
	 * @param task : the task in which one seeks one's service.
	 */
	public Service searchService(Task task) throws ListServiceMemberException {
		int cpt = 0;

		if (this.getServiceList().isEmpty()) { throw new ListServiceMemberException("error: the service list is empty"); }

		while (cpt < this.getServiceList().size() && !(this.getServiceList().get(cpt).contains(task))) {
			cpt++;
		}

		// allows to cover the case of error where one does not find service with this task.
		if (cpt == this.getServiceList().size()) {
			throw new ListServiceMemberException("error: the service does not exist in any of the services of the employer");
		}

		// if we pass all the cases of error, it means that the task has been found.
		return this.getServiceList().get(cpt);
	}
	
	

	public String toString() {
		return "Name : " + this.getName() + ", token : " + this.getToken() + ", *Skill : " + this.displaySkill() + "\n* service : " + this.displayService();
	}
}
