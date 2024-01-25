package reflection.samples;

import java.lang.reflect.Method;

public class AnnotatedMethod {

    @MyAnnotation
    public static void main(String[] args) {

        Method[] methods = AnnotatedMethod.class.getMethods();

        for (Method method : methods) {
            if (method.getAnnotation(MyAnnotation.class) == null) {
                continue;
            }

            System.out.println(method.getName());
        }
    }
}
