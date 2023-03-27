#ifndef PROJETALGOCONSIGNEBAGAGE_VLOCKER_HPP
#define PROJETALGOCONSIGNEBAGAGE_VLOCKER_HPP

#include "VLuggage.hpp"

class VLocker {
    public:
        /**
         * @role : Build the class VLocker with the locker number and
         *         the locker is empty.
         *
         * @param num    : the locker number.
         * @param volume : the space of the locker.
         *
         * @precondition : num >= 0, because the lockers start at 1 but can be set to
         *                 0 if there is a problem with baggage insertion and volume >= 0,
         *                 because they start with a volume greater than 0 but can be set to 0
         *                 if there is no luggage in the locker.
         */
        VLocker(size_t num, double volume);
        ~VLocker();

        //getters :
        size_t getNum()    const;
        double getVolume() const;

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
        void addLuggage(VLuggage * luggage);

        /**
         * @role : remove the luggage in the locker.
         *
         * @precondition : the locker must not be empty.
         */
        void removeLuggage();

        /**
         * @role : == operator allowing the equality test between two Objects
         *         of type VLocker.
         *
         * @param locker : the ticket to compare.
         * @return a boolean if the two VLocker are equals.
         */
        bool operator== (const VLocker & locker) const;
        
    private:
        // attributes :
        size_t     _num;
        double     _volume;
        VLuggage * _luggage;
};

#endif //PROJETALGOCONSIGNEBAGAGE_VLOCKER_HPP