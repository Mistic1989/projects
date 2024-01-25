package fp.sales;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.util.List;
import java.util.stream.Collectors;

public class Repository {
    public static void main(String[] args) throws IOException {
       Repository repository = new Repository();
       List<Entry> entries = repository.getEntries();
       for (Entry entry : entries) {
            System.out.println(entry.getDate());
       }
    }
    private static final String FILE_PATH = "src/fp/sales/sales-data.csv";

    private DateTimeFormatter formatter = DateTimeFormatter
            .ofPattern("dd.MM.yyyy");

    public List<Entry> getEntries() {

        try {
            List<String> lines = Files.readAllLines(Paths.get(FILE_PATH));

            return lines.stream()
                    .skip(1)
                    .map(x -> x.split("\t"))
                    .map(x -> new Entry(x[2], LocalDate.parse(x[0], formatter), x[1], x[3], Double.valueOf(x[5].replace(",", "."))))
                    .collect(Collectors.toList());
        } catch (IOException e) {
            throw new RuntimeException(e);
        }

// Another way for solution

//        lines = lines.stream().skip(1).collect(Collectors.toList());
//        List<Entry> result = lines.stream().map(line -> {
//                    String[] split = line.split("\t");
//                    Entry entry = new Entry();
//                    entry.setProductId(split[2]);
//                    entry.setDate(LocalDate.parse(split[0], formatter));
//                    entry.setState(split[1]);
//                    entry.setCategory(split[3]);
//                    entry.setAmount(Double.valueOf(split[5].replace(",", ".")));
//                    return entry;
//                }).collect(Collectors.toList());

    }
}