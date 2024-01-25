package reflection.samples;

public class ClassFromInstance {

    public static void main(String[] args) {

        MySampleClass instance = new MySampleClass();

        Class<? extends MySampleClass> clazz = instance.getClass();

        System.out.println(clazz == MySampleClass.class);

        System.out.println(clazz.getName());
        System.out.println(clazz.getSimpleName());
        System.out.println(clazz.getPackageName());
    }

}
