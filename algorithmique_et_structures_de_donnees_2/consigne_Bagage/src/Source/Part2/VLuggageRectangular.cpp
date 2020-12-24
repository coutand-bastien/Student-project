#include <cassert>
#include "../../Header/Part2/VLuggageRectangular.hpp"

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
 * @param width   : the width of the luggage.
 * @param height  : the height of the luggage.
 * @param length  : the length of the luggage.
 *
 * @precondition : width > 0 && height > 0 && length > 0, because a baggage cannot have a length
 *                 or a height or a width <= 0
 */
VLuggageRectangular::VLuggageRectangular(const string & name, const string & surname, const string & address, float width, float height, float length) :
                     VLuggage(name, surname, address)
{
    assert(width > 0 && height > 0 && length > 0);
    this -> _height = height;
    this -> _length = length;
    this -> _width  = width;
    this -> volumeCalculation();
}

VLuggageRectangular::~VLuggageRectangular() = default;


/**
 * @role : function which calculate the volume of the luggage.
 */
void VLuggageRectangular::volumeCalculation() {
    this -> _volume = this -> _width * this -> _height * this -> _length;
}

