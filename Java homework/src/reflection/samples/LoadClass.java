package reflection.samples;

import java.lang.reflect.Method;

public class LoadClass {

    public static void main(String[] args) throws Exception {

        Class<?> clazz = Class.forName("samples.MySampleClass2");

        // .class file should be on classpath
        // java -cp ./my-class-path ...

        for (Method method : clazz.getDeclaredMethods()) {
            System.out.println(method.getName());
        }
    }
}
