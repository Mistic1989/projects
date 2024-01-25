package junit.sales;

import static org.hamcrest.Matchers.arrayContainingInAnyOrder;

public class TopSalesFinder {

    public static void main(String[] args) {
        TopSalesFinder tsf = new TopSalesFinder();
        tsf.registerSale(new SalesRecord("p1", 20, 1));
        tsf.registerSale(new SalesRecord("p2", 20, 1));
        tsf.registerSale(new SalesRecord("p2", 20, 1));
        tsf.registerSale(new SalesRecord("p1", 10, 1));
        tsf.registerSale(new SalesRecord("p3", 50, 1));

        tsf.findItemsSoldOver(100);
        System.out.println(arrayContainingInAnyOrder(tsf.findItemsSoldOver(100)));
    }

    private SalesRecord[] salesRecordsArray;

    public TopSalesFinder() {
        this.salesRecordsArray = new SalesRecord[100];
    }

    @Override
    public boolean equals(Object obj) {

        if (!(obj instanceof SalesRecord)) {
            return false;
        }

        SalesRecord other = (SalesRecord) obj;

        for (SalesRecord each : this.salesRecordsArray) {
            if (each.getProductId().equals(other.getProductId())) {
                return true;
            }
        }
        return false;
    }

    public int count(SalesRecord record) {
        int result = 0;
        for (SalesRecord salesRecord : salesRecordsArray) {
            if (salesRecord != null && salesRecord.getProductId().equals(record.getProductId())) {
                result += salesRecord.getItemsSold() * salesRecord.getProductPrice();
            }
        }

        return result;
    }

    public boolean contains(String[] result, String item) {
        for (String productId : result) {
            if (item.equals(productId)) {
                return true;
            }
        }
        return false;
    }

    public void registerSale(SalesRecord record) {
        for (int i = 0; i < salesRecordsArray.length; i++) {
            if (salesRecordsArray[i] == null ) {
                salesRecordsArray[i] = record;
                break;
            }
        }
    }

    public String[] findItemsSoldOver(int amount) {
        int countItems = 0;
        String[] result = new String[100];
        for (SalesRecord record : salesRecordsArray) {
            if (record != null) {
                int soldCount = record.getItemsSold() * record.getProductPrice();
                if (count(record) > soldCount) {
                    soldCount = count(record);
                }
                for (int j = 0; j < result.length; j++) {
                    if (soldCount > amount && result[j] == null && !contains(result, record.getProductId())) {
                        countItems++;
                        result[j] = record.getProductId();
                        break;
                    }
                }
            }
        }

        String[] result2 = new String[countItems];
        for (int i = 0; i < result2.length; i++) {
            if (!contains(result2, result[i])) {
                result2[i] = result[i];
            }
        }

        return result2;
    }
}
