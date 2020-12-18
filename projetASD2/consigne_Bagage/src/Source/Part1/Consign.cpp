#include <cassert>
#include <random>

#include "../../Header/Part1/Consign.hpp"

using namespace std;

/**
 * @role : build the attributes of the class with nbLocker locker for the
 *         empty locker queue. The full locker list is not initialized because at the start
 *         it is empty.
 *
 * @param nbLocker : the number of locker to initialize.
 *
 * @precondition : nbLocker > 0, because you cannot have a number of lockers in a consign
 *                 less than or equal to 0.
 **/
Consign::Consign(int nbLocker) {
    assert(nbLocker > 0);
    this -> _freeLocker_queue = initFreeLocker_queue(nbLocker); // we initialize this queue because at the start no locker is taken.
}

Consign::~Consign() = default;

// getters :
std::unordered_map<Ticket, Locker> Consign::getHashMap()          const { return this -> _hashTable; }        // use for the test.
queue<Locker>                      Consign::getFreeLocker_queue() const { return this -> _freeLocker_queue; } // use for the test.


/**
 * @role : initializes the queue with lockers numbered from 1 to nbLocker
 *         by calling the constructor of Locker. The locker indices start at 1
 *         to be able to leave the number 0, for cases where there is a problem with
 *         the insertion of a baggage.
 *
 * @param nbLocker : the number of lockers to create.
 * @return a queue with nbLocker locker.
 */
queue<Locker> Consign::initFreeLocker_queue(int nbLocker) {
    std::queue<Locker> freeLocker_queue;

    for (size_t i = 1; i <= nbLocker; i++) {
       freeLocker_queue.push(Locker(i));
    }

    return freeLocker_queue;
}


/**
 * @role : function which checks if the empty locker queue is empty.
 *         If, it's empty, then all the lockers are filled.
 *
 * @return a boolean if the consign is full.
 */
bool Consign::consignIsFull() const {
    return this -> _freeLocker_queue.empty();
}


/**
 * @role : function which deposits a luggage in a free locker with the oldest use.
 *         A unit ticket will refer to the locker in question thanks to an associative table.
 *
 * @param luggage : baggage to drop off.
 * @exception : if the free locker queue is empty.
 * @return a ticket referring to the locker where the luggage is located.
 */
Ticket Consign::addLuggage(const Luggage & luggage) noexcept(false) {

    // error handling:
        if (this -> consignIsFull()) throw string("no free locker! (method addLuggage() in Consign.cpp)");

    // Add baggage in the Consign:
        Locker locker = this -> _freeLocker_queue.front();
        locker.addLuggage(luggage);

        this -> _freeLocker_queue.pop(); // deletion of the 1st empty locker in the queue.

    // Add in the hash table:
        Ticket ticket;
        this -> _hashTable.insert(pair<Ticket, Locker>({ticket, locker}));

    return ticket;
}


/**
 * @role : procedure for removing luggage from a used locker.
 *
 * @param ticket : a ticket referring to the locker where the luggage is located.
 * @exception : if the full locker unordered_map is empty or if the ticket does not exist.
 */
void Consign::removeLuggage(const Ticket & ticket) noexcept(false) {
    // error handling:
        if (this -> _hashTable.empty()) throw string("no full locker ! (method removeLuggage() in Consign.cpp)");

        auto it = this -> _hashTable.find(ticket);
        if (it == this -> _hashTable.end()) throw string("this ticket does not exist ! (method removeLuggage() in Consign.cpp)");

    // delete the luggage in the use locker.
        if (!it -> second.lockerIsEmpty()) it -> second.removeLuggage();

    // delete hash table
        this -> _hashTable.erase(ticket);

    // add the locker in the empty lockers:
        this -> _freeLocker_queue.push(it -> second);
}


/**
 * @role : function displaying the number of lockers used in the deposit.
 *
 * @return a string.
 */
string Consign::toString() const {
    string str;
    for (auto & it : this -> _hashTable) {
        str += "The locker N°" + to_string(it.second.getNum()) + " is busy\n";
    }

    return str;
}