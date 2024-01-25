using Domain;
using UnoEngine;

namespace ConsoleApp;

public class ChangeRules(GameEngine engine)
{
    private ValidateInputs Validate { get; set; } = new();
    
    // public string? SetHouseRules()
    // {
    //     DisplayRules(ERuleType.HouseRule);
    //     var result = GetRuleSelection(ERuleType.HouseRule);
    //
    //     if (result.IsValid && result.InputNumber != null)
    //     {
    //         engine.State.Rules.SetHouseRuleActive((EHouseRules) result.InputNumber.Value - 1);
    //     }
    //
    //     return null;
    // }

    public void ChangeCustomRules(string? userChoice)
    {
        if (engine.State.Players.Count < 2)
        {
            Console.WriteLine("Please select how many players play the game first!");
            Thread.Sleep(3000);
            // return null;
        }
        else
        {
            // DisplayRules(ERuleType.CustomRule);
            // var result = GetRuleSelection(ERuleType.CustomRule);

            // if (result.IsValid && result.InputNumber != null)
            // {
            // engine.State.Rules.SetCustomRules(result.InputNumber.Value, engine.State);
            int.TryParse(userChoice, out var inputNumber);
            engine.State.Rules.SetCustomRules(inputNumber, engine.State);
            // } 
        }
        
        // return null;
    }

    // private void DisplayRules(ERuleType ruleType)
    // {
    //     int counter = 1;
    //     engine.State.Rules.AddedRules
    //         .Where(x => x.Type == ruleType)
    //         .ToList()
    //         .ForEach(x => Console.WriteLine($"{counter++}) {x.PromptMessage}"));
    // }

    // private ValidateInputs.ValidationResult GetRuleSelection(ERuleType ruleType)
    // {
    //     return Validate.ValidateAndPromptInput(promptMessage: null, null,
    //         minRange: 1, maxRange: engine.State.Rules.AddedRules.Count(x => x.Type == ruleType));
    //     
    //     // return Validate.ValidateAndPromptInput(
    //     //     "Please select a rule set:", null,
    //     //     minRange: 1, maxRange: engine.State.Rules.AddedRules.Count(x => x.Type == ruleType));
    // }
}