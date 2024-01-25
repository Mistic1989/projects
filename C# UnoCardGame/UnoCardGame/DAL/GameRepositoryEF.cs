using System.Text.Json;
using Domain;
using Domain.Database;
using GameUtilities;

namespace DAL;

public class GameRepositoryEF : IGameRepository
{
    private readonly AppDbContext _ctx;

    public GameRepositoryEF(AppDbContext ctx)
    {
        _ctx = ctx;
    }

    public async void Save(Guid id, GameState state)
    {
        var game = _ctx.Games.FirstOrDefault(g => g.Id == state.Id);
        if (game == null)
        {
            game = new Game()
            {
                Id = state.Id,
                State = JsonSerializer.Serialize(state, Utilities.JsonSerializerOptions),
                Players = state.Players.Select(p => new Player()
                {
                    Id = p.Id,
                    NickName = p.NickName,
                    PlayerType = p.PlayerType,
                    GameId = state.Id,
                    Position = p.Position,
                    Score = p.Score
                }).ToList()
            };
            _ctx.Games.Add(game);
        }
        else
        {
            game.UpdatedAtDt = DateTime.Now;
            game.State = JsonSerializer.Serialize(state, Utilities.JsonSerializerOptions);
            // game.Players = state.Players.Select(p => game.Players!.First(gp => gp.Id == p.Id)).ToList();
        }

        await _ctx.SaveChangesAsync();
        // Console.WriteLine("SaveChanges: " + changeCount);
    }
    
    public async Task SaveAsync(GameState state)
    {
        var game = _ctx.Games.FirstOrDefault(g => g.Id == state.Id);
        if (game != null)
        {
            game.UpdatedAtDt = DateTime.Now;
            game.State = JsonSerializer.Serialize(state, Utilities.JsonSerializerOptions);
        }
        await _ctx.SaveChangesAsync();
    }

    public List<(Guid id, DateTime dt)> GetSaveGames()
    {
        return _ctx.Games
            .OrderByDescending(g => g.UpdatedAtDt)
            .ToList()
            .Select(g => (g.Id, g.UpdatedAtDt))
            .ToList();
    }

    public GameState LoadGame(Guid id)
    {
        var game = _ctx.Games.First(g => g.Id == id);
        return JsonSerializer.Deserialize<GameState>(game.State, Utilities.JsonSerializerOptions)!;
    }
    
    public GameState LoadGameFromDisk(Guid id)
    {
        return null!;
    }
}