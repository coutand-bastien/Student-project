package test;

import exception.*;
import source.*;

import java.io.IOException;
import java.util.ArrayList;

/**
 * we chose to create a class that focuses only on testing all the methods of the different classes.
 */
public class TestClass {
	private Member cyprien, bastien, louis, alexis;
	private Service gardening, babysitting, footing, preparing;
	private Task taskCutGrass;
	private Network food;
	private Admin pierre;

	public TestClass() {
		this.cyprien = new Member("Cyprien",0, new Demie());
	    this.bastien = new Member("Bastien",50, new Zero());
	    this.louis = new Member("Louis",1400, new Demie());
		this.alexis = new Member("Alexis",300, new Normal());
				
	    this.gardening = new Service("gardening",11);
	    this.footing = new Service("fooding",14);
	    this.preparing = new Service("preparing",22);
		this.babysitting = new Service("babysitting",13);

		this.taskCutGrass = new Task("cut grass", 6, 1, louis, true);

		this.food = new Network("food");

		this.pierre = new Admin("Pierre", 1500);
	}
	
	public final void testMemberClass() throws ListSkillMemberException, ListServiceMemberException, ListTaskServiceException, PriceTaskInvalidTaskException, ListMemberNetworkException, ListAdminNetworkException, AdminCommandNetworkException {
		System.out.println();
		System.out.println("//---------------------------TEST MEMBER CLASS------------------------//");


		//-------------test for the method getters------------//
		System.out.println("//-------------test for the method getters------------//");
		System.out.println(this.cyprien.getName());
		System.out.println(this.cyprien.getToken());
		System.out.println();


		//-------------test for the method addToken and getters------------//
		System.out.println("//-------------test for the method addToken and getters------------//");
		cyprien.addToken(12);

		System.out.println("Cyprien Token : "+this.cyprien.getToken());
		System.out.println("Bastien Token : "+this.bastien.getToken());
		System.out.println("Louis Token : "+this.louis.getToken());
		System.out.println();


		//-------------test for the method addService------------//
		System.out.println("//-------------test for the method addService------------//");
		cyprien.addService(this.gardening);
		// cyprien.addService(this.gardening); mettre en evidance erreur addService()
		System.out.println(this.cyprien.toString());
		System.out.println();


		//-------------test for the method addSkill and toString------------//
		System.out.println("//-------------test for the method addSkill and toString------------//");
		cyprien.addSkill("Gardener");
		cyprien.addSkill("God");
		cyprien.addSkill("pruning");
		bastien.addSkill("pruning");

		System.out.println(this.cyprien.toString());
		System.out.println();

		System.out.println("Cyprien Token : "+this.cyprien.getToken());
		System.out.println("Bastien Token : "+this.bastien.getToken());
		System.out.println("Louis Token : "+this.louis.getToken());
		System.out.println();


		//-------------test for the method searchService------------//
		System.out.println("//-------------test for the method searchService------------//");
		Task task = new Task("mow", 1, 1, this.cyprien, false);
		// error test : the task does not exist in the member list.
		// System.out.println(this.cyprien.searchService(task));

		this.gardening.taskAddiction("mow", 1, 1, this.cyprien, false);
		System.out.println(this.cyprien.searchService(task));

		this.gardening.taskDelete("mow", this.cyprien);
		// error test : the task does not exist in any service list.
		// System.out.println(this.cyprien.searchService(task));

		System.out.println(this.bastien.toString());
		System.out.println();
		System.out.println(this.cyprien.toString());
		System.out.println();
		System.out.println(this.louis.toString());
	}
	
	public final void testServiceClass() throws ListTaskServiceException {
		System.out.println();
		System.out.println("//---------------------------TEST SERVICE CLASS------------------------//");
		
		//-------------test for the method displayTask------------//
		// error test : test for an empty list.
		// this.gardening.displayTask();
		// System.out.println();


		//-------------test for the method taskAddiction------------//
		System.out.println("//-------------test for the method taskAddiction------------//");
		this.gardening.taskAddiction("mow", 1, 1, cyprien, false);
		this.gardening.taskAddiction("pruning", 3, 4, bastien, false);
		this.footing.taskAddiction(this.taskCutGrass);
		// error test : for adding an already existing task (ok).
		// this.gardening.taskAddiction("pruning", 3, 4, bastien);
		
		this.gardening.displayTask();
		System.out.println();


		//-------------test for the method taskDelete------------//
		System.out.println("//-------------test for the method taskDelete------------//");
		this.gardening.taskDelete("mow", cyprien);

		this.gardening.taskAddiction(this.taskCutGrass); // add task.
        this.gardening.taskDelete(this.taskCutGrass);
		// error test : of a task that does not exist in the list (ok).
		// this.gardening.taskDelete("mow", bastien);
		System.out.println();


		//-------------test for the method searchTask------------//
		System.out.println("//-------------test for the method searchTask------------//");
		System.out.println(gardening.searchTask("pruning", bastien));
		System.out.println();


		//-------------test for the method sortList------------//
		/*
		//---Commented out because already put in private because only use in adding task---//
		this.gardening.sortList();

		this.gardening.displayTask();
		System.out.println();
		*/
		
		this.gardening.displayTask();
		System.out.println();


		//-------------test for the method contains------------//
		System.out.println("//-------------test for the method contains------------//");
		System.out.println(this.gardening.contains(new Task("pruning", 3, 4, bastien, false)));
		System.out.println();


		//-------------test for the method toString------------//
		System.out.println("//-------------test for the method toString------------//");
		System.out.println(this.babysitting.toString());
        System.out.println(this.gardening.toString());
	}
	
