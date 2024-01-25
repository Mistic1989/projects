
namespace Domain;

public class Rules
{
    public int PlayerHandSize { get; set; } = 7;
    public int PointsToWin { get; set; } = 500;
    public bool NoWildCardsInPlay { get; set; }
    public int GameRoundsAmount { get; set; } = int.MaxValue;
    
    public List<Rule> AddedRules { get; set; } = new List<Rule>();

    private ValidateInputs Validate { get; set; } = new ValidateInputs();
    private ValidateInputs.ValidationResult ValidationResult { get; set; }
    
    public bool IsHouseRuleActive(EHouseRules houseRule)
    {
        return AddedRules.Any(x => x.HouseRuleName == houseRule && x.IsActive);
    }
    
    public Rules()
    {
        // Validate = new ValidateInputs();
        
        // Add House Rules
        AddedRules.Add(new Rule
        {
            HouseRuleName = EHouseRules.Official,
            Type = ERuleType.HouseRule,
            PromptMessage = "Official rules",
            IsActive = true
        });
        AddedRules.Add(new Rule
        {
            HouseRuleName = EHouseRules.SevenO,
            Type = ERuleType.HouseRule,
            PromptMessage = "Seven-0",
            IsActive = false
        });
        AddedRules.Add(new Rule
        {
            HouseRuleName = EHouseRules.Stacking,
            Type = ERuleType.HouseRule,
            PromptMessage = "Stacking",
            IsActive = false
        });
        // Add Custom Rules
        AddedRules.Add(new Rule
        {
            CustomRuleName = ECustomRules.PlayerHandSize,
            Type = ERuleType.CustomRule,
            PromptMessage = "Cards to be dealt to each player",
            IsActive = false,
            DefaultValue = PlayerHandSize.ToString()
        });
        AddedRules.Add(new Rule
        {
            CustomRuleName = ECustomRules.PointsToWin,
            Type = ERuleType.CustomRule,
            PromptMessage = "Points required to win",
            IsActive = false,
            DefaultValue = PointsToWin.ToString()
        });
        AddedRules.Add(new Rule
        {
            CustomRuleName = ECustomRules.NoWildCardsInPlay,
            Type = ERuleType.CustomRule,
            PromptMessage = "Play without any Wild cards (Wild, Wild Draw Four)",
            IsActive = false,
            DefaultValue = NoWildCardsInPlay == false ? "No" : "Yes"
        });
        AddedRules.Add(new Rule
        {
            CustomRuleName = ECustomRules.GameRoundsAmount,
            Type = ERuleType.CustomRule,
            PromptMessage = "Play certain amount rounds to win",
            IsActive = false
        });
    }
    
    public void SetHouseRuleActive(EHouseRules houseRule)
    {
        var ruleObject = AddedRules.FirstOrDefault(x => x.HouseRuleName == houseRule);
        if (ruleObject != null)
        {
            // Toggle the active state of the selected rule
            ruleObject.IsActive = !ruleObject.IsActive;
    
            // If the Official rule is selected, deactivate all other rules
            if (ruleObject.HouseRuleName == EHouseRules.Official)
            {
                foreach (var otherRule in AddedRules.Where(x => x.HouseRuleName != EHouseRules.Official))
                {
                    otherRule.IsActive = false;
                }
            }
            // If any rule other than Official is activated, deactivate the Official rule
            else if (ruleObject.IsActive && AddedRules.Any(x => x.HouseRuleName == EHouseRules.Official))
            {
                var officialRule = AddedRules.First(x => x.HouseRuleName == EHouseRules.Official);
                officialRule.IsActive = false;
            }
        }
    }
    
    // public void SetHouseRuleActive(EHouseRules houseRule)
    // {
    //     var ruleObject = AddedRules.FirstOrDefault(x => x.HouseRuleName == houseRule);
    //     if (ruleObject != null && AddedRules.Contains(ruleObject) && !ruleObject.IsActive)
    //     {
    //         if (ruleObject.HouseRuleName == EHouseRules.Official)
    //         {
    //             ruleObject.IsActive = true;
    //             foreach (var otherRule in AddedRules.Where(x => x.HouseRuleName != EHouseRules.Official))
    //             {
    //                 otherRule.SubjectToChange = default;
    //                 otherRule.IsActive = false;
    //             }
    //         }
    //         else
    //         {
    //             ruleObject.IsActive = true;
    //             // If any rule other than Official becomes active, set Official to false
    //             if (AddedRules.Any(x => x.HouseRuleName == EHouseRules.Official))
    //             {
    //                 var officialRule = AddedRules.First(x => x.HouseRuleName == EHouseRules.Official);
    //                 officialRule.IsActive = false;
    //             }
    //         }
    //     }
    // }
    
