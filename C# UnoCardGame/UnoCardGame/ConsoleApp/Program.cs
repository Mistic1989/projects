
using ConsoleApp;
using ConsoleUI;
using DAL;
using MenuSystem;
using UnoEngine;
using Domain;
using GameUtilities;
using Microsoft.EntityFrameworkCore;

// var appData = Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData);
// var connectionString = "Data Source=<%temppath%>uno.db;Cache=Shared";
// connectionString = connectionString.Replace("<%temppath%>", appData);

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

// Saving and loading of game from json files
// IGameRepository gameRepository = new GameRepositoryFileSystem(engine.State);

// Saving and loading of game from database
// IGameRepository gameRepository = new GameRepositoryEF(db);

var gameController = new GameController(engine, gameRepository);
var gameSetup = new GameSetup(engine, gameRepository, gameController);
var changeRules = new ChangeRules(engine);
var playerSetup = new PlayerSetup(engine);

Console.ForegroundColor = ConsoleColor.White;

string? NewGameMenu()
{
    var startNewGameMenu = new Menu("New Game", new List<MenuItem>()
        {
            new MenuItem()
            {
                Shortcut = "c",
                ItemName = "Player count: ",
                MethodToRun = playerSetup.SetPlayerCount,
                UpdatePlayersCount = () => "Player count: " + engine.State.Players.Count
            },
            new MenuItem()
            {
                Shortcut = "t",
                UpdateNamesTypes = () => engine.State.Players,
                ItemName = "Player names and types: ",
                MethodToRun = playerSetup.SetPlayerNamesTypes,
            },
            new MenuItem()
            {
                Shortcut = "q",
                ItemName = "Start a new game",
                MethodToRun = gameSetup.PlayGame
            },
        });

    return startNewGameMenu.Run(EMenuLevel.Second, engine.State);
}

string? CustomRulesMenu()
{
    var customRulesMenu = new Menu("Custom Rules", new List<MenuItem>());

    int counter = 1;
    for (int i = 0; i < engine!.State.Rules.AddedRules.Count; i++)
    {
        var rule = engine.State.Rules.AddedRules[i];
        if (rule.Type == ERuleType.CustomRule && rule.CustomRuleName != null)
        {
            var menuItem = new MenuItem
            {
                Shortcut = (counter++).ToString(),
                ItemName = rule.PromptMessage,
                SelectedRules = () => (rule.IsActive ? rule.SubjectToChange?.ToString() : rule.DefaultValue)!,
                ToggleCustomRule = (userChoice) => changeRules?.ChangeCustomRules(userChoice)
            };
            customRulesMenu.MenuItems.Add(menuItem.Shortcut, menuItem);
        }
    }

    return customRulesMenu.Run(EMenuLevel.Other, engine.State);
}

string? HouseRulesMenu()
{
    var houseRulesMenu = new Menu("House Rules", new List<MenuItem>());

    for (int i = 0; i < engine!.State.Rules.AddedRules.Count; i++)
    {
        var rule = engine.State.Rules.AddedRules[i];
        if (rule.Type == ERuleType.HouseRule)
        {
            // var i1 = i;
            var menuItem = new MenuItem
            {
                Shortcut = (i + 1).ToString(),
                ItemName = rule.PromptMessage,
                SelectedRules = () => rule.IsActive ? "Active" : "Inactive",
                ToggleHouseRule = () => engine.State.Rules.SetHouseRuleActive(rule.HouseRuleName!.Value)
            };
            houseRulesMenu.MenuItems.Add(menuItem.Shortcut, menuItem);
        }
    }

    return houseRulesMenu.Run(EMenuLevel.Other, engine.State);
}

string? OptionsMenu()
{
    var optionsMenu = new Menu("Options", new List<MenuItem>()
    {
        new MenuItem()
        {
            Shortcut = "u",
            UpdateRules = () => $"House rules | currently active rules:" +
                                $" {String.Join(", ", engine.State.Rules.ActiveRules
                                    .Where(x => x.Type == ERuleType.HouseRule)
                                    .Select(x => x.PromptMessage))}",
            
            MethodToRun = HouseRulesMenu
        },
        new MenuItem()
        {
            Shortcut = "i",
            UpdateRules = () => $"Custom rules | currently active rules:" +
            $" {String.Join(", ", engine.State.Rules.ActiveRules
                .Where(x => x.Type == ERuleType.CustomRule)
                .Select(x => $"{x.PromptMessage}: {x.SubjectToChange}"))}",
            MethodToRun = CustomRulesMenu
        }
    });

    return optionsMenu.Run(EMenuLevel.Second, engine.State);
}

var mainMenu = new Menu(Utilities.GameTitle, new List<MenuItem>()
{
    new MenuItem()
    {
        Shortcut = "y",
        ItemName = "Resume game",
        MethodToRun = gameSetup.ResumeGame
    },
    new MenuItem()
    {
        Shortcut = "s",
        ItemName = "Start a new game",
        UpdatePlayersCount = () => $"Start a new game: players - {engine.State.Players.Count}" +
                                   $" | Current rules set:" +
                                   $" {String.Join(", ", engine.State.Rules.ActiveRules
                                       .Select(x => x.PromptMessage))}",
        UpdateNamesTypes = () => engine.State.Players,
        MethodToRun = NewGameMenu
    },
    new MenuItem()
    {
        Shortcut = "l",
        ItemName = "Load game",
        MethodToRun = gameSetup.LoadGame
    },
    new MenuItem()
    {
        Shortcut = "o",
        ItemName = "Options",
        MethodToRun = OptionsMenu
    },
});

mainMenu.Run(EMenuLevel.First, engine.State);
