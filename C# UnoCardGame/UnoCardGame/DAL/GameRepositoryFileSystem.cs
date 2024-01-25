using System.Runtime.Serialization;
using System.Text.Json;
using Domain;
using GameUtilities;
// using Microsoft.AspNetCore.Hosting;

namespace DAL;


public class GameRepositoryFileSystem : IGameRepository
{
    public static void Main(string[] args)
    {
        
    }
    private GameState State { get; set; }
    
    // private readonly IWebHostEnvironment? _hostingEnvironment;
    
    // public GameRepositoryFileSystem(GameState gameState, IWebHostEnvironment hostingEnvironment)
    // {
    //     State = gameState;
    //     _hostingEnvironment = hostingEnvironment;
    // }
    
    static readonly string AppData = Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData);
    private string _saveFolder = Path.Combine(AppData, "UnoCardGame", "SaveFiles");

    public GameRepositoryFileSystem(GameState gameState)
    {
        State = gameState;
    }

    public void Save(Guid id, GameState state)
    {
        var content = JsonSerializer.Serialize(state, Utilities.JsonSerializerOptions);

        var fileName = Path.ChangeExtension(id.ToString(), ".json");

        if (!Path.Exists(_saveFolder))
        {
            Directory.CreateDirectory(_saveFolder);
        }

        File.WriteAllText(Path.Combine(_saveFolder, fileName), content);
    }

    public List<(Guid id, DateTime dt)> GetSaveGames()
    {
        var data = Directory.EnumerateFiles(_saveFolder);
        var res = data
            .Select(
                path => (
                    Guid.Parse(Path.GetFileNameWithoutExtension(path)),
                    File.GetLastWriteTime(path)
                )
            ).ToList();
        
        return res;
    }

    public GameState LoadGame(Guid id)
    {
        // if (_hostingEnvironment != null)
        // {
        //     var wwwRootPath = _hostingEnvironment.WebRootPath;
        //     // var dataFolderPath = Path.Combine(wwwRootPath, "jsonSaveFiles");
        //     _saveFolder = Path.Combine(wwwRootPath, "jsonSaveFiles");
        // }
        
        var fileName = Path.ChangeExtension(id.ToString(), ".json");

        var jsonStr = File.ReadAllText(Path.Combine(_saveFolder, fileName));
        var res = JsonSerializer.Deserialize<GameState>(jsonStr, Utilities.JsonSerializerOptions);
        if (res == null) throw new SerializationException($"Cannot deserialize {jsonStr}");

        return res;
    }
    
    public GameState LoadGameFromDisk(Guid id)
    {
        var fileName = Path.ChangeExtension(id.ToString(), ".json");
        var jsonStr = File.ReadAllText(Path.Combine(_saveFolder, fileName));
        var res = JsonSerializer.Deserialize<GameState>(jsonStr, Utilities.JsonSerializerOptions);
        if (res == null) throw new SerializationException($"Cannot deserialize {jsonStr}");

        return res;
    }
    
    public async Task SaveAsync(GameState state)
    {
        // var wwwRootPath = _hostingEnvironment!.WebRootPath;
        // _saveFolder = Path.Combine(wwwRootPath, "jsonSaveFiles");
        
        
        var content = JsonSerializer.Serialize(state, Utilities.JsonSerializerOptions);

        var fileName = Path.ChangeExtension(state.Id.ToString(), ".json");

        if (!Path.Exists(_saveFolder))
        {
            Directory.CreateDirectory(_saveFolder);
        }

        await File.WriteAllTextAsync(Path.Combine(_saveFolder, fileName), content);
    }
}