package reflection.tester;

import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.util.List;

public class TestRunner {

    String result;

    public void runTests(List<String> testClassNames) {

        for (String className : testClassNames) {

            Class<?> aClass = getClassName(className);
            Object instance = getInstance(aClass);

            for (Method method : aClass.getDeclaredMethods()) {
                if (method.getAnnotation(MyTest.class) == null) {
                    continue;
                }

                MyTest annotation = method.getAnnotation(MyTest.class);

                invokeMethod(instance, method, annotation);
            }
        }
    }

    private void invokeMethod(Object instance, Method method, MyTest annotation) {
        try {
            method.invoke(instance);
            if (annotation.expected() != MyTest.None.class) {
                result += method.getName() + "() - FAILED ";
            }
        } catch (Exception e) {
            if (!annotation.expected().isAssignableFrom(e.getCause().getClass())) {
                result += method.getName() + "() - FAILED ";
            }
        }
        result += method.getName() + "() - OK ";
    }

    private Object getInstance(Class<?> aClass) {
        try {
            return aClass.getDeclaredConstructor().newInstance();
        } catch (InstantiationException |
                 IllegalAccessException |
                 InvocationTargetException |
                 NoSuchMethodException e) {
            throw new RuntimeException(e);
        }
    }

    private Class<?> getClassName(String className) {
        try {
            return Class.forName(className);
        } catch (ClassNotFoundException e) {
            throw new RuntimeException(e);
        }
    }

    public String getResult() {
        return result;
    }
}
