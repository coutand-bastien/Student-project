#include <cassert>

#include "../../Header/Part1/Locker.hpp"

using namespace std;

/**
 * @role : Build the class Locker with the locker number and
 *         the locker is empty. "0" to say that there is no
 *         weight in the locker.
 *
 * @param num : the locker number.
 *
 * @precondition : num >= 0, because the lockers start at 1 but can be set to
 *                 0 if there is a problem with baggage insertion.
 */
Locker::Locker(size_t num) : _luggage("", "", "", 0)  {
    assert(num >= 0);
    this -> _num = num;
}

Locker::~Locker() = default;


//getters :
size_t   Locker::getNum()     const { return this -> _num;     }
Luggage  Locker::getLuggage() const { return this -> _luggage; }


/**
 * @role : function which checks if the locker is empty.
 *
 * @return a boolean if the locker is empty.
 */
bool Locker::lockerIsEmpty() const {
    return (this -> getLuggage().getWeight() == 0);
}


/**
 * @role : add the luggage in the locker by modifying the luggage attribute.
 *
 * @param luggage : baggage to add.
 * @precondition : the locker must be empty.
 */
void Locker::addLuggage(Luggage const& luggage) {
    if (!lockerIsEmpty()) throw string("there is already luggage in the locker! (method addLuggage() in Locker.cpp)");
    this -> _luggage = luggage;
}


/**
 * @role : remove the luggage in the locker.
 *
 * @precondition : the locker must not be empty.
 */
void Locker::removeLuggage() noexcept(false) {
    if (lockerIsEmpty()) throw string("no luggage in locker! (method removeLuggage() in Locker.cpp)");
    this -> _luggage = {"", "", "", 0};
}


/**
 * @role : == operator allowing the equality test between two Objects
 *         of type Locker.
 *
 * @param locker : the ticket to compare.
 * @return an boolean if the two Locker are equals.
 */
bool Locker::operator== (Locker const& locker) const {
    return this -> getNum() == locker.getNum();
}