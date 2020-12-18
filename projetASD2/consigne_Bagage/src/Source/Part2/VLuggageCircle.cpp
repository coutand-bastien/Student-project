#include <math.h>
#include <cassert>

#include "../../Header/Part2/VLuggageCircle.hpp"

using namespace std;

/**
 * @role : build the attributes of the class and the super abstract class VLuggage with the surname and 
 *         the name of the owner of the luggage as well as his address and
 *         the volume of the luggage.
 * 
 * @param name    : the name of the owner.
 * @param surname : the surname of the owner.
 * @param address : the address of the owner.
 * @param volume  : the volume of the luggage.
 * @param radius  : the luggage radius.
 *
 * @precondition : ray > 0, because a baggage cannot have a radius <= 0.
 */
VLuggageCircle::VLuggageCircle(const string & name, const string & surname, const string & address, float radius) :
                VLuggage(name, surname, address)
{
    assert(radius > 0);
    this -> _radius = radius;
    this -> volumeCalculation();
}

VLuggageCircle::~VLuggageCircle() = default;


/**
 * @role : function which calculate the volume of the luggage.
 *
 * @return volume of the luggage.
 */
void VLuggageCircle::volumeCalculation() {
    this -> _volume = 4/3 * M_PI * pow(this -> _radius, 3);
}

