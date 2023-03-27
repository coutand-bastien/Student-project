package fr.ensibs.ecommerce.session;

import fr.ensibs.ecommerce.entity.Category;
import jakarta.ejb.Stateless;


@Stateless
public class CategoryFacade extends AbstractFacade<Category>  {

    public CategoryFacade() {
        super(Category.class);
    }
}
