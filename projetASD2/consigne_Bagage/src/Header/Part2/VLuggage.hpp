#ifndef PROJETALGOCONSIGNEBAGAGE_VLUGGAGE_HPP
#define PROJETALGOCONSIGNEBAGAGE_VLUGGAGE_HPP

#include <iostream>

class VLuggage {
    public:
        /**
         * @role : build the attributes of the abstract class with the surname and 
         *         the name of the owner of the luggage as well as his address and
         *         the volume of the luggage.
         * 
         * @param name    : the name of the owner.
         * @param surname : the surname of the owner.
         * @param address : the address of the owner.
         */
        VLuggage(const std::string &name, const std::string &surname, const std::string &address);
        virtual ~VLuggage(); // allows the call of daughter destroyers.

        // getter :
        double getVolume() const;

        /**
         * @role : function displaying all information of this luggage.
         */
        std::string toString() const;

    protected:
        // Attributes :
        std::string _name;    // the name of the owner.
        std::string _surname; // the surname of the owner.
        std::string _address; // the address of the owner.
        double      _volume;  // the volume of the luggage.

        /**
         * @role : abstract function which calculate the volume of the luggage,
         *         this function is redefine in the son class.
         */
        virtual void volumeCalculation() = 0;
};

#endif //PROJETALGOCONSIGNEBAGAGE_VLUGGAGE_HPP