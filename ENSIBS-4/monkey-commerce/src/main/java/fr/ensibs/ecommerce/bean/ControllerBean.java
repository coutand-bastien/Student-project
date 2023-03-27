package fr.ensibs.ecommerce.bean;

import jakarta.enterprise.context.RequestScoped;
import jakarta.inject.Named;

@Named("controllerBean")
@RequestScoped
public class ControllerBean {

    /**
     * Get the route to the checkout page
     * @return the route
     */
    public String getCheckout() { return "checkout"; }

    /**
     * Get the route to the cart page
     * @return the route
     */
    public String getCart() {
        return "cart";
    }

    /**
     * Get the route to the shop page
     * @return the route
     */
    public String getShop() {
        return "shop";
    }

}
