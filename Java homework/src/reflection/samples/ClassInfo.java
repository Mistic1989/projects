package reflection.samples;

public class ClassInfo {

    public static void main(String[] args) {

        Class<MySampleClass> clazz = MySampleClass.class;

        // Why Class has type argument
        MySampleClass casted = clazz.cast(null);

        System.out.println(clazz.getName());
        System.out.println(clazz.getSimpleName());
        System.out.println(clazz.getPackageName());


    }

}
