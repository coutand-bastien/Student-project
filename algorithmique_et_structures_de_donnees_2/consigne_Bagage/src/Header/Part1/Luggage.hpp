#ifndef PROJETALGOCONSIGNEBAGAGE_LUGGAGE_HPP
#define PROJETALGOCONSIGNEBAGAGE_LUGGAGE_HPP

#include <iostream>

class Luggage {
    public:
        /**
         * @role : build the attributes of the class with the surname and 
         * the name of the owner of the luggage as well as his address and 
         * the weight of the luggage.
         * 
         * @param name    : the name of the owner.
         * @param surname : the surname of the owner.
         * @param address : the address of the owner.
         * @param weight  : the weight of the luggage.
         *
         * @precondition : weight >= 0, because they start with a weight greater than
         *                 0 but can be set to 0 if there is no luggage in the locker.
         */
        Luggage(const std::string &name, const std::string &surname, const std::string &address, float weight);
        ~Luggage();

        // getters :
        std::string getName()    const;
        std::string getSurname() const;
        std::string getAddress() const;
        float       getWeight()  const;

        /**
         * @role : function displaying all information of this luggage.
         */
        std::string toString() const;

    private:
        // Attributes :
        std::string _name;    //the name of the owner.
        std::string _surname; //the surname of the owner.
        std::string _address; //the address of the owner.
        float       _weight;  //the weight of the luggage.
};

#endif //PROJETALGOCONSIGNEBAGAGE_LUGGAGE_HPP