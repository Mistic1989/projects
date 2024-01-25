using Domain;

namespace DAL;


public interface IGameRepository
{
    void Save(Guid id, GameState state);
    Task SaveAsync(GameState state);
    List<(Guid id, DateTime dt)> GetSaveGames();

    GameState LoadGame(Guid id);
    GameState LoadGameFromDisk(Guid id);
}
