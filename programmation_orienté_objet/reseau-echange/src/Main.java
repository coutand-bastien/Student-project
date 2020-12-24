/*
  @nameProject : Network of exchange services.
 *
 * @project : We are interested in a network of services exchanges in which members perform tasks
 * in favor of other members and receive compensation in exchange. The currency of exchange at
 * within a network is the token.
 *
 * @partOfTheProject : project as part of courses at the University of Nantes.
 *
 * @lastUpdate : 20 december 2019 by Bastien COUTAND and Cyprien GARNIER.
 *
 * @Creator : COUTAND Bastien (bastien.coutand@etu.univ-nantes.fr),
 *            GARNIER Cyprien (cyprien.garnier@etu.univ-nantes.fr).
 */

import test.TestClass;

public class Main {

	public static void main(String[] args) {
		TestClass test = new TestClass();

		try {
			test.testAdminClass();
		    test.testServiceClass();
			test.testNetworkClass();
			test.testTaskClass();
			test.testMemberClass();
		} catch (Exception e) {
			e.printStackTrace();
		}


	}
}
