package inheritance.analyser;

import java.util.List;
import java.util.Objects;

public sealed abstract class AbstractSalesAnalyser permits DifferentiatedTaxSalesAnalyser,
                FlatTaxSalesAnalyser, TaxFreeSalesAnalyser {
    protected final List<SalesRecord> records;

    protected AbstractSalesAnalyser(List<SalesRecord> records) {
        this.records = records;
    }
    protected abstract Double getTaxRate();

    protected abstract String getClassName();


    protected final String getIdOfMostPopularItem() {
        String resultId = "";
        Integer resultSold = 0;

        for (SalesRecord record : records) {

            String id = record.getProductId();
            Integer sold = 0;
            for (SalesRecord salesRecord : records) {
                if (Objects.equals(salesRecord.getProductId(), id)) {
                    sold += salesRecord.getItemsSold();
                }
            }
            if (sold > resultSold) {
                resultSold = sold;
                resultId = id;
            }
        }

        return resultId;
    }

    protected final String getIdOfItemWithLargestTotalSales() {
        String resultId = "";
        Integer finalCount = 0;

        for (SalesRecord record : records) {

            String id = record.getProductId();
            Integer count = 0;
            for (SalesRecord salesRecord : records) {
                if (Objects.equals(salesRecord.getProductId(), id)) {
                    count++;
                }
            }
            if (count > finalCount) {
                finalCount = count;
                resultId = id;
            }
        }

        return resultId;
    }

    protected final Double getTotalSales() {
        Double result = 0.0;
        for (SalesRecord record : records) {
            if (record.hasReducedRate() && getClassName().equals("DifferentiatedTaxSalesAnalyser")) {
                result += (record.getProductPrice() * record.getItemsSold()) / 1.1;
                continue;
            }
            result += (record.getProductPrice() * record.getItemsSold()) / (1 + getTaxRate());
        }
        return result;
    }

    protected final Double getTotalSalesByProductId(String id) {
        Double result = 0.0;
        for (SalesRecord record : records) {
            if (Objects.equals(record.getProductId(), id)) {
                if (record.hasReducedRate() && getClassName().equals("DifferentiatedTaxSalesAnalyser")) {
                    result += (record.getProductPrice() * record.getItemsSold()) / 1.1;
                    continue;
                }
                result += (record.getProductPrice() * record.getItemsSold()) / (1 + getTaxRate());
            }
        }
        return result;
    }
}
