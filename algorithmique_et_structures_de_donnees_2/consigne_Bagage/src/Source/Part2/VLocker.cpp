#include <cassert>

#include "../../Header/Part2/VLocker.hpp"

using namespace std;

/**
 * @role : Build the class VLocker with the locker number and
 *         the locker is empty. "0" to say that there is no
 *         volume in the locker.
 *
 * @param num    : the locker number.
 * @param volume : the space of the locker.
 *
 * @precondition : num >= 0 (type size_t), because the lockers start at 1 but can be set to
 *                 0 if there is a problem with baggage insertion and volume >= 0,
 *                 because they start with a volume greater than 0 but can be set to 0
 *                 if there is no luggage in the locker.
 */
VLocker::VLocker(size_t num, double volume) : _luggage(nullptr) {
    assert(volume >= 0);
    this -> _num     = num;
    this -> _volume  = volume;
}

VLocker::~VLocker() = default;

//getters :
size_t VLocker::getNum()    const { return this -> _num;    }
double VLocker::getVolume() const { return this -> _volume; }

/**
 * @role : function which checks if the locker is empty.
 *
 * @return a boolean if the locker is empty.
 */
bool VLocker::lockerIsEmpty() const {
    return this -> _luggage == nullptr ||
           this -> _luggage -> getVolume() == 0 ;
}

/**
 * @role : add the luggage in the locker by modifying the luggage attribute.
 *
 * @param luggage : baggage to add.
 * @precondition : the locker must be empty.
 */
void VLocker::addLuggage(VLuggage * luggage) {
    if (!lockerIsEmpty()) throw string("there is already luggage in the locker! (method addLuggage() in VLocker.cpp)");
    this -> _luggage = luggage;
}

/**
 * @role : remove the luggage in the locker.
 *
 * @precondition : the locker must not be empty.
 */
void VLocker::removeLuggage() noexcept(false) {
    if (lockerIsEmpty()) throw string("no luggage in locker! (method removeLuggage() in VLocker.cpp)");
    this -> _luggage = nullptr;
}

/**
 * @role : == operator allowing the equality test between two Objects
 *         of type VLocker.
 *
 * @param locker : the ticket to compare.
 * @return a boolean if the two VLocker are equals.
 */
bool VLocker::operator== (const VLocker & locker) const {
    return this -> _num == locker.getNum();
}