	public final void testNetworkClass() throws ListMemberNetworkException, ListServiceNetworkException, ListServiceMemberException, PriceTaskInvalidTaskException, ListSkillMemberException, ListTaskServiceException, ListAdminNetworkException, ListHistoricNetworkException {
		System.out.println();
		System.out.println("//---------------------------TEST NETWORK CLASS------------------------//");

		//-------------test for the method addService------------//
		System.out.println("//-------------test for the method addService------------//");
		this.food.addService(this.footing);
		this.food.addService(this.preparing);
		// error test : insertion of an already existing service.
		// this.food.addService(this.fooding);
		System.out.println(this.food.displayServiceList());
		System.out.println();


		//-------------test for the method removeService------------//
		System.out.println("//-------------test for the method removeService------------//");
		this.food.removeService(this.footing);
		// error test : deleting a service that does not exist.
		// this.food.removeService(this.footing);
		System.out.println(this.food.displayServiceList());
		System.out.println();


		//-------------test for the method addMember------------//
		System.out.println("//-------------test for the method addMember------------//");
		this.food.addMember(this.alexis, this.pierre);
		this.food.addMember(this.cyprien,  this.pierre);
		// error test : insertion of an already existing member.
		// this.food.addMember(this.cyprien);
		System.out.println(this.food.displayMemberList());
		System.out.println();


		//-------------test for the method removeMember and the method removeAllService------------//
		System.out.println("//-------------test for the method removeMember and the method removeAllService------------//");
		this.food.removeMember(this.cyprien,  this.pierre);
		// error test : deleting a member that does not exist.
		// this.food.removeMember(this.cyprien);
		System.out.println(this.food.displayMemberList());
		System.out.println();
		System.out.println(this.food.displayServiceList());
		System.out.println();


		//-------------test for the method addAdmin------------//
		System.out.println("//-------------test for the method addAdmin------------//");
		Admin newBastienAdmin = new Admin(this.bastien);
		Admin newCyprienAdmin = new Admin(this.cyprien);

		this.food.addAdmin(this.bastien, newBastienAdmin,  this.pierre);
		this.food.addAdmin(this.cyprien, newCyprienAdmin,  this.pierre);
		// error test : insertion of an already existing admin.
		// this.food.addMember(this.cyprien);
		System.out.println(this.food.displayAdminList());
		System.out.println();


		//-------------test for the method removeAdmin------------//
		System.out.println("//-------------test for the method removeAdmin------------//");
		this.food.removeAdmin(newBastienAdmin,  this.pierre);
		// error test : deleting a admin that does not exist.
		// this.food.removeAdmin(this.bastien);
		System.out.println(this.food.displayAdminList());
		System.out.println();


		//-------------test for the method displayListService------------//
		System.out.println("//-------------test for the method displayListService------------//");
		System.out.println(this.food.displayServiceList());
		System.out.println();


		//-------------test for the method displayListMember------------//
		System.out.println("//-------------test for the method displayListMember------------//");
		System.out.println(this.food.displayMemberList());
		System.out.println();


		//-------------test for the method displayAdminList------------//
		System.out.println("//-------------test for the method displayAdminList------------//");
		System.out.println(this.food.displayAdminList());
		System.out.println();


		//-------------test for the method addRealiseTaskInHistoric and displayHistoric------------//
		System.out.println("//-------------test for the method addRealiseTaskInHistoric and displayHistoric------------//");
		// error test : the task list of the service preparing is Empty
		//this.food.addRealiseTaskInHistoric(this.preparing, this.taskCutGrass);
		this.preparing.taskAddiction(this.taskCutGrass);
		this.food.addRealiseTaskInHistoric(this.preparing, this.taskCutGrass);
		System.out.println(this.food.displayHistoricList());
		System.out.println();

		//-------------test for the method personWithThisSkill------------//
		System.out.println("//-------------test for the method personWithThisSkill------------//");
		this.bastien.addSkill("gardening");
		this.cyprien.addSkill("gardening");
		ArrayList<Member> l = this.food.personWithThisSkill("gardening");

		for (Member member : l) {
			System.out.println();
			System.out.println(member);
		}

		System.out.println();


		//-------------test for the method taskIsRealized------------//
		System.out.println("//-------------test for the method taskIsRealized------------//");
		Task taskExa = new Task("example", 3, 1, this.bastien, false);
		this.footing.taskAddiction("example", 3, 1, this.bastien, false);

		System.out.println(food.taskIsRealized(taskExa, "exa", this.bastien, this.footing)); // false
		this.bastien.addToken(500);
		this.bastien.addSkill("exa");
		System.out.println(food.taskIsRealized(taskExa, "exa", this.bastien, this.footing)); // true
		System.out.println();


		//-------------test for the method toString------------//
		System.out.println("//-------------test for the method toString------------//");
		System.out.println();
		System.out.println(this.food.toString());
	}

