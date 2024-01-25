
using System.Text.Json;
using Domain;

namespace GameUtilities;

public static class Utilities
{
    public static void Main(string[] args)
    {
        
    }
    
    public static readonly JsonSerializerOptions JsonSerializerOptions = new JsonSerializerOptions()
    {
        WriteIndented = true,
        AllowTrailingCommas = true,
        PropertyNamingPolicy = JsonNamingPolicy.CamelCase,
    };
    
    // public static ValidationResult ValidateAndPromptInputNumber(
    //     string? promptMessage, 
    //     bool repeatUntilValid = true, 
    //     bool displayErrorMessage = true, 
    //     int? minRange = null, 
    //     int? maxRange = null,
    //     string? userInput = null)
    // {
    //     while (true)
    //     {
    //         if (promptMessage != null)
    //         {
    //             Console.WriteLine(promptMessage);
    //         }
    //         
    //         if (userInput == null)
    //         {
    //             userInput = Console.ReadLine()?.Trim().ToLower();
    //         }
    //
    //         var validationResult = ValidateNumberInput(userInput, minRange, maxRange);
    //         if (validationResult.IsValid)
    //         {
    //             return validationResult;
    //         }
    //
    //         if (displayErrorMessage)
    //         {
    //             Console.WriteLine(validationResult.Message);
    //         }
    //
    //         if (!repeatUntilValid)
    //         {
    //             return new ValidationResult(false, validationResult.InputNumber, validationResult.Message);
    //         }
    //
    //         userInput = null;
    //     } 
    // }
    //
    // private static ValidationResult ValidateNumberInput(
    //     string? userInput, 
    //     int? minRange, 
    //     int? maxRange)
    // {
    //     if (string.IsNullOrWhiteSpace(userInput))
    //     {
    //         return new ValidationResult(false, null, "Input cannot be empty.");
    //     }
    //
    //     if (!userInput.All(char.IsDigit))
    //     {
    //         return new ValidationResult(false, null, "Invalid input. Only numbers can be entered.");
    //     }
    //
    //     if (!int.TryParse(userInput, out var input))
    //     {
    //         return new ValidationResult(false, null,"Invalid number format.");
    //     }
    //
    //     if (minRange.HasValue && maxRange.HasValue && (input < minRange.Value || input > maxRange.Value))
    //     {
    //         return new ValidationResult(false, null,$"Input is out of the specified range ({minRange}-{maxRange}).");
    //     }
    //     
    //     return new ValidationResult(true, input);
    // }
    //
    // public struct ValidationResult
    // {
    //     public bool IsValid { get; set; }
    //     public string Message { get; set; }
    //     
    //     public int? InputNumber { get; set; }
    //     public string? InputLetter { get; set; }
    //
    //     public ValidationResult(bool isValid, int? userInputNumber = null, string? userInputLetter = null, string message = "")
    //     {
    //         IsValid = isValid;
    //         Message = message;
    //         InputNumber = userInputNumber;
    //         InputLetter = userInputLetter;
    //     }
    // }
    //
    // public static ValidationResult ValidateAndPromptInputLetter(
    // List<string> validLetters, 
    // string? promptMessage, 
    // bool repeatUntilValid = true, 
    // bool displayErrorMessage = true,
    // bool canBeEmptyString = false,
    // string? userInput = null)
    // {
    // while (true)
    // {
    //     if (promptMessage != null)
    //     {
    //         Console.WriteLine(promptMessage);
    //     }
    //
    //     if (userInput == null)
    //         
    //     {
    //         userInput = Console.ReadLine()?.Trim().ToLower();
    //     }
    //     else
    //     {
    //         userInput = userInput.Trim().ToLower();
    //     }
    //
    //     if (string.IsNullOrWhiteSpace(userInput))
    //     {
    //         if (canBeEmptyString)
    //         {
    //             return new ValidationResult(true, userInputLetter: userInput);
    //         }
    //         if (displayErrorMessage)
    //         {
    //             Console.WriteLine("Input cannot be empty or whitespace.");
    //         }
    //         if (!repeatUntilValid) return new ValidationResult(false, userInputLetter: "",
    //             message: "Input cannot be empty or whitespace.");
    //         userInput = null;
    //         continue;
    //     }
    //
    //     if (!userInput.All(char.IsLetter) || userInput.Length != 1)
    //     {
    //         if (displayErrorMessage)
    //         {
    //             Console.WriteLine("Invalid input. Only a single letter can be entered.");
    //         }
    //         if (!repeatUntilValid) return new ValidationResult(false, userInputLetter: userInput,
    //             message: "Invalid input. Only a single letter can be entered.");
    //         userInput = null;
    //         continue;
    //     }
    //
    //     if (!validLetters.Contains(userInput))
    //     {
    //         if (displayErrorMessage)
    //         {
    //             Console.WriteLine("You entered an incorrect letter.");
    //         }
    //         if (!repeatUntilValid) return new ValidationResult(false, userInputLetter: userInput,
    //             message: "You entered an incorrect letter.");
    //         userInput = null;
    //         continue;
    //     }
    //
    //     return new ValidationResult(true, userInputLetter: userInput);
    // }
    // }   
    
