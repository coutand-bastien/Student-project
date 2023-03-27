package fr.ensibs.ecommerce.entity;

import java.io.Serializable;
import java.util.Collection;
import jakarta.persistence.*;

@Entity
@Table(name = "customer")
public class Customer implements Serializable {

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
    @Column(name = "email", nullable = false, length = 45)
    private String email;

    @Basic(optional = false)
    @Column(name = "phone", nullable = false, length = 45)
    private String phone;

    @Basic(optional = false)
    @Column(name = "address", nullable = false, length = 45)
    private String address;

    @Basic(optional = false)
    @Column(name = "city_region", nullable = false, length = 2)
    private String cityRegion;

    @Basic(optional = false)
    @Column(name = "cc_number", nullable = false, length = 19)
    private String creditCardNumber;

    @OneToMany(cascade = CascadeType.ALL, mappedBy = "customerId")
    private Collection<CustomerOrder> customerOrderCollection;

    public Customer() {}

    public Customer(String name, String email, String phone, String address, String cityRegion, String creditCardNumber) {
        this.name = name;
        this.email = email;
        this.phone = phone;
        this.address = address;
        this.cityRegion = cityRegion;
        this.creditCardNumber = creditCardNumber;
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

    public String getEmail() {
        return this.email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public String getPhone() {
        return this.phone;
    }

    public void setPhone(String phone) {
        this.phone = phone;
    }

    public String getAddress() {
        return this.address;
    }

    public void setAddress(String address) {
        this.address = address;
    }

    public String getCityRegion() {
        return this.cityRegion;
    }

    public void setCityRegion(String cityRegion) {
        this.cityRegion = cityRegion;
    }

    public String getCreditCardNumber() {
        return this.creditCardNumber;
    }

    public void setCreditCardNumber(String ccNumber) {
        this.creditCardNumber = ccNumber;
    }

    @Override
    public int hashCode() {
        int hash = 0;
        hash += (id != null ? id.hashCode() : 0);
        return hash;
    }

    @Override
    public boolean equals(Object object) {
        if (!(object instanceof Customer))
            return false;

        Customer other = (Customer) object;
        return  this.id.equals(other.id) &&
                this.name.equals(other.name) &&
                this.email.equals(other.email) &&
                this.phone.equals(other.phone) &&
                this.address.equals(other.address) &&
                this.cityRegion.equals(other.cityRegion) &&
                this.creditCardNumber.equals(other.creditCardNumber);
    }

    @Override
    public String toString() {
        return "Customer{" +
                "id=" + this.id +
                ", name='" + this.name + '\'' +
                ", email='" + this.email + '\'' +
                ", phone='" + this.phone + '\'' +
                ", address='" + this.address + '\'' +
                ", cityRegion='" + this.cityRegion + '\'' +
                ", ccNumber='" + this.creditCardNumber + '\'' +
                ", customerOrderCollection=" + this.customerOrderCollection +
                '}';
    }
}
