#include "./Test.hpp"

using namespace std;

Test::Test() :
    // part 1 :
    _luggage1("GARNIER"  , "Cyprien", "2 street Pierre, Nantes"       , 100),
    _luggage2("BINKS"    , "Jar-Jar", "3 way of the swamp, Jakku"     , 50 ),
    _luggage3("SKYWALKER", "Luke"   , "56 way of the desert, Dathomir", 30 ),
    _luggage4("REN"      , "Kylo   ", "74 way of the rivers, Kessel"  , 10 ),
    _luggage5("KENOBI"   , "Obi-Wan", "16 way of the forest, Naboo"   , 500),
    _locker1(1),
    _locker2(2),
    _consign(5),
    _ticket1(),

    // part 2 :
    _vLuggage1(new VLuggageRectangular("GARNIER"  , "Cyprien", "2 street Pierre, Nantes"       , 10, 3,  1)),
    _vLuggage2(new VLuggageCircle(     "BINKS"    , "Jar-Jar", "3 way of the swamp, Jakku",        2.5)),
    _vLuggage3(new VLuggageRectangular("SKYWALKER", "Luke"   , "56 way of the desert, Dathomir", 2,  10, 1)),
    _vLuggage4(new VLuggageRectangular("REN"      , "Kylo   ", "74 way of the rivers, Kessel"  , 5,  2,  1)),
    _vLuggage5(new VLuggageRectangular("KENOBI"   , "Obi-Wan", "16 way of the forest, Naboo"   , 5,  5,  1.028)),
    _vLocker1(1, 0),
    _vLocker2(2, 0),
    _vConsign(map<double, unsigned int>() = { {20, 2}, {50, 3} } ),
    _vTicket1()
    {}


Test::~Test() {
    delete _vLuggage1;
    delete _vLuggage2;
    delete _vLuggage3;
    delete _vLuggage4;
    delete _vLuggage5;
}


void Test::displayAllTabP1() const {
    // hashTable :
    cout << "display hashTable :" << endl;

    for(pair<Ticket, Locker> keyValue : this -> _consign.getHashMap()) {
        cout << "The ticket with the secret code : " << keyValue.first.getSecretCode()
             << "is in the locker : " << keyValue.second.getNum() << endl;
    }

    // freeLocker_queue
    cout << "\nthe size of freeLocker_queue is : " << this -> _consign.getFreeLocker_queue().size() << endl;
}


void Test::testLuggage() {
    cout << "\n//------------------- Test for the Luggage class -----------------------///"<< endl;

    cout << "\n//-------- Test for the method toString --------//"<< endl;
        cout << this -> _luggage1.toString() << endl;
}


void Test::testLocker() {
    cout << "\n//------------------- Test for the Locker class -----------------------//"<< endl;

    cout << "\n//-------- Test for the method lockerIsEmpty () --------//"<< endl;
        cout << "The locker1 is empty! : " << this -> _locker1.lockerIsEmpty() << endl;


    cout << "\n//-------- Test for the method addLuggage () --------//"<< endl;
        this -> _locker1.addLuggage(_luggage1);
        cout << "The locker1 is no longer empty after adding luggage. The locker1 is empty ? : " << this -> _locker1.lockerIsEmpty() << endl;

        // error test (there is already luggage in the locker) :
        // this -> _locker1.addLuggage(_luggage1);

    cout << "\n//-------- Test for the method removeLuggage () --------//"<< endl;
        this -> _locker1.removeLuggage();
        cout << "The locker1 is empty after removing the luggage. The locker1 is empty ? : " << this -> _locker1.lockerIsEmpty() << endl;

        // error test (no luggage in locker) :
        // this -> _locker1.removeLuggage();
}


void Test::testTicket() const {
    cout << "\n//------------------- Test for the Ticket class -----------------------//"<< endl;

    cout << "\n//-------- Test for the method getSecretCode() -------//" << endl;
        cout << "The secret code is : " << this -> _ticket1.getSecretCode() << endl;


    cout << "\n//-------- Test for the method hashCalculation() -------//" << endl;
        cout << "The hash of the secret code is : " << this -> _ticket1.hashCalculation() << endl;


    cout << "/\n/-------- Test for the operateur == and != -------//" << endl;
        Ticket ticket2 = this -> _ticket1;
        cout << "ticket1 equals ticket2 : " << (this -> _ticket1 == ticket2) << endl; // answer : 1 (true).
        cout << "ticket1 uneven ticket2 : " << (this -> _ticket1 != ticket2) << endl; // answer : 0 (false).
}


