package pe.jeqo;

import java.io.Serializable;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.Id;
import javax.persistence.NamedQueries;
import javax.persistence.NamedQuery;
import javax.persistence.Table;

@Entity
@NamedQueries({ @NamedQuery(name = "SalesOrder.findAll", query = "select o from SalesOrder o") })
@Table(name = "SALES_ORDER")
public class SalesOrder implements Serializable {
    private static final long serialVersionUID = 337169025416994750L;
    @Column(nullable = false, length = 100)
    private String client;
    @Id
    @Column(nullable = false)
    private Long id;
    @Column(nullable = false)
    private Integer price;

    public SalesOrder() {
    }

    public SalesOrder(String client, Long id, Integer price) {
        this.client = client;
        this.id = id;
        this.price = price;
    }

    public String getClient() {
        return client;
    }

    public void setClient(String client) {
        this.client = client;
    }

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public Integer getPrice() {
        return price;
    }

    public void setPrice(Integer price) {
        this.price = price;
    }
}
