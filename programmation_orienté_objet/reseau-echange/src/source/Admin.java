package source;

import exception.*;

import java.util.ArrayList;
import java.util.Random;

@SuppressWarnings("ALL")
public class Admin extends Member {
	private Network netWork;
	private int mdp;
	
	public Admin(String name, int token) {
		super(name, token, new Normal());
		this.netWork = null;
		Random r = new Random();
		this.mdp = r.nextInt(99999999); // 0 <= mdp >= 99999999.
	}

	/**
	 * @role promote a member to the class of admin  
	 * @param member : the member who want to become a Admin.
	 */
	public Admin(Member member) {
		super(member.getName(), member.getToken(), new Normal());
		this.setSkillList(member.getSkillList());
		this.setServiceList(member.getServiceList());
		this.setIdMember(member.getIdMember());
		this.netWork = null;
		Random r = new Random();
		this.mdp = r.nextInt(99999999);
	}

	public int getMdp() { return this.mdp; }

	public Network getNetwork() { return this.netWork; }
	public void setNetwork(Network netWork) { this.netWork = netWork; }

	/**
	 * @throws AdminCommandNetworkException : if there is already a network for this admin.
	 * @role create new network and add the object in the list of the admin and the member list in the network.
	 * @param name : name of the network who wants to create.
	 */
	public void createNetwork(String name) throws AdminCommandNetworkException {
		if (this.netWork != null) { throw new AdminCommandNetworkException("error: there is already a Network !"); }

		this.netWork = new Network(name);
		this.getNetwork().getAdminList().add(this);
		this.getNetwork().getMemberList().add(this);
	}
	
	/**
	 * @throws AdminCommandNetworkException : you can't add a member if network does not exists. 
	 * @throws ListMemberNetworkException : you can't add a member if it already exists.
	 * @throws ListAdminNetworkException : if you are not admin in this network.
	 * @role add member in the network list member.
	 * @param member :
	 */
	public void addMember(Member member) throws AdminCommandNetworkException, ListMemberNetworkException, ListAdminNetworkException {
		if (this.netWork == null) { throw new AdminCommandNetworkException("error: there is no Network"); }
		this.netWork.addMember(member, this);
		member.setNetwork(this.getNetwork());
	}

	/**
	 * @throws AdminCommandNetworkException : if there is no network.
	 * @throws ListMemberNetworkException : if there is an error in the method removeMember.
	 * @throws ListServiceNetworkException : a propagated error of the remove member in network function.
	 * @throws ListAdminNetworkException : if you are not admin in this network.
	 * @role remove member in the network.
	 * @param member : member you want to remove.
	 */
	public void deleteMember(Member member) throws AdminCommandNetworkException, ListMemberNetworkException, ListServiceNetworkException, ListAdminNetworkException {
		if (this.netWork == null) { throw new AdminCommandNetworkException("error: there is no Network"); }
		this.netWork.removeMember(member, this);
	}

	/**
	 * @throws ListAdminNetworkException : You try to bring in a admin who already exists.
	 * @throws AdminCommandNetworkException : if there is no network.
	 * @throws ListMemberNetworkException : it belongs to the network addAdmin method.
	 * @throws ListServiceNetworkException : a propagated error of the function's addAdmin in network.
	 * @role add an administrator who is already an admin or if is a member to a network.
	 * @param member : the member that we want to add.
	 */
	public void addAdmin(Member member) throws AdminCommandNetworkException, ListAdminNetworkException, ListMemberNetworkException, ListServiceNetworkException {
		if (this.netWork == null) { throw new AdminCommandNetworkException("error: there is no Network"); }

		// if the parameter member isn't of the type Admin.
		if (!(member instanceof Admin)) {
			// creating a new admin with the second constructor and adding the admin network that adds it to the network of the new admin.
			Admin newAdmin = new Admin(member);
			newAdmin.setNetwork(this.getNetwork());
			this.netWork.addAdmin(member, newAdmin, this);
		}
		// if the parameter is a type of Admin.
		else {
			this.netWork.addAdmin(null, (Admin) member, this);
		}
	}

