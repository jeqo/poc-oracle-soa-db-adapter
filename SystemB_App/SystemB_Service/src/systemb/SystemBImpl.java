package systemb;

import com.bea.core.repackaged.springframework.transaction.annotation.Transactional;

import javax.ejb.Stateless;

import javax.ejb.TransactionAttribute;

import javax.ejb.TransactionAttributeType;

import javax.ejb.TransactionManagement;

import javax.ejb.TransactionManagementType;

import javax.inject.Inject;

import javax.jws.WebService;

import javax.persistence.EntityManager;
import javax.persistence.EntityManagerFactory;
import javax.persistence.Persistence;
import javax.persistence.PersistenceContext;

import org.example.Request;
import org.example.Response;

import pe.jeqo.SalesOrder;

@WebService(serviceName = "SystemB", targetNamespace = "urn:SystemB", portName = "SystemBPort",
            endpointInterface = "systemb.SystemB", wsdlLocation = "/WEB-INF/wsdl/SystemB.wsdl")
public class SystemBImpl {

    EntityManager em;

    public SystemBImpl() {
        em = Persistence.createEntityManagerFactory("SystemB_Service").createEntityManager();
    }

    public Response saveSalesOrder(Request request) {
        em.getTransaction().begin();
        SalesOrder salesOrder = new SalesOrder();
        salesOrder.setId(new Long(request.getId()));
        salesOrder.setClient(request.getClient());
        salesOrder.setPrice(request.getAmount().intValue());
        em.persist(salesOrder);
        em.getTransaction().commit();
        Response response = new Response();
        response.setResult("OK");
        return response;
    }
}
