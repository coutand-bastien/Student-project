import fr.ensibs.ecommerce.entity.Customer;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import fr.ensibs.ecommerce.entity.Product;
import fr.ensibs.ecommerce.utils.cart.CartItem;
import fr.ensibs.ecommerce.utils.cart.Cart;

import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

public class CartTest {
    private Cart cart;

    public CartTest() {
        this.cart = null;
    }

    @BeforeEach
    public void setUp() {
        CartItem item1 = new CartItem(new Product("Test Product 1", new BigDecimal("10.0"), "Test Description 1", new Date(), 2));
        CartItem item2 = new CartItem(new Product("Test Product 2", new BigDecimal("20.0"), "Test Description 2", new Date(), 3));
        CartItem item3 = new CartItem(new Product("Test Product 3", new BigDecimal("30.0"), "Test Description 3", new Date(), 4));
        CartItem item4 = new CartItem(new Product("Test Product 4", new BigDecimal("40.0"), "Test Description 4", new Date(), 5));
        ArrayList<CartItem> items = new ArrayList<>(List.of(new CartItem[]{item1, item2, item3, item4}));

        Customer customer = new Customer("couttcoutt", "couttcoutt@gmail.com", "0660676513", "20 l'audouiniere", "FR", "012345689012345678");

        this.cart = new Cart(items, 100.0, customer);
    }

    @Test
    public void testAddItem() {
        Product product = new Product("Test Product 5", new BigDecimal("50.0"), "Test Description 5", new Date(), 5);
        CartItem item   = new CartItem(product);

        try {
            this.cart.addItem(product);
        } catch (Exception e) {
            throw new RuntimeException(e);
        }

        assertEquals(5, this.cart.getItems().size());
        assertTrue(this.cart.getItems().contains(item));
    }

    @Test
    public void testRemoveItem() {
        Product product = new Product("Test Product 2", new BigDecimal("20.0"), "Test Description 2", new Date(), 2);
        CartItem item   = new CartItem(product);

        try {
            this.cart.removeItem(product);
        } catch (Exception e) {
            throw new RuntimeException(e);
        }

        assertEquals(3, this.cart.getItems().size());
        assertFalse(this.cart.getItems().contains(item));
    }

    @Test
    public void testIncreaseQuantity() {
        Product product = new Product("Test Product 4", new BigDecimal("40.0"), "Test Description 4", new Date(), 2);
        CartItem item   = new CartItem(product);

        try {
            this.cart.increaseQuantity(product);
        } catch (Exception e) {
            throw new RuntimeException(e);
        }

        assertEquals(2, item.getQuantity());

        // test exception -> no more products available
        assertEquals(2, item.getQuantity());
    }

    @Test
    public void testDecreaseQuantity() {
        Product product = new Product("Test Product 4", new BigDecimal("40.0"), "Test Description 4", new Date(), 2);
        CartItem item   = new CartItem(product);

        try {
            this.cart.decreaseQuantity(product);
        } catch (Exception e) {
            throw new RuntimeException(e);
        }

        assertEquals(0, item.getQuantity());
    }
}
