package fr.ensibs.ecommerce.utils.cart;

import fr.ensibs.ecommerce.entity.Product;

/**
 * A shopping cart item is a product with a quantity.
 */
public class CartItem {
    /**
     * The product of this shopping cart item.
     */
    private final Product product;

    /**
     * The quantity of this shopping cart item.
     */
    private int quantity;

    public CartItem(Product product, int quantity) {
        this.product  = product;
        this.quantity = quantity;
    }

    public CartItem(Product product) {
        this.product  = product;
        this.quantity = 1;
    }
    
    public Product getProduct() {
        return product;
    }
    
    public int getQuantity() {
        return quantity;
    }

    public void setQuantity(int quantity) {
        this.quantity = quantity;
    }

    /**
     * Increments the quantity of this shopping cart item. If the quantity is not enough,
     * an exception is thrown.
     */
    public void incrementQuantity() {
        this.quantity++;
    }

    /**
     * Decrements the quantity of this shopping cart item. If the quantity is negative,
     * an exception is thrown.
     */
    public void decrementQuantity() {
        this.quantity--;
    }

    /**
     * Returns true if this shopping cart item is equal to the specified object.
     * @param obj the object to compare
     * @return true if this shopping cart item is equal to the specified object
     */
    @Override
    public boolean equals(Object obj) {
        return obj instanceof CartItem && this.product.equals(((CartItem) obj).product);
    }
}
