package reflection.samples;

import java.lang.reflect.Field;

public class ReadPrivateField {

    public static void main(String[] args) throws Exception {

        Field field = MySampleClass.class.getDeclaredField("field2");

        field.setAccessible(true);

        MySampleClass instance = new MySampleClass();

        Object value = field.get(instance);

        System.out.println(value);

    }
}
