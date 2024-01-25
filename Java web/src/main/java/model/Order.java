package model;

import jakarta.persistence.*;
import jakarta.validation.Valid;
import lombok.*;

import java.util.ArrayList;
import java.util.List;


@Data
@AllArgsConstructor
@NoArgsConstructor
@EqualsAndHashCode(callSuper = false)
@RequiredArgsConstructor
@Entity
@Table(name = "orders")
public class Order extends BaseEntity {

    @NonNull
    @Column(name = "order_number")
    private String orderNumber;

    @Valid
    @ElementCollection(fetch = FetchType.EAGER)
    @CollectionTable(
            name = "order_rows",
            joinColumns=@JoinColumn(name = "orders_id",
                    referencedColumnName = "id")
    )
    private List<OrderRow> orderRows = new ArrayList<>();

}
