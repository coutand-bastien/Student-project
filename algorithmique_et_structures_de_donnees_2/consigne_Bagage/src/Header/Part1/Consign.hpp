#ifndef PROJETALGOCONSIGNEBAGAGE_CONSIGN_HPP
#define PROJETALGOCONSIGNEBAGAGE_CONSIGN_HPP

#include <queue>
#include <unordered_map>

#include "Locker.hpp"
#include "../Ticket.hpp"
#include "Luggage.hpp"

class Consign {
    public:
        /**
         * @role : build the attributes of the class with nbLocker locker for the
         *         empty locker queue. The full locker list is not initialized because at the start
         *         it is empty.
         *
         * @param nbLocker : the number of locker to initialize.
         *
         * @precondition : nbLocker > 0, because you cannot have a number of lockers in a consign
         *                 less than or equal to 0.
         **/
        Consign(int nbLocker);
        ~Consign();

        // getters :
        std::unordered_map<Ticket, Locker> getHashMap()          const;
        std::queue<Locker>                 getFreeLocker_queue() const;

        /**
         * @role : function which checks if the empty locker queue is empty.
         *         If, it's empty, then all the lockers are filled.
         *
         * @return a boolean if the consign is full.
         */
        bool consignIsFull() const;

        /**
         * @role : function which deposits a luggage in a free locker with the oldest use.
         *         A unit ticket will refer to the locker in question thanks to an associative table.
         *
         * @param luggage : baggage to drop off.
         * @exception : if the free locker queue is empty.
         * @return a ticket referring to the locker where the luggage is located.
         */
        Ticket addLuggage(const Luggage & luggage) noexcept(false);

        /**
         * @role : procedure for removing luggage from a used locker.
         *
         * @param ticket : a ticket referring to the locker where the luggage is located.
         * @exception : if the full locker list is empty or if the ticket does not exist.
         */
        void removeLuggage(const Ticket & ticket) noexcept(false);

        /**
         * @role : function displaying the number of lockers used in the deposit.
         *
         * @return a string.
         */
        std::string toString() const;

    private:
        // attributes :
        std::queue<Locker>                 _freeLocker_queue; // the empty locker queue.
        std::unordered_map<Ticket, Locker> _hashTable;        // the hash table.

        // method :
        /**
         * @role : initializes the queue with lockers numbered from 1 to nbLocker
         *         by calling the constructor of Locker. The locker indices start at 1
         *         to be able to leave the number 0, for cases where there is a problem with
         *         the insertion of a baggage.
         *
         * @param nbLocker : the number of lockers to create.
         * @return a queue with nbLocker locker.
         */
        std::queue<Locker> initFreeLocker_queue(int nbLocker);
};

#endif //PROJETALGOCONSIGNEBAGAGE_CONSIGN_HPP