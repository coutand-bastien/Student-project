#ifndef CONSIGNE_BAGAGE_VCONSIGN_HPP
#define CONSIGNE_BAGAGE_VCONSIGN_HPP

#include <map>
#include <queue>
#include <unordered_map>

#include "VLocker.hpp"
#include "../Ticket.hpp"

class VConsign {
    public:
        /**
         * @role : The builder initializes the empty locker queues because when building a consign no locker is taken.
         *
         * @param volume_map : It represents a request from a client wanting to build a deposit. This allows an
         *                     addition of realism to the project. In the key, there are the volumes of the lockers and in values a file of size
         *                     corresponding to the number of lockers wanted for this volume (key).
         */
        VConsign(const std::map<double, unsigned int>& volume_map);
        ~VConsign();

        std::map<double, std::queue<VLocker>> getFreeLocker_map() const;
        std::unordered_map<Ticket, VLocker>   getHashMap()        const;

        /**
         * @role : function which checks if the empty locker queue is empty.
         *         If, it's empty, then all the lockers are filled.
         *
         * @return a boolean if consign is full.
         */
        bool consignIsFull() const;

        /**
         * @role : function as which deposits a baggage in a free locker for the oldest use with a volume greater
         *         than or equal as close as possible to the volume of the baggage to be deposited.
         *         A unit ticket will refer to the locker in question, thanks to an associative table.
         *
         * @param baggage : the baggage to be dropped off.
         * @exception : if the free locker queue is empty.
         * @exception : if there is no locker capable of storing luggage due to its volume.
         *
         * @return a ticket referring to the locker where the luggage is located.
         */
        Ticket addLuggage(VLuggage * luggage) noexcept(false);

        /**
         * @role : procedure for removing luggage from a used locker. it builds a new queue
         *         if the one does not exist in the empty locker list because if it exists in
         *         the full lockers then it was before in the empty lockers.
         *
         * @param ticket : a ticket referring to the locker where the luggage is located.
         * @exception : if the full locker unordered_map is empty or if the ticket does not exist.
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
            std::map<double, std::queue<VLocker>> _freeLocker_map; // the empty lockers by volume.
            std::unordered_map<Ticket, VLocker>   _hashTable;      // the hash table.

        // method:
            /**
             * @role : the function initializes a map made up of keys which are duplicates (volumes)
             *         and values which are queues (empty locker files), thanks to the map passed as a parameter
             *         which contains the volume and value, the number of lockers desired.
             *         Initializes the queue with lockers numbered from 1 to nbLocker
             *         by calling the constructor of VLocker. The locker indices start at 1
             *         to be able to leave the number 0, for cases where there is a problem with
             *         the insertion of a baggage.
             *
             * @param nbLocker_queue : the number of queues to create with empty lockers.
             * @param volume_map     : the list of the number of lockers (values) desired according
             *                         to their volume (keys).
             *
             * @return a map composed of the key (volume) and values (empty locker queue)
             */
            std::map<double, std::queue<VLocker>> initFreeLocker_map(const std::map<double, unsigned int>& volume_map) noexcept(false);
};

#endif //CONSIGNE_BAGAGE_VCONSIGN_HPP