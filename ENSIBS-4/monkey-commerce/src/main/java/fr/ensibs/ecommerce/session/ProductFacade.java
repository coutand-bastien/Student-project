package fr.ensibs.ecommerce.session;

import fr.ensibs.ecommerce.entity.Product;
import jakarta.ejb.Stateless;

import java.util.List;

@Stateless
public class ProductFacade extends AbstractFacade<Product> {

    public ProductFacade() {
        super(Product.class);
    }

    @Override
    public List<Product> findAll() {
        List<Product> products = super.findAll();
        products.removeIf(product -> product.getBaseQuantity() <= 0);
        return products;
    }
}
