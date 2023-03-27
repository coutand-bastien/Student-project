import fr.ensibs.ecommerce.entity.Product;
import fr.ensibs.ecommerce.utils.cart.CartItem;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.math.BigDecimal;
import java.util.Date;

import static org.junit.jupiter.api.Assertions.*;

public class CartItemTest {
    private CartItem item;

    public CartItemTest() {
        this.item = null;
    }

    @BeforeEach
    public void setUp() {
        Product product = new Product("Test Product", new BigDecimal("10.0"), "Test Description", new Date(), 2);
        this.item       = new CartItem(product);
    }

    @Test
    public void testIncrementQuantity() {
        // Verify initial quantity
        assertEquals(1, item.getQuantity());

        item.incrementQuantity();
        assertEquals(2, item.getQuantity());
    }

    @Test
    public void testDecrementQuantity() {
        // Verify initial quantity
        assertEquals(1, item.getQuantity());

        // Decrement quantity
        item.decrementQuantity();
        assertEquals(0, item.getQuantity());
    }
}
