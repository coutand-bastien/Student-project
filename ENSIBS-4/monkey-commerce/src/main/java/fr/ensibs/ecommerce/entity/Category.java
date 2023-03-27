package fr.ensibs.ecommerce.entity;

import jakarta.persistence.*;
import java.io.Serializable;
import java.util.Collection;

@Entity
@Table(name = "category")
public class Category implements Serializable {

    private static final long serialVersionUID = 1L;

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Basic(optional = false)
    @Column(name = "id", nullable = false)
    private Integer id;

    @Basic(optional = false)
    @Column(name = "name", nullable = false, length = 45)
    private String name;

    @Basic(optional = false)
    @Column(name = "description", nullable = false, length = 255)
    private String description;

    @OneToMany(mappedBy="categoryId", cascade = CascadeType.ALL)
    private Collection<Product> productCollection;

    public Category() {}

    public Category(String name) {
        this.name = name;
    }

    public int getId() {
        return this.id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public String getName() {
        return this.name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getDescription() {
        return this.description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public Collection<Product> getProductCollection() {
        return this.productCollection;
    }

    public void setProductCollection(Collection<Product> productCollection) {
        this.productCollection = productCollection;
    }

    @Override
    public int hashCode() {
        int hash = 0;
        hash += (id != null ? id.hashCode() : 0);
        return hash;
    }

    @Override
    public boolean equals(Object object) {
        if (!(object instanceof Category))
            return false;

        Category other = (Category) object;
        return this.id.equals(other.id) && this.name.equals(other.name);
    }

    @Override
    public String toString() {
        return "Category{" +
                "id=" + this.id +
                ", name='" + this.name + '\'' +
                ", description='" + this.description + '\'' +
                ", productCollection=" + this.productCollection +
                '}';
    }
}