    public void SetCustomRuleActive(ECustomRules customRule)
    {
        var ruleObject = AddedRules.First(x => x.CustomRuleName == customRule);
        if (!ruleObject.IsActive)
        {
            ruleObject.IsActive = true;
            if (AddedRules.Any(x => x.HouseRuleName == EHouseRules.Official))
            {
                var officialRule = AddedRules.First(x => x.HouseRuleName == EHouseRules.Official);
                officialRule.IsActive = false;
            }
        }
    }

    public void SetCustomRules(int userChoice, GameState state)
    {
        if (userChoice == 1)
        {
            var playersAmount = state.Players.Count;
            var maxPossibleHandSize = 107 / playersAmount;
            
            // Console.WriteLine($"Enter a number between 1-{maxPossibleHandSize}");
            //
            // do
            // {
            //     string? input = Console.ReadLine();
            //     ValidationResult = Validate.ValidateAndPromptInput($"Enter a number between 1-{maxPossibleHandSize}",
            //         null, minRange: 1, maxRange: maxPossibleHandSize);
            // } while (!ValidationResult.IsValid);
            //
            
            ValidationResult = Validate.ValidateAndPromptInput($"Enter a number between 1-{maxPossibleHandSize}",
                null, minRange: 1, maxRange: maxPossibleHandSize);
            
            if (ValidationResult.IsValid && ValidationResult.InputNumber.HasValue)
            {
                PlayerHandSize = ValidationResult.InputNumber.Value;
                var rule = AddedRules.First(x => x.CustomRuleName == ECustomRules.PlayerHandSize);
                rule.SubjectToChange = PlayerHandSize;
                SetCustomRuleActive((ECustomRules)userChoice - 1);
            }
        }
        else if (userChoice == 2)
        {
            ValidateInputs.ValidationResult validation = Validate.ValidateAndPromptInput(
                "Enter a number starting from 1", null,
                minRange: 1);
            if (validation.IsValid && validation.InputNumber.HasValue)
            {
                PointsToWin = validation.InputNumber.Value;
                var rule = AddedRules.First(x => x.CustomRuleName == ECustomRules.PointsToWin);
                rule.SubjectToChange = PointsToWin;
                SetCustomRuleActive((ECustomRules)userChoice - 1);
            }
        }
        else if (userChoice == 3)
        {
            ValidateInputs.ValidationResult validation = Validate.ValidateAndPromptInput(
                "Yes(y) or No(n)?", new List<string> { "y", "n" });
            if (validation.IsValid && validation.InputLetter != null)
            {
                NoWildCardsInPlay = validation.InputLetter == "y";
                if (validation.InputLetter == "y")
                {
                    var rule = AddedRules.First(x => x.CustomRuleName == ECustomRules.NoWildCardsInPlay);
                    rule.SubjectToChange = NoWildCardsInPlay ? "Yes" : "No";
                    SetCustomRuleActive((ECustomRules)userChoice - 1);
                }
            }
        }
        else if (userChoice == 4)
        {
            ValidateInputs.ValidationResult validation = Validate.ValidateAndPromptInput(
                "Enter a number starting from 1", null, minRange: 1);
            if (validation.IsValid && validation.InputNumber.HasValue)
            {
                GameRoundsAmount = validation.InputNumber.Value;
                var rule = AddedRules.First(x => x.CustomRuleName == ECustomRules.GameRoundsAmount);
                rule.SubjectToChange = GameRoundsAmount;
                SetCustomRuleActive((ECustomRules)userChoice - 1);
            }
        }
    }
    
    //Return all active rules
    public List<Rule> ActiveRules => AddedRules.Where(x => x.IsActive).ToList();
}