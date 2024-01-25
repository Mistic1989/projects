using DAL;
using Domain;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using UnoEngine;

namespace WebApp.Pages.Play;

public class LoadGame : PageModel
{
    private readonly AppDbContext _context;

    private IGameRepository _gameRepository;
    public GameEngine Engine { get; set; } = default!;
    
    public LoadGame(AppDbContext context)
    {
        _context = context;
        _gameRepository = new GameRepositoryEF(_context);
    }

    [BindProperty(SupportsGet = true)]
    public Guid GameId { get; set; }

    [BindProperty(SupportsGet = true)]
    public Guid PlayerId { get; set; }
    
    public void OnGet()
    {
        var gameState = _gameRepository.LoadGame(GameId);

        Engine = new GameEngine()
        {
            State = gameState
        };
    }
    
    public IActionResult OnPost(string engineJson, Guid selectedCard)
    {
        if (!ModelState.IsValid)
        {
            return Page();
        }
        // Engine = JsonConvert.DeserializeObject<GameEngine>(engineJson)!;
        
        
        // var gameEngineJson = JsonConvert.SerializeObject(Engine);
        // HttpContext.Session.SetString("GameEngine", gameEngineJson);
        
        return Page();
        // return RedirectToPage("./Index");
    }
}