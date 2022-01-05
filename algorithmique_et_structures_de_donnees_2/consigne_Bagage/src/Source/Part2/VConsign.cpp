#include <random>

#include "../../Header/Part2/VConsign.hpp"

using namespace std;

/**
 * @role : The builder initializes the empty locker queues because when building a consign no locker is taken.
 *
 * @param volume_map : It represents a request from a client wanting to build a deposit. This allows an
 *                     addition of realism to the project. In the key, there are the volumes of the lockers and in values a file of size
 *                     corresponding to the number of lockers wanted for this volume (key).
 */
VConsign::VConsign(const map<double, unsigned int>& volume_map) {
    this -> _freeLocker_map = initFreeLocker_map(volume_map);
}

VConsign::~VConsign() = default;

map<double, queue<VLocker>>         VConsign::getFreeLocker_map() const { return this -> _freeLocker_map; } // use for the test.
std::unordered_map<Ticket, VLocker> VConsign::getHashMap()        const { return this -> _hashTable;      } // use for the test.


/**
 * @role : the function initializes a map made up of keys which are duplicates (volumes)
 *         and values which are queues (empty locker files), thanks to the map passed as a parameter
 *         which contains the volume and value, the number of lockers desired.
 *         Initializes the queue with lockers numbered from 1 to nbLocker
 *         by calling the constructor of VLocker. The locker indices start at 1
 *         to be able to leave the number 0, for cases where there is a problem with
 *         the insertion of a baggage.
 *
 * @param nbLocker_queue : the number of queues to create with empty lockers.
 * @param volume_map     : the list of the number of lockers (values) desired according
 *                         to their volume (keys).
 * @exception : if the request contains no lockers.
 * @exception : the request contains lockers with negative volume.
 *
 * @return a map composed of the key (volume) and values (empty locker queue).
 */
map<double, queue<VLocker>> VConsign::initFreeLocker_map(const map<double, unsigned int>& volume_map) noexcept(false) {
    // error handling:
        if (volume_map.empty()) throw string("the request contains no lockers ! (method initFreeLocker_map() in VConsign.cpp)");

    map<double, queue<VLocker>> freeLocker_map;
    double volume;
    int nbOfLocker = 0; // number of lockers total.

    for(auto itv_m : volume_map) {
        queue<VLocker> freeLocker_queue; // new queue at each loop.

        if (itv_m.first <= 0) throw string("the request contains lockers with negative volume ! (method initFreeLocker_map() in VConsign.cpp)");
        volume = itv_m.first;

        for (size_t i = 1; i <= itv_m.second; i++) {
            freeLocker_queue.push(VLocker(i + nbOfLocker, volume));
        }

        nbOfLocker += itv_m.second; // we add the number of loop turns done.
        freeLocker_map.insert(pair<double, queue<VLocker>>({volume, freeLocker_queue}));
    }

    return freeLocker_map;
}


/**
 * @role : function which checks if the empty locker queue is empty.
 *         If, it's empty, then all the lockers are filled.
 *
 * @return a boolean if consign is full.
 */
bool VConsign::consignIsFull() const {
    return this -> _freeLocker_map.empty();
}


/**
 * @role : function as which deposits a baggage in a free locker for the oldest use with a volume greater
 *         than or equal as close as possible to the volume of the baggage to be deposited.
 *         A unit ticket will refer to the locker in question, thanks to an associative table.
 *
 * @param baggage : the baggage to be dropped off.
 * @exception : if the free locker queue is empty.
 * @exception : if there is no locker capable of storing luggage due to its volume.
 *
 * @return a ticket referring to the locker where the luggage is located.
 */
Ticket VConsign::addLuggage(VLuggage * luggage) noexcept(false) {
    // error handling:
        if (this -> consignIsFull()) throw string("no free locker! (method addLuggage() in VConsign.cpp)");

    // Add baggage in the Consign
        auto value     = _freeLocker_map.find(luggage -> getVolume());
        queue<VLocker> freeLocker_queue;

        /*
         * if the baggage volume is not equal to a locker volume, we look for
         * the nearest locker volume which is strictly greater than that of the luggage.
         */
        if (value == _freeLocker_map.end()) {
            value = _freeLocker_map.begin();

            /*
             * stop: if we reach the end of the map, or if the volume of the locker (key) is greater
             *       than the volume of the luggage and the associated queue is not empty.
             */
            while(value != _freeLocker_map.end() && value -> first < luggage -> getVolume()) value++;

            if (value == _freeLocker_map.end()) throw string("no free locker able of supporting the volume of luggage! (method addLuggage() in VConsign.cpp)");
        }

        VLocker locker = value -> second.front();
        value -> second.pop(); // deletion of the 1st empty locker in the queue.

        // if the queue is empty then delete the line in the map.
        if (value -> second.empty()) this -> _freeLocker_map.erase(value);

        locker.addLuggage(luggage);

    // Add in the hash table:
        Ticket ticket;
        this -> _hashTable.insert(pair<Ticket, VLocker>({ticket, locker}));

    return ticket;
}


/**
 * @role : procedure for removing luggage from a used locker. it builds a new queue
 *         if the one does not exist in the empty locker list because if it exists in
 *         the full lockers then it was before in the empty lockers.
 *
 * @param ticket : a ticket referring to the locker where the luggage is located.
 * @exception : if the full locker unordered_map is empty or if the ticket does not exist.
 */
void VConsign::removeLuggage(const Ticket &ticket) noexcept(false) {
    // error handling:
        if (this -> _hashTable.empty()) throw string("no full locker ! (method removeLuggage() in VConsign.cpp)");

        auto itht = this -> _hashTable.find(ticket);
        if (itht == this -> _hashTable.end()) throw string("this ticket does not exist ! (method removeLuggage() in VConsign.cpp)");

    // delete the luggage in the use locker.
        if (!itht -> second.lockerIsEmpty()) itht -> second.removeLuggage();

    // delete in the hash table
        this -> _hashTable.erase(ticket);

    // add the locker in the empty lockers:
        auto itfl_m = this -> _freeLocker_map.find(itht -> second.getVolume());

        /*
         * if the locker volume (key) does not exist, we add it because if it is in
         * the full lockers then it was before in the empty lockers.
         */
        if (itfl_m != this -> _freeLocker_map.end()) {
            itfl_m->second.push(itht->second);
        }
        else {
            queue<VLocker> freeLocker_queue;
            freeLocker_queue.push(itht -> second); // added locker emptied of his luggage in the queue.
            this -> _freeLocker_map.insert(pair<double, queue<VLocker>>({itht -> second.getVolume(), freeLocker_queue}));
        }
}


/**
 * @role : function displaying the number of lockers used in the consign.
 *
 * @return a string.
 */
std::string VConsign::toString() const {
    string str;
    for (auto & it : this -> _hashTable) {
        str += "The locker N°" + to_string(it.second.getNum()) + " is busy\n";
    }

    return str;
}