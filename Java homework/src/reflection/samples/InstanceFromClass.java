package reflection.samples;

public class InstanceFromClass {

    public static void main(String[] args) throws Exception {

        Class<MySampleClass2> clazz = MySampleClass2.class;

        MySampleClass2 instance = clazz.getDeclaredConstructor().newInstance();

        instance.hello();
    }

}