void Test::testConsign() {
    cout << "\n//------------------- Test for the Consign class -----------------------//"<< endl;

    cout << "\n//-------- Test for the method addLuggage() -------//" << endl;
        Ticket ticket1 = this -> _consign.addLuggage(this -> _luggage1);
        Ticket ticket2 = this -> _consign.addLuggage(this -> _luggage2);

        this -> displayAllTabP1();

        Ticket ticket3 = this -> _consign.addLuggage(this -> _luggage3); // the locker 3.
        Ticket ticket4 = this -> _consign.addLuggage(this -> _luggage4); // the locker 4.

        cout << "the least used empty locker is : " << this -> _consign.getFreeLocker_queue().front().getNum() << endl; // answer : 5.

        // warning test :
        // this -> _consign.addLuggage(this -> _luggage5);
        // cout << "the least used empty locker is : " << this -> _consign.getFreeLocker_queue().front().getNum() << endl; // answer : 0.


    cout << "\n//-------- Test for the method consignIsFull() -------//" << endl;
        cout << "consign is full ? : " << this -> _consign.consignIsFull() << endl; // answer : 0 (false).

        // the locker has a size of 5 empty compartments at the start.
        Ticket ticket5 = this -> _consign.addLuggage(this -> _luggage5);

        // error test (no free locker) :
        // this -> _consign.addLuggage(this -> _luggage5);

        cout << "consign is full ? : " << this -> _consign.consignIsFull() << endl; // answer : 1 (true).


    cout << "\n//-------- Test for the method removeLuggage() -------//" << endl;
        this -> _consign.removeLuggage(ticket1); // the locker 1 has remove.
        this -> _consign.removeLuggage(ticket4); // the locker 4 has remove.

        this -> displayAllTabP1();

        // error test1 (his ticket does not exist) :
        // this -> _consign.removeLuggage(this -> _ticket1);

        /*
            // error test2 (no full locker) :
            this -> _consign.removeLuggage(ticket2);
            this -> _consign.removeLuggage(ticket3);
            this -> _consign.removeLuggage(ticket5);
            this -> _consign.removeLuggage(ticket5);
         */


    cout << "\n//-------- Test for the method toString() -------//" << endl;
        cout << this -> _consign.toString() << endl;
}



                                ////////////////////////////////////////
                                //              PART 2                //
                                ////////////////////////////////////////



void Test::displayAllTabP2() const {
    // hashTable :
    cout << "display hashTable :" << endl;

    for (pair<Ticket, VLocker> keyValue : this->_vConsign.getHashMap()) {
        cout << "The ticket with the secret code : " << keyValue.first.getSecretCode()
             << "is in the locker : " << keyValue.second.getNum() << endl;
    }

    cout << endl;

    // freeLocker_map
    for (pair<double, queue<VLocker>> keyValue : this->_vConsign.getFreeLocker_map()) {
        cout << "In the consign, there are " << keyValue.second.size() << " locker with "
             << keyValue.first << " volume." << endl;
    }
}


void Test::testVLocker() {
    cout << "\n//------------------- Test for the VLocker class -----------------------//"<< endl;

    cout << "\n//-------- Test for the method VLocker() -------//" << endl;
        cout << "it's ok" << endl;

        // error test (volume >= 0) :
        // VLocker vLockerError = VLocker(0, -50);


    cout << "\n//-------- Test for the method lockerIsEmpty () --------//"<< endl;
        cout << "The vlocker1 is empty! : " << this -> _vLocker1.lockerIsEmpty() << endl; // Answer : 1 (true).


    cout << "\n//-------- Test for the method addLuggage () --------//"<< endl;
        this -> _vLocker1.addLuggage(_vLuggage1);
        cout << "The vlocker1 is no longer empty after adding luggage. The vlocker1 is empty ? : " << this -> _vLocker1.lockerIsEmpty() << endl; // Answer : 0 (false).

        // error test (there is already luggage in the locker) :
        // this -> _vLocker1.addLuggage(_vLuggage1);


    cout << "\n//-------- Test for the method removeLuggage () --------//"<< endl;
        this -> _vLocker1.removeLuggage();
        cout << "The vlocker1 is empty after removing the luggage. The vlocker1 is empty ? : " << this -> _vLocker1.lockerIsEmpty() << endl; // Answer : 1 (true).

        // error test (no luggage in locker) :
        // this -> _vLocker1.removeLuggage();
}


