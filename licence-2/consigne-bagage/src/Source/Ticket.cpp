#include <random>

#include "../Header/Ticket.hpp"

using namespace std;

/**
 * @role : constructor generating a SIZESECRETCODE character string with lowercase
 *         or uppercase letters drawn at random.
 */
Ticket::Ticket() {
    // seed the random number generator named mt.
    random_device rd;
    mt19937 mt(rd());

    uniform_real_distribution<double> rand0(65, 123); // last value not included.
    uniform_real_distribution<double> rand1(65, 91);  // [A (65) - Z (90)]  (ASCII value)
    uniform_real_distribution<double> rand2(97, 123); // [a (97) - z (122)] (ASCII value)

    // initialization of the secret code of SIZESECRETCODE letters (lowercase or uppercase).
    for (int i = 0; i < SIZESECRETCODE; i++) {
        this -> _secretCode += (char) ((rand0(mt) > 100) ? rand1(mt) : rand2(mt));
    }
}

Ticket::~Ticket() = default;

// getter :
string Ticket::getSecretCode() const { return this->_secretCode; }


/**
 * @role : == operator allowing the equality test between two Objects
 *         of type Ticket. It is useful for using unordered_map in the
 *         class Consign.
 *
 * @param ticket : the ticket to compare.
 * @return an boolean if the two tickets are equals.
 */
bool Ticket::operator==(Ticket const& ticket) const {
    return this -> _secretCode       == getSecretCode() &&
           this -> hashCalculation() == ticket.hashCalculation();
}


/**
 * @role : != operator allowing the inequality test between two Objects
 *         of type Ticket. It is useful for using unordered_map in the
 *         class Consign.
 *
 * @param ticket : the ticket to compare.
 * @return an boolean if the two tickets are not equals.
 */
bool Ticket::operator!=(Ticket const& ticket) const {
    return this -> _secretCode       != ticket.getSecretCode() ||
           this -> hashCalculation() != ticket.hashCalculation();
}

/**
 * @role : function for calculating the hash of the secret code of a ticket.
 *          It works thanks to the addition of the ASCII code of all the letters
 *          of the code.
 *
 * @return a hash code.
 */
size_t Ticket::hashCalculation() const {
    size_t hashAscii = 0;

    for (char chr : this -> _secretCode) {
        hashAscii += (int)chr;
    }

    return hashAscii;
}