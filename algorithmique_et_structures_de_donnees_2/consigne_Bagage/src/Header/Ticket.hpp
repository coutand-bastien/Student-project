#ifndef PROJETALGOCONSIGNEBAGAGE_TICKET_HPP
#define PROJETALGOCONSIGNEBAGAGE_TICKET_HPP

#include <iostream>

int const SIZESECRETCODE = 50; // size of the secretCode.

class Ticket {
    public:
        /**
         * @role : constructor generating a SIZESECRETCODE character string with lowercase
         *         or uppercase letters drawn at random.
         */
        Ticket();
        ~Ticket();

        // getter :
        std::string getSecretCode() const;

        /**
         * @role : == operator allowing the equality test between two Objects
         *         of type Ticket. It's useful for using unordered_map in the
         *         class Consign.
         *
         * @param ticket : the ticket to compare.
         * @return an boolean if the two tickets are equals.
         */
        bool operator== (const Ticket & ticket) const;

        /**
         * @role : != operator allowing the inequality test between two Objects
         *         of type Ticket. It's useful for using unordered_map in the
         *         class Consign.
         *
         * @param ticket : the ticket to compare.
         * @return an boolean if the two tickets are not equals.
         */
        bool operator!= (Ticket const& ticket) const;

        /**
         * @ role : function for calculating the hash of the secret code of a ticket.
         *          It works thanks to the addition of the ASCII code of all the letters
         *          of the code.
         * @return a hash code.
         */
        size_t hashCalculation() const;

    private:
        // attribute :
        std::string _secretCode; // identity of the ticket.
};

/**
 * @role : operator specialization () in the hash struct, for Ticket type objects.
 *         It's useful for using unordered_map in the class Consign.
 */
namespace std {
    template<>
    struct hash<Ticket> {
        size_t operator()(const Ticket &x) const {
            return x.hashCalculation();
        }
    };
}

#endif //PROJETALGOCONSIGNEBAGAGE_TICKET_HPP