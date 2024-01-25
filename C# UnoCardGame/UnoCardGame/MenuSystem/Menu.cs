
using Domain;

namespace MenuSystem;


public class Menu
{
    private string? Title { get; set; }

    public Dictionary<string, MenuItem> MenuItems { get; set; } = new();
    
    private const string MenuSeparator = "----------------------------------------------------------------------------";
    
    private static readonly HashSet<string?> ReservedShortcuts = new() {"x", "b", "r"};
    
    private ValidateInputs Validate { get; set; }
    
    public Menu(string? title, List<MenuItem> menuItems)
    {
        Validate = new ValidateInputs();
        
        Title = title;
        
        foreach (var menuItem in menuItems)
        {
            if (ReservedShortcuts.Contains(menuItem.Shortcut.ToLower()))
            {
                throw new ApplicationException(
                    $"Menu shortcut '{menuItem.Shortcut.ToLower()}' in not allowed list!");
            }

            if (MenuItems.ContainsKey(menuItem.Shortcut.ToLower()))
            {
                throw new ApplicationException(
                    $"Menu shortcut '{menuItem.Shortcut.ToLower()}' is already registered!");
            }

            MenuItems[menuItem.Shortcut.ToLower()] = menuItem;
        }
    }
    
    private void Draw(EMenuLevel menuLevel, GameState? state = null)
    {
        if (!string.IsNullOrWhiteSpace(Title))
        {
            Console.WriteLine(Title);
            Console.WriteLine(MenuSeparator);
        }

        foreach (var menuItem in MenuItems)
        {

            // If player count is less than 2, then start a new game option is not available
            if (Title == "New Game" && menuItem.Key == "q" && state?.Players.Count < 2)
            {
                continue;
            }
            
            // If it is not possible to resume game then don't show it in the menu
            if (menuItem.Key == "y" && menuLevel == EMenuLevel.First && state != null && state.ExitGame == false)
            {
                continue;
            }
            
            Console.Write(menuItem.Key);
            Console.Write(" | ");
            
            if (menuItem.Value.UpdateRules != null)
            {
                // Console.WriteLine(menuItem.Key + " | " + menuItem.Value.UpdateRules());
                Console.Write(menuItem.Value.UpdateRules());
            }
            

                // Console.Write(menuItem.Value.SelectedRules != null
                //     ? menuItem.Value.SelectedRules()
                //     : menuItem.Value.ItemName);

            if (menuItem.Value.SelectedRules != null)
            {
                Console.WriteLine(menuItem.Value.ItemName + " | " + menuItem.Value.SelectedRules());
            } 
            else
            {
                Console.WriteLine(menuItem.Value.UpdatePlayersCount != null
                    ? menuItem.Value.UpdatePlayersCount()
                    : menuItem.Value.ItemName);
            }
            
            if (menuItem.Value.UpdateNamesTypes != null && menuItem.Value.UpdateNamesTypes().Count != 0)
            {
                Console.WriteLine(string.Join(", ", menuItem.Value.UpdateNamesTypes()
                    .Select(x => $"{x.NickName} ({x.PlayerType})")));
            }
        }
        
        if (menuLevel != EMenuLevel.First)
        { 
            Console.WriteLine("b | Back");
            
            if (menuLevel == EMenuLevel.Other)
            {
                Console.WriteLine("r | Return to main");
            }
        }
        
        Console.WriteLine("x | Exit");

        Console.WriteLine(MenuSeparator);
        Console.WriteLine("Your choice:");
    }
    
    public string Run(EMenuLevel menuLevel = EMenuLevel.First, GameState? state = null) {
        
        Console.Clear();
        
        var userChoice = "";
        
        var acceptedShortcuts = MenuItems.Keys.ToList();
        acceptedShortcuts.Add("b");
        acceptedShortcuts.Add("x");
        if (menuLevel == EMenuLevel.Other)
        {
            acceptedShortcuts.Add("r");
        }

        while (!ReservedShortcuts.Contains(userChoice)) {
            
            if (MenuItems.ContainsKey("q") && state?.Players.Count < 2)
            {
                acceptedShortcuts = new List<string> { "t", "c", "b", "x" };
            }

            if (MenuItems.ContainsKey("q") && state?.Players.Count > 1)
            {
                acceptedShortcuts = new List<string> { "q", "t", "c", "b", "x" };
            }
            
            if (state != null && state.ExitGame == false)
            {
                Draw(menuLevel, state);
            }
            else
            {
                Draw(menuLevel);
            }

            var minRange = 0;
            var maxRange = 0;

            ValidateInputs.ValidationResult validationResult;
            
            if (state != null && state.Rules.AddedRules.Count > 0)
            {
                var houseRules = state.Rules.AddedRules.Where(x => x.Type == ERuleType.HouseRule).ToList();
                var customRules = state.Rules.AddedRules.Where(x => x.Type == ERuleType.CustomRule).ToList();

                if (Title == "House Rules" && houseRules.Count > 0)
                {
                    minRange = 1;
                    maxRange = houseRules.Count;
                }

                if (Title == "Custom Rules" && customRules.Count > 0)
                {
                    minRange = 1;
                    maxRange = customRules.Count;
                }
            }

            if (Title == "House Rules" || Title == "Custom Rules")
            {
                validationResult = Validate.ValidateAndPromptInput(
                    null, validLetters: acceptedShortcuts, inputMode: ValidateInputs.InputMode.Any,
                    minRange: minRange, maxRange: maxRange
                );
            }
            else
            {
                validationResult = Validate.ValidateAndPromptInput(
                    null, validLetters: acceptedShortcuts, inputMode: ValidateInputs.InputMode.LetterOnly
                );
            }
            
            userChoice = validationResult.InputLetter ?? validationResult.InputNumber.ToString();

            if (validationResult.IsValid)
            {
                if (MenuItems.ContainsKey(userChoice!))
                {
                    if (Title == "House Rules")
                    {
                        MenuItems[userChoice!.ToLower()].ToggleHouseRule?.Invoke();
                    }
                    if (Title == "Custom Rules")
                    {
                        MenuItems[userChoice!.ToLower()].ToggleCustomRule?.Invoke(userChoice);
                    }
                }
                
                if (MenuItems.ContainsKey(userChoice!)
                    && MenuItems[userChoice!.ToLower()].MethodToRun != null) {
                    
                    var result = MenuItems[userChoice.ToLower()].MethodToRun!();
                    if (result?.ToLower() == "x") {
                        userChoice = "x";
                    }
                    if (result?.ToLower() == "r") {
                        userChoice = "b";
                    }
                }
                
            } else if (!ReservedShortcuts.Contains(userChoice!.ToLower())) {
                
                Console.WriteLine("Undefined shortcut");
                
            }

            Console.WriteLine(string.Empty);
            Console.Clear();
        }
        
        return userChoice!;
    }
}