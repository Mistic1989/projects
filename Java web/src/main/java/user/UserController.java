package user;

import dao.UserDao;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
public class UserController {

    private UserDao dao;

    public UserController(UserDao dao) {
        this.dao = dao;
    }

    @GetMapping("/version")
    public String version() {
        return "version";
    }

    @GetMapping("/users")
    @PreAuthorize("hasRole('ADMIN')")
    public List<User> getAllUsers() {
        return dao.findUsers();
    }

    @GetMapping("/users/{username}")
    @PreAuthorize("hasRole('ADMIN') or #username == authentication.name")
    public User getUserByName(@PathVariable String username) {
        return dao.getUser(username);
    }

//    @GetMapping("/")
//    public String frontPage() {
//        return "Front page!";
//    }
//
//    @GetMapping("/count")
//    public String counter(HttpSession session) {
//
//        Object count = session.getAttribute("count");
//
//        count = count instanceof Integer i
//                ? i + 1
//                : 0;
//
//        session.setAttribute("count", count);
//
//        return String.valueOf(count);
//    }

//    @GetMapping("/info")
//    public String info(Principal principal) {
//        String user = principal != null ? principal.getName() : "";
//
//        return "Current user: " + user;
//    }

//    @GetMapping("/admin/info")
//    public String adminInfo(Principal principal) {
//        return "Admin user info: " + principal.getName();
//    }

//    @GetMapping("/users/{username}")
//    public User getUserByName(@PathVariable String username) {
//        return new UserDao().getUserByUserName(username);
//    }
}