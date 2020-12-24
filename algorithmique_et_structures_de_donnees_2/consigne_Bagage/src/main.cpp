/*
 * @nameProject : VLuggage storage.
 *
 * @project : We are interested in developing a luggage storage system. VLuggage storage is
 *            represented by a list of lockers. VLuggage can be left in a free locker and a
 *            return ticket can be obtained. With a ticket, you can collect the corresponding
 *            baggage. A user does not know where his luggage is.
 *
 * @partOfTheProject : project as part of courses at the University of Nantes.
 *
 * @lastUpdate : 7 may 2020 by Bastien COUTAND and Cyprien GARNIER.
 *
 * @Creator : COUTAND Bastien (bastien.coutand@etu.univ-nantes.fr),
 *            GARNIER Cyprien (cyprien.garnier@etu.univ-nantes.fr).
 */
#include "Test/Test.hpp"

using namespace std;

int main() {
    string choice, boole;

    // restart loop.
    do {
        Test test; // new Test for each loop (prevents mistakes).

        // loop check.
        do {
            cout << "To perform the tests of part 1 please type 1, of part 2 please type 2\n" << endl;
            cin >> choice;

            if (choice != "1" && choice != "2") cout << "\nERROR : please enter 1 or 2" << endl;
        } while (choice != "1" && choice != "2");

        try {
            if (choice == "1") {
                test.testLocker();
                test.testLuggage();
                test.testTicket();
                test.testConsign();
            } else {
                test.testVLocker();
                test.testVLuggage();
                test.testTicket();
                test.testVConsign();
            }
        }
        catch (const string &e) {
            cout << "ERROR : " << e << endl;
        }

        // loop check.
        do {
            cout << "do you want to start again? (y/n)" << endl;
            cin >> boole;

            if (boole != "y" && boole != "n" && boole != "Y" && boole != "N") cout << "\nERROR : please enter y or n" << endl;
        } while (boole != "y" && boole != "n" && boole != "Y" && boole != "N");

    } while(boole != "N" && boole != "n");

    return 0;
}
