package reflection.samples;

import java.lang.reflect.Method;

public class LoadClassAndInvokeMethod {

    public static void main(String[] args) throws Exception {

        Class<?> clazz = Class.forName("samples.MySampleClass2");

        Method method = clazz.getDeclaredMethod("hello");

        Object instance = clazz.getDeclaredConstructor().newInstance();

        method.invoke(instance);
    }

}
