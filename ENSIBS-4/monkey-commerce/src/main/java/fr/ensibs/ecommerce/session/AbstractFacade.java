package fr.ensibs.ecommerce.session;

import jakarta.ejb.Stateless;
import jakarta.persistence.EntityManager;
import jakarta.persistence.PersistenceContext;
import jakarta.persistence.criteria.CriteriaQuery;

import java.util.List;

/**
 * @param <T> the type of the entity
 */
@Stateless
public abstract class AbstractFacade<T> implements Facade<T> {

    @PersistenceContext(unitName = "ecommercePersistenceUnit")
    private EntityManager entityManager;

    private final Class<T> entityClass;

    public AbstractFacade(Class<T> entityClass) {
        this.entityClass = entityClass;
    }

    /**
     * Create a new entity in the database
     * @param entity the entity to create
     */
    public void create(T entity) {
        this.entityManager.persist(entity);
    }

    /**
     * Update an entity in the database
     * @param entity the entity to update
     */
    public void edit(T entity) {
        this.entityManager.merge(entity);
    }

    /**
     * Remove an entity from the database
     * @param entity the entity to remove
     */
    public void remove(T entity) {
        this.entityManager.remove(this.entityManager.merge(entity));
    }

    /**
     * Find an entity by its primary key
     * @param id the primary key
     * @return the entity
     */
    public T find(Object id) {
        return this.entityManager.find(this.entityClass, id);
    }

    /**
     * Find all entities
     * @return the list of entities
     */
    public List<T> findAll() {
        CriteriaQuery<T> cq = this.entityManager.getCriteriaBuilder().createQuery(this.entityClass);
        cq.select(cq.from(this.entityClass));
        return this.entityManager.createQuery(cq).getResultList();
    }
}
