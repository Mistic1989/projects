package reflection.samples;

import java.lang.reflect.Field;

public class Fields {

    public static void main(String[] args) {

        Field[] fields = MySampleClass.class.getDeclaredFields();

        for (Field field : fields) {
            System.out.printf("%s %s\n",
                    field.getType(), field.getName());
        }

    }
}
