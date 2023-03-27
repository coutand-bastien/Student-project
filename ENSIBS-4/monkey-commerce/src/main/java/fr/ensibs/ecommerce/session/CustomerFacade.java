package fr.ensibs.ecommerce.session;

import fr.ensibs.ecommerce.entity.Customer;
import jakarta.ejb.Stateless;

@Stateless
public class CustomerFacade extends AbstractFacade<Customer> {

    public CustomerFacade() {
        super(Customer.class);
    }
    
}
