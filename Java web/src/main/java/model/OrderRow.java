package model;

import jakarta.persistence.*;
import jakarta.validation.constraints.Min;
import lombok.*;
import org.jetbrains.annotations.NotNull;

@Data
@AllArgsConstructor
@NoArgsConstructor
@Builder
@Embeddable
public class OrderRow {

    @NonNull
    @Column(name = "item_name")
    private String itemName;

    @NotNull
    @Min(1)
    private Integer price;

    @NotNull
    @Min(1)
    private Integer quantity;
}
