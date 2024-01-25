using ConsoleApp;
using Microsoft.AspNetCore.Mvc.RazorPages;
using DAL;
using Microsoft.EntityFrameworkCore;
using UnoEngine;

namespace WebApp.Pages.Menu;

public class NewGame : PageModel
{
    private readonly AppDbContext _context;

    private IGameRepository _gameRepository;
    public GameEngine Engine { get; set; } = new();
    
    public NewGame(AppDbContext context)
    {
        _context = context;
        
        // _gameRepository = new GameRepositoryEF(_context);
        
        bool useFileSystem = false;

        if (useFileSystem)
        {
            _gameRepository = new GameRepositoryFileSystem(Engine.State);
        }
        else
        {
            _gameRepository = new GameRepositoryEF(_context);
        }
    }
    
    public void OnGet()
    {
        var connectionString = "DataSource=<%temppath%>uno.db;Cache=Shared";
        connectionString = connectionString.Replace("<%temppath%>", Path.GetTempPath());

        var contextOptions = new DbContextOptionsBuilder<AppDbContext>()
            .UseSqlite(connectionString)
            .EnableDetailedErrors()
            .EnableSensitiveDataLogging()
            .Options;
        using var db = new AppDbContext(contextOptions);
        // apply all the migrations
        db.Database.Migrate();

        var engine = new GameEngine();

        //Switch between file system and database saving
        bool useFileSystem = false;

        IGameRepository gameRepository;

        if (useFileSystem)
        {
            gameRepository = new GameRepositoryFileSystem(engine.State);
        }
        else
        {
            gameRepository = new GameRepositoryEF(db);
        }
        
        var changeRules = new ChangeRules(engine);
        var playerSetup = new PlayerSetup(engine);
    }
}