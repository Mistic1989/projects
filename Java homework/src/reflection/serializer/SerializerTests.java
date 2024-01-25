package reflection.serializer;

import org.junit.Test;

import static org.hamcrest.CoreMatchers.is;
import static org.junit.Assert.assertThat;

public class SerializerTests {

    @Test
    public void serializesAndDeserializesObjects() {

        Customer customer = new Customer("Alice", "Smith");

        String asString = new Serializer().serialize(customer);

        assertThat(asString, is("firstName:Alice|lastName:Smith"));

        Customer restored = new Serializer()
                .deserialize(asString, Customer.class);

        assertThat(restored.getFirstName(), is(customer.getFirstName()));
        assertThat(restored.getLastName(), is(customer.getLastName()));
    }

    @Test
    public void canHandleConflictingSymbols() {
        Customer customer = new Customer("Alice%25", "Sm|th:");

        String asString = new Serializer().serialize(customer);

        assertThat(asString, is("firstName:Alice%2525|lastName:Sm%7cth%3a"));

        Customer restored = new Serializer()
                .deserialize(asString, Customer.class);

        assertThat(restored.getFirstName(), is(customer.getFirstName()));
        assertThat(restored.getLastName(), is(customer.getLastName()));
    }
}