#ifndef PROJETALGOCONSIGNEBAGAGE_LOCKER_HPP
#define PROJETALGOCONSIGNEBAGAGE_LOCKER_HPP

#include "Luggage.hpp"

class Locker {
    public:
        /**
         * @role : Build the class Locker with the locker number and
         *         the locker is empty.
         *
         * @param num : the locker number.
         *
         * @precondition : num >= 0, because the lockers start at 1 but can be set to
         *                 0 if there is a problem with baggage insertion.
         */
        Locker(size_t num);
        ~Locker();

        //getters :
        size_t  getNum()     const;
        Luggage getLuggage() const;

        /**
         * @role : function which checks if the locker is empty.
         *
         * @return a boolean if the locker is empty.
         */
        bool lockerIsEmpty() const;

        /**
         * @role : add the luggage in the locker by modifying the luggage attribute.
         *
         * @param luggage : baggage to add.
         * @precondition : the locker must be empty.
         */
        void addLuggage(const Luggage& luggage);

        /**
         * @role : remove the luggage in the locker.
         *
         * @precondition : the locker must not be empty.
         */
        void removeLuggage();

        /**
         * @role : == operator allowing the equality test between two Objects
         *         of type Locker.
         *
         * @param locker : the ticket to compare.
         * @return an boolean if the two Locker are equals.
         */
        bool operator== (const Locker & locker) const;
        
    private:
        // attributes :
        size_t _num;
        Luggage _luggage;
};

#endif //PROJETALGOCONSIGNEBAGAGE_LOCKER_HPP