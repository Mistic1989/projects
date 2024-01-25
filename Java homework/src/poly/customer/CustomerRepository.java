package poly.customer;

import java.io.*;
import java.nio.file.Files;
import java.nio.file.Path;
import java.time.LocalDate;
import java.util.ArrayList;
import java.util.List;
import java.util.Objects;
import java.util.Optional;

public class CustomerRepository {

    public static void main(String[] args) throws IOException {
        CustomerRepository uus = new CustomerRepository();
        BonusCollector collector = new BonusCollector(new CustomerRepository());
        collector.gatherCustomerBonus("c1", new Order(10, LocalDate.parse("2023-03-28")));
        System.out.println(uus.getCustomerById("c1").get().getBonusPoints());

    }

    private static final String FILE_PATH = "src/poly/customer/data.txt";

    private List<AbstractCustomer> customers = new ArrayList<>();

    public Optional<AbstractCustomer> getCustomerById(String id) {

        List<String> lines;

        try {
            lines = Files.readAllLines(Path.of(FILE_PATH));
        } catch (IOException e) {
            throw new RuntimeException("Cannot read file path");
        }

        for (String line : lines) {

            String[] parts = line.split(";");
            if (parts[0].equals("REGULAR") && id.equals(parts[1])) {
                List<String> date = List.of(parts[4].split("-"));
                return Optional.of(new RegularCustomer(parts[1], parts[2], Integer.parseInt(parts[3]),
                        LocalDate.of(Integer.parseInt(date.get(0)), Integer.parseInt(date.get(1)),
                                     Integer.parseInt(date.get(2)))));
            }
            if (parts[0].equals("GOLD") && id.equals(parts[1])) {
                return Optional.of(new GoldCustomer(parts[1], parts[2], Integer.parseInt(parts[3])));
            }
        }

        return Optional.empty();
    }

    public void fromFiletoCustomersList(String path) {
        List<String> lines;

        try {
            lines = Files.readAllLines(Path.of(path));
        } catch (IOException e) {
            throw new RuntimeException("Cannot read file path");
        }

        for (String line : lines) {

            String[] parts = line.split(";");
            if (parts[0].equals("REGULAR")) {
                List<String> date = List.of(parts[4].split("-"));
                customers.add(new RegularCustomer(parts[1], parts[2], Integer.parseInt(parts[3]),
                        LocalDate.of(Integer.parseInt(date.get(0)), Integer.parseInt(date.get(1)),
                                Integer.parseInt(date.get(2)))));
            }
            if (parts[0].equals("GOLD")) {
                customers.add(new GoldCustomer(parts[1], parts[2], Integer.parseInt(parts[3])));
            }
        }
    }

    public void remove(String id) {
        List<String> lines;

        try {
            lines = Files.readAllLines(Path.of(FILE_PATH));
        } catch (IOException e) {
            throw new RuntimeException("Cannot read file path");
        }

        for (String line : lines) {
            String[] parts = line.split(";");

            if (parts.length > 1 && !id.equals(parts[1])) {
                Optional<AbstractCustomer> customer = getCustomerById(parts[1]);
                customers.add(customer.get());
            }
        }
        try {
            FileWriter writer = new FileWriter(FILE_PATH);
            writer.write("");
            writer.close();
        } catch (IOException e) {
            throw new RuntimeException(e);
        }

        List<AbstractCustomer> customersCopy = new ArrayList<>(customers);

        for (AbstractCustomer customer : customersCopy) {
            save(customer);
        }
    }

    public void save(AbstractCustomer customer) {
        fromFiletoCustomersList(FILE_PATH);
        Optional<AbstractCustomer> customerInRepo = getCustomerById(customer.getId());

        if (customerInRepo.isEmpty()) {
            writeToFile(customer);

            if (!customers.contains(customer)) {
                customers.add(customer);
            }

        } else {
            for (AbstractCustomer abstractCustomer : customers) {
               if (abstractCustomer.getId().equals(customer.getId())) {
                    abstractCustomer.bonusPoints = customer.getBonusPoints();
                    break;
                }
            }
            try {
                FileWriter writer = new FileWriter(FILE_PATH);
                writer.write("");
                writer.close();
            } catch (IOException e) {
                throw new RuntimeException(e);
            }
            for (AbstractCustomer abstractCustomer : customers) {
                writeToFile(abstractCustomer);
            }
        }
    }

    private static void writeToFile(AbstractCustomer customer) {

        try {
            FileWriter writer = new FileWriter(FILE_PATH, true);
            writer.write(
                    customer.getCustomerType() + ";" +
                            customer.getId() + ";" +
                            customer.getName() + ";" +
                            customer.getBonusPoints() + ";");

            if (Objects.equals(customer.getCustomerType(), "REGULAR")) {
                writer.write(customer.getLastOrderDate().toString());
            }
            writer.write("\n");
            writer.close();
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }

    public int getCustomerCount() {
        return customers.size();
    }
}
