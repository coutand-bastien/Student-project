#ifndef PROJETALGOCONSIGNEBAGAGE_VLUGGAGERECTANGULAR_HPP
#define PROJETALGOCONSIGNEBAGAGE_VLUGGAGERECTANGULAR_HPP

#include "VLuggage.hpp"

class VLuggageRectangular: public VLuggage {
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
         * @param width   : the width of the luggage.
         * @param height  : the height of the luggage.
         * @param length  : the length of the luggage.
         *
         * @precondition : width > 0 && height > 0 && length > 0, because a baggage cannot have a length
         *                 or a height or a width <= 0
         */
        VLuggageRectangular(const std::string & name, const std::string & surname, const std::string & address, float width, float height, float length);
        ~VLuggageRectangular();

    protected :
        // Attributes :
            float _height, _length, _width;

        // Method :
            /**
             * @role : function which calculate the volume of the luggage.
             */
            void volumeCalculation();
};

#endif //PROJETALGOCONSIGNEBAGAGE_VLUGGAGERECTANGULAR_HPP