	public final void testFileReaderClass() throws IOException {
		FileReader f = new FileReader();

		//-------------test for the method writeTask------------//
		f.writeTask(this.bastien);

		//-------------test for the method readTask------------//
		f.readTask(this.gardening);
	}

	public final void testTaskClass() throws PriceTaskInvalidTaskException, ListTaskServiceException, IOException {
		System.out.println();
		System.out.println("//---------------------------TEST TASK CLASS------------------------//");

		//-------------test for the method operationPrice and method equals------------//
		System.out.println("//-------------test for the method operationPrice and method equals------------//");
		Task taskPruning = this.gardening.searchTask("pruning", this.bastien);
		System.out.println("the price of the task " + taskPruning.getName() + " costs: " + taskPruning.operationPrice(this.gardening, taskPruning) + " tokens.");
		System.out.println();


		//-------------test for the method isRealized------------//
		System.out.println("//-------------test for the method isRealized------------//");
		System.out.println(taskPruning.isRealized(4, this.bastien, this.gardening)); // true
		System.out.println();


		//-------------test for the method toString via displayTask------------//
		System.out.println("//-------------test for the method toString via displayTask------------//");
		this.gardening.displayTask();
		System.out.println();


		//-------------test second constructor------------//
		System.out.println("//-------------test second constructor------------//");
		this.testFileReaderClass();
		this.gardening.displayTask();
	}
	
	public final void testAdminClass() throws AdminCommandNetworkException, ListAdminNetworkException, ListServiceNetworkException, ListMemberNetworkException, ListTaskServiceException, ListServiceMemberException, ListSkillMemberException {
		System.out.println();
		System.out.println("//---------------------------TEST ADMIN CLASS------------------------//");

		//-------------test for the method createNetwork------------//
		System.out.println("//-------------test for the method createNetwork------------//");
		this.pierre.createNetwork("fast food");
		// error test : if the admin have already a network.
		// this.pierre.createNetwork("...");
		System.out.println();


		//-------------test for the method addAdmin------------//
		System.out.println("//-------------test for the method addAdmin------------//");
		// error test : there is any network who is assign to pierre.
        // this.pierre.addAdmin(this.bastien);
        this.pierre.addAdmin(bastien);

        // error : bastien is already add to a member in the method.
        // this.pierre.addMember(this.bastien);

		System.out.println(this.pierre.getNetwork().toString());
		System.out.println();

		this.pierre.getNetwork().getAdminList().get(1).addMember(this.cyprien); // bastien can add also a member so it's also an Admin.
		System.out.println(this.pierre.getNetwork().displayMemberList());
		System.out.println();


		//-------------test for the method deleteAdmin------------//
		System.out.println("//-------------test for the method deleteAdmin------------//");
		this.pierre.deleteAdmin(this.pierre.getNetwork().getAdminList().get(1));
		System.out.println(this.pierre.getNetwork().toString());
		System.out.println();


		//-------------test for the method validateTask------------//
		System.out.println("//-------------test for the method validateTask------------//");
		this.louis.addService(gardening);
		this.louis.getServiceList().get(0).taskAddiction(this.taskCutGrass);
		
		// error test : nobody has the skill cut grass 
		// this.pierre.validateTask(this.taskCutGrass, this.louis); 
		this.gardening.displayTask();

		System.out.println();

		this.pierre.addMember(alexis);
		this.alexis.addSkill("cut grass");
		this.pierre.validateTask(this.taskCutGrass, this.louis); // true
		// error test : the only task of the service has been validated, the task list is empty
		// this.gardening.displayTask();
	}
}