package fr.ensibs.ecommerce.bean;

import fr.ensibs.ecommerce.entity.Category;
import fr.ensibs.ecommerce.entity.Product;
import fr.ensibs.ecommerce.session.CategoryFacade;
import jakarta.ejb.EJB;
import jakarta.enterprise.context.SessionScoped;
import jakarta.inject.Named;

import java.io.Serializable;
import java.util.Collection;
import java.util.List;

@Named("emplateBean")
@SessionScoped
public class EmplateBean implements Serializable {

    /**
     * The category facade
     */
    private @EJB CategoryFacade categoryFacade;

    /**
     * The selected category
     */
    private Category selectedCategory;

    /**
     * The category name
     */
    private String categoryName;

    public EmplateBean() {
        this.categoryName = "1"; // default to avoid errors in cart.xhtml
    }

    public Category getSelectedCategory() {
       return this.selectedCategory;
    }

    public void setSelectedCategory(Category selectedCategory) {
        this.selectedCategory = selectedCategory;
    }

    public String getCategoryName() {
        return categoryName;
    }

    public void setCategoryName(String categoryName) {
        this.categoryName = categoryName;
    }

    /**
     * Get the products from the selected category
     * @return the list of products
     */
    public Collection<Product> productsFromCategory() {
        this.selectedCategory = this.categoryFacade.find(Integer.parseInt(this.categoryName));
        return this.selectedCategory.getProductCollection();
    }

    /**
     * Get all categories
     * @return the list of categories
     */
    public List<Category> listAllCategories() {
        return this.categoryFacade.findAll();
    }
}
