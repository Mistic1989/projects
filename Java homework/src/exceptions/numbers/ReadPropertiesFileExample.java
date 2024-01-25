package exceptions.numbers;

import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.util.Properties;

public class ReadPropertiesFileExample {

    public static void main(String[] args) {
        String filePath = "src/exceptions/numbers/numbers_et.properties";

        Properties properties = new Properties();
        FileInputStream is = null;

        try {
            is = new FileInputStream(filePath);

            InputStreamReader reader = new InputStreamReader(
                    is, StandardCharsets.UTF_8);

            properties.load(reader);
        } catch (Exception e) {
            // handle exceptions
        } finally {
            close(is);
        }

        System.out.println(properties.containsKey(String.valueOf(1)));
        System.out.println(properties.getProperty(String.valueOf(10)));

    }

    private static void close(FileInputStream is) {
        if (is == null) {
            return;
        }

        try {
            is.close();
        } catch (IOException ignore) {}
    }

}
