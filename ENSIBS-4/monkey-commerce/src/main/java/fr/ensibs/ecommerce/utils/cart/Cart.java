package fr.ensibs.ecommerce.utils.cart;

import fr.ensibs.ecommerce.entity.Customer;
import fr.ensibs.ecommerce.entity.CustomerOrder;
import fr.ensibs.ecommerce.entity.Product;
import fr.ensibs.ecommerce.session.CustomerFacade;
import fr.ensibs.ecommerce.session.CustomerOrderFacade;
import fr.ensibs.ecommerce.session.ProductFacade;
import jakarta.ejb.EJB;
import jakarta.ejb.Stateless;

import java.io.Serializable;
import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;
import java.util.Random;

/**
 * A shopping cart is a list of shopping cart items.
 */
@Stateless
public class Cart implements Serializable  {
    /**
     * The product facade to access the products in the database
     */
    @EJB
    private ProductFacade productFacade;

    /**
     * The customer order facade to access the customer orders in the database
     */
    @EJB
    private CustomerOrderFacade customerOrderFacade;

    /**
     * The customer facade to access the customers in the database
     */
    @EJB
    private CustomerFacade customerFacade;

    /**
     * The list of shopping cart products.
     */
    private final List<CartItem> items;

    /**
     * The total price of the shopping cart.
     */
    private double total;

    /**
     * The customer
     */
    private Customer customer;

    /**
     * The customer order
     */
    private final CustomerOrder customerOrder;

    /**
     * USE ONLY FOR TESTS
     */
    public Cart(ArrayList<CartItem> items, double total, Customer customer) {
        this.items         = items;
        this.total         = total;
        this.customer      = customer;
        this.customerOrder = new CustomerOrder();
    }

    public Cart() {
        this.customer      = new Customer();
        this.customerOrder = new CustomerOrder();
        this.items         = new ArrayList<>();
        this.total         = 0;
    }

    public List<CartItem> getItems() {
        return this.items;
    }

    public double getTotal() {
        return this.total;
    }

    public Customer getCustomer() {
        return this.customer;
    }

    public void setCustomer(Customer customer) {
        this.customer = customer;
    }

    public CustomerOrder getCustomerOrder() {
        return this.customerOrder;
    }

    /**
     * Get the shopping cart item of the specified product
     *
     * @param product the product
     * @throws Exception if the product is null or if the product does not exist in the shopping cart
     * @return the shopping cart item of the specified product
     * @see CartItem
     * @see Product
     */
    private CartItem getCartItem(Product product) throws Exception {
        if (product == null)
            throw new Exception("Cannot get shopping cart item of null product");

        if (!this.items.contains(new CartItem(product)))
            throw new Exception("Cannot get shopping cart item of product that does not exist in shopping cart");

        return this.items.get(this.items.indexOf(new CartItem(product)));
    }
        
    /**
     * Adds a shoppingCartItem to the ShoppingCart's items list. If item of the specified product
     * already exists in shopping cart list, the quantity of that item is incremented.
     *
     * @param product the Product that defines the type of shopping cart item
     * @throws Exception if the product is null or if the product does not exist in the database
     * @see CartItem
     * @see Product
     */
    public void addItem(Product product) throws Exception {
        if (product == null)
            throw new Exception("Cannot add null product to cart");
        
        CartItem scItem = new CartItem(product);

        if (this.items.contains(scItem)) {
            this.increaseQuantity(scItem.getProduct());
        } else {
            this.items.add(scItem);
            this.total = calculateTotal();
        }
    }

    /**
     * Removes the ShoppingCartItem of the specified product from the ShoppingCart's items list.
     *
     * @param product the Product that defines the type of shopping cart item
     * @throws Exception if the product is null or if the product does not exist in the database
     * @see CartItem
     * @see Product
     */
    public void removeItem(Product product) throws Exception {
        CartItem itemMirror_tmp = new CartItem(product); // mirror of the item to remove, not the item itself

        if (!this.items.contains(itemMirror_tmp))
            throw new Exception("Cannot remove non-existing item from cart");

        CartItem theItem = this.items.get(this.items.indexOf(itemMirror_tmp));
        this.items.remove(theItem);

        this.total = calculateTotal();
    }
    
    /**
     * Updates the ShoppingCartItem of the specified product to the specified quantity. If '0'
     * is the given quantity, the ShoppingCartItem is removed from the ShoppingCart's items list.
     *
     * @param productId the Product that defines the type of shopping cart item
     * @param quantity the number which the ShoppingCartItem is updated to
     * @throws Exception if the product is null or if the product does not exist in the database or
     *                                  if the quantity is greater than the base quantity of the product
     * @see CartItem
     * @see Product
     */
    public void update(int productId, int quantity) throws Exception {
        Product product = this.productFacade.find(productId);

        if(product == null)
            throw new Exception("Cannot update non-existing product in cart");

        if (product.getBaseQuantity() - quantity < 0)
            throw new Exception("Cannot update product in cart with quantity greater than base quantity");

        CartItem itemMirror_tmp = new CartItem(product); // mirror of the item to update, not the item itself

        if (!this.items.contains(itemMirror_tmp))
            throw new Exception("Cannot update non-existing item in cart");

        CartItem theItem = this.items.get(this.items.indexOf(itemMirror_tmp));

        // remove the item if quantity is 0 or less
        if (quantity > 0) {
            theItem.setQuantity(quantity);
        } else {
            this.items.remove(itemMirror_tmp);
        }

        this.total = calculateTotal(); // update the total
    }


