package inheritance.pager;

import java.util.Arrays;
import java.util.List;

public class FilteringPager {

    public static void main(String[] args) {
        List<Integer> data = Arrays.asList(
                1, null, null, 2,
                null, 3, 4);

        SimplePager simplePager = new SimplePager(data, 4);
        FilteringPager pager = new FilteringPager(simplePager, 2);

        System.out.println(pager.getNextPage());
    }

    @SuppressWarnings("PMD.UnusedPrivateField")
    private final SimplePager dataSource;
    @SuppressWarnings("PMD.UnusedPrivateField")
    private final int pageSize;

    public FilteringPager(SimplePager dataSource, int pageSize) {
        this.dataSource = dataSource;
        this.pageSize = pageSize;
    }

    public List<Integer> getNextPage() {
        throw new RuntimeException("not implemented yet");
    }

    public List<Integer> getCurrentPage() {
        throw new RuntimeException("not implemented yet");
    }

    public List<Integer> getPreviousPage() {
        throw new RuntimeException("not implemented yet");
    }
}