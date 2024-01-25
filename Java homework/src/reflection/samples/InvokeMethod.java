package reflection.samples;

import java.lang.reflect.Method;

public class InvokeMethod {

    public static void main(String[] args) throws Exception {

        Method method = MySampleClass2.class.getDeclaredMethod("hello");

        MySampleClass2 instance = new MySampleClass2();

        method.invoke(instance);
    }

}
