#include <cassert>

#include "../../Header/Part1/Luggage.hpp"

using namespace std;
/**
 * @role : build the attributes of the class with the surname and 
 *         the name of the owner of the luggage as well as his address and
 *         the weight of the luggage.
 * 
 * @param name    : the name of the owner.
 * @param surname : the surname of the owner.
 * @param address : the address of the owner.
 * @param weight  : the weight of the luggage.
 *
 * @precondition : weight >= 0, because they start with a weight greater than
 *                 0 but can be set to 0 if there is no luggage in the locker.
 *
 */
Luggage::Luggage(const string & name, const string & surname, const string & address, float weight) {
    assert(weight >= 0);
    this -> _name     = name;
    this -> _surname  = surname;
    this -> _address  = address;
    this -> _weight   = weight;
}


Luggage::~Luggage() = default;

// getters :
float  Luggage::getWeight()  const { return this -> _weight;  }
string Luggage::getName()    const { return this -> _name;    }
string Luggage::getSurname() const { return this -> _surname; }
string Luggage::getAddress() const { return this -> _address; }

/**
 * @role : function displaying all information of this luggage.
 */
string Luggage::toString() const {
    return "Baggage belongs to " + this -> getName() + " " + this -> getSurname() + " " + this -> getAddress() +
           ", a baggage at a weight of " + to_string(this -> getWeight()) + "Kg";
}