package fp.sales;

import java.time.LocalDate;
import java.util.*;
import java.util.stream.Collectors;

public class Analyser {

    private Repository repository;

    public static void main(String[] args) {
        Repository repo = new Repository();
        Analyser analyser = new Analyser(repo);

        System.out.println(analyser.statesWithBiggestSales());
    }

    public Analyser(Repository repository) {
        this.repository = repository;
    }

    public Double getTotalSales() {
        Double sum = repository.getEntries().stream()
                .mapToDouble(each -> each.getAmount())
                .sum();

        return sum;
    }

    public Double getSalesByCategory(String category) {
        Double sum = repository.getEntries().stream()
                .filter(x -> x.getCategory().equals(category))
                .mapToDouble(each -> each.getAmount())
                .sum();

        return sum;
    }

    public Double getSalesBetween(LocalDate start, LocalDate end) {
        Double sum = repository.getEntries().stream()
                .filter(x -> x.getDate().isAfter(LocalDate.parse("2016-01-01")))
                .filter(x -> x.getDate().isBefore(LocalDate.parse("2016-03-31")))
                .mapToDouble(each -> each.getAmount())
                .sum();

        return sum;
    }

    public String mostExpensiveItems() {
        List<String> sorted = repository.getEntries().stream()
            .sorted(Collections.reverseOrder(
                    Comparator.comparing(each -> each.getAmount())))
            .map(x -> x.getProductId())
            .limit(3)
            .toList();

        return sorted.stream().sorted().collect(Collectors.joining(", "));
    }

    public String statesWithBiggestSales() {
        Map<String, Double> map = repository.getEntries().stream().collect(
                Collectors.toMap(
                        each -> each.getState(),
                        each -> each.getAmount(),
                        (a, b) -> a + b));

        List<String> result = map.entrySet().stream()
                .sorted(Map.Entry.comparingByValue(Comparator.reverseOrder()))
                .limit(3)
                .map(x -> x.getKey())
                .toList();

        return String.join(", ", result);
    }
}
