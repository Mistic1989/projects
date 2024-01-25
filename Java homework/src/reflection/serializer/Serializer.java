package reflection.serializer;

import java.lang.reflect.Field;
import java.util.ArrayList;
import java.util.List;

public class Serializer {

    public String serialize(Object instance) {
        Field[] fields = instance.getClass().getDeclaredFields();

        List<String> pairs = new ArrayList<>();
        for (Field field : fields) {

            Stored annotation = field.getAnnotation(Stored.class);
            if (annotation == null) {
                continue;
            }

            String fieldName = "".equals(annotation.value()) ? field.getName() : annotation.value();

            String pair = fieldName
                    + ":"
                    + encode(String.valueOf(getFieldValue(instance, field)));

            pairs.add(pair);
        }

        return String.join("|", pairs);
    }

    private String encode(String input) {
        return input.replaceAll("%", "%25")
                    .replaceAll(":", "%3a")
                    .replaceAll("\\|", "%7c");
    }

    private String decode(String input) {
        return input.replaceAll("%25", "%")
                .replaceAll("%3a", ":")
                .replaceAll("%7c", "|");
    }

    private Object getFieldValue(Object instance, Field field) {
        try {
            field.setAccessible(true);

            return field.get(instance);

        } catch (IllegalAccessException e) {
            throw new RuntimeException(e);
        }
    }

    private void setFieldValue(Field field, Object instance, Object value) {
        try {
            field.setAccessible(true);

            field.set(instance, value);

        } catch (IllegalAccessException e) {
            throw new RuntimeException(e);
        }
    }

    public <T> T deserialize(String inputString,
                            Class<T> clazz) {

        T instance;

        try {
            instance = clazz.getDeclaredConstructor().newInstance();
        } catch (Exception e) {
            throw new RuntimeException(e);
        }

        Field[] fields = clazz.getDeclaredFields();

        for (Field field : fields) {

            Stored annotation = field.getAnnotation(Stored.class);
            if (annotation == null) {
                continue;
            }

            String fieldName = "".equals(annotation.value()) ? field.getName() : annotation.value();

            String value = decode(getFieldValue(inputString, fieldName));

            if (field.getType() == int.class) {
                setFieldValue(field, instance, Integer.parseInt(value));
            } else {
                setFieldValue(field, instance, value);
            }

        }

        return instance;
    }

    private String getFieldValue(String inputString, String fieldName) {
        for (String pair : inputString.split("\\|")) {
            String[] keyAndValue = pair.split(":");
            if (keyAndValue[0].equals(fieldName)) {
                return keyAndValue[1];
            }
        }
        throw new RuntimeException("no such field" + fieldName);
    }

}
