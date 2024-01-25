package reflection.serializer;

public class Main {

//    public static void main(String[] args) {
//        String key = "key";
//        String value = "a:a%1";
//
////        Integer.toHexString('%');
////        Integer.toHexString('|');
////        Integer.toHexString(':');
//
//        value = value.replaceAll("%", "%25");
//        value = value.replaceAll(":", "%3a");
//        value = value.replaceAll("\\|", "%7c");
//
//        String combo = key + ":" + value;
//
//        String value1 = combo.split(":")[1];
//
//        value1 = value1.replaceAll("%3a", ":");
//        value1 = value1.replaceAll("%7c", "|");
//        value1 = value1.replaceAll("%25", "%");
//    }

    public static void main(String[] args) {
        Post post = new Post("Post : 1", "Post :%: text", 3);

        System.out.println(post);

        String postAsString = new Serializer().serialize(post);

        System.out.println(postAsString);

        Post restored = new Serializer()
                .deserialize(postAsString, Post.class);

        System.out.println(restored);
    }
}
