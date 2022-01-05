#include "../../Header/Part2/VLuggage.hpp"

using namespace std;

/**
 * @role : build the attributes of the abstract class with the surname and 
 *         the name of the owner of the luggage as well as his address and
 *         the volume of the luggage.
 * 
 * @param name    : the name of the owner.
 * @param surname : the surname of the owner.
 * @param address : the address of the owner.
 */
VLuggage::VLuggage(const string &name, const string &surname, const string &address) {
    this -> _name     = name;
    this -> _surname  = surname;
    this -> _address  = address;
}

VLuggage::~VLuggage() = default;

// getter :
double VLuggage::getVolume() const { return this -> _volume; }

/**
 * @role : function displaying all information of this luggage.
 */
string VLuggage::toString() const {
    return "Baggage belongs to " + this -> _name + " " + this -> _surname + " " + this -> _address +
           ", a baggage at a weight of " + to_string(this -> _volume) + "m³";
}