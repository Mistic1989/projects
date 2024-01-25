using ConsoleUI;
using DAL;
using Domain;
using UnoEngine;

namespace ConsoleApp;

public class GameSetup(GameEngine engine, IGameRepository gameRepository, GameController gameController)
{
    private ValidateInputs Validate { get; set; } = new();

    public string? LoadGame()
    {
        Console.WriteLine("Saved games");
        var saveGameList = gameRepository.GetSaveGames();
        var saveGameListDisplay = saveGameList.Select((s, i) => (i + 1) + " - " + s).ToList();

        if (saveGameListDisplay.Count == 0) return null;

        Guid gameId = default;

        Console.WriteLine(string.Join("\n", saveGameListDisplay));

        ValidateInputs.ValidationResult result = Validate.ValidateAndPromptInput(
            $"Select game to load (1..{saveGameListDisplay.Count}):", null,
            minRange: 1, maxRange: saveGameListDisplay.Count);

        var userChoice = result.InputNumber;
        if (result.IsValid && userChoice != null)
        {
            gameId = saveGameList[userChoice.Value - 1].id;
            Console.WriteLine($"Loading file: {gameId}");
        }
        
        var gameState = gameRepository.LoadGame(gameId);
        engine = new GameEngine()
        {
            State = gameState
        };

        gameController = new GameController(engine, gameRepository);

        gameController.Run();

        return null;
    }
    
    public string? ResumeGame()
    {
        engine.State.ExitGame = false;
        
        // Console.WriteLine("THE GAME HAS BEGUN!");

        gameController.Run();

        return null;
    }

    public string PlayGame()
    {
        string? messages;
        
        if (engine.State.ExitGame == false)
        {
            messages = engine.InitializeGame();
        } 
        else
        {
            var players = engine.State.Players;
            var currentRules = engine.State.Rules;
            
            engine = new GameEngine();
            engine.State.Players = players;
            engine.State.Rules = currentRules;
            messages = engine.InitializeGame();
            // gameRepository = new GameRepositoryFileSystem(engine.State);
            gameController = new GameController(engine, gameRepository);
            engine.State.ExitGame = false;
        }

        // Console.WriteLine("THE GAME HAS BEGUN!");

        gameController.Run(messages);

        return "r";
    }
}