package reflection.samples;

import java.lang.reflect.Field;

public class ReadField {

    public static void main(String[] args) throws Exception {

        Field field = MySampleClass.class.getDeclaredField("field1");

        MySampleClass instance = new MySampleClass();

        Object value = field.get(instance);

        System.out.println(value);

    }
}