    // public static List<GameCard> Draw(int count, List<GameCard> drawPile, GameState state)
    // {
    //     var drawnCards = new List<GameCard>();
    //     int cardsToTake = count;
    //     
    //     if (cardsToTake > state.DrawPile.Count && state.DrawPile.Count != 0)
    //     {
    //         // Take all cards from the remaining draw pile
    //         drawnCards = state.DrawPile;
    //         cardsToTake -= drawnCards.Count;
    //         state.DrawPile.Clear();
    //     }
    //
    //     if (state.DrawPile.Count == 0)
    //     {
    //         ReshuffleCards(state);
    //     }
    //     
    //     var takenCards = state.DrawPile.Take(cardsToTake).ToList();
    //     drawnCards.AddRange(takenCards);
    //
    //     state.DrawPile.RemoveAll(x => takenCards.Contains(x));
    //     
    //     return drawnCards;
    // }

    // private static void ReshuffleCards(GameState state)
    // {
    //     var currentCard = state.DiscardPile[^1];
    //     state.DiscardPile.RemoveAt(state.DiscardPile.Count - 1);
    //     state.DrawPile = state.DiscardPile;
    //     ShuffleCards(state);
    //     state.DiscardPile = new List<GameCard>();
    //     state.DiscardPile.Add(currentCard);
    // }

    public static bool HasMatch(GameCard tableCard, GameCard playersCard)
    {
        return tableCard.CardColor == playersCard.CardColor
               || tableCard.CardValue == playersCard.CardValue
               || playersCard.CardColor == ECardColor.Wild;
    }
    
    public static bool HasMatch(ECardColor tableCardColor, ECardColor playersCardColor)
    {
        return tableCardColor == playersCardColor
               || playersCardColor == ECardColor.Wild;
    }
    
    public static void PrintStringWithDelay(string inputString, int delayMilliseconds)
    {
        for (int i = 0; i < inputString.Length; i++)
        {
            Console.Write(inputString[i]);
            Thread.Sleep(delayMilliseconds);
        }
    }

    public static readonly String GameTitle = "\u2588\u2500\u2588\u2500\u2588\u2500\u2500\u2588\u2500\u2588\u2588\u2588" +
                                              "\u2588\u2500\u2500\u2500\u2500\u2588\u2588\u2588\u2588\u2500\u2588\u2588" +
                                              "\u2588\u2588\u2500\u2588\u2588\u2588\u2588\u2500\u2588\u2588\u2588\u2588" +
                                              "\u2500\u2500\u2500\u2500\u2500\u2588\u2588\u2588\u2588\u2500\u2588\u2588" +
                                              "\u2588\u2588\u2500\u2588\u2500\u2500\u2500\u2588\u2500\u2588\u2588\u2588" +
                                              "\n\u2588\u2500\u2588\u2500\u2588\u2588\u2500\u2588\u2500\u2588\u2500\u2500" +
                                              "\u2588\u2500\u2500\u2500\u2500\u2588\u2500\u2500\u2588\u2500\u2588\u2500" +
                                              "\u2500\u2588\u2500\u2588\u2500\u2500\u2588\u2500\u2588\u2500\u2500\u2588" +
                                              "\u2588\u2500\u2500\u2500\u2500\u2588\u2500\u2500\u2500\u2500\u2588\u2500" +
                                              "\u2500\u2588\u2500\u2588\u2588\u2500\u2588\u2588\u2500\u2588\u2500\u2500" +
                                              "\n\u2588\u2500\u2588\u2500\u2588\u2500\u2588\u2588\u2500\u2588\u2500\u2500" +
                                              "\u2588\u2500\u2500\u2500\u2500\u2588\u2500\u2500\u2500\u2500\u2588\u2588" +
                                              "\u2588\u2588\u2500\u2588\u2588\u2588\u2588\u2500\u2588\u2500\u2500\u2588" +
                                              "\u2588\u2500\u2500\u2500\u2500\u2588\u2500\u2588\u2588\u2500\u2588\u2588" +
                                              "\u2588\u2588\u2500\u2588\u2500\u2588\u2500\u2588\u2500\u2588\u2588\u2588" +
                                              "\n\u2588\u2500\u2588\u2500\u2588\u2500\u2500\u2588\u2500\u2588\u2500\u2500" +
                                              "\u2588\u2500\u2500\u2500\u2500\u2588\u2500\u2500\u2588\u2500\u2588\u2500" +
                                              "\u2500\u2588\u2500\u2588\u2500\u2588\u2500\u2500\u2588\u2500\u2500\u2588" +
                                              "\u2588\u2500\u2500\u2500\u2500\u2588\u2500\u2500\u2588\u2500\u2588\u2500" +
                                              "\u2500\u2588\u2500\u2588\u2500\u2500\u2500\u2588\u2500\u2588\u2500\u2500" +
                                              "\n\u2588\u2588\u2588\u2500\u2588\u2500\u2500\u2588\u2500\u2588\u2588\u2588" +
                                              "\u2588\u2500\u2500\u2500\u2500\u2588\u2588\u2588\u2588\u2500\u2588\u2500" +
                                              "\u2500\u2588\u2500\u2588\u2500\u2588\u2500\u2500\u2588\u2588\u2588\u2588" +
                                              "\u2500\u2500\u2500\u2500\u2500\u2588\u2588\u2588\u2588\u2500\u2588\u2500" +
                                              "\u2500\u2588\u2500\u2588\u2500\u2500\u2500\u2588\u2500\u2588\u2588\u2588\n";
}