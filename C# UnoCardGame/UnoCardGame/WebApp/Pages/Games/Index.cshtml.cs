
using System.Runtime.Serialization;
using System.Text.Json;
using Microsoft.AspNetCore.Mvc.RazorPages;
using Microsoft.EntityFrameworkCore;
using DAL;
using Domain;
using Domain.Database;
using GameUtilities;
using UnoEngine;

namespace WebApp.Pages.Games
{
    public class IndexModel : PageModel
    {
        private readonly AppDbContext _context;
        
        private IGameRepository? _gameRepository;
        
        private readonly IWebHostEnvironment _hostingEnvironment;
        
        public GameEngine Engine { get; set; } = new();

        public IndexModel(AppDbContext context, IWebHostEnvironment hostingEnvironment)
        {
            _context = context;
            
            _hostingEnvironment = hostingEnvironment;
        
            // _gameRepository = new GameRepositoryEF(_context);
        
            bool useFileSystem = false;
            
            if (useFileSystem)
            {
                _gameRepository = new GameRepositoryFileSystem(Engine.State);
            }
        }

        public IList<Game> Game { get;set; } = new List<Game>();
        // public List<(Guid id, DateTime dt)> Games { get;set; } = default!;
        
        public async Task OnGetAsync()
        {
            if (_gameRepository != null)
            {
                var webRootPath = _hostingEnvironment.WebRootPath;
                var dataFolderPath = Path.Combine(webRootPath, "jsonSaveFiles");
            
                if (!Directory.Exists(dataFolderPath))
                {
                    Directory.CreateDirectory(dataFolderPath);
                }
                
                foreach (var game in _gameRepository.GetSaveGames())
                {
                    GameState state =_gameRepository.LoadGameFromDisk(game.id);
                    // _gameRepository = new GameRepositoryFileSystem(state, _hostingEnvironment);
                    var gameObject = new Game
                    {
                        Id = game.id,
                        CreatedAtDt = game.dt,
                        State = JsonSerializer.Serialize(state, Utilities.JsonSerializerOptions),
                        Players = state.Players
                    };
                    
                    var fileName = $"{game.id}.json";
                    var filePath = Path.Combine(dataFolderPath, fileName);
                    var jsonDataToWrite = JsonSerializer.Serialize(game, Utilities.JsonSerializerOptions);
                    await System.IO.File.WriteAllTextAsync(filePath, jsonDataToWrite);
                    
                    Game.Add(gameObject);
                }
            }
            else
            {
                Game = await _context.Games
                    .Include(g => g.Players)
                    .OrderByDescending(g => g.UpdatedAtDt)
                    .ToListAsync(); 
            }
        }
    }
}