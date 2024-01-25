package user;

import jakarta.persistence.*;
import lombok.*;

import java.util.ArrayList;
import java.util.List;

@Data
@NoArgsConstructor
@EqualsAndHashCode(callSuper = false)
@AllArgsConstructor
@Entity
@Table(name = "users")
public class User {

    @Id
    @NonNull
    @Column(name = "username")
    private String username;

    @NonNull
    @Column(name = "password")
    private String password;

    @NonNull
    @Column(name = "enabled")
    private Boolean enabled;

    @NonNull
    @Column(name = "first_name")
    private String firstname;

    @NonNull
    @ElementCollection(fetch = FetchType.EAGER)
    @CollectionTable(
            name = "authorities",
            joinColumns = @JoinColumn(name = "username", referencedColumnName = "username")
    )
    private List<Authority> authorities = new ArrayList<>();

}
