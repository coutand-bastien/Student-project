package fr.ensibs.ecommerce.session;

import jakarta.ejb.Local;

import java.util.List;

@Local
public interface Facade<T> {
    
    void create(T entity);
    
    void edit(T entity);
    
    void remove(T entity);

    T find(T id);
    
    List<T> findAll();
}