void Test::testVLuggage() {
    cout << "\n//------------------- Test for the son class of VLuggage class -----------------------//"<< endl;

    cout << "\n//-------- Test for the method VLuggage() -------//" << endl;
        cout << "it's ok" << endl;

        // error test (width > 0 && height > 0 && length > 0) :
        // VLuggageRectangular vLuggageRectangularError("Paul", "Jacques", "75 rue  of apple", -5, 10, 2);

    cout << "\n//-------- Test for the method volumeCalculation() of vLuggageRectangular -------//" << endl;
        cout << "Volume of the _LuggageRect1 " << this -> _vLuggage1 -> getVolume() << endl;


    cout << "\n//-------- Test for the method volumeCalculation() of vLuggageCircle -------//" << endl;
        cout << "Volume of the _LuggageCirc2 " << this -> _vLuggage2 -> getVolume() << endl;


    cout << "\n//-------- Test for the method toString() -------//" << endl;
        cout << this -> _vLuggage1 -> toString() << endl;
        cout << this -> _vLuggage2 -> toString() << endl;
}


void Test::testVConsign() {
    cout << "\n//------------------- Test for the VConsign class -----------------------//"<< endl;

    cout << "\n//-------- Test for the method initFreeLocker_map() -------//" << endl;
        cout << "it's ok" << endl;

        // error test (the request contains no lockers) :
        // VConsign vConsignError = map<double, unsigned int>();

        // error test (the request contains lockers with negative volume) :
        //VConsign vConsignError = map<double, unsigned int>() = { {10, 2}, {-32, 3} };


    cout << "\n//-------- Test for the method addLuggage() -------//" << endl;
        Ticket ticket1 = this -> _vConsign.addLuggage(this -> _vLuggage1); // the locker 3
        Ticket ticket2 = this -> _vConsign.addLuggage(this -> _vLuggage2); // the locker 4

        this -> displayAllTabP2();

        Ticket ticket3 = this -> _vConsign.addLuggage(this -> _vLuggage3); // the locker 1.
        Ticket ticket4 = this -> _vConsign.addLuggage(this -> _vLuggage4); // the locker 2.

        cout << endl;

        for(pair<double, queue<VLocker>> keyValue : this -> _vConsign.getFreeLocker_map()) {
            cout << "the least used empty locker is " << keyValue.second.front().getNum() << " for the " << keyValue.first << " volume." << endl; // answer 5
        }


    cout << "\n//-------- Test for the method consignIsFull() -------//" << endl;
        cout << "consign is full ? : " << this -> _vConsign.consignIsFull() << endl; // answer : 0 (false).

        // the locker has a size of 5 empty compartments at the start.
        Ticket ticket5 = this -> _vConsign.addLuggage(this -> _vLuggage5);

        // error test (no free locker) :
        // this -> _vConsign.addLuggage(this -> _vLuggage5);

        cout << "consign is full ? : " << this -> _vConsign.consignIsFull() << endl; // answer : 1 (true).


    cout << "\n//-------- Test for the method removeLuggage() -------//" << endl;
        this -> _vConsign.removeLuggage(ticket1); // the locker 3 has remove.
        this -> _vConsign.removeLuggage(ticket4); // the locker 2 has remove.

        this -> displayAllTabP2();

        // error test1 (his ticket does not exist) :
        // this -> _vConsign.removeLuggage(this -> _vTicket1);

        /*
            // error test2 (no full locker) :
            this -> _vConsign.removeLuggage(ticket2);
            this -> _vConsign.removeLuggage(ticket3);
            this -> _vConsign.removeLuggage(ticket5);
            this -> _vConsign.removeLuggage(ticket5);
         */


    cout << "\n//-------- Test for the method toString() -------//" << endl;
        cout << this -> _vConsign.toString() << endl;
}