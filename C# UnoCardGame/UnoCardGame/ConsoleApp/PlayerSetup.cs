using Domain;
using UnoEngine;

namespace ConsoleApp;

public class PlayerSetup(GameEngine engine)
{
    private ValidateInputs Validate { get; set; } = new();
    
    public string? SetPlayerCount() {

        ValidateInputs.ValidationResult result = Validate.ValidateAndPromptInput(
            "Please enter a number of players between 2-10", null, 
            minRange: 2, maxRange: 10, inputMode: ValidateInputs.InputMode.NumberOnly);
        
        if (result.IsValid && result.InputNumber.HasValue)
        {
            CreatePlayers(result.InputNumber.ToString()!);
        }

        return null;
    }

    public void CreatePlayers(string playersCount)
    {
        List<Player> temp = new List<Player>();
        
        for (int i = 0; i < int.Parse(playersCount); i++)
        {
            temp.Add(new Player()
            {
                NickName = "Human " + (i + 1),
                PlayerType = EPlayerType.Human,
                Position = i + 1,
            });
        }

        engine.State.Players = temp;
    }

    public string? SetPlayerNamesTypes() 
    {
        foreach (var player in engine.State.Players)
        {
            player.NickName = GetUniquePlayerName();
            player.PlayerType = GetPlayerType();
        }

        return null;
    }
    
    private string GetUniquePlayerName()
    {
        var usedNickNames = engine.State.Players.Select(x => x.NickName).ToList();
        string playerName;
        ValidateInputs.ValidationResult result;
        do
        {
            Console.WriteLine("Enter the player name (2-20 symbols): ");
            result = Validate.ValidateAndPromptInput(null, null, minLength: 2, maxLength: 20);
            playerName = result.InputLetter ?? "";

            if (usedNickNames.Contains(playerName))
            {
                Console.WriteLine("That name is already taken.");
            }
        }
        while (!result.IsValid || usedNickNames.Contains(playerName));

        usedNickNames.Add(playerName);
        return playerName;
    }

    private EPlayerType GetPlayerType()
    {
        Console.WriteLine("Select player type: \n1) Human\n2) AI");
        var typeResult = Validate.ValidateAndPromptInput(null, null,
            minRange: 1, maxRange: 2, inputMode: ValidateInputs.InputMode.NumberOnly);
        return typeResult.InputNumber == 1 ? EPlayerType.Human : EPlayerType.AI;
    }
}