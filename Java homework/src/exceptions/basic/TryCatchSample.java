package exceptions.basic;

public class TryCatchSample {
    public static void main(String[]args){
        Resource resource = new Resource().setData("stuff");
        String data = new TryCatchSample().readDataFrom(resource);
        System.out.println(data);
    }

    public String readDataFrom(Resource resource) {
        try {
            resource.open();
            return resource.read();
        }
        catch (Exception e) {
            return "someDefaultValue";
        }
        finally {
            resource.close();
        }
    }
}
