#ifndef PROJETALGOCONSIGNEBAGAGE_VLUGGAGECIRCLE_HPP
#define PROJETALGOCONSIGNEBAGAGE_VLUGGAGECIRCLE_HPP

#include "VLuggage.hpp"

class VLuggageCircle: public VLuggage {
    public:
        
        /**
         * @role : build the attributes of the class and the super abstract class VLuggage with the surname and 
         *         the name of the owner of the luggage as well as his address and
         *         the volume of the luggage.
         * 
         * @param name    : the name of the owner.
         * @param surname : the surname of the owner.
         * @param address : the address of the owner.
         * @param volume  : the volume of the luggage.
         * @param ray     : the luggage radius.
         *
         * @precondition : ray > 0, because a baggage cannot have a radius <= 0.
         */
        VLuggageCircle(const std::string & name, const std::string & surname, const std::string & address, float radius);
        ~VLuggageCircle();



    protected :
        // Attribute :
            float _radius;

        // Method :
            /**
             * @role : function which calculate the volume of the luggage.
             */
            void volumeCalculation();
};

#endif //PROJETALGOCONSIGNEBAGAGE_VLUGGAGECIRCLE_HPP