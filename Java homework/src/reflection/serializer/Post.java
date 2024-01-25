package reflection.serializer;

public class Post {

    @Stored("post-title")
    private String title;

    @Stored
    private String text;
    private int replyCount;

    public Post() {
    }

    public Post(String title, String text, int replyCount) {
        this.title = title;
        this.text = text;
        this.replyCount = replyCount;
    }

    @Override
    public String toString() {
        return "Post{" +
                "title='" + title + '\'' +
                ", text='" + text + '\'' +
                ", replyCount=" + replyCount +
                '}';
    }
}