	/**
	 * @throws AdminCommandNetworkException : if there is no network.
	 * @throws ListAdminNetworkException : if there is an error in the method removeAdmin.
	 * @throws ListServiceNetworkException : a propagated error of the function's removeAdmin in network.
	 * @role remove admin in the network.
	 * @param admin : admin you want to remove.
	 */
	public void deleteAdmin(Admin admin) throws AdminCommandNetworkException, ListAdminNetworkException, ListServiceNetworkException {
		if (this.netWork == null) { throw new AdminCommandNetworkException("error: there is no Network"); }
		this.netWork.removeAdmin(admin, this);
	}

	/**
	 * @role allows you to sort a member list with the bubble sort method.
	 *       Sorts the members by their token count, the lowest at the top of the list.
	 * @link https://fr.wikipedia.org/wiki/Tri_%C3%A0_bulles.
	 */
	private void sortMemberList(ArrayList<Member> memberList) {
		Member member;

		for (int i = 0; i < memberList.size(); i++) {
			for(int j = 1; j < (memberList.size() - i); j++) {
				int s1 = memberList.get(j-1).getToken();
				int s2 = memberList.get(j).getToken();

				if (s1 < s2){
					member = memberList.get(j-1);
					memberList.set(j-1, memberList.get(j));
					memberList.set(j, member);
				}
			}
		}
	}
	
	/**
	 * @role valid if a task can be performed or not.
	 * @param task : task to validate
	 * @param employer : people who create this task.
	 */
	public void validateTask(Task task, Member employer) {
		try {
			
			ArrayList<Member> personWithSkillList = this.getNetwork().personWithThisSkill(task.getName());
			
			int nbPeopleSkill = personWithSkillList.size();
			
			Service service = employer.searchService(task);
			
			ArrayList<Member> workerList = new ArrayList<>();
			
			if(task.isRealized(nbPeopleSkill, task.getEmployer(), service)) {
				
				task.setIsAchievable(true);
				this.sortMemberList(personWithSkillList); // sort member list in function of there token.
				//garde les x premiers membre avec le bon skill x = nb de gens necessaire a l'accomplissement de la tache
				for(int i=0; i<task.getNumberOfPeopleWorking();i++) {
					workerList.add(personWithSkillList.get(i));
					System.out.println(workerList.get(i).getName());
				}
				
				// we force the payment of the user once the task is finished
				pay(employer.searchService(task), task.getName(), workerList,employer);
			}
			else {
				throw new TaskPayAdminException("error: the task is not achievable ");
			}

		}
		
		catch(PriceTaskInvalidTaskException | ListServiceMemberException | TaskPayAdminException | ListTaskServiceException e) {
			e.printStackTrace();
		}

	}
	/**
	 * @throws ListTaskServiceException : task does not exists for this employer.
	 * @throws PriceTaskInvalidTaskException : 
	 * @throws TaskPayAdminException : task is not achievable. Or the employer does not have enough tokens.
	 * @role the employer pays the members who realized one of his tasks.
	 * @param service : name of service corresponding to the task who have to pay.
	 * @param nameTask : name of the task that you have to pay.
	 * @param workerList : list of members who worked on the task.
	 * @param employer : people who pay the task.
	 */
	private void pay(Service service, String nameTask, ArrayList<Member> workerList,Member employer) throws PriceTaskInvalidTaskException, ListTaskServiceException {
		Task task = service.searchTask(nameTask, employer);
				
		//amount owed by the employer after the reduction imposed by his social class
		double amount = (int) (task.operationPrice(service, task) * employer.getSocialClass().reduction());
				
		//pay each member of the list
		for (int i = 0; i < workerList.size(); i++) {
			workerList.get(i).addToken((int) (amount / workerList.size()));
		}

		this.removeToken((int) (amount));
		this.getNetwork().addRealiseTaskInHistoric(service, task);

		
		
		
	}
}