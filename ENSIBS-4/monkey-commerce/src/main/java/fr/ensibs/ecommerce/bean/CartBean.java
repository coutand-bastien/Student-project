package fr.ensibs.ecommerce.bean;

import fr.ensibs.ecommerce.entity.Product;
import fr.ensibs.ecommerce.utils.cart.Cart;
import jakarta.ejb.EJB;
import jakarta.enterprise.context.SessionScoped;
import jakarta.inject.Named;

import java.io.Serializable;

@Named("cartBean")
@SessionScoped
public class CartBean implements Serializable  {
    /**
     * The shopping cart
     */
    private @EJB Cart cart;

    /**
     * The error messages
     */
    private String errorMessage;

    public CartBean() {}

    public Cart getCart() {
        return this.cart;
    }

    public String getErrorMessage() {
        return this.errorMessage;
    }


    /**
     * Clear the shopping cart and get the route to the cart page
     */
    public String clearCart() {
        this.cart.clear();
        return "cart";
    }

    /**
     * Add a product from the shopping cart
     * @param product the product to add
     */
    public void addItem(Product product) {
        if (product == null) {
            this.errorMessage = "The product must be specified"; return;
        }

        try {
            this.cart.addItem(product);
            this.errorMessage = null;
        }
        catch (Exception e) {
            this.errorMessage = e.getMessage();
        }
    }

    /**
     * Remove a product from the shopping cart
     * @param product the product to remove
     */
    public void removeItem(Product product) {
        if (product == null) {
            this.errorMessage = "The product must be specified"; return;
        }

        try {
            this.cart.removeItem(product);
            this.errorMessage = null;
        }
        catch (Exception e) {
            this.errorMessage = e.getMessage();
        }
    }

    /**
     * Update the quantity of a product in the shopping cart
     */
    public void updateItem(String quantity, String productId) {
        if (quantity == null || productId == null) {
            this.errorMessage = "The quantity and the product id must be specified"; return;
        }

        int qty = Integer.parseInt(quantity);

        if (qty <= 0) {
            this.errorMessage = "Cannot update negative or null quantity in cart"; return;
        }

        try {
            this.cart.update(Integer.parseInt(productId), qty);
            this.errorMessage = null;
        }
        catch (Exception e) {
            this.errorMessage = e.getMessage();
        }
    }


    /**
     * Increase the quantity of a product in the shopping cart. If the quantity is already at the maximum, print an error
     * message in the console and to the client.
     * @param product the product
     */
    public void increaseQuantity(Product product) {
        if (product == null) {
            this.errorMessage = "The product must be specified"; return;
        }

        try {
            this.cart.increaseQuantity(product);
            this.errorMessage = null;
        }
        catch (Exception e) {
            this.errorMessage = e.getMessage();
        }
    }

    /**
     * Decrease the quantity of a product in the shopping cart. If the quantity is already at the minimum, print an error
     * message in the console and to the client.
     * @param product the product
     */
    public void decreaseQuantity(Product product) {
        if (product == null) {
            this.errorMessage = "The product must be specified"; return;
        }

        try {
            this.cart.decreaseQuantity(product);
            this.errorMessage = null;
        }
        catch (Exception e) {
            this.errorMessage = e.getMessage();
        }
    }

    /**
     * Get the total price of the shopping cart (without shipping). If there is an error, print an error message in the
     * console and to the client.
     * @return the total price
     */
    public String purchase() {
        try {
            this.cart.purchase();
            this.errorMessage = null;
            return "order";
        }
        catch (Exception e) {
            this.errorMessage = e.getMessage();
            return "checkout";
        }
    }
}