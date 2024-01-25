package exceptions.numbers;


import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.util.Properties;


public class NumberConverter {

    String lang;
    Properties readProperties;

    public static void main(String[] args) {
        NumberConverter converter = new NumberConverter("en");
        System.out.println(converter.numberInWords(989));
    }

    public NumberConverter(String lang) {
        this.lang = lang;
        this.readProperties = readProperties(this.lang);
    }

    public Properties readProperties(String lang) {
        String filePath = String.format("src/exceptions/numbers/numbers_%s.properties", lang);
        Properties properties = new Properties();
        FileInputStream is = null;

        try {
            is = new FileInputStream(filePath);

            InputStreamReader reader = new InputStreamReader(
                    is, StandardCharsets.UTF_8);

            properties.load(reader);
        } catch (IOException e) {
            throw new MissingLanguageFileException(lang, new FileNotFoundException());
        } catch (IllegalArgumentException e) {
            throw new BrokenLanguageFileException(lang, new FileNotFoundException());
        }
        finally {
            close(is);
        }

        return properties;
    }

    public String handleTeens(int tens, int ones, Properties readProperties, String teensStr) {
        if (tens == 1) {
            if (readProperties.containsKey(String.valueOf(tens * 10 + ones))) {
                teensStr = readProperties.getProperty(String.valueOf(tens * 10 + ones));
            } else {
                teensStr = readProperties.getProperty(String.valueOf(ones)) + readProperties.getProperty("teen");
            }
        }

        return teensStr;
    }

    public String handleHundreds(int hundred, int ones, Properties readProperties,
                                 String hundredStr, String tensStr, String teensStr) {
        if (hundred > 0) {
            hundredStr += readProperties.getProperty(String.valueOf(hundred)) +
                    readProperties.getProperty("hundreds-before-delimiter") +
                    readProperties.getProperty("hundred");
            if (ones != 0 && tensStr.length() == 0 && teensStr.length() == 0) {
                hundredStr += readProperties.getProperty("hundreds-after-delimiter") +
                        readProperties.getProperty(String.valueOf(ones));
            }
            if (tensStr.length() > 0) {
                hundredStr += readProperties.getProperty("hundreds-after-delimiter") +
                        tensStr;
            }
            if (teensStr.length() > 0) {
                hundredStr += readProperties.getProperty("hundreds-after-delimiter") +
                        teensStr;
            }
        }

        return hundredStr;
    }

    public String handleTens(int tens, int ones, Properties readProperties, String tensStr) {

        if (tens > 1 && tens < 10 && !readProperties.containsKey(String.valueOf(tens * 10))) {
            tensStr = readProperties.getProperty(String.valueOf(tens)) +
                    readProperties.getProperty("tens-suffix");
            if (ones != 0) {
                tensStr += readProperties.getProperty("tens-after-delimiter") +
                        readProperties.getProperty(String.valueOf(ones));
            }
        }
        if (tens > 1 && tens < 10 && readProperties.containsKey(String.valueOf(tens * 10))) {
            tensStr = readProperties.getProperty(String.valueOf(tens * 10));
            if (ones != 0) {
                tensStr += readProperties.getProperty("tens-after-delimiter") +
                        readProperties.getProperty(String.valueOf(ones));
            }
        }

        return tensStr;
    }

    public String numberInWords(Integer number) {

        if (number == null) {
            return "null";
        }
        Properties readProperties = readProperties(this.lang);

        if (readProperties.containsKey(String.valueOf(number))) {
            return readProperties.getProperty(String.valueOf(number));
        }

        int ones = number % 10;
        int tens = number / 10;
        int hundred = number / 100;
        // If number is above 99, make recalculations for tens
        if (number > 99) {
            tens = (number - (number / 100) * 100) / 10;
        }
        String tensStr = "";
        String teensStr = "";
        String hundredStr = "";

        // Handle numbers between 10-19 (teen)
        teensStr = handleTeens(tens, ones, readProperties, teensStr);

        // Handle numbers between 20-99 (tens)
        tensStr = handleTens(tens, ones, readProperties, tensStr);

        // Handle numbers above 99 (hundred)
        hundredStr = handleHundreds(hundred, ones, readProperties, hundredStr, tensStr, teensStr);

        if (hundredStr.length() > 0) {
            return hundredStr;
        }

        if (tensStr.length() == 0 && teensStr.length() == 0) {
            throw new MissingTranslationException(String.valueOf(number));
        }

        return tensStr + teensStr;
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
