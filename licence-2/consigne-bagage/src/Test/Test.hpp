#ifndef PROJETALGOCONSIGNEBAGAGE_TEST_HPP
#define PROJETALGOCONSIGNEBAGAGE_TEST_HPP

#include "../Header/Part1/Consign.hpp"
#include "../Header/Part1/Locker.hpp"
#include "../Header/Part1/Luggage.hpp"

#include "../Header/Ticket.hpp"

#include "../Header/Part2/VConsign.hpp"
#include "../Header/Part2/VLocker.hpp"
#include "../Header/Part2/VLuggage.hpp"
#include "../Header/Part2/VLuggageRectangular.hpp"
#include "../Header/Part2/VLuggageCircle.hpp"

class Test {
    public:
        Test();
        ~Test();

        // test part 1 :
        void testLuggage();
        void testLocker();
        void testConsign();

        // test part 1 and 2 :
        void testTicket() const;

        // test part 2 :
        void testVLuggage();
        void testVLocker();
        void testVConsign();

    private:
        // Attributes part 1:
        Luggage _luggage1, _luggage2, _luggage3, _luggage4, _luggage5;
        Locker  _locker1,_locker2;
        Ticket  _ticket1;
        Consign _consign;

        // Attributes part 2:
        VLuggage* _vLuggage1, *_vLuggage2, *_vLuggage3, *_vLuggage4, *_vLuggage5;
        VLocker   _vLocker1,_vLocker2;
        Ticket    _vTicket1;
        VConsign  _vConsign;

        // Methods part 1 :
        void displayAllTabP1() const;

        // Methods part 2 :
        void displayAllTabP2() const;
};

#endif //PROJETALGOCONSIGNEBAGAGE_TEST_HPP