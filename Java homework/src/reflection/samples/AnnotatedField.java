package reflection.samples;

import java.lang.reflect.Field;

public class AnnotatedField {

    @MyAnnotation("note for field 1")
    private String field1;

    @MyAnnotation("note for field 2")
    private String field2;

    public static void main(String[] args) {

        Field[] fields = AnnotatedField.class.getDeclaredFields();

        for (Field field : fields) {

            MyAnnotation annotation = field.getAnnotation(MyAnnotation.class);

            String text = String.format("'%s' has note '%s'",
                                field.getName(), annotation.value());

            System.out.println(text);
        }

    }
}
