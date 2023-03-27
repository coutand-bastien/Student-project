package fr.ensibs.ecommerce.session;

import fr.ensibs.ecommerce.entity.CustomerOrder;
import jakarta.ejb.Stateless;

@Stateless
public class CustomerOrderFacade extends AbstractFacade<CustomerOrder> {

    public CustomerOrderFacade() {
        super(CustomerOrder.class);
    }
    
}
