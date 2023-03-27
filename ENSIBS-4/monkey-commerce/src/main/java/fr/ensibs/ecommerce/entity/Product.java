package fr.ensibs.ecommerce.entity;

import java.io.Serializable;
import java.math.BigDecimal;
import java.util.Collection;
import java.util.Date;
import jakarta.persistence.*;

@Entity
@Table(name = "product")
public class Product implements Serializable {

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
    @Column(name = "price", nullable = false, precision = 5, scale = 2)
    private BigDecimal price;

    @Basic(optional = false)
    @Column(name = "description", nullable = false)
    private String description;

    @Basic(optional = false)
    @Column(name = "last_update", nullable = false)
    @Temporal(TemporalType.TIMESTAMP)
    private Date lastUpdate;

    @Basic(optional = false)
    @Column(name = "base_quantity", nullable = false)
    private int baseQuantity;

    @ManyToOne(optional = false)
    @JoinColumn(name = "category_id", referencedColumnName = "id", nullable = false)
    private Category categoryId;

    @ManyToMany(mappedBy = "productCollection")
    private Collection<CustomerOrder> customerOrderCollection;

    public Product() {}

    public Product(String name, BigDecimal price, String description, Date lastUpdate, int baseQuantity) {
        this.name = name;
        this.price = price;
        this.description = description;
        this.lastUpdate = lastUpdate;
        this.baseQuantity = baseQuantity;
    }

    public Integer getId() {
        return this.id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public String getName() {
        return this.name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public BigDecimal getPrice() {
        return this.price;
    }

    public void setPrice(BigDecimal price) {
        this.price = price;
    }

    public String getDescription() {
        return this.description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public Date getLastUpdate() {
        return this.lastUpdate;
    }

    public void setLastUpdate(Date lastUpdate) {
        this.lastUpdate = lastUpdate;
    }

    public Collection<CustomerOrder> getCustomerOrderCollection() {
        return this.customerOrderCollection;
    }

    public void setCustomerOrderCollection(Collection<CustomerOrder> customerOrderCollection) {
        this.customerOrderCollection = customerOrderCollection;
    }

    public int getBaseQuantity() {
        return this.baseQuantity;
    }

    public void setBaseQuantity(int baseQuantity) {
        this.baseQuantity = baseQuantity;
    }

    public Category getCategoryId() {
        return this.categoryId;
    }

    public void setCategoryId(Category categoryId) {
        this.categoryId = categoryId;
    }

    @Override
    public int hashCode() {
        int hash = 0;
        hash += (id != null ? id.hashCode() : 0);
        return hash;
    }

    @Override
    public boolean equals(Object object) {
        if (!(object instanceof Product))
            return false;

        Product other = (Product) object;
        return  this.id.equals(other.id) &&
                this.name.equals(other.name) &&
                this.price.equals(other.price);
    }

    @Override
    public String toString() {
        return "Product{" +
                "id=" + this.id +
                ", name='" + this.name + '\'' +
                ", price=" + this.price +
                ", description='" + this.description + '\'' +
                ", lastUpdate=" + this.lastUpdate +
                ", baseQuantity=" + this.baseQuantity +
                ", customerOrderCollection=" + this.customerOrderCollection +
                '}';
    }
}
