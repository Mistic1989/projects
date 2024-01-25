package config.security;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;

@Data
public class LoginCredentials {

//    @JsonProperty("userName")
    private String userName;
    private String password;

}
