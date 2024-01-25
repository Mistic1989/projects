package fp;

import org.junit.Test;

import java.util.Collections;
import java.util.Comparator;
import java.util.List;
import java.util.stream.Collectors;


public class Persons {

    private List<Person> persons = List.of(
            new Person(1, "Alice", 22),
            new Person(2, "Bob", 20),
            new Person(3, "Carol", 21));

    @Test
    public void findsPersonById() {
        List<Person> result = persons.stream()
                .filter(p -> p.getId().equals(2))
                .collect(Collectors.toList());

        System.out.println(result);
    }
    @Test
    public void removePersonById() {
        List<Person> result = persons.stream()
                .filter(p -> !p.getId().equals(2))
                .collect(Collectors.toList());

        System.out.println(result);
    }

    @Test
    public void findsPersonNames() {
        String result = persons.stream()
                .map(p -> p.getName())
                .collect(Collectors.joining(", "));

        System.out.println(result);
    }

    @Test
    public void reverseSortedByAge() {
        List<Person> result = persons.stream()
                .sorted(Collections.reverseOrder(
                        Comparator.comparing(each -> each.getAge())))
                .collect(Collectors.toList());

        System.out.println(result);
    }
}