    /**
     * Increases the quantity of the item with the given id by 1 and updates the total cost.
     * And calculates the total cost of the shopping cart.
     * @param product : the product of the item to increase the quantity of
     * @throws Exception if the given product is null or if the given quantity is null or negative
     */
    public void increaseQuantity(Product product) throws Exception {
        CartItem item = this.getCartItem(product);

        if (item.getProduct().getBaseQuantity() - (item.getQuantity() + 1) >= 0) {
            item.incrementQuantity();
            this.total += item.getProduct().getPrice().doubleValue();
        }
        else {
            throw new Exception("Cannot increase quantity of product in cart with quantity greater than base quantity");
        }
    }

    /**
     * Decreases the quantity of the item with the given id by 1 and updates the total cost.
     * And calculates the total cost of the shopping cart. If the quantity of the item is 1,
     * the item is removed from the shopping cart.
     * @param product : the product of the item to increase the quantity of
     * @throws Exception if the given product is null or if the given quantity is null or negative
     */
    public void decreaseQuantity(Product product) throws Exception {
        CartItem item = this.getCartItem(product);

        if (item.getQuantity() - 1 <= 0) {
            this.removeItem(item.getProduct());
        } else {
            item.decrementQuantity();
            this.total -= item.getProduct().getPrice().doubleValue();
        }
    }
    
    /**
     * Returns the sum of the product price multiplied by the quantity for all
     * items in shopping cart list. This is the total cost excluding the surcharge.
     *
     * @return the cost of all items times their quantities
     * @see CartItem
     */
    private double calculateTotal() {
        double amount = 0;

        for (CartItem scItem : items)
            amount += (scItem.getQuantity() * scItem.getProduct().getPrice().doubleValue());

        return amount;
    }
    
    /**
     * Empties the shopping cart. All items are removed from the shopping cart
     * items list, numberOfItems and total are reset to '0'.
     */
    public void clear() {
        this.items.clear();
        this.total = 0;
    }

    /**
     * Secure the purchase of the products in the shopping cart by checking the customer's information.
     * @throws Exception if the customer's name, email or phone number is invalid
     */
    private void securePurchase() throws Exception {
        if (this.customer.getName() == null ||
                !this.customer.getName().matches("^[a-zA-ZÀ-ÖØ-öø-ÿ\s'-]{1,45}$") ||
                this.customer.getName().isEmpty() ||
                this.customer.getName().length() > 45) {
            throw new Exception("Invalid name");
        }

        if (this.customer.getEmail() == null ||
                !this.customer.getEmail().matches("^[A-Za-z0-9+_.-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$") ||
                this.customer.getEmail().isEmpty() ||
                this.customer.getEmail().length() > 45) {
           throw new Exception("Invalid email");
        }

        if (this.customer.getPhone() == null ||
                !this.customer.getPhone().matches("^[0-9]{10}$")
                || this.customer.getPhone().isEmpty() ||
                this.customer.getPhone().length() > 10) {
            throw new Exception("Invalid phone");
        }

        // This regex does not allow special characters that could be used in XSS or SSTI attacks, such as <, >, &, ', ", (, ), {, }, [, ], ;, :, ,, \\, |, or /. It therefore validates addresses without risk of attacks of this type.
        if (this.customer.getAddress() == null ||
                !this.customer.getAddress().matches("^([0-9]*) ?([a-zA-Z,'\\. ]*) ?([0-9]{0,5}) ?([a-zA-Z]*)$") ||
                this.customer.getAddress().isEmpty() ||
                this.customer.getAddress().length() > 45) {
            throw new Exception("Invalid address");
        }

        if (this.customer.getCityRegion() == null ||
                this.customer.getCityRegion().isEmpty() ||
                this.customer.getCityRegion().length() > 2) {
            throw new Exception("Invalid city region");
        }

        if (this.customer.getCreditCardNumber() == null ||
                !this.customer.getCreditCardNumber().matches("^[0-9]{19}$") ||
                this.customer.getCreditCardNumber().isEmpty() ||
                this.customer.getCreditCardNumber().length() > 19) {
            throw new Exception("Invalid credit card number");
        }
    }

    /**
     * Purchase the products in the shopping cart
     * @throws Exception if the customer's information is invalid
     * @see CustomerFacade
     * @see CustomerOrderFacade
     * @see ProductFacade
     * @see Product
     * @see Customer
     * @see CustomerOrder
     * @see CartItem
     */
    public void purchase() throws Exception {
        this.securePurchase(); // check if the customer's information is valid

        this.customerFacade.create(this.customer); // create the customer of the order

        this.customerOrder.setCustomerId(this.customer);
        this.customerOrder.setAmount(BigDecimal.valueOf(this.total));
        this.customerOrder.setDateCreated(new Date());
        this.customerOrder.setConfirmationNumber(new Random().nextInt(1000000));

        for (CartItem cartItem : this.items) {
            this.customerOrder.getProductCollection().add(cartItem.getProduct());

            // for each product in the shopping cart, update the base quantity
            Product product = cartItem.getProduct();
            product.setBaseQuantity(product.getBaseQuantity() - cartItem.getQuantity()); // update the base quantity
            this.productFacade.edit(product); // udpate the product in the database
        }

        this.customerOrderFacade.create(this.customerOrder);
    }
}
