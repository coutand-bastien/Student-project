package fr.ensibs.ecommerce.entity;

import java.io.Serializable;
import java.math.BigDecimal;
import java.util.Collection;
import java.util.Date;
import jakarta.persistence.*;

@Entity
@Table(name = "customer_order")
public class CustomerOrder implements Serializable {

    private static final long serialVersionUID = 1L;

    @Id
    @Basic(optional = false)
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "id", nullable = false)
    private Integer id;

    @Basic(optional = false)
    @Column(nullable = false, precision = 6, scale = 2)
    private BigDecimal amount;

    @Basic(optional = false)
    @Column(name = "date_created", nullable = false)
    @Temporal(TemporalType.TIMESTAMP)
    private Date dateCreated;

    @Basic(optional = false)
    @Column(name = "confirmation_number", nullable = false)
    private int confirmationNumber;

    @ManyToMany
    @JoinTable(name = "ordered_product",
            joinColumns = {@JoinColumn(name = "customer_order_id", referencedColumnName = "id")},
            inverseJoinColumns = {@JoinColumn(name = "product_id", referencedColumnName = "id")})
    private Collection<Product> productCollection;

    @JoinColumn(name = "customer_id", referencedColumnName = "id", nullable = false)
    @ManyToOne(optional = false)
    private Customer customerId;

    public CustomerOrder() {
        this.productCollection = new java.util.ArrayList<>();
    }

    public Integer getId() {
        return this.id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public BigDecimal getAmount() {
        return this.amount;
    }

    public void setAmount(BigDecimal amount) {
        this.amount = amount;
    }

    public Date getDateCreated() {
        return this.dateCreated;
    }

    public void setDateCreated(Date dateCreated) {
        this.dateCreated = dateCreated;
    }

    public int getConfirmationNumber() {
        return this.confirmationNumber;
    }

    public void setConfirmationNumber(int confirmationNumber) {
        this.confirmationNumber = confirmationNumber;
    }

    public Collection<Product> getProductCollection() {
        return this.productCollection;
    }

    public void setProductCollection(Collection<Product> productCollection) {
        this.productCollection = productCollection;
    }

    public Customer getCustomerId() {
        return this.customerId;
    }

    public void setCustomerId(Customer customerId) {
        this.customerId = customerId;
    }

    @Override
    public int hashCode() {
        int hash = 0;
        hash += (id != null ? id.hashCode() : 0);
        return hash;
    }

    @Override
    public boolean equals(Object object) {
        if (!(object instanceof CustomerOrder))
            return false;

        CustomerOrder other = (CustomerOrder) object;
        return  this.id.equals(other.id) &&
                this.amount.equals(other.amount) &&
                this.dateCreated.equals(other.dateCreated) &&
                this.confirmationNumber == other.confirmationNumber;
    }

    @Override
    public String toString() {
        return "CustomerOrder{" +
                "id=" + this.id +
                ", amount=" + this.amount +
                ", dateCreated=" + this.dateCreated +
                ", confirmationNumber=" + this.confirmationNumber +
                ", productCollection=" + this.productCollection +
                '}';
    }
}
