package reflection.samples;

import java.lang.reflect.Field;

public class WriteField {

    public static void main(String[] args) throws Exception {

        Field field = MySampleClass.class.getDeclaredField("field1");

        MySampleClass instance = new MySampleClass();

        field.set(instance, "changed ...");

        System.out.println(instance.field1);
    }
}
